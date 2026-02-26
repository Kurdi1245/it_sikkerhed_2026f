from fastapi import FastAPI, Header, HTTPException
import requests

app = FastAPI(title="Order Microservice")

AUTH_SERVER_URL = "http://127.0.0.1:8000"

orders_db = {}

def validate_token(token: str):
    response = requests.get(
        f"{AUTH_SERVER_URL}/validate_token",
        headers={"token": token}
    )

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return response.json()


@app.post("/orders")
def create_order(product: str, token: str = Header(...)):

    user_data = validate_token(token)
    username = user_data["username"]

    if username not in orders_db:
        orders_db[username] = []

    orders_db[username].append(product)

    return {"message": "Order created", "orders": orders_db[username]}


@app.get("/orders")
def get_orders(token: str = Header(...)):

    user_data = validate_token(token)
    username = user_data["username"]

    return {"orders": orders_db.get(username, [])}