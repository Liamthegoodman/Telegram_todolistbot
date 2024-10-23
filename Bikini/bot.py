import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
TOKEN = '7240540353:AAH37vm_frxam_YTqcOMtjRScrERa0jQIcU'
BOT_USERNAME = '@bikini_bottom_spongebob_bot'

# States for conversation handler
TASK, PRIORITY, DUE_DATE = range(3)

# Command handler for /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username if user.username else f"{user.first_name} {user.last_name}"
    logger.info(f"User {username} started the bot")
    await update.message.reply_text(
        f"Hi {user.first_name}! I'm your To-Do List Bot. Here's what I can do:\n"
        "/add - Add a new task\n"
        "/list - Show your to-do list\n"
        "/finish - Mark a task as finished"
    )

async def add_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("What task would you like to add?")
    return TASK

async def set_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['task'] = update.message.text
    reply_keyboard = [['High', 'Medium', 'Low']]
    await update.message.reply_text(
        "What's the priority of this task?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )
    return PRIORITY

async def set_priority(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['priority'] = update.message.text
    await update.message.reply_text(
        "When is this task due? Please use the format YYYY-MM-DD.",
        reply_markup=ReplyKeyboardRemove()
    )
    return DUE_DATE

async def set_due_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        due_date = datetime.strptime(update.message.text, "%Y-%m-%d")
        context.user_data['due_date'] = due_date
        task = context.user_data['task']
        priority = context.user_data['priority']
        
        if 'tasks' not in context.user_data:
            context.user_data['tasks'] = []
        
        context.user_data['tasks'].append({
            'task': task,
            'priority': priority,
            'due_date': due_date,
            'status': 'Pending'
        })
        
        await update.message.reply_text(f"Task added successfully!\nTask: {task}\nPriority: {priority}\nDue Date: {due_date.strftime('%Y-%m-%d')}")
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text("Invalid date format. Please use YYYY-MM-DD.")
        return DUE_DATE

async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if 'tasks' not in context.user_data or not context.user_data['tasks']:
        await update.message.reply_text("Your to-do list is empty.")
    else:
        task_list = "Your To-Do List:\n"
        for i, task in enumerate(context.user_data['tasks'], 1):
            task_list += f"{i}. {task['task']} - Priority: {task['priority']} - Due: {task['due_date'].strftime('%Y-%m-%d')} - Status: {task['status']}\n"
        await update.message.reply_text(task_list)

async def finish_task(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if 'tasks' not in context.user_data or not context.user_data['tasks']:
        await update.message.reply_text("Your to-do list is empty.")
    else:
        task_list = "Which task would you like to mark as finished? Reply with the number.\n"
        for i, task in enumerate(context.user_data['tasks'], 1):
            task_list += f"{i}. {task['task']}\n"
        await update.message.reply_text(task_list)
        return TASK

async def mark_finished(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        task_num = int(update.message.text) - 1
        if 0 <= task_num < len(context.user_data['tasks']):
            context.user_data['tasks'][task_num]['status'] = 'Finished'
            await update.message.reply_text(f"Task '{context.user_data['tasks'][task_num]['task']}' marked as finished.")
        else:
            await update.message.reply_text("Invalid task number.")
    except ValueError:
        await update.message.reply_text("Please enter a valid number.")
    return ConversationHandler.END

async def check_due_tasks(context: ContextTypes.DEFAULT_TYPE) -> None:
    for user_id, user_data in context.application.user_data.items():
        if 'tasks' in user_data:
            for task in user_data['tasks']:
                if task['status'] == 'Pending':
                    days_until_due = (task['due_date'].date() - datetime.now().date()).days
                    if days_until_due == 1:
                        reminder_text = f"Reminder: Your task '{task['task']}' is due tomorrow!"
                        await context.bot.send_message(chat_id=user_id, text=reminder_text)

async def log_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username if user.username else f"{user.first_name} {user.last_name}"
    logger.info(f"User {username} interacted with the bot")

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add", add_task)],
        states={
            TASK: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_task)],
            PRIORITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_priority)],
            DUE_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_due_date)],
        },
        fallbacks=[],
    )

    finish_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("finish", finish_task)],
        states={
            TASK: [MessageHandler(filters.TEXT & ~filters.COMMAND, mark_finished)],
        },
        fallbacks=[],
    )

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(conv_handler)
    application.add_handler(finish_conv_handler)
    application.add_handler(CommandHandler("list", list_tasks))

    # Add a handler to log all interactions
    application.add_handler(MessageHandler(filters.ALL, log_user), group=-1)

    # Set up job to check due tasks every hour
    job_queue = application.job_queue
    job_queue.run_repeating(check_due_tasks, interval=3600)

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()