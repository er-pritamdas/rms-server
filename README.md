# RMS (Reel Management System)

An AI-powered knowledge ingestion platform.

RMS collects information from Slack, extracts useful content such as links, documents, and media, processes them using AI, and stores structured knowledge for future semantic search.

---

## 🚀 Features

### Current Features
- **Slack Events API Integration**: Listens to messages and URL verification challenges.
- **Event-Driven Architecture**: Decoupled message handling.
- **Flask Backend**: Light and flexible REST API.
- **Slack Parser**: Extracts and normalizes message components.
- **Pydantic Models**: Strongly-typed data validation for text, emojis, and links.
- **Console Printer**: Beautifully formatted terminal logging for processed events.
- **Event Logging**: Stores the last `100` raw Slack event payloads in `logs/slack_events.json`.

### Planned Features
- 📸 Instagram Downloader
- 🎥 YouTube Downloader
- 🌐 Website Scraper
- 🎙️ Whisper Transcription
- 🦜 LangChain Integration
- 🐘 PostgreSQL & Vector Database
- 🔍 Semantic Search

---

## 📂 Project Structure

```text
rms-server/
├── app.py                  # Main Flask entrypoint & Slack Event listener
├── config.py               # Global application configuration
├── requirements.txt        # Application dependencies
├── .env.example            # Environment configuration template
├── handlers/               # Event dispatchers & processors
│   └── message_handler.py
├── models/                 # Pydantic data schemas
│   ├── content.py          # Content blocks (Text, Emoji, Link)
│   └── message.py          # ParsedMessage schema
├── parsers/                # Payloads parsers
│   └── slack_parser.py     # Parses Slack JSON into internal models
└── printers/               # Output formatting
    └── console_printer.py  # Pretty printer for the terminal
```

---

## 🛠️ Getting Started

### Prerequisites
- Python 3.10+
- Virtual environment (`venv`)

### Setup Instructions

1. **Clone the repository and navigate to the project directory:**
   ```bash
   cd rms-server
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Copy the example environment file and fill in your Slack token:
   ```bash
   cp .env.example .env
   ```

5. **Start the Flask server:**
   ```bash
   python app.py
   ```

---

## 💻 Development

### Code Formatting
Ensure code style consistency before submitting pull requests:

- **Format code** with `black`:
  ```bash
  black .
  ```
- **Sort imports** with `isort`:
  ```bash
  isort .
  ```
- **Lint code** with `ruff`:
  ```bash
  ruff check .
  ```