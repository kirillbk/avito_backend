from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()

class Settings(BaseSettings):
    server_address: str
    
    postgres_conn: str
    postgres_jdbc_url: str
    postgres_username: str 
    postgres_password: str
    postgres_host: str
    postgres_port: str
    postgres_database: str
    
    debug: bool = False


config = Settings() 