#!/bin/bash

echo "🚀 Creating RMS Server Project..."

# Create folders
mkdir -p models
mkdir -p parsers
mkdir -p handlers
mkdir -p printers
mkdir -p logs

# Root files
touch app.py
touch config.py
touch .env
touch README.md
touch requirements.txt

# Package initialization
touch models/__init__.py
touch parsers/__init__.py
touch handlers/__init__.py
touch printers/__init__.py

# Python files
touch models/message.py
touch models/content.py

touch parsers/slack_parser.py

touch handlers/message_handler.py

touch printers/console_printer.py

# Logs
echo "[]" > logs/slack_events.json

echo "✅ Project Created Successfully!"