from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gemini_api_key: str = ""
    
    upload_dir: str = "./uploads"
    vector_db_path: str = "./data/chroma_db"
    
    max_file_size_mb: int = 10
    chunk_size: int = 500
    chunk_overlap: int = 50
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
