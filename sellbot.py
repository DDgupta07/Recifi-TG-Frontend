"""
This code handles buy/sell operations, manual swaps, and swaps 
triggered by pulse notifications in the Pulse Tracker notification bot.
Users are redirected here to swap tokens, enabling them to buy any token with Ether
or sell tokens to obtain Ether. In manual swap mode, users can specify any token 
address for the swap.
"""


from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
    ForceReply,
    BotCommand,
)
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)
import requests
from decimal import getcontext
import json
from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

# set decimal precision
getcontext().prec = 18



WAITING_FOR_SELL_QUANTITY = 1
WAITING_FOR_SELL_TARGET_PRICE = 2
WAITING_FOR_BUY_QUANTITY = 3
WAITING_FOR_BUY_TARGET_PRICE = 4
WAITING_FOR_SWAP_QUANTITY = 5
WAITING_FOR_BUY_TOKEN_ADDRESS = 6
WAITING_FOR_BUY_AMOUNT = 7
WAITING_FOR_SELL_TOKEN_ADDRESS = 8
WAITING_FOR_SELL_AMOUNT = 9
CLOSE_BUTTON = "x Close"


def calling_backend_api(url, method, payload):
    """
    This function takes three parameters: `url`, `http_verb`, and `payload`.
    It determines the appropriate HTTP method to use, makes a request to the
    backend API using the `requests` library, retrieves the response from the
    backend, and returns the response data.
    """
    try:
        payload = json.dumps(payload)
        headers = {"Content-Type": "application/json"}
        if method == "GET":
            response = requests.get(url, headers=headers, data=payload)
            return response.text
        elif method == "POST":
            response = requests.post(url, headers=headers, data=payload)
            return response.text
        elif method == "PUT" or method == "PATCH":
            response = requests.patch(url, headers=headers, data=payload)
            return response.text
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, data=payload)
            return response.text

    except Exception as e:
        print(str(e))


async def start(update: Update, context: Application) -> None:
    try:
        """
        In the start command of the bot, two scenarios are handled:
        1. When the user is redirected via Pulse Tracker, three parameters
        are passed through Recifi linking. If this condition is met, buy and sell
        swap buttons are displayed upon reaching the bot.
        2. When the user directly starts the bot from the Sell Bot, the
        else part is executed. The actual functionality of this bot involves
        buying and selling tokens.
        """
        query = update.message.text.split()
        params = ''
        if len(query)>1:
            params = query[1].split("_")
        if len(params)==2:
            token_name = params[0]
            token_address = params[1]
            context.user_data["token_name"] = token_name
            context.user_data["token_address"] = token_address
            keyboard = [
                [InlineKeyboardButton("🧿 Buy Token", callback_data="buy_token")],
                [InlineKeyboardButton("🧿 Sell Token", callback_data="sell_token")],
                [InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")],
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                f"🛠️ Contract address: {token_address} \n\n💳 Token name: {token_name}\n\nDo you wish to buy or sell?",
                reply_markup=reply_markup,
            )
        elif len(params) == 3:
            # Parse the parameters from the Recifi link            
            token_name = params[0]
            token_address = params[1]
            percentage = params[2]
            context.user_data["percentage"] = percentage
            context.user_data["token_name"] = token_name
            context.user_data["token_address"] = token_address
            keyboard = [
                [InlineKeyboardButton("🧿 Buy Token", callback_data="buy_token")],
                [InlineKeyboardButton("🧿 Sell Token", callback_data="sell_token")],
                [InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")],
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                f"🛠️ Contract address: {token_address} \n\n💳 Token name: {token_name}\n\n📈 Percentage change over 24 hrs: {percentage}% \n\nDo you wish to buy or sell?",
                reply_markup=reply_markup,
            )

        else:
            main_bot_Recifi_link = "https://t.me/RecifiWhalesAI_bot?start=redirect"

            keyboard = [
                [InlineKeyboardButton("🧿 Manual Buy/Sell", callback_data="swap_bot")],
                [InlineKeyboardButton("🧿 Limit buy bot", callback_data="buy_bot"),InlineKeyboardButton("🧿 Limit sell bot", callback_data="sell_bot")],
                [InlineKeyboardButton("🧿 View orders", callback_data="open_order"),InlineKeyboardButton("🧿 Cancel open order", callback_data="cancel_order")],
                
                [InlineKeyboardButton("🔙 Back To Recifi Whales AI Bot", url=main_bot_Recifi_link)],
                [InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")],
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "🛠️ Recifi Whales AI Bot - Giving users an almost unfair advantage",
                reply_markup=reply_markup,
            )

    except Exception as e:
        print(e)


async def button(update: Update, context: Application) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()

    if query.data == "buy_bot":
        """
        In this scenario, buy other token and we ask to user enter amount if us-er have difault wallet
        """
        user_id = query.from_user.id
        url = f"{BASE_URL}api/default-wallet/?telegram_user_id={user_id}"
        payload = {}
        method = "GET"
        get_default_user_wallet = calling_backend_api(url, method, payload)
        get_default_user_wallet = json.loads(get_default_user_wallet)
        if get_default_user_wallet["status"]:
            await query.message.reply_text(
                f"You have {get_default_user_wallet['data']['balance']} ETH in your wallet \n\n Enter the amount of ETH in USDT to buy? ",
                reply_markup=ForceReply(selective=True),
            )
            return WAITING_FOR_BUY_QUANTITY
        else:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"😞 {get_default_user_wallet['message']}",
            )

    if query.data == "cancel_order":
        user_id = query.from_user.id
        url = f"{BASE_URL}api/trade/?telegram_user_id={user_id}&status=open"
        payload = {}
        method = "GET"
        response = calling_backend_api(url, method, payload)
        response = json.loads(response)
        keyboard = list()
        if response["status"]:
            for count, order in enumerate(response["data"]):
                callback_data = f"can_order_{order['uuid']}"
                keyboard.append(
                    [
                        InlineKeyboardButton(
                            f"wallet {count+1}: {order['trade_type']} {order['quantity'] } {order['target_price'] }",
                            callback_data=callback_data,
                        )
                    ]
                )
            keyboard.append([InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                reply_markup=reply_markup,
            )
        else:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=response["message"]
            )
    elif query.data == "close":
        # Remove the menu
        await query.message.delete()
    if query.data.startswith("can_order_"):
        uuid = query.data.split("_")[-1]
        url = f"{BASE_URL}api/trade/{uuid}/"
        payload = {}
        method = "PATCH"
        response = calling_backend_api(url, method, payload)
        response = json.loads(response)
        await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=response["message"]
            )

    if query.data == "open_order":
        keyboard = [
            [
                InlineKeyboardButton(
                    "✨ View open orders", callback_data="view_or_open"
                )
            ],
            [InlineKeyboardButton("✨ View closed orders", callback_data="view_or_closed")],
            [InlineKeyboardButton("✨ View cancelled orders", callback_data="view_or_cancelled")],
            
            [InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Select to view",
            reply_markup=reply_markup,
        )


    if query.data.startswith("view_or_"):
        status = query.data.split("_")[-1]
        user_id = query.from_user.id
        url = f"{BASE_URL}api/trade/?telegram_user_id={user_id}&status={status}"
        payload = {}
        method = "GET"
        response = calling_backend_api(url, method, payload)
        response = json.loads(response)
        message_list = list()
        if status == "open":
            heading = "List of open orders"
        elif status == "closed":
            heading = "List of closed orders"
        else:
            heading = "List of cancelled orders"
        message_list.append(f"{heading}\n\n")
        if response["status"]:
            for trade in response['data']:
                text = f'🛒 Trade type: {trade["trade_type"]}\n📦 Quantity: {trade["quantity"]}\n🎯 Target price: {trade["target_price"]}\n'
                message_list.append(text)
            message = '\n'.join(message_list)
        else:
            message = response["message"]
        await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=message,
            )


    if query.data == "buy_token":
        """
        This section handles the redirection for buying tokens (swap buy, where we purchase other tokens
        using ether) and prompts the user to enter the amount.
        """

        user_id = query.from_user.id
        url = f"{BASE_URL}api/default-wallet/?telegram_user_id={user_id}"
        payload = {}
        method = "GET"
        get_default_user_wallet = calling_backend_api(url, method, payload)
        get_default_user_wallet = json.loads(get_default_user_wallet)
        if get_default_user_wallet["status"]:
            if get_default_user_wallet["data"]["balance"] <= 0:
                await context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text="you have 0 ETH please fund your wallet first",
                )
                return ConversationHandler.END
            await query.message.reply_text(
                f"Your Ether balance is {get_default_user_wallet['data']['balance']}\n\n How much do you want to buy?",
                reply_markup=ForceReply(selective=True),
            )
            return WAITING_FOR_BUY_AMOUNT
        else:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"😞 {get_default_user_wallet['message']}",
            )

    if query.data == "sell_token":
        """
        This section handles the redirection for selling tokens (swap sell, where we purchase ether
        using other token) and prompts the user to enter the amount.
        """
        user_id = query.from_user.id
        url = f"{BASE_URL}api/default-wallet/?telegram_user_id={user_id}"
        payload = {}
        method = "GET"
        get_default_user_wallet = calling_backend_api(url, method, payload)
        get_default_user_wallet = json.loads(get_default_user_wallet)
        if get_default_user_wallet["status"]:
            url1 = f"{BASE_URL}api/token-balance/"
            payload = {
                "telegram_user_id": user_id,
                "token_address": context.user_data.get("token_address"),
            }
            method = "POST"
            response = calling_backend_api(url1, method, payload)
            response = json.loads(response)
            token_holdings = response["data"]["balance"]
            token_name = context.user_data.get("token_name")
            if token_holdings:
                # for token_hol_dict in token_holdings:
                #     if token_name in token_hol_dict:
                await query.message.reply_text(
                    f"💳 You have {token_holdings} in {token_name}.\n\n How much do you want to sell?:",
                    reply_markup=ForceReply(selective=True),
                )
                return WAITING_FOR_SELL_AMOUNT
            await query.message.reply_text(
                f"😞 You have 0 balance in {token_name}",
            )
            return ConversationHandler.END

        else:
            await context.bot.send_message(
                chat_id=query.message.chat_id, text=get_default_user_wallet["message"]
            )

    elif query.data == "sell_bot":
        """
        In this scenario, sell other token and we ask to user enter amount if user have difault wallet
        """
        user_id = query.from_user.id
        url = f"{BASE_URL}api/default-wallet/?telegram_user_id={user_id}"
        payload = {}
        method = "GET"
        get_default_user_wallet = calling_backend_api(url, method, payload)
        get_default_user_wallet = json.loads(get_default_user_wallet)
        if get_default_user_wallet["status"]:
            await query.message.reply_text(
                f"You have {get_default_user_wallet['data']['balance']} ETH in your wallet \n\nEnter quantity of ETH to sell:",
                reply_markup=ForceReply(selective=True),
            )
            return WAITING_FOR_SELL_QUANTITY
        else:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"😞 {get_default_user_wallet['message']}",
            )

    elif query.data == "buy_swap_bot":
        """
        In this scenario, when the user selects the manual buy button and ask to user enter token
        address which you have to buy
        """
        await query.message.reply_text(
            "Enter token address:", reply_markup=ForceReply(selective=True)
        )
        return WAITING_FOR_BUY_TOKEN_ADDRESS

    elif query.data == "sell_swap_bot":
        """
        In this scenario, when the user selects the manual sell button and ask to user enter token
        address which you have to sell
        """
        await query.message.reply_text(
            "Enter token address:", reply_markup=ForceReply(selective=True)
        )
        return WAITING_FOR_SELL_TOKEN_ADDRESS

    elif query.data == "swap_bot":
        """
        In this scenario, when the user selects the manual buy-sell button and after initiates the direct start command.
        """

        keyboard = [
            [InlineKeyboardButton("🧿 Manual buy", callback_data="buy_swap_bot")],
            [InlineKeyboardButton("🧿 Manual sell", callback_data="sell_swap_bot")],
            [InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="🛠️ Recifi Whales AI Bot - Giving users an almost unfair advantage",
            reply_markup=reply_markup,
        )


async def receive_buy_token_address(update: Update, context: Application):
    token_address = update.message.text
    context.user_data["token_address"] = token_address
    await update.message.reply_text(
        "Please enter amount in $ETH:", reply_markup=ForceReply(selective=True)
    )
    return WAITING_FOR_BUY_AMOUNT


async def receive_sell_token_address(update: Update, context: Application):
    token_address = update.message.text
    context.user_data["token_address"] = token_address
    url = f"{BASE_URL}api/token-balance/"
    user_id = update.effective_user.id
    payload = {
        "telegram_user_id": user_id,
        "token_address": token_address,
    }
    method = "POST"
    response = calling_backend_api(url, method, payload)
    response = json.loads(response)
    token_name = ''
    if response['status']:
        token_name = response['data']['token_name']
    await update.message.reply_text(
        f"Please enter amount in {token_name}:", reply_markup=ForceReply(selective=True)
    )
    return WAITING_FOR_SELL_AMOUNT


async def receive_sell_amount(update: Update, context: Application):
    """swap sell"""
    amount = update.message.text
    token_address = context.user_data.get("token_address")
    url = f"{BASE_URL}api/swap-token/"
    user_id = update.effective_user.id
    payload = {
        "telegram_user_id": user_id,
        "amount": amount,
        "token_address": token_address,
        "swap_type": "sell",
    }
    method = "POST"
    response = calling_backend_api(url, method, payload)
    response = json.loads(response)

    message = response["message"]

    await update.message.reply_text(message)
    return ConversationHandler.END


async def receive_buy_amount(update: Update, context: Application):
    """"""
    amount = update.message.text
    token_address = context.user_data.get("token_address")
    url = f"{BASE_URL}api/swap-token/"
    user_id = update.effective_user.id
    payload = {
        "telegram_user_id": user_id,
        "amount": amount,
        "token_address": token_address,
        "swap_type": "buy",
    }
    method = "POST"
    response = calling_backend_api(url, method, payload)
    response = json.loads(response)
    message = response["message"]
    await update.message.reply_text(message)
    return ConversationHandler.END


async def receive_buy_eth_quantity(update: Update, context: Application) -> int:
    eth_quantity = update.message.text
    context.user_data["eth_quantity"] = eth_quantity

    await update.message.reply_text(
        "Enter target price in USDT:", reply_markup=ForceReply(selective=True)
    )
    return WAITING_FOR_BUY_TARGET_PRICE


async def receive_buy_target_price(update: Update, context: Application) -> int:
    user_id = update.effective_user.id
    target_price_usd = update.message.text
    eth_quantity = context.user_data.get("eth_quantity")
    url = f"{BASE_URL}api/trade/"
    payload = {
        "telegram_user_id": user_id,
        "trade_type": "buy",
        "quantity": eth_quantity,
        "target_price": target_price_usd,
    }
    method = "POST"
    response = calling_backend_api(url, method, payload)
    response = json.loads(response)
    main_bot_Recifi_link = "https://t.me/RecifiWhalesAI_bot?start=redirect"
    keyboard = [
        [InlineKeyboardButton("🧿 Main bot", url=main_bot_Recifi_link)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if response["status"]:

        message = f'✅ {response["message"]} for {eth_quantity} quantity at target price {target_price_usd}'
        await update.message.reply_text(message, reply_markup=reply_markup)
    else:
        message = f'❌ {response["message"]}'
        await update.message.reply_text(message, reply_markup=reply_markup)
    return ConversationHandler.END


async def receive_sell_eth_quantity(update: Update, context: Application) -> int:
    eth_quantity = update.message.text
    context.user_data["eth_quantity"] = eth_quantity
    await update.message.reply_text(
        "Enter target price in USDT:", reply_markup=ForceReply(selective=True)
    )
    return WAITING_FOR_SELL_TARGET_PRICE


async def receive_sell_target_price(update: Update, context: Application) -> int:
    user_id = update.effective_user.id
    target_price_usd = update.message.text
    eth_quantity = context.user_data.get("eth_quantity")
    url = f"{BASE_URL}api/trade/"
    payload = {
        "telegram_user_id": user_id,
        "trade_type": "sell",
        "quantity": eth_quantity,
        "target_price": target_price_usd,
    }
    method = "POST"
    response = calling_backend_api(url, method, payload)
    response = json.loads(response)
    main_bot_Recifi_link = "https://t.me/RecifiWhalesAI_bot?start=redirect"
    keyboard = [
        [InlineKeyboardButton("🧿 Main bot", url=main_bot_Recifi_link)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if response["status"]:
        message = f"✅ {response['message']} for {eth_quantity} quantity at target price {target_price_usd}"
        await update.message.reply_text(message, reply_markup=reply_markup)
    else:
        message = f'❌ {response["message"]}'
        await update.message.reply_text(message, reply_markup=reply_markup)

    return ConversationHandler.END


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands([BotCommand("start", "start ")])


def main() -> None:
    """Run the bot."""

    # Access the environment variables
    buy_sell_bot_token = os.getenv("BUY_SELL_BOT_TOKEN")
    # Create the Application and pass it your bot's token.
    application = (
        Application.builder().token(buy_sell_bot_token).post_init(post_init).build()
    )

    # Define the conversation handler with states
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button)],
        states={
            WAITING_FOR_BUY_QUANTITY: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, receive_buy_eth_quantity
                )
            ],
            WAITING_FOR_BUY_TARGET_PRICE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, receive_buy_target_price
                )
            ],
            WAITING_FOR_SELL_QUANTITY: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, receive_sell_eth_quantity
                )
            ],
            WAITING_FOR_SELL_TARGET_PRICE: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, receive_sell_target_price
                )
            ],
            WAITING_FOR_BUY_TOKEN_ADDRESS: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, receive_buy_token_address
                )
            ],
            WAITING_FOR_BUY_AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_buy_amount)
            ],
            WAITING_FOR_SELL_TOKEN_ADDRESS: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, receive_sell_token_address
                )
            ],
            WAITING_FOR_SELL_AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_sell_amount)
            ],
        },
        fallbacks=[],
        allow_reentry=True,
    )
    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
