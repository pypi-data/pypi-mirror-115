from pydantic import BaseModel
from typing import Optional
from pydantic import Field


class EnvironModel(BaseModel):
    class Config:
        extra='ignore'
    def __init__(__pydantic_self__, dotenv_path: str = None) -> None:
        from dotenv import load_dotenv
        from os import environ
        from os.path import exists
        from pydantic import ValidationError
        from .exceptions import EnvException
        if dotenv_path and not exists(dotenv_path): raise FileNotFoundError(dotenv_path)
        load_dotenv(dotenv_path=dotenv_path)
        try:
            super().__init__(**environ)
        except ValidationError as e:
            raise EnvException(e)
        

