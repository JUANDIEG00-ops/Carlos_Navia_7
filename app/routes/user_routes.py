from fastapi import APIRouter, HTTPException, Query, Response, status
from typing import List, Optional
from app.schemas.user_schema import UserCreate, UserResponse, RoleType

router = APIRouter(prefix="/users", tags=["Users"])

# Base de datos simulada en memoria
db_users: List[dict] = [
    {"id": 1, "name": "Carlos Gomez", "email": "carlos@example.com", "role": "admin", "is_active": True},
    {"id": 2, "name": "Ana Martinez", "email": "ana@example.com", "role": "support", "is_active": False},
]

# Función auxiliar para agregar cabeceras personalizadas
def set_custom_headers(response: Response):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

# GET /users (Listar y filtrar por Query Parameters)
@router.get("", response_model=List[UserResponse])
def get_users(
    response: Response,
    role: Optional[RoleType] = Query(None, description="Filtrar por rol"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo")
):
    set_custom_headers(response)
    filtered = db_users

    if role is not None:
        filtered = [u for u in filtered if u["role"] == role]
    if is_active is not None:
        filtered = [u for u in filtered if u["is_active"] == is_active]

    return filtered

# GET /users/{user_id} (Path Parameter)
@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, response: Response):
    set_custom_headers(response)
    for user in db_users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

# POST /users (Crear usuario)
@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, response: Response):
    set_custom_headers(response)
    
    # Validar correo duplicado
    for existing_user in db_users:
        if existing_user["email"] == user.email:
            raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")

    # Autoincrementar ID
    new_id = max([u["id"] for u in db_users], default=0) + 1
    new_user = {"id": new_id, **user.model_dump()}
    db_users.append(new_user)
    
    return new_user