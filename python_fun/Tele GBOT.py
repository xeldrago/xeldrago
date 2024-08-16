import openpyxl
from telegram import Bot, Update, InputFile
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, Filters, PollHandler

# Replace with your own Telegram Bot API token
BOT_TOKEN = 'YOUR_BOT_TOKEN'

# Initialize the bot
bot = Bot(token=BOT_TOKEN)

# Function to handle the /start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! I can export poll data to Excel. Just forward a poll to me!")

# Function to handle incoming polls
def handle_poll(update: Update, context: CallbackContext):
    poll = update.poll

    # Create or open an Excel file
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Add headers
    sheet.append(["Question", "Options", "Votes"])

    # Extract poll data and add it to the Excel sheet
    question = poll.question
    options = ", ".join(option.text for option in poll.options)
    votes = ", ".join(str(option.voter_count) for option in poll.options)

    sheet.append([question, options, votes])

    # Save the Excel file
    file_name = f"{question.replace(' ', '_')}.xlsx"
    workbook.save(file_name)

    # Send the Excel file to the user
    context.bot.send_document(chat_id=update.effective_chat.id, document=InputFile(file_name))

# Create an Updater and attach handlerscd
updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(PollHandler(handle_poll))

# Start the bot
updater.start_polling()
updater.idle()
