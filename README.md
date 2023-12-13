# Referral-telegram-bot

The bot allows users to request personalized referral links. When a user joins the group using the generated link, the administrator receives a private message with the information: "username1 joined, invited by username2" (where username1 is the username of the newly joined user, and username2 is the username of the link creator).
***
## Installation

Install the required Python package using pip:
```bash
pip install python-telegram-bot
```
Start the script:
```bash
python3 /path_to_bot_directory/src/bot_referral.py
```
### Configuration
The bot is designed to provide basic management of a referral link system. Follow the steps below to configure the bot:
1. **Group Chat ID (GROUP_CHAT_ID)**: Set the ID of the group chat for which invitation links are needed.
2. **Bot Token (BOT_TOKEN)**: Obtain a unique token by messaging @BotFather on Telegram. Set this token as the value of BOT_TOKEN
3. **Developer/Admin User ID (DEV_USER_ID)**: Set the administrator's ID who will receive updates privately.

## Usage
In private chat, use the command `/CreateLink` to obtained a personalized referral link. Share it with your friends. When a user joins the group using the link, the administrator receives a notification with the relevant information.
