from typing import Optional

from pydantic import BaseModel


class UserUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    private: Optional[bool]
