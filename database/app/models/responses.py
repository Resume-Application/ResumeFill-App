from sqlmodel import Field, SQLModel

class ResponseBase(SQLModel):
    formResponse: str

class Response(ResponseBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")

class ResponseCreate(ResponseBase):
    pass

class ResponsePublic(ResponseBase):
    id: int
    user_id: int | None
