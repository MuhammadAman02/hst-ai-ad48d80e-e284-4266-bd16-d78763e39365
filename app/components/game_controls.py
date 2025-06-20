"""
Game Controls Component
Control buttons and instructions for the Snake game
"""

from nicegui import ui
from typing import Callable, Optional


class GameControls:
    """Game control buttons and instructions"""
    
    def __init__(self, 
                 on_start: Optional[Callable] = None,
                 on_pause: Optional[Callable] = None,
                 on_reset: Optional[Callable] = None):
        self.on_start = on_start
        self.on_pause = on_pause
        self.on_reset = on_reset
        self._setup_controls()
    
    def _setup_controls(self):
        """Setup the control buttons"""
        with ui.card().classes('p-4 bg-gray-800 border border-gray-600'):
            ui.label('Game Controls').classes('text-xl font-bold text-white mb-3')
            
            # Control buttons
            with ui.row().classes('gap-2 mb-4'):
                ui.button('Start/Resume', on_click=self._handle_start).classes('bg-green-600 hover:bg-green-700')
                ui.button('Pause', on_click=self._handle_pause).classes('bg-yellow-600 hover:bg-yellow-700')
                ui.button('Reset', on_click=self._handle_reset).classes('bg-red-600 hover:bg-red-700')
            
            # Instructions
            ui.separator().classes('my-3')
            ui.label('Instructions').classes('text-lg font-bold text-white mb-2')
            
            with ui.column().classes('gap-1 text-gray-300'):
                ui.label('🎮 Use arrow keys or WASD to move')
                ui.label('⏸️ Press SPACE to pause/resume')
                ui.label('🔄 Press R to restart')
                ui.label('🎯 Eat food to grow and score points')
                ui.label('💀 Avoid walls and your own tail')
    
    def _handle_start(self):
        """Handle start button click"""
        if self.on_start:
            self.on_start()
    
    def _handle_pause(self):
        """Handle pause button click"""
        if self.on_pause:
            self.on_pause()
    
    def _handle_reset(self):
        """Handle reset button click"""
        if self.on_reset:
            self.on_reset()


class KeyboardInstructions:
    """Keyboard control instructions component"""
    
    def __init__(self):
        self._setup_instructions()
    
    def _setup_instructions(self):
        """Setup keyboard instructions"""
        with ui.card().classes('p-4 bg-gray-800 border border-gray-600 mt-4'):
            ui.label('Keyboard Controls').classes('text-lg font-bold text-white mb-3')
            
            # Control mapping
            controls = [
                ('↑ / W', 'Move Up'),
                ('↓ / S', 'Move Down'),
                ('← / A', 'Move Left'),
                ('→ / D', 'Move Right'),
                ('SPACE', 'Pause/Resume'),
                ('R', 'Restart Game'),
            ]
            
            for key, action in controls:
                with ui.row().classes('justify-between items-center py-1'):
                    ui.label(key).classes('font-mono bg-gray-700 px-2 py-1 rounded text-yellow-400')
                    ui.label(action).classes('text-gray-300')