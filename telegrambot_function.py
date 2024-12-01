"""
Requirement
installed python-telegram-bot-21.2,requests==2.31.0
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
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import json

import requests
import json
from telegram.constants import ParseMode
from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL = os.getenv("BASE_URL")
# Define states
WAITING_FOR_ACCOUNT_NAME = 1
WAITING_FOR_PRIVATE_KEY = 2
WAITING_FOR_CREATE_WALLET_NAME = 3
WAITING_FOR_ACCOUNT_NAME_FOR_RENAME = 4
WAITING_FOR_AMOUNT = 5
WAITING_FOR_ADDRESS = 6
WAITING_FOR_CONTRACT_ADDRESS = 7
WAITING_FOR_PRIVATE_KEY_TO_VERIFY = 8
WAITING_FOR_BUY_AMOUNT = 9
WAITING_FOR_RecifiWHALES_COPY_WALLET_NAME = 10
WAITING_FOR_RecifiWHALES_COPY_WALLET_ADDRESS = 11
WAITING_FOR_SELL_AMOUNT = 12
WAITING_FOR_RECIPIENT_ADDRESS = 13
WAITING_FOR_ERC20_TOKEN_ADDRESS = 14
WAITING_FOR_ERC20_AMOUNT = 15
WAITING_FOR_PERCENTAGE_FOR_FUTURE = 16
WAITING_FOR_PERCENTAGE_UPDATE = 17
WAITING_FOR_GAS_PRICE = 18
WAITING_FOR_SLIPPAGE = 19
CHOOSE_AN_OPTION = "Choose an option:"
CLOSE_BUTTON = "x Close"



# Use case of this function is to call backend api to get output.
def calling_backend_api(url, method, payload):
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
    """Sends a message with three inline buttons attached."""
    user_id = update.effective_user.id
    url = f"{BASE_URL}api/user-wallet/?telegram_user_id={user_id}"
    payload = {}
    method = "GET"
    get_user_wallet = calling_backend_api(url, method, payload)
    get_user_wallet = json.loads(get_user_wallet)
    if len(get_user_wallet["data"]) == 0:
        keyboard = [
            [InlineKeyboardButton("✨ Create Wallet", callback_data="create_wallet")],
            [InlineKeyboardButton("✍️ Import Wallet", callback_data="import_wallet")],
            # [InlineKeyboardButton("🧿 Pulse tracker", callback_data="4")],
            [InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "🛠️ Recifi Whales AI Bot - Giving users an almost unfair advantage",
            reply_markup=reply_markup,
        )
    else:
        buy_sell_Recifi_link = "https://t.me/RecifiWhaleAi_sell_bot?start=redirect"
        Recifi_whales_alert_Recifi_link = "https://t.me/RecifiWhalesAlert_bot"
        

        keyboard = [
            [
                InlineKeyboardButton(
                    "🤖 Recifi AI Buy & Sell Bot", callback_data="1", url=buy_sell_Recifi_link
                )
            ],
            [InlineKeyboardButton("📊 Pulse Tracker", callback_data="pulse_tracker")],
            [
                InlineKeyboardButton(
                    "🐋 Recifi Whales Tracker", callback_data="Recifi_whales"
                )
            ],
            [
                InlineKeyboardButton(
                    "🐋 AI Copy Trader", callback_data="Recifi_whales_future"
                )
            ],
            [
                InlineKeyboardButton(
                    "🐋 Whale Movement Alert", url=Recifi_whales_alert_Recifi_link
                )
            ],
            
            
            [InlineKeyboardButton("📈 Dashboard", callback_data="dashboard")],
            [
                InlineKeyboardButton(
                    "⚙️ Wallet Management", callback_data="wallet_settings"
                ),InlineKeyboardButton("💳 Wallets", callback_data="wallet_list_show")
            ],
            [InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "🛠️ Recifi Whales AI Bot - Giving users an almost unfair advantage",
            reply_markup=reply_markup,
        )

async def buy_sell(update: Update, context: Application) -> None:
    buy_sell_Recifi_link = "https://t.me/RecifiWhaleAi_sell_bot?start=redirect"
    keyboard = [
            [
                InlineKeyboardButton(
                    "🤖 Recifi AI Buy & Sell Bot", callback_data="1", url=buy_sell_Recifi_link
                )
            ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Click to jump on Recifi AI Buy & Sell Bot",
        reply_markup=reply_markup,
    )

async def pulse_tracker(update: Update, context: Application) -> None:
    keyboard = [
            [
                InlineKeyboardButton(
                    "📊 Pulse Tracker", callback_data="pulse_tracker"
                )
            ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Click Pulse Tracker",
        reply_markup=reply_markup,
    )

async def Recifi_whales_tracker(update: Update, context: Application) -> None:
    keyboard = [
            [
                InlineKeyboardButton(
                    "🐋 Recifi Whales Tracker", callback_data="Recifi_whales"
                )
            ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Click Recifi Whales Tracker",
        reply_markup=reply_markup,
    )

async def ai_copy_trader(update: Update, context: Application) -> None:
    keyboard = [
            [
                InlineKeyboardButton(
                    "🐋 AI Copy Trader", callback_data="Recifi_whales_future"
                )
            ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Click AI Copy Trader",
        reply_markup=reply_markup,
    )

async def whale_movement_alert(update: Update, context: Application) -> None:
    Recifi_whales_alert_Recifi_link = "https://t.me/RecifiWhalesAlert_bot"
    keyboard = [
            [
                InlineKeyboardButton(
                    "🐋 Whale Movement Alert", url=Recifi_whales_alert_Recifi_link
                )
            ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Click Whale Movement Alert",
        reply_markup=reply_markup,
    )

async def dashboard(update: Update, context: Application) -> None:
    keyboard = [
            [
                InlineKeyboardButton(
                    "📈 Dashboard", callback_data="dashboard"
                )
            ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Click Dashboard",
        reply_markup=reply_markup,
    )

async def import_wallet(update: Update, context: Application) -> None:
    keyboard = [
            [
                InlineKeyboardButton("✍️ Import Wallet", callback_data="import_wallet")
            ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Click Import Wallet",
        reply_markup=reply_markup,
    )

async def create_wallet(update: Update, context: Application) -> None:
    keyboard = [
            [
                InlineKeyboardButton("✨ Create Wallet", callback_data="create_wallet")
            ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Click Create Wallet",
        reply_markup=reply_markup,
    )

async def wallet(update: Update, context: Application) -> None:
    keyboard = [
            [
                InlineKeyboardButton("💳 Wallets", callback_data="wallet_list_show")
            ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Click Wallets",
        reply_markup=reply_markup,
    )

async def wallet_management(update: Update, context: Application) -> None:
    keyboard = [
            [
                 InlineKeyboardButton(
                    "⚙️ Wallet Management", callback_data="wallet_settings")
            ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Click Wallet Management",
        reply_markup=reply_markup,
    )

async def button(update: Update, context: Application) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()

    if query.data == "2":
        keyboard = [
            [InlineKeyboardButton("✨ Create Wallet", callback_data="create_wallet")],
            [InlineKeyboardButton("✍️ Import Wallet", callback_data="import_wallet")],
            [InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=CHOOSE_AN_OPTION,
            reply_markup=reply_markup,
        )
    elif query.data == "wallet_list_show":
        user_id = query.from_user.id
        url = f"{BASE_URL}api/user-wallet/?telegram_user_id={user_id}"
        payload = {}
        method = "GET"
        get_user_wallet = calling_backend_api(url, method, payload)
        get_user_wallet = json.loads(get_user_wallet)
        message_data = list()
        message_data.append('List of your wallets\n\n')
        for count, wallet in enumerate(get_user_wallet["data"]):
            if wallet["is_default"]:
                text = f"✅ {count+1} wallet(Default) : {wallet['wallet_name']} \naddress : `{wallet['wallet_address']}`\nETH balance : {wallet['balance']}\nEtherscan url [Click here]({wallet['etherscan_url']})\n\n"
                
            else:
                text = f"✅{count+1} wallet: {wallet['wallet_name']} \naddress : `{wallet['wallet_address']}`\nETH balance : {wallet['balance']}\nEtherscan url [Click here]({wallet['etherscan_url']})\n\n"
            message_data.append(str(text))
        message = ''.join(message_data)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=message,parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )

    elif query.data=="Recifi_whales_future":
        keyboard = [
            
            [InlineKeyboardButton("📈 Top 5 gainers", callback_data="future_change_gainers")],
            [InlineKeyboardButton("📉 Top 5 losers", callback_data="future_change_losers")],
            [InlineKeyboardButton("📉 Open future trades", callback_data="open_future_trades")],
            [InlineKeyboardButton("📉 Cancelled future trades", callback_data="cancelled_future_trades")],
            [InlineKeyboardButton("📉 Edit future trades", callback_data="edit_future_trades")],
            [InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=CHOOSE_AN_OPTION,
            reply_markup=reply_markup,
        )
    elif query.data.startswith("future_change_"):
        callback_data = query.data.split("_")[-1]
        
        keyboard = [
            [InlineKeyboardButton("📈 24 hours duration", callback_data=f"{callback_data}_future_24h")],
            [InlineKeyboardButton("📈 7 days duration", callback_data=f"{callback_data}_future_7d")],
            [InlineKeyboardButton("📈 1 month duration", callback_data=f"{callback_data}_future_1m")],
            [InlineKeyboardButton("📈 1 year duration", callback_data=f"{callback_data}_future_1y")],
            [InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"Choose a duration for {callback_data}",
            reply_markup=reply_markup,
        )
    elif query.data=="open_future_trades":
        user_id = query.from_user.id
        url = f"{BASE_URL}api/future-trade/?telegram_user_id={user_id}"
        payload = {}
        method = "GET"
        response = calling_backend_api(url, method, payload)
        response = json.loads(response)
        if response['status']:
            message_data = list()
            message_data.append('✨ Your future trade ✨\n\n')
            for count, data in enumerate(response['data']):
                message = f"{count+1} Wallet: `{data['Recifiwhale']['wallet_address']}`\nPercentage: {data['percentage_amount']}\n\n"
                message_data.append(message)
            message = "\n".join(message_data)
            await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN
        )   
        else:
            await context.bot.send_message(
            chat_id=query.message.chat_id,
            text='You have not future trade'
        )

    elif query.data.startswith("gainers_future"):
        duration = query.data.split("_")[-1]
        telegram_user_id = query.from_user.id
        if duration == '24h':
            url = f"{BASE_URL}api/Recifi-whale/?telegram_user_id={telegram_user_id}"
        else:
            url = f"{BASE_URL}api/Recifi-whale/?duration={duration}?telegram_user_id={telegram_user_id}"
        payload = {}
        method = "GET"
        get_Recifi_whales_wallet = calling_backend_api(url, method, payload)
        get_Recifi_whales_wallet = json.loads(get_Recifi_whales_wallet)
        context.user_data["future_wallet_data_for_ether"] = get_Recifi_whales_wallet
        keyboard = list()
        text = ""
           
        for count, wallet in enumerate(get_Recifi_whales_wallet["data"]):
            callback_data = f"Recifi_f_{wallet['uuid']}"
            
            data_to_show = f"💳 {wallet['wallet_address'][:4]}...{wallet['wallet_address'][-4:]}  {wallet['percentage_change']}%"

            text = text + f"{data_to_show}\n\n"
            keyboard.append(
                [
                    InlineKeyboardButton(
                        data_to_show,
                        callback_data=callback_data,
                    )
                ]
            )
        keyboard.append([InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="✨ Top 5 performing wallets\n\n✨ Choose a wallet to copy future trades",
            reply_markup=reply_markup,
        )
    elif query.data=="cancelled_future_trades":
        user_id = query.from_user.id
        url = f"{BASE_URL}api/future-trade/?telegram_user_id={user_id}"
        payload = {}
        method = "GET"
        response = calling_backend_api(url, method, payload)
        response = json.loads(response)
        keyboard = list()
        text = ""
        if not response["status"]:
            await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="You have not any open future trade to cancel",
        )
            
        for count, wallet in enumerate(response["data"]):
            callback_data = f"Recifi_f_cancel_{wallet['uuid']}"
            
            data_to_show = f"💳 {wallet['Recifiwhale']['wallet_address'][:4]}...{wallet['Recifiwhale']['wallet_address'][-4:]}  {wallet['percentage_amount']}%"

            text = text + f"{data_to_show}\n\n"
            keyboard.append(
                [
                    InlineKeyboardButton(
                        data_to_show,
                        callback_data=callback_data,
                    )
                ]
            )
        keyboard.append([InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="✨ Choose wallet to cancel future trade\n\n",
            reply_markup=reply_markup,
        )
    elif query.data.startswith('Recifi_f_cancel_'):
        uuid = query.data.split("_")[-1]
        url = f"{BASE_URL}api/future-trade/{uuid}/"
        payload = {}
        method = "DELETE"
        response = calling_backend_api(url, method, payload)
        response = json.loads(response)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"🟢 {response['message']}"
        )
    
    elif query.data=="edit_future_trades":
        user_id = query.from_user.id
        url = f"{BASE_URL}api/future-trade/?telegram_user_id={user_id}"
        payload = {}
        method = "GET"
        response = calling_backend_api(url, method, payload)
        response = json.loads(response)
        keyboard = list()
        text = ""
        if not response["status"]:
            await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="You have not any open future trade to update",
        )
           
        for count, wallet in enumerate(response["data"]):
            callback_data = f"Recifi_f_edit_{wallet['uuid']}"
            
            data_to_show = f"💳 {wallet['Recifiwhale']['wallet_address'][:4]}...{wallet['Recifiwhale']['wallet_address'][-4:]}  {wallet['percentage_amount']}%"

            text = text + f"{data_to_show}\n\n"
            keyboard.append(
                [
                    InlineKeyboardButton(
                        data_to_show,
                        callback_data=callback_data,
                    )
                ]
            )
        keyboard.append([InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="✨ Choose wallet to edit future trade\n\n",
            reply_markup=reply_markup,
        )
    elif query.data.startswith('Recifi_f_edit_'):
        uuid_data = query.data.split("_")[-1]
        context.user_data["uuid_data"] = uuid_data
        await query.message.reply_text(
                "Enter a new percentage for copy trade",
                reply_markup=ForceReply(selective=True),
            )
        return WAITING_FOR_PERCENTAGE_UPDATE

    elif query.data.startswith( "losers_future"):
        duration = query.data.split("_")[-1]
        telegram_user_id = query.from_user.id
        if duration == '24h':
            url = f"{BASE_URL}api/Recifi-whale/?type=losers&telegram_user_id={telegram_user_id}"
        else:
            url = f"{BASE_URL}api/Recifi-whale/?type=losers&duration={duration}?telegram_user_id={telegram_user_id}"
        payload = {}
        method = "GET"
        get_Recifi_whales_wallet = calling_backend_api(url, method, payload)
        get_Recifi_whales_wallet = json.loads(get_Recifi_whales_wallet)
        context.user_data["future_wallet_data_for_ether"] = get_Recifi_whales_wallet
        keyboard = list()
        text = ""
        for count, wallet in enumerate(get_Recifi_whales_wallet["data"]):
            callback_data = f"Recifi_f_{wallet['uuid']}"
            data_to_show = f"💳 {wallet['wallet_address'][:4]}...{wallet['wallet_address'][-4:]}  {wallet['percentage_change']}%"

            text = text + f"{data_to_show}\n\n"
            keyboard.append(
                [
                    InlineKeyboardButton(
                        data_to_show,
                        callback_data=callback_data,
                    )
                ]
            )
        keyboard.append([InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="✨ Worst 5 performing wallets\n\n✨ Choose a wallet to copy future trades",
            reply_markup=reply_markup,
        )

    elif query.data=="my_wallet_Recifiwhale": 
        telegram_user_id = query.from_user.id
        url = f"{BASE_URL}api/Recifiwhale-wallets/?telegram_user_id={telegram_user_id}"
        payload = {}
        method = "GET"
        response = calling_backend_api(url, method, payload)
        response = json.loads(response)

        data_to_show = ["✨ Your whale wallet ✨\n"]

        if len(response['data']) == 0:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="✨ Add your whale wallet first",
            )
        else:
            for count, data in enumerate(response['data']):
                data_to_show.append(f"wallet {count + 1}: `{data['wallet_address']}`\n")
            
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="\n".join(data_to_show),
                parse_mode=ParseMode.MARKDOWN,
            )

    elif query.data=="delete_wallet_Recifiwhale": 
        telegram_user_id = query.from_user.id
        url = f"{BASE_URL}api/Recifiwhale-wallets/?telegram_user_id={telegram_user_id}"
        payload = {}
        method = "GET"
        response = calling_backend_api(url, method, payload)
        response = json.loads(response)
        if len(response['data']) == 0:
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="✨ Add your whale wallet first",
            )
        else:
            keyboard = []
            for count, data in enumerate(response["data"]):
                callback_data = f"can_whale_wall_{data['uuid']}"
                keyboard.append(
                    [
                        InlineKeyboardButton(
                            f"wallet {count + 1}: {data['wallet_address'][:4]}--{data['wallet_address'][-4:]}",
                            callback_data=callback_data,
                        )
                    ]
                )
            
            # Add a close button to the keyboard
            keyboard.append([InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")])
            
            # Create the inline keyboard markup
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Send the message with the inline keyboard
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text="✨ Choose whale wallet to delete",
                reply_markup=reply_markup,
            )
    elif query.data.startswith("can_whale_wall_"):
        uuid = query.data.split("_")[-1]
        telegram_user_id = query.from_user.id
        url = f"{BASE_URL}api/Recifiwhale-wallets/{uuid}/?telegram_user_id={telegram_user_id}"
        payload = {}
        method = "PATCH"
        response = calling_backend_api(url, method, payload)
        response = json.loads(response)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"🟢 {response['message']}",
        )


    elif query.data=="Recifi_whales":    
        keyboard = [
            
            [InlineKeyboardButton("📈 Top 5 gainers", callback_data="hour_change_gainers")],
            [InlineKeyboardButton("📉 Top 5 losers", callback_data="hour_change_losers")],
            [InlineKeyboardButton("🎫 Added whale wallet", callback_data="my_wallet_Recifiwhale")],
            [InlineKeyboardButton("🎫 add whale wallet", callback_data="add_wallet_Recifiwhale")],
            [InlineKeyboardButton("🎫 Delete whale wallet", callback_data="delete_wallet_Recifiwhale")],
            [InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=CHOOSE_AN_OPTION,
            reply_markup=reply_markup,
        )

    elif query.data.startswith("hour_change_"):
        callback_data = query.data.split("_")[-1]
        
        keyboard = [
            [InlineKeyboardButton("📈 24 hours duration", callback_data=f"{callback_data}_24h")],
            [InlineKeyboardButton("📈 7 days duration", callback_data=f"{callback_data}_7d")],
            [InlineKeyboardButton("📈 1 month duration", callback_data=f"{callback_data}_1m")],
            [InlineKeyboardButton("📈 1 year duration", callback_data=f"{callback_data}_1y")],
            [InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"Choose a duration for {callback_data}",
            reply_markup=reply_markup,
        )
    
    elif query.data == "add_wallet_Recifiwhale":
         await query.message.reply_text(
                "Enter whale wallet name:",
                reply_markup=ForceReply(selective=True),
            )
         return WAITING_FOR_RecifiWHALES_COPY_WALLET_NAME

    elif query.data.startswith( "losers"):
        duration = query.data.split("_")[-1]
        telegram_user_id = query.from_user.id
        if duration == '24h':
            url = f"{BASE_URL}api/Recifi-whale/?type=losers&telegram_user_id={telegram_user_id}"
        else:
            url = f"{BASE_URL}api/Recifi-whale/?type=losers&duration={duration}?telegram_user_id={telegram_user_id}"
        payload = {}
        method = "GET"
        get_Recifi_whales_wallet = calling_backend_api(url, method, payload)
        get_Recifi_whales_wallet = json.loads(get_Recifi_whales_wallet)

        keyboard = list()
        text = ""
        future_data = context.user_data.get("future_data")
        for count, wallet in enumerate(get_Recifi_whales_wallet["data"]):
            if future_data == "future":
                callback_data = f"Recifi_f_{wallet['uuid']}"
            else:
                callback_data = f"Recifi_w_{wallet['wallet_address']}"
            data_to_show = f"💳 {wallet['wallet_address'][:4]}...{wallet['wallet_address'][-4:]}  {wallet['percentage_change']}%"

            text = text + f"{data_to_show}\n\n"
            keyboard.append(
                [
                    InlineKeyboardButton(
                        data_to_show,
                        callback_data=callback_data,
                    )
                ]
            )
        keyboard.append([InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="✨ Worst 5 performing wallets\n\n✨ Choose a wallet to see the top token holdings",
            reply_markup=reply_markup,
        )
   
    elif query.data.startswith("Recifi_f_"):
        wallet_uuid = query.data.split("_")[-1]
        # user_id = query.from_user.id
        # response = 'future_wallet_data_for_ether'
        wallet_add = ''
        for wallet in context.user_data.get("future_wallet_data_for_ether")['data']:
            if wallet_uuid == wallet['uuid']:
                wallet_add = wallet['wallet_address']
                break
        ether_wallet_link = f"https://etherscan.io/address/{wallet_add}"
        context.user_data["wallet_uuid"] = wallet_uuid
        await query.message.reply_text(
        f"Wallet address :`{wallet_add}`\n[Etherscan link]({ether_wallet_link})\nEnter percentage amount to copy future trade:", reply_markup=ForceReply(selective=True)
        ,parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True)
        return WAITING_FOR_PERCENTAGE_FOR_FUTURE
   
    elif query.data.startswith("gainers"):
        duration = query.data.split("_")[-1]
        telegram_user_id = query.from_user.id
        if duration == '24h':
            url = f"{BASE_URL}api/Recifi-whale/?telegram_user_id={telegram_user_id}"
        else:
            url = f"{BASE_URL}api/Recifi-whale/?duration={duration}?telegram_user_id={telegram_user_id}"
        payload = {}
        method = "GET"
        get_Recifi_whales_wallet = calling_backend_api(url, method, payload)
        get_Recifi_whales_wallet = json.loads(get_Recifi_whales_wallet)

        keyboard = list()
        text = ""
        future_data = context.user_data.get("future_data")
           
        for count, wallet in enumerate(get_Recifi_whales_wallet["data"]):
            if future_data == "future":
                callback_data = f"Recifi_f_{wallet['uuid']}"
            else:
                callback_data = f"Recifi_w_{wallet['wallet_address']}"
            data_to_show = f"💳 {wallet['wallet_address'][:4]}...{wallet['wallet_address'][-4:]}  {wallet['percentage_change']}%"

            text = text + f"{data_to_show}\n\n"
            keyboard.append(
                [
                    InlineKeyboardButton(
                        data_to_show,
                        callback_data=callback_data,
                    )
                ]
            )
        keyboard.append([InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="✨ Top 5 performing wallets\n\n✨ Choose a wallet to see the top token holdings",
            reply_markup=reply_markup,
        )
   
    elif query.data.startswith("Recifi_w_"):

        wallet_address = query.data.split("_")[-1]
        url = f"{BASE_URL}api/wallet-holdings/?wallet_address={wallet_address}"
        payload = {}
        method = "GET"
        get_Recifi_whales_holding = calling_backend_api(url, method, payload)
        get_Recifi_whales_holding = json.loads(get_Recifi_whales_holding)

        keyboard = []

        for token in get_Recifi_whales_holding["data"]:
            text = (
                f"💰 Symbol: `{token['symbol']}`\n"
                f"✨ Contract Name: {token['contract_name']}\n"
                f"✨ Contract Address: `{token['contract_address']}`\n"
                f"💰 Balance: {token['balance']}\n"
                f"✨ Total USD value: {token['pretty_quote']}\n🔍 Token Etherscan Link [Click here]({token['token_url']})\n🛠️ DexTools Link [Click here]({token['dex_url']})\n"
            )
            button = InlineKeyboardButton(
                f"Buy/sell {token['symbol']}",
                callback_data=f"bd2__{token['symbol']}_{token['contract_address']}",
            )
            keyboard.append([button])
            await update.callback_query.message.reply_text(text,parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,)

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.reply_text(
            "Select a token:", reply_markup=reply_markup,
            
        )
    
    elif query.data.startswith("bd2__"):
        token_name, token_address = query.data.split("__")[-1].rsplit("_", 1)
        context.user_data["token_address"] = token_address
        context.user_data["token_name"] = token_name
        keyboard = [
            [InlineKeyboardButton(f"🛒 Buy {token_name}", callback_data="Recifiwhales_copy_buy")],
            [InlineKeyboardButton(f"🛒 Sell {token_name}", callback_data="Recifiwhales_copy_sell")],
            [InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=CHOOSE_AN_OPTION,
            reply_markup=reply_markup,
        )

    elif query.data == "Recifiwhales_copy_sell":
        user_id = query.from_user.id
        token_name = context.user_data.get("token_name")
        url = f"{BASE_URL}api/default-wallet/?telegram_user_id={user_id}"
        payload = {}
        method = "GET"
        get_default_user_wallet = calling_backend_api(url, method, payload)
        get_default_user_wallet = json.loads(get_default_user_wallet)
        if get_default_user_wallet["status"]:
            if context.user_data.get("token_name") == 'ETH':
                await query.message.reply_text(
                    "💳 How much do you want to sell?:",
                    reply_markup=ForceReply(selective=True),
                )
                return WAITING_FOR_SELL_AMOUNT
            url1 = f"{BASE_URL}api/token-balance/"
            payload = {
                "telegram_user_id": user_id,
                "token_address": context.user_data.get("token_address"),
            }
            method = "POST"
            response = calling_backend_api(url1, method, payload)
            response = json.loads(response)
            token_holdings = response["data"]["balance"]
            
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


    elif query.data == "Recifiwhales_copy_buy":
        user_id = query.from_user.id
        url = f"{BASE_URL}api/default-wallet/?telegram_user_id={user_id}"
        payload = {}
        method = "GET"
        get_default_user_wallet = calling_backend_api(url, method, payload)
        get_default_user_wallet = json.loads(get_default_user_wallet)
        if get_default_user_wallet["status"]:
            
            
            if context.user_data.get("token_name") == 'ETH':
                url = f"{BASE_URL}api/token-balance/"
                user_id = update.effective_user.id
                token_address = '0xdac17f958d2ee523a2206206994597c13d831ec7'
                payload = {
                    "telegram_user_id": user_id,
                    "token_address": token_address,
                }
                method = "POST"
                response = calling_backend_api(url, method, payload)
                response = json.loads(response)
                if response['status']:
                    await query.message.reply_text(
                    f"Your USDT balance is {response['data']['balance']}\n\n Enter the amount of ETH in USDT to buy?",
                    reply_markup=ForceReply(selective=True),
                    )
                    return WAITING_FOR_BUY_AMOUNT
            else:
                if get_default_user_wallet["data"]["balance"] <= 0:
                    await context.bot.send_message(
                        chat_id=query.message.chat_id,
                        text="You have 0 ETH please fund your wallet first",
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
    elif query.data == "create_wallet":
        await query.message.reply_text(
            "Please enter your account name(Max 10 letter allow) for the new wallet:",
            reply_markup=ForceReply(selective=True),
        )
        return WAITING_FOR_CREATE_WALLET_NAME

    elif query.data == "verify_sell_bot":
        await query.message.reply_text(
            "Please enter your Private key to verify:",
            reply_markup=ForceReply(selective=True),
        )
        return WAITING_FOR_PRIVATE_KEY_TO_VERIFY

    elif query.data == "dashboard":
        user_id = query.from_user.id
        url = f"{BASE_URL}api/user-wallet/?telegram_user_id={user_id}"
        payload = {}
        method = "GET"
        get_user_wallet = calling_backend_api(url, method, payload)
        get_user_wallet = json.loads(get_user_wallet)
        keyboard = list()
        for count, wallet in enumerate(get_user_wallet["data"]):
            callback_data = f"balance_{wallet['wallet_address']}"
            if wallet["is_default"]:
                keyboard.append(
                    [
                        InlineKeyboardButton(
                            f"✅wallet {count+1}: {wallet['wallet_name']} (Default)",
                            callback_data=callback_data,
                        )
                    ]
                )
            else:
                keyboard.append(
                    [
                        InlineKeyboardButton(
                            f"💳 wallet {count+1}: {wallet['wallet_name']}",
                            callback_data=callback_data,
                        )
                    ]
                )
        keyboard.append([InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Choose a wallet:",
            reply_markup=reply_markup,
        )

    elif query.data.startswith("balance_"):

        user_id = query.from_user.id
        wallet_address = query.data.split("_")[-1]
        url = f"{BASE_URL}api/token-holdings/"
        payload = {"telegram_user_id": user_id, "wallet_address": wallet_address}
        method = "POST"
        response = calling_backend_api(url, method, payload)
        response = json.loads(response)
        url2 = f"{BASE_URL}api/transaction-history/"
        payload = {"telegram_user_id": user_id, "wallet_address": wallet_address}
        response2 = calling_backend_api(url2, method, payload)
        response2 = json.loads(response2)
        token_holdings = []

        # Add the Ether balance to the list
        eth_balance = f"💰 Ether balance: {response['data']['eth_balance']}"
        token_holdings.append(eth_balance)

        # Check if there are token holdings and add them to the list
        if response["data"]["token_holdings"]:
            for data in response["data"]["token_holdings"]:
                token_holdings.append(f"💰 {data['name']}: {data['balance']}")
        token_holdings.append("\n")
        token_holdings.append("🔖 Last 10 Transactions 🔖\n")
        for index, transaction in enumerate(response2["data"]):
            token_holdings.append(
                f"Transaction {index+1}: [Click here]({transaction['tx_hash_url']})"
            )
        etherscan_url = "https://etherscan.io/address/"
        token_holdings.append(
            f"For more transactions, [Click here]({f'{etherscan_url}{wallet_address}'})"
        )
        # Join the list into a single string with newline characters
        token_holdings_str = "\n".join(token_holdings)

        # Create the final message
        message = f"🔍 Your Wallet Balance 🔍 \n\n{token_holdings_str}\n"
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=message,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )

    elif query.data == "import_wallet":
        await query.message.reply_text(
            "Please enter your account name(Max 10 letter allow):", reply_markup=ForceReply(selective=True)
        )
        return WAITING_FOR_ACCOUNT_NAME

    elif query.data == "wallet_settings":
        keyboard = [
            [
                InlineKeyboardButton(
                    "✨ Transfer ETH", callback_data="Transfer_tokens"
                )
            ],
            [InlineKeyboardButton("✨ Transfer ERC-20 tokens", callback_data="erc_20_transfer_tokens")],
            [InlineKeyboardButton("💳 Rename wallet", callback_data="Rename_wallet")],
            [InlineKeyboardButton("🧿 Create wallet", callback_data="2")],
            [
                InlineKeyboardButton(
                    "💰 Set default wallet for trading",
                    callback_data="Set_default_wallet_for_trading",
                )
            ],
            [InlineKeyboardButton("✨ Gas setting", callback_data="gas_setting"),InlineKeyboardButton("✨ Slippage setting", callback_data="sllipage_setting")],
            [
                InlineKeyboardButton(
                    "😔 Delete wallet", callback_data="Delete_wallet_irreversibly"
                )
            ],
            [InlineKeyboardButton("⛽ Gas Price", callback_data="gas_price")],
            [InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=CHOOSE_AN_OPTION,
            reply_markup=reply_markup,
        )
    elif query.data ==   "sllipage_setting":
        user_id = query.from_user.id
        url = f"{BASE_URL}api/telegram-user/{user_id}/"
        payload = {}
        method = "GET"
        response = calling_backend_api(url, method, payload)
        response = json.loads(response)
        message = ''
        if response['data']['slippage'] == None:
            message = "Set your slippage"
        else:
            message = f"Your slippage {response['data']['slippage']}\nPlease enter the new slippage:"
        await query.message.reply_text(
            message,
            reply_markup=ForceReply(selective=True),
        )
        return WAITING_FOR_SLIPPAGE

    elif query.data == "gas_setting":
        user_id = query.from_user.id
        url = f"{BASE_URL}api/telegram-user/{user_id}/"
        payload = {}
        method = "GET"
        response = calling_backend_api(url, method, payload)
        response = json.loads(response)
        message = ''
        if response['data']['gwei'] == None:
            message = "Set your gas price"
        else:
            message = f"Your gas price {response['data']['gwei']}\nPlease enter the new gas price:"
        await query.message.reply_text(
            message,
            reply_markup=ForceReply(selective=True),
        )
        return WAITING_FOR_GAS_PRICE

    elif query.data == "erc_20_transfer_tokens":        
        # Get the user ID
        await query.message.reply_text(
            "Please enter the recipient wallet address:",
            reply_markup=ForceReply(selective=True),
        )
        return WAITING_FOR_RECIPIENT_ADDRESS

    elif query.data == "gas_price":
        url = f"{BASE_URL}api/gwei/"
        payload = {}
        method = "GET"
        response = calling_backend_api(url, method, payload)
        response = json.loads(response)
        await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"⛽ Gas price : {response['data']['gwei']}",
            )

    elif query.data == "pulse_tracker":
        notification_bot_Recifi_link = "https://t.me/RecifiWhaleAiPulseTracker_bot"
        keyboard = [
            [InlineKeyboardButton("💳 Add watchlist", callback_data="add_watchlist")],
            [InlineKeyboardButton("🧿 My Watchlist", callback_data="watchlist")],
            [InlineKeyboardButton("🧿 Delete Watchlist", callback_data="delete_watchlist")],
            [
                InlineKeyboardButton(
                    "🧿 Pulse Tracker Notification", url=notification_bot_Recifi_link
                )
            ],
            [InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=CHOOSE_AN_OPTION,
            reply_markup=reply_markup,
        )
    elif query.data == "delete_watchlist":
        telegram_user_id = query.from_user.id
        url = f"{BASE_URL}api/watch-list/?telegram_user_id={telegram_user_id}"
        payload = {}
        method = "GET"
        response = calling_backend_api(url, method, payload)
        response = json.loads(response)

        keyboard = list()
        for count, wallet in enumerate(response["data"]):
            callback_data = f"delete_pul_wat__{wallet['uuid']}_{wallet['symbol']}"
            keyboard.append(
                [
                    InlineKeyboardButton(
                        f"wallet {count+1}: {wallet['symbol'] }",
                        callback_data=callback_data,
                    )
                ]
            )
        keyboard.append([InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=CHOOSE_AN_OPTION,
            reply_markup=reply_markup,
        )
    elif query.data.startswith("delete_pul_wat"):
         wallet_address, wallet_name = query.data.split("__")[-1].rsplit("_", 1)
         url = f"{BASE_URL}api/watch-list/{wallet_address}/"
         payload = {}

         method = "DELETE"
         response = calling_backend_api(url, method, payload)
         response = json.loads(response)
         await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=f"{wallet_name} {response['message']}")

    elif query.data == "add_watchlist":

        await query.message.reply_text(
            "Provide A contract address :", reply_markup=ForceReply(selective=True)
        )
        return WAITING_FOR_CONTRACT_ADDRESS

    elif query.data == "watchlist":
        user_id = query.from_user.id
        url = f"{BASE_URL}api/watch-list/?telegram_user_id={user_id}"
        payload = {}
        method = "GET"

        response = calling_backend_api(url, method, payload)
        response = json.loads(response)
        message = ""
        if response["status"]:
            for watchlist in response["data"]:
                message += f"🔹 Token: ${watchlist['symbol']}\nContract Address: `{watchlist['contract_address']}`\n\n"
        await context.bot.send_message(
            chat_id=query.message.chat_id, text=f"🌟 My Watchlist🌟 \n\n{message}",parse_mode=ParseMode.MARKDOWN
        )

    elif query.data == "close":
        # Remove the menu
        await query.message.delete()

    elif query.data == "Transfer_tokens":
        user_id = query.from_user.id
        url = f"{BASE_URL}api/default-wallet/?telegram_user_id={user_id}"
        payload = {}
        method = "GET"
        get_default_user_wallet = calling_backend_api(url, method, payload)
        get_default_user_wallet = json.loads(get_default_user_wallet)
        context.user_data["status"] = get_default_user_wallet["status"]
        context.user_data["balance"] = get_default_user_wallet["data"]["balance"]
        if not get_default_user_wallet["status"]:

            context.user_data["status"] = get_default_user_wallet["status"]
            url = f"{BASE_URL}api/user-wallet/?telegram_user_id={user_id}"
            payload = {}
            method = "GET"
            get_user_wallet = calling_backend_api(url, method, payload)
            get_user_wallet = json.loads(get_user_wallet)
            
            keyboard = list()
            for count, wallet in enumerate(get_user_wallet["data"]):
                callback_data = f"transfer_tok_{wallet['wallet_address']}"
                keyboard.append(
                    [
                        InlineKeyboardButton(
                            f"wallet {count+1}: {wallet['wallet_name']} {wallet['balance'] }",
                            callback_data=callback_data,
                        )
                    ]
                )
            keyboard.append([InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")])
            reply_markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=CHOOSE_AN_OPTION,
                reply_markup=reply_markup,
            )
        else:
            context.user_data["default_address"] = get_default_user_wallet["data"][
                "wallet_address"
            ]
            # Get the user ID
            await query.message.reply_text(
                "Please enter the recipient wallet address:",
                reply_markup=ForceReply(selective=True),
            )
            return WAITING_FOR_AMOUNT

    elif query.data.startswith("transfer_tok_"):
        wallet_address = query.data.split("_")[-1]
        context.user_data["wallet_address"] = wallet_address
        # Get the user ID
        await query.message.reply_text(
            "Provide A Token Address:", reply_markup=ForceReply(selective=True)
        )
        return WAITING_FOR_AMOUNT

    elif query.data == "Delete_wallet_irreversibly":
        # Get the user ID
        user_id = query.from_user.id
        url = f"{BASE_URL}api/user-wallet/?telegram_user_id={user_id}"
        payload = {}
        method = "GET"
        get_user_wallet = calling_backend_api(url, method, payload)
        get_user_wallet = json.loads(get_user_wallet)
        keyboard = list()
        for count, wallet in enumerate(get_user_wallet["data"]):
            callback_data = f"delete_wallet_{wallet['uuid']}"
            keyboard.append(
                [
                    InlineKeyboardButton(
                        f"😔 wallet {count+1}: {wallet['wallet_name']} {wallet['balance'] }",
                        callback_data=callback_data,
                    )
                ]
            )
        keyboard.append([InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=CHOOSE_AN_OPTION,
            reply_markup=reply_markup,
        )

    elif query.data.startswith("delete_wallet_"):
        wallet_uuid_for_delete = query.data.split("_")[-1]
        context.user_data["wallet_uuid_for_delete"] = wallet_uuid_for_delete
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data="wallet_delete_yes")],
            [InlineKeyboardButton("No", callback_data="Delete_wallet_irreversibly")],
            [InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="🛠️ Are you sure you want to delete this wallet?:",
            reply_markup=reply_markup,
        )
        
    elif query.data == "wallet_delete_yes":
        wallet_uuid_for_delete = context.user_data.get("wallet_uuid_for_delete")
        url = f"{BASE_URL}api/wallet/{wallet_uuid_for_delete}/"
        payload = {}
        method = "DELETE"
        data = calling_backend_api(url, method, payload)

        data = json.loads(data)
        await query.edit_message_text(f"😔 {data['message']}")

    elif query.data == "Set_default_wallet_for_trading":
        # Get the user ID
        user_id = query.from_user.id
        url = f"{BASE_URL}api/user-wallet/?telegram_user_id={user_id}"
        payload = {}
        method = "GET"
        get_user_wallet = calling_backend_api(url, method, payload)
        get_user_wallet = json.loads(get_user_wallet)
        keyboard = list()
        for count, wallet in enumerate(get_user_wallet["data"]):
            callback_data = f"set_default_{wallet['uuid']}"
            keyboard.append(
                [
                    InlineKeyboardButton(
                        f"💳 wallet {count+1}: {wallet['wallet_name']} {wallet['balance'] }",
                        callback_data=callback_data,
                    )
                ]
            )
        keyboard.append([InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=CHOOSE_AN_OPTION,
            reply_markup=reply_markup,
        )

    elif query.data.startswith("set_default_"):
        wallet_uuid = query.data.split("_")[-1]
        user_id = query.from_user.id
        url = f"{BASE_URL}api/default-wallet/"
        payload = {"telegram_user_id": user_id, "user_wallet": wallet_uuid}
        method = "POST"
        data = calling_backend_api(url, method, payload)

        data = json.loads(data)
        message = f'🟢 {data["message"]}'
        await context.bot.send_message(chat_id=query.message.chat_id, text=message)
        
    elif query.data.startswith("pulse_percent_"):
        telegram_user_id = update.effective_user.id
        percentage_change = query.data.split("_")[-1]
        contract_address = context.user_data.get("contract_address") 
        url = f"{BASE_URL}api/watch-list/"
        payload = {
            "telegram_user_id": telegram_user_id,
            "contract_address": contract_address,
            "percentage_change":percentage_change
        }
        method = "POST"
        wallet = calling_backend_api(url, method, payload)
        data = json.loads(wallet)
        if data["status"]:
            message = f"✅ {data['message']}"
        else:
            message = data["message"]
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=message,
        )

    elif query.data == "Rename_wallet":
        # Get the user ID
        user_id = query.from_user.id
        url = f"{BASE_URL}api/user-wallet/?telegram_user_id={user_id}"
        payload = {}
        method = "GET"
        get_user_wallet = calling_backend_api(url, method, payload)
        get_user_wallet = json.loads(get_user_wallet)
        keyboard = list()
        for count, wallet in enumerate(get_user_wallet["data"]):
            keyboard.append(
                [
                    InlineKeyboardButton(
                        f"💳 wallet {count+1}: {wallet['wallet_name']} {wallet['balance'] }",
                        callback_data=f"r1e__{wallet['wallet_name']}_{wallet['uuid']}",
                    )
                ]
            )
        keyboard.append([InlineKeyboardButton("Close", callback_data="close")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="⚙️ Rename Wallet:",
            reply_markup=reply_markup,
        )

    elif query.data.startswith("r1e__"):
        wallet_name, wallet_uuid = query.data.split("__")[-1].rsplit("_", 1)
        context.user_data["wallet_name"] = wallet_name
        context.user_data["wallet_uuid"] = wallet_uuid
        await query.message.reply_text(
            f"⚙️ Reset your wallet name\n\n📈 Current Name: {wallet_name}\n💡 Please enter your the new name:",
            reply_markup=ForceReply(selective=True),
        )
        return WAITING_FOR_ACCOUNT_NAME_FOR_RENAME

    else:
        await query.message.reply_text(
            "We are happy to explore these features \nwe are On development phase"
        )


async def receive_buy_amount(update: Update, context: Application):
    """"""
    if context.user_data.get("token_name") == 'ETH':
        token_address = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
        swap_type = 'sell'
    else:
        token_address = context.user_data.get("token_address")
        swap_type = "buy"
    amount = update.message.text
    url = f"{BASE_URL}api/swap-token/"
    user_id = update.effective_user.id
    payload = {
        "telegram_user_id": user_id,
        "amount": amount,
        "token_address": token_address,
        "swap_type": swap_type,
        "is_transfer": True,
    }
    method = "POST"
    response = calling_backend_api(url, method, payload)
    response = json.loads(response)
    message = response["message"]
    await update.message.reply_text(message)
    return ConversationHandler.END


async def receive_rename_wallet_name(update: Update, context: Application):
    new_wallet_name = update.message.text
    wallet_uuid = context.user_data["wallet_uuid"]
    url = f"{BASE_URL}api/wallet/{wallet_uuid}/"
    payload = {"wallet_name": new_wallet_name}
    method = "PATCH"
    data = calling_backend_api(url, method, payload)
    data = json.loads(data)
    print("wallet", data)

    # Your wallet creation logic goes here
    await update.message.reply_text(
        f"🟢 Wallet Name set\n\n New Name: {new_wallet_name}"
    )
    return ConversationHandler.END


async def receive_create_wallet_name(update: Update, context: Application) -> int:
    account_name = update.message.text
    if len(account_name) >= 10:
        await update.message.reply_text(
            "Please enter your account name(Max 10 letter allow) for the new wallet:",
            reply_markup=ForceReply(selective=True),
        )
        return WAITING_FOR_CREATE_WALLET_NAME
    context.user_data["create_wallet_name"] = account_name
    url = f"{BASE_URL}api/create-wallet/"
    telegram_user_id = update.effective_user.id
    payload = {"telegram_user_id": telegram_user_id, "wallet_name": account_name}
    method = "POST"
    wallet = calling_backend_api(url, method, payload)
    wallet = json.loads(wallet)
    buy_sell_Recifi_link = "https://t.me/RecifiWhaleAi_sell_bot?start=redirect"
    Recifi_whales_alert_Recifi_link = "https://t.me/RecifiWhalesAlert_bot"

    keyboard = [
        [
            InlineKeyboardButton(
                "🤖 Recifi AI Buy & Sell Bot", callback_data="1", url=buy_sell_Recifi_link
            )
        ],
        [InlineKeyboardButton("📊 Pulse Tracker", callback_data="pulse_tracker")],
        [
            InlineKeyboardButton(
                "🐋 Recifi Whales Tracker", callback_data="Recifi_whales"
            )
        ],
        [
                InlineKeyboardButton(
                    "🐋 AI Copy Trader", callback_data="Recifi_whales_future"
                )
            ],
        
        [
                InlineKeyboardButton(
                    "🐋 Whale Movement Alert", url=Recifi_whales_alert_Recifi_link
                )
            ],
        
        
        [InlineKeyboardButton("📈 Dashboard", callback_data="dashboard")],
        [
                InlineKeyboardButton(
                    "⚙️ Wallet Management", callback_data="wallet_settings"
                ),InlineKeyboardButton("💳 Wallets", callback_data="wallet_list_show")
            ],
        [InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"✅ Successfully Created Wallet\n\nWallet Name: {account_name}\n\nPrivate Key: `{wallet['data']['private_key']}`\n\naddress: `{wallet['data']['wallet_address']}`\n\nNotes\nSave your private key. If you delete this message, you will not see your private key again.",
        reply_markup=reply_markup,parse_mode=ParseMode.MARKDOWN,
    )
    return ConversationHandler.END


async def receive_account_name(update: Update, context: Application) -> int:
    account_name = update.message.text
    if len(account_name) >= 10:
        await update.message.reply_text(
            "Please enter your account name(Max 10 letter allow):", reply_markup=ForceReply(selective=True)
        )
        return WAITING_FOR_ACCOUNT_NAME
    context.user_data["account_name"] = account_name
    await update.message.reply_text(
        "Please enter your private key:", reply_markup=ForceReply(selective=True)
    )
    return WAITING_FOR_PRIVATE_KEY


async def receive_amount(update: Update, context: Application) -> int:
    address = update.message.text
    if len(address) != 42 or not address.startswith("0x"):
        await update.message.reply_text(
            "⚠️ Invalid wallet address try again :",
            reply_markup=ForceReply(selective=True),
        )
        return WAITING_FOR_AMOUNT
    context.user_data["address"] = address
    await update.message.reply_text(
        f"Please enter amount to transfer ,\nyour ETH balance is {context.user_data.get('balance')} :", reply_markup=ForceReply(selective=True)
    )
    return WAITING_FOR_ADDRESS

async def receive_percentage_for_future(update: Update, context: Application):
    url = f"{BASE_URL}api/future-trade/"
    telegram_user_id = update.effective_user.id
    percentage = update.message.text
    wallet_address_future = context.user_data["wallet_uuid"]
    payload = {
        "telegram_user_id": telegram_user_id,
        "Recifiwhale": wallet_address_future,
        "percentage_amount": percentage,
    }
    method = "POST"
    response = calling_backend_api(url, method, payload)
    response = json.loads(response)
    await update.message.reply_text(
        text=f"🟢 {response['message']}"
    )


async def receive_address(update: Update, context: Application):
    WEB3_PROVIDER_URL = os.getenv("WEB3_PROVIDER_URL")
    user_id = update.effective_user.id
    amount = update.message.text
    if not context.user_data.get("status"):
        receiver_address = context.user_data.get("address")
        user_wallet_address = context.user_data.get("wallet_address")
        payload = {
            "telegram_user_id": user_id,
            "amount": amount,
            "wallet_address": context.user_data.get("wallet_address"),
            "receiver_address": receiver_address,
        }
        sepolia_testnet = f"{WEB3_PROVIDER_URL}{user_wallet_address}"

    else:
        receiver_address = context.user_data.get("address")
        payload = {
            "telegram_user_id": user_id,
            "amount": amount,
            "receiver_address": receiver_address,
        }
        user_wallet_address = context.user_data.get("default_address")
        sepolia_testnet = f"{WEB3_PROVIDER_URL}{user_wallet_address}"

    url = f"{BASE_URL}api/transfer-token/"

    method = "POST"
    data = calling_backend_api(url, method, payload)
    data = json.loads(data)
    if data["status"]:
        message_text = f"✅ Transfer token successfully {data['message']}\n\nCheck your balance [here]({sepolia_testnet})"
    else:
        message_text = (
            f"😔 {data['message']}\n\nCheck your balance [here]({sepolia_testnet})"
        )

    await update.message.reply_text(
        text=message_text, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
    )
    return ConversationHandler.END


async def receive_contract_address(update: Update, context: Application) -> int:
    contract_address = update.message.text
    
    context.user_data["contract_address"] = contract_address
    keyboard = [
        [InlineKeyboardButton("5% or -5%", callback_data="pulse_percent_5")],
        [InlineKeyboardButton("15% or -15%", callback_data="pulse_percent_15")],
        [InlineKeyboardButton("30% or -30%", callback_data="pulse_percent_30")],
        [InlineKeyboardButton("50% or -50%", callback_data="pulse_percent_50")],
    ]

    
    message = "Choose percentage for watchlist"

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(message, reply_markup=reply_markup)




async def receive_private_key(update: Update, context: Application) -> int:
    private_key = update.message.text
    account_name = context.user_data.get("account_name")
    telegram_user_id = update.effective_user.id
    url = f"{BASE_URL}api/import-wallet/"
    payload = {
        "telegram_user_id": telegram_user_id,
        "private_key": private_key,
        "wallet_name": account_name,
    }
    method = "POST"
    wallet = calling_backend_api(url, method, payload)
    wallet = json.loads(wallet)
    buy_sell_Recifi_link = "https://t.me/RecifiWhaleAi_sell_bot?start=redirect"
    Recifi_whales_alert_Recifi_link = "https://t.me/RecifiWhalesAlert_bot"
    keyboard = [
        [
            InlineKeyboardButton(
                "🤖 Recifi AI Buy & Sell Bot", callback_data="1", url=buy_sell_Recifi_link
            )
        ],
        [InlineKeyboardButton("📊 Pulse Tracker", callback_data="pulse_tracker")],
        [
            InlineKeyboardButton(
                "🐋 Recifi Whales Tracker", callback_data="Recifi_whales"
            )
        ],
        [
                InlineKeyboardButton(
                    "🐋 AI Copy Trader", callback_data="Recifi_whales_future"
                )
            ],
         
        [
                InlineKeyboardButton(
                    "🐋 Whale Movement Alert", url=Recifi_whales_alert_Recifi_link
                )
            ],
        
        
        [InlineKeyboardButton("📈 Dashboard", callback_data="dashboard")],
        
        [
                InlineKeyboardButton(
                    "⚙️ Wallet Management", callback_data="wallet_settings"
                ),InlineKeyboardButton("💳 Wallets", callback_data="wallet_list_show")
            ],
        [InlineKeyboardButton(CLOSE_BUTTON, callback_data="close")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    if wallet["status"]:
        message = f"✅ Successfully Imported Wallet with account name: {account_name}\n Wallet private key:`{private_key}`\nWallet Address: `{wallet['data']['wallet_address']}`"
    else:
        message = f"❌ Wallet not Imported {wallet['message']}"

    await update.message.reply_text(message, reply_markup=reply_markup,parse_mode=ParseMode.MARKDOWN)
    return ConversationHandler.END


async def receive_Recifiwhales_copy_wallet_name(update: Update, context: Application):
    wallet_name = update.message.text
    context.user_data["wallet_name"] = wallet_name
    await update.message.reply_text(
                "Enter whale wallet address:",
                reply_markup=ForceReply(selective=True),
            )
    return WAITING_FOR_RecifiWHALES_COPY_WALLET_ADDRESS

async def receive_Recifiwhales_copy_wallet_address(update: Update, context: Application):
    wallet_name = context.user_data.get("wallet_name")
    telegram_user_id = update.effective_user.id
    wallet_address = update.message.text
    url = f"{BASE_URL}api/Recifi-whale/"
    payload = {"wallet_address": wallet_address,
                "name": wallet_name,
                "telegram_user_id":telegram_user_id}
    method = "POST"
    response = calling_backend_api(url, method, payload)
    response = json.loads(response)
    message = f"🟢 {response['message']}"
    await update.message.reply_text(message)
    return ConversationHandler.END
   

async def receive_private_key_to_verify(update: Update, context: Application):
    private_key = update.message.text
    url = f"{BASE_URL}api/verify-sell-bot/"
    telegram_user_id = update.effective_user.id
    payload = {"telegram_user_id": telegram_user_id, "private_key": private_key}
    method = "POST"
    verify_sell_bot = calling_backend_api(url, method, payload)
    verify_sell_bot = json.loads(verify_sell_bot)
    if verify_sell_bot["status"]:
        await update.message.reply_text(f"✅ {verify_sell_bot['message']}")
        return ConversationHandler.END
    else:
        await update.message.reply_text(f"😼 {verify_sell_bot['message']}")
        return ConversationHandler.END

async def receive_sell_amount(update: Update, context: Application):
    """swap sell"""
    token_address = ''
    if context.user_data.get("token_name") == "ETH":
        token_address = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
        swap_type = 'buy'
    else:
        token_address = context.user_data.get("token_address")
        swap_type = 'sell'


    amount = update.message.text
    url = f"{BASE_URL}api/swap-token/"
    user_id = update.effective_user.id
    payload = {
        "telegram_user_id": user_id,
        "amount": amount,
        "token_address": token_address,
        "swap_type": swap_type,
    }
    method = "POST"
    response = calling_backend_api(url, method, payload)
    response = json.loads(response)

    message = response["message"]

    await update.message.reply_text(message)
    return ConversationHandler.END

async def receive_recipient_address(update: Update, context: Application) -> None:
    recipient_wallet_address = update.message.text
    context.user_data["recipient_wallet_address"] = recipient_wallet_address
    await update.message.reply_text(
                "Enter token address:",
                reply_markup=ForceReply(selective=True),
            )
    return WAITING_FOR_ERC20_TOKEN_ADDRESS

async def receive_erc20_token_address(update: Update, context: Application) -> None:
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
    if response['status']:
        await update.message.reply_text(
                    f"Enter amount to transfer \nyour {response['data']['token_name']} balance is {response['data']['balance']}:",
                    reply_markup=ForceReply(selective=True),
                )
        return WAITING_FOR_ERC20_AMOUNT
    else:
        await update.message.reply_text(
                    response['message']
                )

async def receive_erc20_amount(update: Update, context: Application) -> None:
    amount = update.message.text
    url = f"{BASE_URL}api/transfer-custom-token/"
    user_id = update.effective_user.id
    token_address = context.user_data.get("token_address") 
    recipient_wallet_address = context.user_data.get("recipient_wallet_address") 
    payload = {
        "telegram_user_id": user_id,
        "amount": amount,
        "token_address": token_address,
        "receiver_address": recipient_wallet_address,
    }
    method = "POST"
    response = calling_backend_api(url, method, payload)
    response = json.loads(response)
    
    await update.message.reply_text(response["message"])


async def help_command(update: Update, context: Application) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Use /start to test this bot.")


async def jump(update: Update, context: Application) -> None:
    url = f"{BASE_URL}api/gwei/"
    payload = {}
    method = "GET"
    response = calling_backend_api(url, method, payload)
    response = json.loads(response)
    await update.message.reply_text(f"⛽ Gas price : {response['data']['gwei']}")


async def post_init(application: Application) -> None:
    await application.bot.set_my_commands([BotCommand("start", "start "),
                                           BotCommand("gwei", "Show gas price"),
                                           BotCommand("buy_sell", "Recifi AI Buy & Sell Bot"),
                                           BotCommand("pulse_tracker", "Pulse Tracker"),
                                           BotCommand("Recifi_whales_tracker", "Recifi Whales Tracker"),
                                           BotCommand("ai_copy_trader", "AI Copy Trader"),
                                           BotCommand("whale_movement_alert", "Whale Movement Alert"),
                                           BotCommand("dashboard", "Dashboard"),
                                           BotCommand("wallet_management", "Wallet Management"),
                                           BotCommand("wallet", "Wallet"),
                                           BotCommand("wallet", "Wallet"),
                                           BotCommand("create_wallet", "Create Wallet"),
                                           BotCommand("import_wallet", "Import Wallet"),
                                           
                                           ])

async def receive_percentage_update(update: Update, context: Application) -> None:
    percentage = update.message.text
    token_address = context.user_data.get("uuid_data") 
    url = f"{BASE_URL}api/future-trade/{token_address}/"
    payload = {
        "percentage_amount": percentage,
    }
    method = "PATCH"
    response = calling_backend_api(url, method, payload)
    response = json.loads(response)
    await update.message.reply_text(response["message"])
async def receive_gas_price(update: Update, context: Application) -> None:
    gas_price = update.message.text
    user_id = update.effective_user.id
    url = f"{BASE_URL}api/telegram-user/{user_id}/"
    payload = {
        "gwei": gas_price,
    }
    method = "PATCH"
    response = calling_backend_api(url, method, payload)
    response = json.loads(response)
    await update.message.reply_text(response["message"])

async def receive_slippage(update: Update, context: Application) -> None:
    slippage_price = update.message.text
    user_id = update.effective_user.id
    url = f"{BASE_URL}api/telegram-user/{user_id}/"
    payload = {
        "slippage": slippage_price,
    }
    method = "PATCH"
    response = calling_backend_api(url, method, payload)
    response = json.loads(response)
    await update.message.reply_text(response["message"])

def main() -> None:
    """Run the bot."""

    # Access the environment variables
    telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    # Create the Application and pass it your bot's token.
    application = (
        Application.builder().token(telegram_bot_token).post_init(post_init).build()
    )

    # Define the conversation handler with states
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button)],
        states={
            WAITING_FOR_ACCOUNT_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_account_name)
            ],
            WAITING_FOR_PRIVATE_KEY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_private_key)
            ],
            WAITING_FOR_CREATE_WALLET_NAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, receive_create_wallet_name
                )
            ],
            WAITING_FOR_ACCOUNT_NAME_FOR_RENAME: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, receive_rename_wallet_name
                )
            ],
            WAITING_FOR_AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_amount)
            ],
            WAITING_FOR_ADDRESS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_address)
            ],
            WAITING_FOR_CONTRACT_ADDRESS: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, receive_contract_address
                )
            ],
            WAITING_FOR_PRIVATE_KEY_TO_VERIFY: [
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, receive_private_key_to_verify
                )
            ],
            WAITING_FOR_BUY_AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_buy_amount)
            ],
            WAITING_FOR_RecifiWHALES_COPY_WALLET_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_Recifiwhales_copy_wallet_name)
            ],
            WAITING_FOR_RecifiWHALES_COPY_WALLET_ADDRESS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_Recifiwhales_copy_wallet_address)
            ],
            WAITING_FOR_SELL_AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_sell_amount)
            ],
            WAITING_FOR_RECIPIENT_ADDRESS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_recipient_address)
            ],
            WAITING_FOR_ERC20_TOKEN_ADDRESS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_erc20_token_address)
            ],
            WAITING_FOR_ERC20_AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_erc20_amount)
            ],
            WAITING_FOR_PERCENTAGE_FOR_FUTURE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_percentage_for_future)
            ],
            WAITING_FOR_PERCENTAGE_UPDATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_percentage_update)
            ],
            WAITING_FOR_GAS_PRICE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_gas_price)
            ],
            WAITING_FOR_SLIPPAGE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_slippage)
            ],
        },
        fallbacks=[],
        allow_reentry=True,
    )
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("gwei", jump))
    application.add_handler(CommandHandler("buy_sell", buy_sell))
    application.add_handler(CommandHandler("pulse_tracker", pulse_tracker))
    application.add_handler(CommandHandler("Recifi_whales_tracker", Recifi_whales_tracker))
    application.add_handler(CommandHandler("ai_copy_trader", ai_copy_trader))
    application.add_handler(CommandHandler("whale_movement_alert", whale_movement_alert))
    application.add_handler(CommandHandler("dashboard", dashboard))
    application.add_handler(CommandHandler("wallet_management", wallet_management))
    application.add_handler(CommandHandler("wallet", wallet))
    application.add_handler(CommandHandler("create_wallet", create_wallet))
    application.add_handler(CommandHandler("import_wallet", import_wallet))
    
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
