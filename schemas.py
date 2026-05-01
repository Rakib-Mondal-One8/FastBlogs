from pydantic import BaseModel,Field,EmailStr,field_validator

class BlogCreate(BaseModel):
    title : str = Field(min_length=5)
    content: str = Field(min_length=10)
    author: str = Field(min_length=2)

class UserCreate(BaseModel):
    email : EmailStr
    username : str = Field(min_length=2)
    first_name : str = Field(min_length=2)
    last_name : str = Field(min_length=2)
    password : str = Field(min_length=5)
    phone_number : str = Field(min_length=10)
    role : str = Field()

    @field_validator('email')
    def check_domain(cls,v):
        v = v.lower()
        if not v.endswith('@gmail.com'):
            raise ValueError("Only gmail are allowed!")
        return v


class PasswordChange(BaseModel):
    password: str
    new_password : str

class PhoneNumberChange(BaseModel):
    new_phone_number : str = Field(min_length=10,max_length=15)

class EmailUpdate(BaseModel):
    new_email: EmailStr

    @field_validator('new_email')
    def check_domain(cls,v):
        v = v.lower()
        if not v.endswith("@gmail.com"):
            raise ValueError("Only gmail are allowed!")
        return v
