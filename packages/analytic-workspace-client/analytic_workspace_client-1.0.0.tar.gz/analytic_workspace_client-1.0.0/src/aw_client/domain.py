from pydantic import BaseModel


class APIConfig(BaseModel):
    """ """
    aw_url: str
    token: str
