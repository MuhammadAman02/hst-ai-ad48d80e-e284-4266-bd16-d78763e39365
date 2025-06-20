"""
Snake Game - Main Application
Professional Snake game with NiceGUI interface
"""

from nicegui import ui, app
from core.game_engine import SnakeGameEngine
from models.game_state import Direction
from app.components.game_board import GameBoard
from app.components.score_display import ScoreDisplay, HighScoreTable
from app.components.game_controls import GameControls, KeyboardInstructions
from app.config import settings
import asyncio


class SnakeGameApp:
    """Main Snake Game Application"""
    
    def __init__(self):
        self.game_engine = SnakeGameEngine()
        self.game_board = None
        self.score_display = None
        self.high_score_table = None
        self.game_timer = None
        self.is_running = False
        
        # Setup the UI
        self._setup_ui()
        
        # Start the game loop
        self._start_game_loop()
    
    def _setup_ui(self):
        """Setup the main user interface"""
        # Page configuration
        ui.colors(primary='#1f2937')
        
        # Main layout
        with ui.column().classes('w-full max-w-7xl mx-auto p-4'):
            # Header
            with ui.row().classes('w-full justify-center mb-6'):
                ui.label('🐍 Snake Game').classes('text-4xl font-bold text-white')
            
            # Game area
            with ui.row().classes('w-full gap-6 justify-center'):
                # Left panel - Game board
                with ui.column().classes('items-center'):
                    self.game_board = GameBoard(on_key_press=self._handle_key_press)
                
                # Right panel - Controls and scores
                with ui.column().classes('w-80 gap-4'):
                    self.score_display = ScoreDisplay()
                    GameControls(
                        on_start=self._start_game,
                        on_pause=self._toggle_pause,
                        on_reset=self._reset_game
                    )
                    KeyboardInstructions()
            
            # High scores table
            with ui.row().classes('w-full justify-center mt-6'):
                with ui.column().classes('w-96'):
                    self.high_score_table = HighScoreTable()
        
        # Initial display update
        self._update_display()
    
    def _handle_key_press(self, key: str):
        """Handle keyboard input for game controls"""
        # Movement keys
        key_to_direction = {
            'arrowup': Direction.UP,
            'w': Direction.UP,
            'arrowdown': Direction.DOWN,
            's': Direction.DOWN,
            'arrowleft': Direction.LEFT,
            'a': Direction.LEFT,
            'arrowright': Direction.RIGHT,
            'd': Direction.RIGHT,
        }
        
        if key in key_to_direction:
            self.game_engine.change_direction(key_to_direction[key])
        elif key == ' ':  # Space for pause
            self._toggle_pause()
        elif key == 'r':  # R for reset
            self._reset_game()
    
    def _start_game_loop(self):
        """Start the main game loop"""
        if not self.is_running:
            self.is_running = True
            self.game_timer = ui.timer(
                settings.game_speed / 1000.0,  # Convert to seconds
                self._game_tick
            )
    
    def _stop_game_loop(self):
        """Stop the main game loop"""
        if self.game_timer:
            self.game_timer.cancel()
            self.game_timer = None
        self.is_running = False
    
    def _game_tick(self):
        """Single game loop iteration"""
        # Update game state
        continue_game = self.game_engine.update()
        
        # Update display
        self._update_display()
        
        # Stop loop if game over
        if not continue_game and self.game_engine.get_game_state().is_game_over:
            self._stop_game_loop()
    
    def _update_display(self):
        """Update all UI components"""
        game_state = self.game_engine.get_game_state()
        high_score = self.game_engine.get_high_score()
        high_scores = self.game_engine.get_high_scores()
        
        # Update components
        if self.game_board:
            self.game_board.update_display(game_state)
        
        if self.score_display:
            self.score_display.update(game_state, high_score)
        
        if self.high_score_table:
            self.high_score_table.update(high_scores)
    
    def _start_game(self):
        """Start or resume the game"""
        game_state = self.game_engine.get_game_state()
        
        if game_state.is_game_over:
            self._reset_game()
        elif game_state.is_paused:
            self._toggle_pause()
        elif not self.is_running:
            self._start_game_loop()
    
    def _toggle_pause(self):
        """Toggle game pause state"""
        self.game_engine.toggle_pause()
        game_state = self.game_engine.get_game_state()
        
        if game_state.is_paused:
            self._stop_game_loop()
        else:
            self._start_game_loop()
        
        self._update_display()
    
    def _reset_game(self):
        """Reset the game to initial state"""
        self._stop_game_loop()
        self.game_engine.reset_game()
        self._update_display()
        self._start_game_loop()


# Global app instance
snake_app = None


@ui.page('/')
async def index():
    """Main game page"""
    global snake_app
    
    # Setup page
    ui.add_head_html('''
        <title>Snake Game - Professional Python Implementation</title>
        <meta name="description" content="Classic Snake game built with Python and NiceGUI">
        <style>
            body { 
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            }
            .nicegui-content { 
                padding: 0; 
                background: transparent; 
            }
        </style>
    ''')
    
    # Initialize the game
    snake_app = SnakeGameApp()


@ui.page('/health')
async def health():
    """Health check endpoint"""
    return {'status': 'healthy', 'game': 'snake', 'version': '1.0.0'}


def main():
    """Main application entry point"""
    # Configure NiceGUI
    ui.run(
        host=settings.host,
        port=settings.port,
        title="Snake Game",
        favicon="🐍",
        dark=True,
        show=False,  # Don't auto-open browser
        reload=settings.debug
    )


if __name__ in {"__main__", "__mp_main__"}:
    main()