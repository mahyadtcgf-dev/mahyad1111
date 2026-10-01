from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.models import get_db, User, UserRole
from app.auth.router import get_current_user

def check_role(allowed_roles: list[UserRole]):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to access this resource"
            )
        return current_user
    return role_checker

# Pre-defined permission helpers
is_admin = check_role([UserRole.SUPER_ADMIN, UserRole.ADMIN])
is_super_admin = check_role([UserRole.SUPER_ADMIN])
is_operator = check_role([UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.OPERATOR])
