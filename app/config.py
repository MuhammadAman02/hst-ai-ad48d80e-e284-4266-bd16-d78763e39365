"""
Application Configuration
"""

import os
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # Game Configuration
    game_speed: int = 150  # milliseconds between moves
    board_size: int = 20   # board dimensions (20x20)
    high_score_file: str = "high_scores.json"
    
    # Visual Configuration
    cell_size: int = 25    # pixels per cell
    border_width: int = 2
    
    # Colors
    background_color: str = "#1a1a2e"
    border_color: str = "#16213e"
    snake_color: str = "#0f3460"
    snake_head_color: str = "#e94560"
    food_color: str = "#f39c12"
    text_color: str = "#ffffff"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()