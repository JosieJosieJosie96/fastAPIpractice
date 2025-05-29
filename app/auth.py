from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if not (secrets.compare_digest(credentials.username, "admin") and
            secrets.compare_digest(credentials.password, "secret")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
