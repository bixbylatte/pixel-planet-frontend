"""
Configuration for Pixel Planet Frontend
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration"""

    # API Configuration
    API_BASE_URL = os.getenv(
        "API_BASE_URL",
        "https://pixel-planet-api-eixw6uscdq-uc.a.run.app"
    )
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "60"))

    # App Configuration
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    PAGE_TITLE = os.getenv("PAGE_TITLE", "Pixelcast")

    # Default values
    DEFAULT_LOCATION = os.getenv("DEFAULT_LOCATION", "San Francisco, CA")
    DEFAULT_LATITUDE = float(os.getenv("DEFAULT_LATITUDE", "37.7749"))
    DEFAULT_LONGITUDE = float(os.getenv("DEFAULT_LONGITUDE", "-122.4194"))


config = Config()
