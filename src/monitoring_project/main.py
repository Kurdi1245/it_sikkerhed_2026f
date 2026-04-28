from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from logger import LOGGER
import json

app = FastAPI()

USERS = {
    "alice": "password123",
    "bob": "hunter2",
}


class LoginRequest(BaseModel):
    username: str
    password: str


@app.get("/")
def root():
    LOGGER.info("Root endpoint besøgt")
    return {"message": "API kører!"}


@app.post("/login")
def login(req: LoginRequest):
    if req.username not in USERS:
        LOGGER.error(
            "Login fejlede - ukendt bruger",
            extra={"http_error_code": 401, "username": req.username}
        )
        raise HTTPException(status_code=401, detail="Ukendt bruger")

    if USERS[req.username] != req.password:
        LOGGER.error(
            "Login fejlede - forkert kodeord",
            extra={"http_error_code": 401, "username": req.username}
        )
        raise HTTPException(status_code=401, detail="Forkert kodeord")

    LOGGER.info("Login lykkedes", extra={"username": req.username})
    return {"message": f"Velkommen, {req.username}!"}


@app.get("/metrics")
def metrics():
    LOGGER.flush()

    try:
        raw = LOGGER.read_file()
    except Exception:
        raw = ""

    error_counts: dict[str, int] = {}
    login_success = 0
    info_count = 0

    for line in raw.strip().splitlines():
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue

        level = entry.get("levelname", "")
        message = entry.get("message", "")

        if level == "ERROR":
            code = str(entry.get("http_error_code", "unknown"))
            error_counts[code] = error_counts.get(code, 0) + 1
        elif level == "INFO":
            info_count += 1
            if "Login lykkedes" in message:
                login_success += 1

    lines = []
    lines.append("# HELP app_log_info_total Antal INFO beskeder")
    lines.append("# TYPE app_log_info_total counter")
    lines.append(f"app_log_info_total {info_count}")
    lines.append("")
    lines.append("# HELP app_login_success_total Antal vellykkede logins")
    lines.append("# TYPE app_login_success_total counter")
    lines.append(f"app_login_success_total {login_success}")
    lines.append("")
    lines.append("# HELP app_log_errors_total Fejl per HTTP error code")
    lines.append("# TYPE app_log_errors_total counter")

    if error_counts:
        for code, count in error_counts.items():
            lines.append(f'app_log_errors_total{{http_error_code="{code}"}} {count}')
    else:
        lines.append('app_log_errors_total{http_error_code="none"} 0')

    return PlainTextResponse("\n".join(lines) + "\n")