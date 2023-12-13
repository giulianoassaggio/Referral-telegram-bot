#pip install python-telegram-bot

import logging
from telegram import Update, ChatMemberUpdated, Chat, ChatMember
from telegram.ext import Application, CommandHandler, ContextTypes, ChatMemberHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

"""
CONFIGURATION:
The bot is designed to provide basic management of a referral link system.
Each user can request a link privately from the bot, and the bot will dynamically create a personalized link with a name matching the username of the requester.
When a user uses the generated link to join the group, the administrator receives a private message in the chat with the following content:
"username1 joined, invited by username2" (where username1 is the username of the newly joined user, and username2 is the username of the link creator).

GROUP_CHAT_ID: id of the group chat (for which invitation links are needed)
BOT_TOKEN: unique token provided by @fatherbot
DEV_USER_ID: administrator's ID who will receive updates privately.
"""
GROUP_CHAT_ID   =   1   # Usually, a "-100" is added in front of the ID. 
                        # If there are any issues, set DEBUG = True and launch /CreateLink in the group.
                        # This will print the correct ID on the screen.
DEV_USER_ID     =   1
BOT_TOKEN       =   "token"

DEBUG = False

async def CreateLink(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Creates on-the-fly a personalized link. Username of the creator will be used as link's name, 
    to track referrals
    """

    if DEBUG:
        print("greet_chat_member called")
    
    chat_id = update.effective_chat.id              # (id -> int) chat where the command is used
    user = update.effective_message.from_user.id    # (id -> int) user who used the command
    if DEBUG:
        print(chat_id)
        print(user)

    if (update.effective_chat.type == "private"):   # Command can only be used in private chats
        
        # Get the username and create a link with the name as the username
        username2 = update.effective_message.from_user.username # Accordng to documentation, username2 is the username of the link creator
        invite_link = (await context.bot.create_chat_invite_link(GROUP_CHAT_ID, name=username2)).invite_link
        # Send a message with the personal invite link
        await context.bot.send_message(chat, invite_link)

    else:
        await context.bot.send_message(chat, "Command CreateLink must be used in private chat")
    
async def greet_chat_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    if new member joins, send the admin a message with ref info
    """
    if DEBUG:
        print("greet_chat_member called")

    username1 = update.chat_member.new_chat_member.user.username    # According to the documentation, username1 is the username of the newly joined user
    
    if username1 is None:
        return
    if update.chat_member.invite_link is None:
        return

    invite_link = update.chat_member.invite_link.name   # name corresponds to username2

    if DEBUG:
        print(update.chat_member)
    
    mex = ""
    if invite_link is None:
        mex = f"@{username1} didn't use any referral link to join the group"
    else:
        mex = f"@{username1} joined, invited by @{invite_link}"
    await context.bot.send_message(DEV_USER_ID, mex)
    

if __name__ == '__main__':
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("CreateLink", CreateLink))
    application.add_handler(ChatMemberHandler(greet_chat_members, ChatMemberHandler.CHAT_MEMBER))
    application.run_polling(allowed_updates=Update.ALL_TYPES)
