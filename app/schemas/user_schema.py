from pydantic import BaseModel, EmailStr, Field
from typing import Literal

# Definición de roles permitidos
RoleType = Literal["admin", "support", "user"]

# Esquema para la creación de un usuario (Entrada)
class UserCreate(BaseModel):
    name: str = Field(..., min_length=3, description="Nombre del usuario (mínimo 3 caracteres)")
    email: EmailStr = Field(..., description="Correo electrónico válido")
    role: RoleType = Field(default="user", description="Rol del usuario")
    is_active: bool = Field(default=True, description="Estado del usuario")

# Esquema de respuesta (Salida)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleType
    is_active: bool