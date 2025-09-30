from pydantic import BaseModel, EmailStr, Field

class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    phone: str = Field(...)
    user_type: str = Field(default="victim") # Can be "victim" or "guardian"

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "johndoe@example.com",
                "password": "your_secure_password",
                "phone": "1234567890",
                "user_type": "victim"
            }
        }