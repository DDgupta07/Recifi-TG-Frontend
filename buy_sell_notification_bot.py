"""Handles notifications for successful buy and sell transactions when orders
   are placed through the buy-sell bot."""

from telegram import Update
from telegram.ext import Application
from dotenv import load_dotenv
import os

load_dotenv()



def main() -> None:
    """Run the bot."""

    # Access the environment variables
    buy_sell_notification_bot_token = os.getenv("BUY_SELL_NOTIFICATION_BOT_TOKEN")
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(buy_sell_notification_bot_token).build()

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
