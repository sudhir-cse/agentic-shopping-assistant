from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    OPENAI_API_KEY: str
    GROQ_API_KEY: str
    LANGSMITH_API_KEY: str
    QDRANT_URL: str = ""
    QDRANT_API_KEY: str = ""
    SUPABASE_URL: str = ""
    SUPABASE_LANGGRAPH_USER: str = ""
    SUPABASE_LANGGRAPH_PASSWORD: str = ""
    SUPABASE_TOOLS_USER: str = ""
    SUPABASE_TOOLS_PASSWORD: str = ""
    CO_API_KEY: str = ""

    model_config = SettingsConfigDict(env_file=".env")

config = Config()