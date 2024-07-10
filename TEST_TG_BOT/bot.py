# THIS IS ALL CREATED BY AI BECUSE IM A LAZY BITCHASS HAHAHAHAHAHAHHAH :3
import os
import logging
import json
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
my_secret = os.environ['TGBOTAPI']
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Define conversation states
TITLE, CONTENT = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks for the title."""
    await update.message.reply_text(
        "Hi! I'm a bot that collects a title and content for your blog. "
        "Let's begin! Please send me the title of your blog post."
    )
    return TITLE

async def title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the title and asks for the content."""
    user = update.message.from_user
    context.user_data['title'] = update.message.text
    logger.info("Title from %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "Great! Now, please send me the content of your blog post."
    )
    return CONTENT

async def content(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the content, saves data to a file, and ends the conversation."""
    user = update.message.from_user
    context.user_data['content'] = update.message.text
    logger.info("Content from %s: %s", user.first_name, update.message.text)

    # Prepare data for saving
    data = {
        "poster": user.first_name,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "title": context.user_data['title'],
        "content": context.user_data['content']
    }

    # Save data to a JSON file
    with open('blog_posts.json', 'a') as f:
        json.dump(data, f)
        f.write('\n')  # Add a newline for easier reading and parsing

    await update.message.reply_text(
        f"Thank you! Your blog post has been saved:\n"
        f"Title: {context.user_data['title']}\n"
        f"Content: {context.user_data['content']}\n"
        f"You can start a new blog post by sending /start."
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day."
    )
    return ConversationHandler.END

def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(my_secret).build()

    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, title)],
            CONTENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, content)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()