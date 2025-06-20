"""
Game State Models
"""

from pydantic import BaseModel, Field
from typing import List, Tuple, Optional
from enum import Enum
import json
import os
from datetime import datetime


class Direction(str, Enum):
    """Snake movement directions"""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class Position(BaseModel):
    """2D position on the game board"""
    x: int = Field(..., ge=0)
    y: int = Field(..., ge=0)
    
    def __eq__(self, other):
        if isinstance(other, Position):
            return self.x == other.x and self.y == other.y
        return False
    
    def __hash__(self):
        return hash((self.x, self.y))


class GameState(BaseModel):
    """Complete game state"""
    snake: List[Position] = Field(default_factory=list)
    food: Optional[Position] = None
    direction: Direction = Direction.RIGHT
    score: int = 0
    is_game_over: bool = False
    is_paused: bool = False
    board_size: int = 20
    
    def reset(self):
        """Reset game to initial state"""
        center = self.board_size // 2
        self.snake = [
            Position(x=center, y=center),
            Position(x=center-1, y=center),
            Position(x=center-2, y=center)
        ]
        self.direction = Direction.RIGHT
        self.score = 0
        self.is_game_over = False
        self.is_paused = False
        self.food = None


class HighScore(BaseModel):
    """High score entry"""
    score: int
    date: str
    player: str = "Player"


class HighScores(BaseModel):
    """High scores collection"""
    scores: List[HighScore] = Field(default_factory=list)
    
    def add_score(self, score: int, player: str = "Player"):
        """Add a new high score"""
        new_score = HighScore(
            score=score,
            date=datetime.now().strftime("%Y-%m-%d %H:%M"),
            player=player
        )
        self.scores.append(new_score)
        self.scores.sort(key=lambda x: x.score, reverse=True)
        self.scores = self.scores[:10]  # Keep top 10
    
    def get_high_score(self) -> int:
        """Get the highest score"""
        return self.scores[0].score if self.scores else 0
    
    def save_to_file(self, filename: str):
        """Save high scores to file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.model_dump(), f, indent=2)
        except Exception as e:
            print(f"Error saving high scores: {e}")
    
    @classmethod
    def load_from_file(cls, filename: str) -> 'HighScores':
        """Load high scores from file"""
        if not os.path.exists(filename):
            return cls()
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        except Exception as e:
            print(f"Error loading high scores: {e}")
            return cls()