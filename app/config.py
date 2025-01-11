from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Just for example
    # database_username:str
    # database_password:str
    # secret_key:str="1234567890"
    database_username:str
    algorithm:str
    secret_key:str
    database_password:str
    database_name:str
    database_hostname:str
    database_port:str
    access_token_expire_minutes:int
    
    class Config:
        env_file=".env"
        
settings=Settings()