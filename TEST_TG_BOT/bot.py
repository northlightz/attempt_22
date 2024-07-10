#!/usr/bin/env python
# pylint: disable=unused-argument

import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters

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
        "Hi! I'm a simple bot that collects a title and content. "
        "Let's begin! Please send me the title."
    )
    return TITLE

async def title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the title and asks for the content."""
    user = update.message.from_user
    context.user_data['title'] = update.message.text
    logger.info("Title of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "Great! Now, please send me the content."
    )
    return CONTENT

async def content(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the content and ends the conversation."""
    user = update.message.from_user
    context.user_data['content'] = update.message.text
    logger.info("Content of %s: %s", user.first_name, update.message.text)
    
    # Here you can add code to use the title and content
    # For example, you could save them to a file or database
    
    await update.message.reply_text(
        f"Thank you! I've received the following:\n"
        f"Title: {context.user_data['title']}\n"
        f"Content: {context.user_data['content']}\n"
        f"You can start over by sending /start."
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
    application = Application.builder().token("YOUR_BOT_TOKEN").build()

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