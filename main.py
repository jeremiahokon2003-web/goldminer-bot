# main.py
import telebot
from telebot import types

# === BOT CONFIG ===
BOT_TOKEN =  "7993651877:AAG54NYdIQi_8B19sR-G_THDpa-CyemRL98"
ADMIN_ID = 8275205737
bot = telebot.TeleBot("7993651877:AAG54NYdIQi_8B19sR-G_THDpa-CyemRL98")

# === USER DATA STORAGE ===
users = {}
pending_deposits = {}
pending_withdrawals = {}

# === START COMMAND ===
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    if user_id not in users:
        users[user_id] = {
            "balance": 0,
            "referrals": 0,
            "ref_earnings": 0,
            "package": None,
            "daily_signin": False,
            "earnings": 0
        }
    markup = main_menu()
    bot.send_message(
        user_id,
        f"👋 Welcome to *Gold Miner Investments Bot*\n\n"
        "Invest smartly and earn daily profits.\n"
        "Select an option below 👇",
        parse_mode="Markdown",
        reply_markup=markup
    )

# === MAIN MENU ===
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💼 Dashboard", "💰 Buy Package")
    markup.add("🏦 Recharge", "💸 Withdraw")
    markup.add("👥 Referral", "🧾 History")
    markup.add("🎁 Daily Sign In", "💰 Claim Earnings")
    markup.add("☎️ Customer Service 1", "☎️ Customer Service 2")
    return markup

# === DASHBOARD ===
@bot.message_handler(func=lambda m: m.text == "💼 Dashboard")
def dashboard(message):
    user = users.get(message.chat.id, {})
    bot.send_message(
        message.chat.id,
        f"🏦 *Your Dashboard*\n\n"
        f"💰 Balance: ₦{user.get('balance', 0)}\n"
        f"💸 Earnings: ₦{user.get('earnings', 0)}\n"
        f"👥 Referrals: {user.get('referrals', 0)}\n"
        f"🎁 Package: {user.get('package', 'None')}",
        parse_mode="Markdown"
    )

# === BUY PACKAGE ===
@bot.message_handler(func=lambda m: m.text == "💰 Buy Package")
def buy_package(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("₦500 Package", callback_data="pkg_500"))
    markup.add(types.InlineKeyboardButton("₦2000 Package", callback_data="pkg_2000"))
    markup.add(types.InlineKeyboardButton("₦5000 Package", callback_data="pkg_5000"))
    bot.send_message(message.chat.id, "Choose a package to buy 👇", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("pkg_"))
def package_selected(call):
    pkg = call.data.split("_")[1]
    pkg_amount = int(pkg)
    users[call.message.chat.id]["package"] = pkg_amount
    bot.send_message(call.message.chat.id, f"✅ You selected ₦{pkg_amount} package.\nMake payment to continue.\n\n"
                                           "🏦 *Bank Details*\n"
                                           "Bank: Tenn Bank\n"
                                           "Account Name: Daniel Chewkube Uche\n"
                                           "Account Number: 9110163205\n\n"
                                           "Send screenshot to admin for approval.",
                                           parse_mode="Markdown")

# === RECHARGE ===
@bot.message_handler(func=lambda m: m.text == "🏦 Recharge")
def recharge(message):
    bot.send_message(message.chat.id,
                     "🏦 *Recharge Instructions*\n\n"
                     "Send payment to the account below:\n"
                     "Bank: Tenn Bank\n"
                     "Account Name: Daniel Chewkube Uche\n"
                     "Account Number: 9110163205\n\n"
                     "After payment, send a message to admin for approval.",
                     parse_mode="Markdown")

# === WITHDRAW ===
@bot.message_handler(func=lambda m: m.text == "💸 Withdraw")
def withdraw(message):
    user = users.get(message.chat.id, {})
    if user.get("package") is None:
        bot.send_message(message.chat.id, "❌ You must buy a package before you can withdraw.")
        return
    bot.send_message(message.chat.id, "Enter the amount you want to withdraw:")
    bot.register_next_step_handler(message, process_withdraw)

def process_withdraw(message):
    amount = int(message.text)
    user_id = message.chat.id
    user = users[user_id]
    if amount > user["balance"]:
        bot.send_message(user_id, "❌ Insufficient balance.")
    else:
        fee = int(amount * 0.15)
        final = amount - fee
        pending_withdrawals[user_id] = {"amount": final}
        bot.send_message(user_id, f"✅ Withdrawal request sent.\nYou will receive ₦{final} after 15% fee.")
        bot.send_message(ADMIN_ID, f"📤 Withdrawal request:\nUser: {user_id}\nAmount: ₦{final}")

# === CLAIM EARNINGS ===
@bot.message_handler(func=lambda m: m.text == "💰 Claim Earnings")
def claim_earnings(message):
    user = users.get(message.chat.id, {})
    pkg = user.get("package")
    if not pkg:
        bot.send_message(message.chat.id, "❌ You have no active package.")
        return

    if pkg == 500:
        profit = 1000
    elif pkg == 2000:
        profit = 700
    elif pkg == 5000:
        profit = 950
    else:
        profit = 0

    user["earnings"] += profit
    user["balance"] += profit
    bot.send_message(message.chat.id, f"✅ You claimed ₦{profit} earnings for today!")

# === DAILY SIGN IN ===
@bot.message_handler(func=lambda m: m.text == "🎁 Daily Sign In")
def daily_signin(message):
    user = users.get(message.chat.id, {})
    if user.get("daily_signin"):
        bot.send_message(message.chat.id, "❌ You have already signed in today.")
    else:
        user["balance"] += 10
        user["daily_signin"] = True
        bot.send_message(message.chat.id, "✅ You earned ₦10 for daily sign-in!")

# === CUSTOMER SERVICE ===
@bot.message_handler(func=lambda m: m.text == "☎️ Customer Service 1")
def cust1(message):
    bot.send_message(message.chat.id, "📞 Opening chat with Customer Service 1...")
    bot.send_message(message.chat.id, "👉 Click here: t.me/Goldminer003")

@bot.message_handler(func=lambda m: m.text == "☎️ Customer Service 2")
def cust2(message):
    bot.send_message(message.chat.id, "📞 Opening chat with Customer Service 2...")
    bot.send_message(message.chat.id, "👉 Click here: t.me/Goldminer004")

# === ADMIN PANEL ===
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.chat.id != 8275205737:
    bot.send_message(message.chat.id, "You are not authorized")
        bot.send_message(message.chat.id, "Access denied ❌")
        return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💰 Approve Deposit", "❌ Reject Deposit")
    markup.add("💸 Approve Withdrawal", "🚫 Reject Withdrawal")
    markup.add("➕ Add Balance", "➖ Deduct Balance")
    markup.add("👤 View User Info", "🧾 Transaction History")
    bot.send_message(message.chat.id, "⚙️ *Admin Panel*", parse_mode="Markdown", reply_markup=markup)

print("🤖 Gold Miner Bot running...")
bot.polling(non_stop=True)
