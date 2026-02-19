import json
from fastapi import FastAPI, Depends, HTTPException, Header, Body, Query, Path
from typing import List
from pydantic import BaseModel

from src.auth_eksempel.user_service import User_service
from src.auth_eksempel.models import User, Role
from src.auth_eksempel.auth_rest_api_models import RegisterUserRequest, GetBearerTokenRequest, ActivateUserRequest
from src.auth_eksempel.auth_service import Auth_service  # <- Manglede

# Nyt Pydantic model til password-ændring
class ChangePasswordRequest(BaseModel):
    username: str
    new_password: str

# Pydantic model til delete
class DeleteUserRequest(BaseModel):
    username: str

# Pydantic model til get
class GetUserRequest(BaseModel):
    username: str

class Auth_rest_api:

    def __init__(self, database_file: str = "db_user_flat_file.json"):
        self.user_service = User_service(database_file)

        self.app = FastAPI()
        #self.app.add_event_handler("startup", self.on_startup)

        self.app.post("/register_user")(self.register_user)
        self.app.post("/get_bearer_token")(self.get_bearer_token)
        self.app.post("/deactivate_user")(self.deactivate_user)
        self.app.post("/activate_user")(self.activate_user)
        # nye endpoints
        self.app.put("/change_password")(self.change_password)  # PUT, ikke POST
        self.app.get("/get_user")(self.get_user)
        self.app.delete("/delete_user/{username}")(self.delete_user)  # DELETE med path


    def register_user(self, post_variables: RegisterUserRequest):
        self.user_service.register_user(
            post_variables.username, 
            post_variables.password, 
            post_variables.first_name, 
            post_variables.last_name, 
            post_variables.roles
        )
        return { "status": "user created"}
    def change_password(self, token: str, username: str, new_password: str):
        payload = Auth_service.verify_token(token)
        acting_username = payload["sub"]

        # Only admin or self can change password
        if acting_username != username and not self._user_has_at_least_one_role_for_access(acting_username, [Role.admin]):
            raise HTTPException(status_code=403, detail="Not authorized to change this password")

        user = self._get_user(username)
        user.password = Auth_service.hash_password(new_password)
        self._save_database()
        return {"status": f"Password for '{username}' has been updated"}
        
    def get_bearer_token(self, post_variables: GetBearerTokenRequest):
        token = self.user_service.get_bearer_token(post_variables.username, post_variables.password)
        return {"token": token}

    def deactivate_user(
            self, 
            post_variables: ActivateUserRequest,
            token: str = Header(...)
        ):

        if not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")

        self.user_service.deactivate_user(token, post_variables.username)
        return { "status": f"user '{post_variables.username}' has been deactivated"}

    def activate_user(
            self, 
            post_variables: ActivateUserRequest,
            token: str = Header(...)
        ):
        if not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")
        
        self.user_service.activate_user(token, post_variables.username)
        return { "status": f"user '{post_variables.username}' has been reactivated"}
        
    # ---------- Password endpoint ----------
    def change_password(self, post_variables: ChangePasswordRequest, token: str = Header(...)):
        if not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")

        # Kald User_service til at ændre password
        payload = Auth_service.verify_token(token)
        acting_username = payload["sub"]

        # Kun admin eller self kan ændre password
        if acting_username != post_variables.username and not self.user_service._user_has_at_least_one_role_for_access(acting_username, [Role.admin]):
            raise HTTPException(status_code=403, detail="Not authorized to change this password")

        user = self.user_service._get_user(post_variables.username)
        user.password = Auth_service.hash_password(post_variables.new_password)
        self.user_service._save_database()

        return {"status": f"Password for '{post_variables.username}' has been updated"}
            
    # --- Get user (GET med query parameter) ---
    def get_user(self, username: str = Query(...), token: str = Header(...)):
        if not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")

        payload = Auth_service.verify_token(token)
        acting_username = payload["sub"]

        # Kun admin eller self
        if acting_username != username and not self.user_service._user_has_at_least_one_role_for_access(acting_username, [Role.admin]):
            raise HTTPException(status_code=403, detail="Not authorized to view this user")

        user = self.user_service._get_user(username)
        return {
            "username": user.username,
            "first_name": Auth_service.decrypt_data(user.first_name),
            "last_name": Auth_service.decrypt_data(user.last_name),
            "active": user.active,
            "roles": [role.value for role in user.roles]
        }

    # --- Delete user (DELETE med path parameter) ---
    def delete_user(self, username: str = Path(...), token: str = Header(...)):
        if not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")

        payload = Auth_service.verify_token(token)
        acting_username = payload["sub"]

        # Kun admin kan slette andre, self kan slette sig selv
        if acting_username != username and not self.user_service._user_has_at_least_one_role_for_access(acting_username, [Role.admin]):
            raise HTTPException(status_code=403, detail="Not authorized to delete this user")

        if username in self.user_service._user_db:
            del self.user_service._user_db[username]
            self.user_service._save_database()
            return {"status": f"User '{username}' deleted"}
        else:
            raise HTTPException(status_code=404, detail="User not found")