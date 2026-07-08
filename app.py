"""
Main Flask Application

This file acts as the entry point of the RMS Server.
"""

import json
import os
from parsers.slack_parser import parse_message
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, jsonify, request

from config import LOG_FILE, MAX_LOGS
from handlers.message_handler import handle_message

load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """
    Health Check Endpoint
    """
    return "RMS Server Running 🚀"


@app.route("/slack/events", methods=["POST"])
def slack_events():
    """
    Entry point for Slack Events API.
    """

    data = request.get_json()

    save_event_log(data)

    # Slack URL Verification
    if data.get("type") == "url_verification":
        return jsonify(
            {
                "challenge": data["challenge"]
            }
        )

    handle_event(data)

    return "", 200


def handle_event(data: dict):
    """
    Dispatch incoming Slack Events.
    """

    event = data.get("event", {})
    event_type = event.get("type")

    if event_type == "message":

        parsed_message = parse_message(event)

        print(parsed_message)

        handle_message(parsed_message)

    else:
        print(f"Unhandled Event : {event_type}")


def save_event_log(data: dict):
    """
    Save every incoming Slack payload.

    Keeps only the latest MAX_LOGS events.
    """

    logs = []

    if not os.path.exists(LOG_FILE):

        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

        with open(LOG_FILE, "w") as file:
            json.dump([], file)

    with open(LOG_FILE, "r") as file:

        try:
            logs = json.load(file)

        except json.JSONDecodeError:
            logs = []

    logs.append(
        {
            "received_at": datetime.now().isoformat(),
            "payload": data,
        }
    )

    logs = logs[-MAX_LOGS:]

    with open(LOG_FILE, "w") as file:
        json.dump(logs, file, indent=4)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )