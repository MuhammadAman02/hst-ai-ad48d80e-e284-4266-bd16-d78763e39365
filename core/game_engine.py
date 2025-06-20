"""
Snake Game Engine
Core game logic and mechanics
"""

import random
from typing import Optional, Tuple
from models.game_state import GameState, Position, Direction, HighScores
from app.config import settings


class SnakeGameEngine:
    """Snake game logic engine"""
    
    def __init__(self):
        self.game_state = GameState(board_size=settings.board_size)
        self.high_scores = HighScores.load_from_file(settings.high_score_file)
        self.reset_game()
    
    def reset_game(self):
        """Reset the game to initial state"""
        self.game_state.reset()
        self._spawn_food()
    
    def _spawn_food(self):
        """Spawn food at a random empty position"""
        while True:
            food_pos = Position(
                x=random.randint(0, self.game_state.board_size - 1),
                y=random.randint(0, self.game_state.board_size - 1)
            )
            
            # Ensure food doesn't spawn on snake
            if food_pos not in self.game_state.snake:
                self.game_state.food = food_pos
                break
    
    def change_direction(self, new_direction: Direction):
        """Change snake direction (prevent 180-degree turns)"""
        if self.game_state.is_game_over or self.game_state.is_paused:
            return
        
        # Prevent reverse direction
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }
        
        if new_direction != opposite_directions.get(self.game_state.direction):
            self.game_state.direction = new_direction
    
    def toggle_pause(self):
        """Toggle game pause state"""
        if not self.game_state.is_game_over:
            self.game_state.is_paused = not self.game_state.is_paused
    
    def update(self) -> bool:
        """Update game state - returns True if game continues"""
        if self.game_state.is_game_over or self.game_state.is_paused:
            return False
        
        # Calculate new head position
        head = self.game_state.snake[0]
        new_head = self._get_next_position(head, self.game_state.direction)
        
        # Check wall collision
        if (new_head.x < 0 or new_head.x >= self.game_state.board_size or
            new_head.y < 0 or new_head.y >= self.game_state.board_size):
            self._game_over()
            return False
        
        # Check self collision
        if new_head in self.game_state.snake:
            self._game_over()
            return False
        
        # Move snake
        self.game_state.snake.insert(0, new_head)
        
        # Check food collision
        if new_head == self.game_state.food:
            self.game_state.score += 10
            self._spawn_food()
        else:
            # Remove tail if no food eaten
            self.game_state.snake.pop()
        
        return True
    
    def _get_next_position(self, current: Position, direction: Direction) -> Position:
        """Calculate next position based on direction"""
        direction_map = {
            Direction.UP: (0, -1),
            Direction.DOWN: (0, 1),
            Direction.LEFT: (-1, 0),
            Direction.RIGHT: (1, 0)
        }
        
        dx, dy = direction_map[direction]
        return Position(x=current.x + dx, y=current.y + dy)
    
    def _game_over(self):
        """Handle game over"""
        self.game_state.is_game_over = True
        
        # Check if it's a high score
        if self.game_state.score > 0:
            self.high_scores.add_score(self.game_state.score)
            self.high_scores.save_to_file(settings.high_score_file)
    
    def get_game_state(self) -> GameState:
        """Get current game state"""
        return self.game_state
    
    def get_high_score(self) -> int:
        """Get the current high score"""
        return self.high_scores.get_high_score()
    
    def get_high_scores(self) -> HighScores:
        """Get all high scores"""
        return self.high_scores