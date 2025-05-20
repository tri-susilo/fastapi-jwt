from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from app.schemas.user_schema import UserCreate, UserLogin, TokenResponse
from app.controllers.user_controller import UserController
from app.config.database import get_db
from fastapi import HTTPException, Header
from app.services.jwt_service import create_access_token, create_refresh_token, decode_token
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = UserController.register(db, user)
    return {"message": "User created successfully", "user": {"username": new_user.username, "email": new_user.email}}

# @router.post("/login", response_model=TokenResponse)
# def login(user: UserLogin, db: Session = Depends(get_db)):
#     return UserController.login(db, user)



@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    result = UserController.login(db, user)  # hasil: tokens + user

    response = JSONResponse(content={
        "message": "Login berhasil",

    })

    response.set_cookie(key="access_token", value=result["access_token"], httponly=True)
    response.set_cookie(key="refresh_token", value=result["refresh_token"], httponly=True)

    return response

@router.post("/refresh")
def refresh_token(request: Request):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    payload = decode_token(token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=400, detail="Not a refresh token")

    new_access = create_access_token({"sub": payload["sub"], "role": payload["role"]})
    new_refresh = create_refresh_token({"sub": payload["sub"], "role": payload["role"]})

    response = JSONResponse(content={"message": "Token refreshed"})
    response.set_cookie("access_token", new_access, httponly=True)
    response.set_cookie("refresh_token", new_refresh, httponly=True)

    return response


# @router.post("/refresh", response_model=TokenResponse)
# def refresh_token(authorization: str = Header(...)):
#     token = authorization.replace("Bearer ", "")
#     payload = decode_token(token)
#     if payload.get("type") != "refresh":
#         raise HTTPException(status_code=400, detail="Not a refresh token")

#     new_access = create_access_token({"sub": payload["sub"], "role": payload["role"]})
#     new_refresh = create_refresh_token({"sub": payload["sub"], "role": payload["role"]})

#     return {
#         "access_token": new_access,
#         "refresh_token": new_refresh,
#         "token_type": "bearer"
#     }

