"""
This script handles notifications for the Pulse Tracker bot.
 It alerts users when a token's value increases or decreases by more than 100%.
 When a user clicks the buy/sell button, they are redirected to another bot (Buy-Sell bot)
 to execute the transaction.
"""


from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler
import requests
from decimal import getcontext
import json
from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

# set decimal precision
getcontext().prec = 18



def calling_backend_api(url, method, payload=None):
    try:
        headers = {"Content-Type": "application/json"}

        if payload is not None:
            payload = json.dumps(payload)

        methods = {
            "GET": requests.get,
            "POST": requests.post,
            "PUT": requests.put,
            "PATCH": requests.patch,
            "DELETE": requests.delete,
        }

        if method not in methods:
            return "Invalid HTTP method"

        if method == "GET":
            response = methods[method](url, headers=headers, params=payload)
        else:
            response = methods[method](url, headers=headers, data=payload)

        if response.status_code in [200, 201]:
            return response.text
        else:
            response = json.loads(response.text)
            return response

    except Exception as e:
        return str(e)


async def swap(update: Update, context: Application) -> None:
    """Sends a message with three inline buttons attached."""

    await update.message.reply_text(
        "🛠️ Recifi Whales Pulse Tracker Notifications"
    )


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands([BotCommand("start", "start")])


def main() -> None:
    """Run the bot."""

    # Access the environment variables
    pulse_tracker_notification_bot_token = os.getenv(
        "PULSE_TRACKER_NOTIFICATION_BOT_TOKEN"
    )
    # Create the Application and pass it your bot's token.
    application = (
        Application.builder()
        .token(pulse_tracker_notification_bot_token)
        .post_init(post_init)
        .build()
    )

    application.add_handler(CommandHandler("start", swap))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
