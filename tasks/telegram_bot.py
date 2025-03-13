import os
import sys
import logging
import django
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from asgiref.sync import sync_to_async

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_manager_api.settings")
django.setup()

from tasks.models import UserProfile, User, Task

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    logger.error("❌ TELEGRAM_BOT_TOKEN NOT FOUND! Check your .env file.")
    exit(1)

logger.info(f"🔹 Starting bot with token: {TELEGRAM_BOT_TOKEN[:10]}...")


app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()


@sync_to_async
def get_or_create_user(user_id, chat_id):
    """Registers a user in Django via Telegram"""
    logger.info(f"🔹 Checking user: user_id={user_id}, chat_id={chat_id}")

    profile = UserProfile.objects.filter(telegram_id=user_id).first()

    if profile and profile.user:
        logger.info(f"✅ Profile found: {profile.user}")
        profile.telegram_chat_id = chat_id
        profile.save()
        return profile.user

    user, created = User.objects.get_or_create(username=f"telegram_{user_id}")

    if created:
        logger.info(f"✅ New user created: {user.username}")

    profile, _ = UserProfile.objects.get_or_create(
        user=user,
        defaults={'telegram_id': user_id}
    )
    profile.telegram_chat_id = chat_id
    profile.save()

    return user


@sync_to_async
def get_user_tasks(user):
    """Retrieves a user's task list"""
    tasks = Task.objects.filter(user=user).order_by('-deadline')

    if not tasks:
        return "❌ You have no tasks yet."

    message = "📌 *Your tasks:*\n\n"

    for task in tasks:
        deadline_str = (task.deadline.strftime('%d.%m.%Y')
                        if task.deadline else " No deadline")
        message += (
                        f"🔹*Task ID - {task.id}*\n"
                        f" *Title:* {task.title}\n"
                        f" *Status:* {task.get_status_display()}\n"
                        f" *Priority:* {task.get_priority_display()}\n"
                        f" *Deadline:* {deadline_str}\n\n"
                    )

    return message


@sync_to_async
def get_user_profile(user_id):
    """Retrieves a user profile by Telegram ID"""
    return (UserProfile.objects
            .filter(telegram_id=user_id)
            .select_related("user").first()
            )


async def tasks(update: Update, context: CallbackContext):
    """Sends the user their task list"""
    user_id = update.message.from_user.id

    profile = await get_user_profile(user_id)

    if not profile or not profile.user:
        await update.message.reply_text(
            "❌ You are not registered. Send /start."
            )
        return
    user_tasks = await get_user_tasks(profile.user)
    await update.message.reply_text(user_tasks, parse_mode='Markdown')

app.add_handler(CommandHandler("tasks", tasks))


async def start(update: Update, context: CallbackContext):
    """Registers the user and saves their chat_id"""
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id

    logger.info(
        f"🔹Received message from User ID: {user_id}, Chat ID: {chat_id}"
        )

    user = await get_or_create_user(user_id, chat_id)
    await update.message.reply_text(
                f"✅ You are registered as {user.username}!\n"
                "Now you can manage your tasks."
            )

app.add_handler(CommandHandler("start", start))


@sync_to_async
def create_task(user, title):
    """Creates a new task"""
    return Task.objects.create(user=user,
                               title=title,
                               status='new',
                               priority='medium'
                               )


async def new_task(update: Update, context: CallbackContext):
    """Creates a new task via Telegram"""
    user_id = update.message.from_user.id

    profile = await sync_to_async(lambda: UserProfile.objects
                                  .filter(telegram_id=user_id)
                                  .first())()

    if not profile:
        await update.message.reply_text(
            "❌ You are not registered. Send /start."
            )
        return

    user = await sync_to_async(lambda: profile.user)()

    title = " ".join(context.args) if context.args else None

    if not title:
        await update.message.reply_text(
                    "❌ Enter the task name after the command.\n"
                    "Example: /newtask Complete API"
                )
        return

    task = await create_task(user, title)

    await update.message.reply_text(f"✅ Task created: {task.title}")

app.add_handler(CommandHandler("newtask", new_task))


@sync_to_async
def delete_task(user_id, task_id):
    """Deletes a task by user ID"""
    try:
        user = User.objects.get(id=user_id)
        task = Task.objects.get(id=task_id, user=user)
        task.delete()
        return f"✅ Task '{task.title}' has been deleted."
    except Task.DoesNotExist:
        return "❌ Task not found or you do not have access."
    except User.DoesNotExist:
        return "❌ User not found."
    except Exception as e:
        return f"❌ Error: {str(e)}"


async def deletetask(update: Update, context: CallbackContext):
    """Handles the `/deletetask task_id` command"""
    user_id = update.message.from_user.id

    profile = await get_user_profile(user_id)

    if not profile or not profile.user:
        await update.message.reply_text(
                    "You are not registered. Send /start."
                )
        return

    if len(context.args) < 1:
        await update.message.reply_text(
                "❌ Use the command format:\n"
                "/deletetask <task_id>"
            )
        return

    task_id = context.args[0]

    result = await delete_task(profile.user.id, task_id)
    await update.message.reply_text(result)

app.add_handler(CommandHandler("deletetask", deletetask))


@sync_to_async
def update_task(user_id, task_id, new_status):
    """Updates a task status"""
    try:
        user = User.objects.get(id=user_id)
        task = Task.objects.get(id=task_id, user=user)
        task.status = new_status
        task.save()
        return (
                f"✅ Task '{task.title}' status updated to "
                f"'{task.get_status_display()}'."
            )
    except Task.DoesNotExist:
        return "❌ Task not found or you do not have access."
    except User.DoesNotExist:
        return "❌ User not found."
    except Exception as e:
        return f"❌ Error: {str(e)}"


async def updatetask(update: Update, context: CallbackContext):
    """Handles the `/updatetask task_id new_status` command"""
    user_id = update.message.from_user.id

    profile = await get_user_profile(user_id)

    if not profile or not profile.user:
        await update.message.reply_text(
            "❌ You are not registered. Send /start."
            )
        return

    if len(context.args) < 2:
        await update.message.reply_text(
            "❌ Use the command format:\n/updatetask <task_id> <new_status>"
            )
        return

    task_id = context.args[0]
    new_status = context.args[1]

    valid_statuses = ["new", "in_progress", "done", "canceled"]
    if new_status not in valid_statuses:
        await update.message.reply_text(
            f"❌ Invalid status. Available: {', '.join(valid_statuses)}"
            )
        return

    result = await update_task(profile.user.id, task_id, new_status)
    await update.message.reply_text(result)

app.add_handler(CommandHandler("updatetask", updatetask))


if __name__ == '__main__':
    logger.info("🔹 Starting bot...")
    app.run_polling()
