# Telegram_todolistbot
Here's your full `README.md` file without the **License** and **Contributing** sections:

```markdown
# To-Do List Telegram Bot

This project is a **Telegram Bot** designed to help users manage their tasks with ease. The bot allows users to add tasks, set priorities and due dates, view the task list, and mark tasks as completed. Additionally, the bot will remind users of tasks that are due soon.

## Features

- **Task Management**:
  - Add tasks with priorities (High, Medium, Low) and due dates.
  - List current tasks, showing their priority and due date.
  - Mark tasks as finished.
  
- **Reminders**: Automatically sends a reminder one day before a task is due.
  
- **Logging**: User interactions and tasks are logged to help track activity and provide a foundation for debugging.

## Technologies Used

- **Python**: The bot is developed in Python.
- **python-telegram-bot**: Used to interface with Telegram's Bot API.

## Setup and Installation

### Prerequisites

- **Python 3.7+** installed on your machine.
- A Telegram bot token. You can create your bot and get the token via [BotFather](https://core.telegram.org/bots#botfather).

### Installation Steps

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. **Install dependencies**:

   Install the required libraries using `pip`:

   ```bash
   pip install python-telegram-bot==20.0b0
   ```

3. **Configure the bot**:

   In the `bot.py` file, replace the placeholder token with your bot’s token:

   ```python
   TOKEN = 'your-telegram-bot-token'
   ```

4. **Run the bot**:

   To start the bot, run:

   ```bash
   python bot.py
   ```

   The bot will begin polling Telegram for updates and respond to user commands.

## Bot Commands

The following commands are available for users to interact with the bot:

- **/start**: Sends a welcome message and provides instructions for using the bot.
- **/add**: Initiates a conversation to add a new task. The bot will ask for task details such as name, priority, and due date.
- **/list**: Displays all tasks in the user’s to-do list, including their priority, due date, and status (Pending or Finished).
- **/finish**: Allows users to mark a task as finished by selecting the task from the list.
- **/help**: (Optional) You can add this to provide a detailed explanation of each command.

## Conversation Flow

### Task Addition Flow:
1. **/add** command starts the conversation.
   - The bot asks, "What task would you like to add?"
2. User provides the task name.
   - The bot asks, "What's the priority of this task? (High, Medium, Low)"
3. User selects the priority.
   - The bot asks, "When is this task due? (Please use the format YYYY-MM-DD)"
4. User provides the due date.
   - The bot confirms, "Task added successfully!" and ends the conversation.

### Task Completion Flow:
1. **/finish** command starts the conversation.
   - The bot lists all tasks and asks, "Which task would you like to mark as finished? Reply with the task number."
2. User replies with the task number.
   - The bot marks the task as finished and responds, "Task marked as finished."

## Task Management

Each task managed by the bot consists of the following attributes:
- **Task Name**: A brief description of the task.
- **Priority**: High, Medium, or Low based on the user’s selection.
- **Due Date**: The deadline for the task in the format YYYY-MM-DD.
- **Status**: Either Pending or Finished.

Users can view the status and details of all tasks using the **/list** command, which provides an overview of each task.

### Example Task List:
```
Your To-Do List:
1. Buy groceries - Priority: High - Due: 2024-10-25 - Status: Pending
2. Submit report - Priority: Medium - Due: 2024-10-30 - Status: Pending
```

### Example Reminder

The bot will automatically check for tasks due the next day and send users a reminder.

#### Sample Reminder Message:
> "Reminder: Your task 'Buy groceries' is due tomorrow!"

## Logging

The bot logs each interaction, including task creation, listing tasks, and marking tasks as finished. This helps track user activity and can be useful for debugging purposes.

### Sample Log Output:
```bash
2024-10-22 14:45:01,123 - __main__ - INFO - User JohnDoe added a new task: 'Buy groceries'
2024-10-22 14:46:03,456 - __main__ - INFO - User JohnDoe listed all tasks
```

## Extending the Bot

### Adding New Features

To extend the bot with new functionality:

1. **Define new command handlers** using `CommandHandler` or create more complex conversation flows using `ConversationHandler`.
2. **Add the handler** to the application’s handler list in the `main` function.

For example, to add a **/delete** command that allows users to remove a task, follow a similar structure to the **/finish** command.

