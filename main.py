#!/usr/bin/env python3
"""
Snake Game - Entry Point
Professional Snake game implementation with NiceGUI
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import and run the application
if __name__ == "__main__":
    from app.main import main
    main()