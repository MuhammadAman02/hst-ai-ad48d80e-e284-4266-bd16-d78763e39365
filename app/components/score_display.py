"""
Score Display Component
Shows current score, high score, and game statistics
"""

from nicegui import ui
from models.game_state import GameState, HighScores


class ScoreDisplay:
    """Score and statistics display component"""
    
    def __init__(self):
        self.score_label = None
        self.high_score_label = None
        self.length_label = None
        self._setup_display()
    
    def _setup_display(self):
        """Setup the score display UI"""
        with ui.card().classes('p-4 bg-gray-800 border border-gray-600'):
            ui.label('Game Statistics').classes('text-xl font-bold text-white mb-3')
            
            with ui.column().classes('gap-2'):
                self.score_label = ui.label('Score: 0').classes('text-lg text-green-400 font-mono')
                self.high_score_label = ui.label('High Score: 0').classes('text-lg text-yellow-400 font-mono')
                self.length_label = ui.label('Length: 3').classes('text-lg text-blue-400 font-mono')
    
    def update(self, game_state: GameState, high_score: int):
        """Update the score display"""
        if self.score_label:
            self.score_label.text = f'Score: {game_state.score}'
        
        if self.high_score_label:
            self.high_score_label.text = f'High Score: {high_score}'
        
        if self.length_label:
            self.length_label.text = f'Length: {len(game_state.snake)}'


class HighScoreTable:
    """High scores table component"""
    
    def __init__(self):
        self.table = None
        self._setup_table()
    
    def _setup_table(self):
        """Setup the high scores table"""
        with ui.card().classes('p-4 bg-gray-800 border border-gray-600 mt-4'):
            ui.label('High Scores').classes('text-xl font-bold text-white mb-3')
            
            # Table headers
            with ui.row().classes('w-full text-gray-300 font-bold border-b border-gray-600 pb-2'):
                ui.label('Rank').classes('w-16 text-center')
                ui.label('Score').classes('w-20 text-center')
                ui.label('Date').classes('flex-1 text-center')
            
            # Table content container
            self.table_content = ui.column().classes('w-full')
    
    def update(self, high_scores: HighScores):
        """Update the high scores table"""
        if not self.table_content:
            return
        
        # Clear existing content
        self.table_content.clear()
        
        # Add high scores
        for i, score in enumerate(high_scores.scores[:10], 1):
            with self.table_content:
                with ui.row().classes('w-full text-gray-200 py-1 hover:bg-gray-700 rounded'):
                    ui.label(f'#{i}').classes('w-16 text-center font-mono')
                    ui.label(str(score.score)).classes('w-20 text-center font-mono text-green-400')
                    ui.label(score.date).classes('flex-1 text-center text-sm')
        
        # Show message if no scores
        if not high_scores.scores:
            with self.table_content:
                ui.label('No high scores yet!').classes('text-gray-400 text-center py-4')