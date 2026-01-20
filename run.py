import sys
import os

# Add the current directory to python path so we can import 'bot'
sys.path.append(os.getcwd())

from bot.main import main

if __name__ == "__main__":
    main()
