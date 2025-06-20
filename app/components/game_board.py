"""
Game Board Component
Visual representation of the Snake game
"""

from nicegui import ui
from typing import Callable, Optional
from models.game_state import GameState, Position
from app.config import settings


class GameBoard:
    """Snake game board component"""
    
    def __init__(self, on_key_press: Optional[Callable] = None):
        self.on_key_press = on_key_press
        self.canvas = None
        self.game_state: Optional[GameState] = None
        self._setup_board()
    
    def _setup_board(self):
        """Setup the game board canvas"""
        board_pixel_size = settings.board_size * settings.cell_size
        
        with ui.card().classes('p-4 bg-gray-900 border-2 border-gray-700'):
            with ui.row().classes('justify-center'):
                self.canvas = ui.canvas(
                    width=board_pixel_size,
                    height=board_pixel_size
                ).classes('border-2 border-gray-600 rounded-lg')
                
                # Setup keyboard controls
                if self.on_key_press:
                    self.canvas.on('keydown', self._handle_keydown)
                
                # Make canvas focusable for keyboard events
                self.canvas.props('tabindex="0"')
                
        # Focus the canvas for immediate keyboard input
        ui.timer(0.1, lambda: self.canvas.run_method('focus'), once=True)
    
    def _handle_keydown(self, event):
        """Handle keyboard input"""
        if self.on_key_press:
            key = event.args.get('key', '').lower()
            self.on_key_press(key)
    
    def update_display(self, game_state: GameState):
        """Update the visual display of the game"""
        self.game_state = game_state
        self._draw_game()
    
    def _draw_game(self):
        """Draw the complete game state"""
        if not self.canvas or not self.game_state:
            return
        
        # Clear canvas
        self.canvas.clear()
        
        # Draw background
        self._draw_background()
        
        # Draw food
        if self.game_state.food:
            self._draw_food(self.game_state.food)
        
        # Draw snake
        self._draw_snake(self.game_state.snake)
        
        # Draw game over overlay
        if self.game_state.is_game_over:
            self._draw_game_over()
        elif self.game_state.is_paused:
            self._draw_paused()
    
    def _draw_background(self):
        """Draw the game background"""
        board_size = settings.board_size * settings.cell_size
        
        # Background
        self.canvas.rect(0, 0, board_size, board_size).fill_color(settings.background_color)
        
        # Grid lines
        for i in range(settings.board_size + 1):
            pos = i * settings.cell_size
            # Vertical lines
            self.canvas.line(pos, 0, pos, board_size).stroke_color(settings.border_color).stroke_width(1)
            # Horizontal lines
            self.canvas.line(0, pos, board_size, pos).stroke_color(settings.border_color).stroke_width(1)
    
    def _draw_food(self, food: Position):
        """Draw food item"""
        x = food.x * settings.cell_size + 2
        y = food.y * settings.cell_size + 2
        size = settings.cell_size - 4
        
        # Draw food as a circle
        center_x = x + size // 2
        center_y = y + size // 2
        radius = size // 2 - 2
        
        self.canvas.circle(center_x, center_y, radius).fill_color(settings.food_color)
    
    def _draw_snake(self, snake: list[Position]):
        """Draw the snake"""
        for i, segment in enumerate(snake):
            x = segment.x * settings.cell_size + 1
            y = segment.y * settings.cell_size + 1
            size = settings.cell_size - 2
            
            # Head is different color
            color = settings.snake_head_color if i == 0 else settings.snake_color
            
            self.canvas.rect(x, y, size, size).fill_color(color).stroke_color('#ffffff').stroke_width(1)
    
    def _draw_game_over(self):
        """Draw game over overlay"""
        board_size = settings.board_size * settings.cell_size
        
        # Semi-transparent overlay
        self.canvas.rect(0, 0, board_size, board_size).fill_color('rgba(0, 0, 0, 0.7)')
        
        # Game Over text
        center_x = board_size // 2
        center_y = board_size // 2
        
        self.canvas.text('GAME OVER', center_x, center_y - 20).font_size(24).fill_color('#ff4444').text_anchor('middle')
        self.canvas.text('Press R to restart', center_x, center_y + 10).font_size(16).fill_color('#ffffff').text_anchor('middle')
    
    def _draw_paused(self):
        """Draw paused overlay"""
        board_size = settings.board_size * settings.cell_size
        
        # Semi-transparent overlay
        self.canvas.rect(0, 0, board_size, board_size).fill_color('rgba(0, 0, 0, 0.5)')
        
        # Paused text
        center_x = board_size // 2
        center_y = board_size // 2
        
        self.canvas.text('PAUSED', center_x, center_y - 10).font_size(24).fill_color('#ffff44').text_anchor('middle')
        self.canvas.text('Press SPACE to continue', center_x, center_y + 20).font_size(14).fill_color('#ffffff').text_anchor('middle')