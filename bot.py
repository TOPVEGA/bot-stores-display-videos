# MIT License

# Copyright (c) 2026 VEGA

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# لوجيك | Logic وجهتك البرمجية الأولى  بالوطن العربي
# شروحات - أكواد - وأحدث تقنيات برمجية - وحلول تقنية
# بواسطه: @TopVeGa


from pyrogram import Client, filters, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
import json
import time
import os
import asyncio
from datetime import datetime
from typing import List, Dict
import sys

app = Client(
    "Foreign_TV",
    api_id=8186557,
    api_hash="efd77b34c69c164ce158037ff5a0d117",
    bot_token="9273725485:AAGbwQb...."#توكن هنا
)

OWNER_VEGA = [481322119]

DATA_FILES = {
    "menus": "menus.json",
    "buttons": "buttons.json",
    "channels": "channels.json",
    "users": "users.json",
    "settings": "settings.json",
    "conversations": "conversations.json",
    "banned_users": "banned_users.json",
    "user_activity": "user_activity.json",
    "images": "images.json"
}

for file in DATA_FILES.values():
    if not os.path.exists(file):
        with open(file, 'w', encoding='utf-8') as f:
            if file == "settings.json":
                json.dump({"contact_enabled": False}, f)
            elif file == "conversations.json":
                json.dump({}, f)
            elif file == "banned_users.json":
                json.dump([], f)
            elif file == "user_activity.json":
                json.dump({}, f)
            elif file == "images.json":
                json.dump({}, f)
            else:
                json.dump([], f)

if not os.path.exists(DATA_FILES["settings"]):
    with open(DATA_FILES["settings"], 'w', encoding='utf-8') as f:
        json.dump({"contact_enabled": False, "developers": OWNER_VEGA}, f)

if not os.path.exists(DATA_FILES["menus"]):
    with open(DATA_FILES["menus"], 'w', encoding='utf-8') as f:
        json.dump([], f)

def load_data(file_name):
    if not os.path.exists(file_name):
        return []
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if file_name == DATA_FILES["settings"] and "developers" not in data:
            data["developers"] = OWNER_VEGA
            save_data(file_name, data)
        return data

def save_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_contact_status():
    settings = load_data(DATA_FILES["settings"])
    return settings.get("contact_enabled", False)

def set_contact_status(status):
    settings = load_data(DATA_FILES["settings"])
    settings["contact_enabled"] = status
    save_data(DATA_FILES["settings"], settings)

def add_conversation(user_id):
    conversations = load_data(DATA_FILES["conversations"])
    conversations[str(user_id)] = True
    save_data(DATA_FILES["conversations"], conversations)

def remove_conversation(user_id):
    conversations = load_data(DATA_FILES["conversations"])
    if str(user_id) in conversations:
        del conversations[str(user_id)]
        save_data(DATA_FILES["conversations"], conversations)

def ban_user(user_id):
    banned_users = load_data(DATA_FILES["banned_users"])
    if user_id not in banned_users:
        banned_users.append(user_id)
        save_data(DATA_FILES["banned_users"], banned_users)

def unban_user(user_id):
    banned_users = load_data(DATA_FILES["banned_users"])
    if user_id in banned_users:
        banned_users.remove(user_id)
        save_data(DATA_FILES["banned_users"], banned_users)

def is_banned(user_id):
    banned_users = load_data(DATA_FILES["banned_users"])
    return user_id in banned_users

def update_user_activity(user_id):
    user_activity = load_data(DATA_FILES["user_activity"])
    current_time = time.time()
    if str(user_id) not in user_activity:
        user_activity[str(user_id)] = {"last_press": current_time, "press_count": 1}
    else:
        last_press = user_activity[str(user_id)]["last_press"]
        press_count = user_activity[str(user_id)]["press_count"]
        if current_time - last_press < 5:
            press_count += 1
        else:
            press_count = 1
        user_activity[str(user_id)] = {"last_press": current_time, "press_count": press_count}
    save_data(DATA_FILES["user_activity"], user_activity)
    return user_activity[str(user_id)]

def is_developer(user_id):
    settings = load_data(DATA_FILES["settings"])
    developers = settings.get("developers", [])
    return user_id in developers

class States:
    CHOOSE_ACTION = 1
    GET_MENU_IMAGE = 2
    GET_MENU_NAME = 3
    GET_VIDEO = 4
    GET_TITLE = 5
    SELECT_MENU = 6
    DELETE_MENU = 7
    MANAGE_BUTTONS = 8
    DELETE_BUTTON = 9

user_data = {}

async def check_subscription_vega(user_id):
    try:
        channels = load_data(DATA_FILES["channels"])
        if not channels:
            return True
        for channel in channels:
            try:
                chat_member = await app.get_chat_member(int(channel["channel_id"]), user_id)
                if chat_member.status in ['left', 'kicked']:
                    return False
            except Exception:
                return False
        return True
    except Exception as e:
        print(f"Subscription check error: {e}")
        return False

async def show_channels_menu_vega(user_id):
    channels = load_data(DATA_FILES["channels"])
    keyboard = []
    for channel in channels:
        username = channel["username"] if channel["username"] else f"channel_{channel['id']}"
        keyboard.append([InlineKeyboardButton(f"انضم إلى {username}", url=f"t.me/{username}")])
    keyboard.append([InlineKeyboardButton("تحقق من الاشتراك", callback_data="check_subscription")])
    return InlineKeyboardMarkup(keyboard)

async def broadcast_message_vega(message: Message, text: str):
    try:
        users = load_data(DATA_FILES["users"])
        success = 0
        failed = 0
        msg = await message.reply("جاري الاذاعة عزيزي المطور")
        for user in users:
            try:
                await app.send_message(user["user_id"], text)
                success += 1
                time.sleep(0.5)
            except Exception as e:
                failed += 1
            if success % 10 == 0:
                await msg.edit(f"التقدم: {success+failed}/{len(users)}")
        await msg.edit(f"تم الإرسال بنجاح إلى {success} مستخدم\nفشل الإرسال إلى {failed} مستخدم")
    except Exception as e:
        await message.reply(f"هناك خطأ عزيزي المطور :- {e}")

@app.on_message(filters.command(["تفعيل التواصل"], "") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def enable_contact_vega(client, message: Message):
    set_contact_status(True)
    await message.reply("تم تفعيل التواصل بنجاح.")

@app.on_message(filters.command(["تعطيل التواصل"], "") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def disable_contact_vega(client, message: Message):
    set_contact_status(False)
    await message.reply("تم تعطيل التواصل بنجاح.")

@app.on_message(filters.command(["رد"], "") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def reply_to_user_vega(client, message: Message):
    if len(message.command) < 3:
        await message.reply("استخدم الأمر هكذا:\nرد user_id الرسالة")
        return
    user_id = int(message.command[1])
    reply_text = " ".join(message.command[2:])
    try:
        await app.send_message(user_id, f"رد من المطور:\n\n{reply_text}")
        await message.reply("تم إرسال الرد بنجاح.")
    except Exception as e:
        await message.reply(f"فشل إرسال الرد: {e}")

async def delete_video_after_delay_vega(chat_id, message_id, delay=3600):
    await asyncio.sleep(delay)
    try:
        await app.delete_messages(chat_id, message_id)
    except Exception as e:
        print(f"فشل حذف الفيديو: {e}")

@app.on_message(filters.command(["جلب نسخة"], "") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def download_backup_vega(client, message: Message):
    try:
        for file_name in DATA_FILES.values():
            if os.path.exists(file_name):
                await message.reply_document(file_name)
        await message.reply("تم إرسال نسخة من ملفات التخزين بنجاح.")
    except Exception as e:
        await message.reply(f"فشل إرسال النسخة: {e}")

@app.on_message(filters.command(["رفع نسخة"], "") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))) & filters.document)
async def upload_backup_vega(client, message: Message):
    try:
        file_name = message.document.file_name
        if file_name not in DATA_FILES.values():
            await message.reply("اسم الملف غير صحيح.")
            return
        await message.download(file_name=file_name)
        await message.reply(f"تم تحديث الملف {file_name} بنجاح.")
    except Exception as e:
        await message.reply(f"فشل تحديث الملف: {e}")

@app.on_message(filters.command(["رفع مطور"], "") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def promote_developer_vega(client, message: Message):
    if len(message.command) < 2:
        await message.reply("استخدم الأمر هكذا:\nرفع_مطور user_id")
        return
    try:
        user_id = int(message.command[1])
        settings = load_data(DATA_FILES["settings"])
        if "developers" not in settings:
            settings["developers"] = OWNER_VEGA
        if user_id in settings["developers"]:
            await message.reply("هذا المستخدم مطور بالفعل.")
            return
        settings["developers"].append(user_id)
        save_data(DATA_FILES["settings"], settings)
        await message.reply(f"تم رفع المستخدم {user_id} كمطور بنجاح.")
    except Exception as e:
        await message.reply(f"فشل رفع المطور: {e}")

@app.on_message(filters.command(["تنزيل مطور"], "") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def demote_developer_vega(client, message: Message):
    if len(message.command) < 2:
        await message.reply("استخدم الأمر هكذا:\nتنزيل_مطور user_id")
        return
    try:
        user_id = int(message.command[1])
        settings = load_data(DATA_FILES["settings"])
        if "developers" not in settings:
            settings["developers"] = OWNER_VEGA
        if user_id not in settings["developers"]:
            await message.reply("هذا المستخدم ليس مطورا.")
            return
        settings["developers"].remove(user_id)
        save_data(DATA_FILES["settings"], settings)
        await message.reply(f"تم تنزيل المستخدم {user_id} من المطورين بنجاح.")
    except Exception as e:
        await message.reply(f"فشل تنزيل المطور: {e}")

@app.on_message(filters.command(["تحديث"], "") & filters.user(OWNER_VEGA))
async def restart_bot_vega(client, message: Message):
    await message.reply("جاري إعادة تشغيل البوت...")
    python = sys.executable
    os.execl(python, python, *sys.argv)

@app.on_message(filters.command(["اضف قناة"], "") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def add_channel_vega(client, message: Message):
    try:
        if len(message.command) < 2:
            await message.reply("استخدم الأمر هكذا:\nاضف قناة @username")
            return
        username = message.command[1].replace("@", "")
        try:
            chat = await app.get_chat(username)
            channels = load_data(DATA_FILES["channels"])
            if any(channel["username"] == username for channel in channels):
                await message.reply(f"القناة {username} موجودة بالفعل!")
                return
            new_channel = {
                "id": len(channels) + 1,
                "channel_id": str(chat.id),
                "username": username
            }
            channels.append(new_channel)
            save_data(DATA_FILES["channels"], channels)
            await message.reply(f"تم إضافة القناة {username} بنجاح")
        except Exception as e:
            await message.reply(f"فشل إضافة القناة: {e}")
    except Exception as e:
        await message.reply(f"حدث خطأ: {e}")

@app.on_message(filters.command(["حذف قناة"], "") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def remove_channel_vega(client, message: Message):
    try:
        if len(message.command) < 2:
            await message.reply("استخدم الأمر هكذا:\nحذف قناة @username")
            return
        username = message.command[1].replace("@", "")
        channels = load_data(DATA_FILES["channels"])
        channels = [channel for channel in channels if channel["username"] != username]
        save_data(DATA_FILES["channels"], channels)
        await message.reply(f"تم حذف القناة {username} بنجاح" if len(channels) > 0 else "القناة غير موجودة")
    except Exception as e:
        await message.reply(f"حدث خطأ: {e}")

@app.on_message(filters.command(["حظر"], "") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def ban_user_command_vega(client, message: Message):
    if len(message.command) < 2:
        await message.reply("استخدم الأمر هكذا:\nحظر user_id")
        return
    user_id = int(message.command[1])
    ban_user(user_id)
    user_info = await app.get_users(user_id)
    await notify_OWNER_VEGAs_vega({"user_id": user_id, "first_name": user_info.first_name}, "حظر")
    await message.reply(f"تم حظر المستخدم {user_id} بنجاح.")

@app.on_message(filters.command(["الغاء حظر"], "") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def unban_user_command_vega(client, message: Message):
    if len(message.command) < 2:
        await message.reply("استخدم الأمر هكذا:\nالغاء_حظر user_id")
        return
    user_id = int(message.command[1])
    unban_user(user_id)
    user_info = await app.get_users(user_id)
    await notify_OWNER_VEGAs_vega({"user_id": user_id, "first_name": user_info.first_name}, "إلغاء حظر")
    await message.reply(f"تم إلغاء حظر المستخدم {user_id} بنجاح.")

@app.on_message(filters.command(["شيير"], "") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def broadcast_command_vega(client, message: Message):
    if len(message.command) < 2:
        await message.reply("استخدم الأمر هكذا:\nشيير النص المراد اذاعت")
        return
    text = message.text.split(" ", 1)[1]
    await broadcast_message_vega(message, text)

@app.on_callback_query(filters.regex(r"^back_to_control_panel$") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def back_to_control_panel_vega(client, query):
    users = load_data(DATA_FILES["users"])
    user_count = len(users)
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"عدد المستخدمين ({user_count})", callback_data="user_count"),
         InlineKeyboardButton(f"عدد القنوات", callback_data="channel_count")],
        [InlineKeyboardButton("عرض القوائم", callback_data="view_menus"),
        InlineKeyboardButton("حذف قائمة", callback_data="delete_menu")],
        [InlineKeyboardButton("إضافة محتوى", callback_data="add_content"),
        InlineKeyboardButton("حذف زر من قائمة", callback_data="delete_button_from_menu")],
        [InlineKeyboardButton("رفع مطور", callback_data="promote_developer"),
         InlineKeyboardButton("تنزيل مطور", callback_data="demote_developer")],
        [InlineKeyboardButton("اضف قناة", callback_data="promote_channal"),
         InlineKeyboardButton("حذف قناة", callback_data="demote_channal")],
        [InlineKeyboardButton("حظر", callback_data="baaaaan"),
         InlineKeyboardButton("الغاء حظر", callback_data="unbaaaaan")],
        [InlineKeyboardButton("تفعيل التواصل", callback_data="twasssolon"),
         InlineKeyboardButton("تعطيل التواصل", callback_data="twasssolof")],
        [InlineKeyboardButton("اذاعه للمستخدمين", callback_data="sharrrrrrei"),
         InlineKeyboardButton("تحديث البوت", callback_data="reeeeestart")]
    ])
    await query.message.edit("مرحبآ بك مطوري هذه لوحة التحكم والإدارة للبوت\nتم تطويري من قبل فيجا تيم t.me/vegaone", reply_markup=keyboard)

@app.on_message(filters.command("start") & filters.private & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def control_panel_vega(client, message: Message):
    users = load_data(DATA_FILES["users"])
    user_count = len(users)
    channels = load_data(DATA_FILES["channels"])
    channel_count = len(channels)
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"عدد المستخدمين ({user_count})", callback_data="user_count"),
         InlineKeyboardButton(f"عدد القنوات ({channel_count})", callback_data="channel_count")],
        [InlineKeyboardButton("عرض القوائم", callback_data="view_menus"),
         InlineKeyboardButton("حذف قائمة", callback_data="delete_menu")],
        [InlineKeyboardButton("إضافة محتوى", callback_data="add_content"),
         InlineKeyboardButton("حذف زر من قائمة", callback_data="delete_button_from_menu")],
        [InlineKeyboardButton("رفع مطور", callback_data="promote_developer"),
         InlineKeyboardButton("تنزيل مطور", callback_data="demote_developer")],
        [InlineKeyboardButton("اضف قناة", callback_data="promote_channal"),
         InlineKeyboardButton("حذف قناة", callback_data="demote_channal")],
        [InlineKeyboardButton("حظر", callback_data="baaaaan"),
         InlineKeyboardButton("الغاء حظر", callback_data="unbaaaaan")],
        [InlineKeyboardButton("تفعيل التواصل", callback_data="twasssolon"),
         InlineKeyboardButton("تعطيل التواصل", callback_data="twasssolof")],
        [InlineKeyboardButton("اذاعه للمستخدمين", callback_data="sharrrrrrei"),
         InlineKeyboardButton("تحديث البوت", callback_data="reeeeestart")]
    ])
    await message.reply("مرحبآ بك مطوري هذه لوحة التحكم والإدارة للبوت\nتم تطويري من قبل فيجا تيم t.me/vegaone", reply_markup=keyboard)

@app.on_callback_query(filters.regex(r"^channel_count$") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def show_channel_count_vega(client, query):
    channels = load_data(DATA_FILES["channels"])
    channel_count = len(channels)
    await query.message.edit(f"عدد القنوات المضافة للاشتراك الإجباري: {channel_count}")

@app.on_callback_query(filters.regex(r"^user_count$") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def show_user_count_vega(client, query):
    users = load_data(DATA_FILES["users"])
    user_count = len(users)
    await query.message.edit(f"عدد المستخدمين في البوت : {user_count}")

@app.on_callback_query(filters.regex(r"^promote_developer$") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def promote_developer_callback_vega(client, query):
    await query.message.edit("استخدم الأمر: رفع مطور user_id")

@app.on_callback_query(filters.regex(r"^demote_developer$") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def demote_developer_callback_vega(client, query):
    await query.message.edit("استخدم الأمر: تنزيل مطور user_id")

@app.on_callback_query(filters.regex(r"^promote_channal$") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def promote_channel_callback_vega(client, query):
    await query.message.edit("استخدم الأمر: اضف قناة user_id")

@app.on_callback_query(filters.regex(r"^demote_channal$") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def demote_channel_callback_vega(client, query):
    await query.message.edit("استخدم الأمر: حذف قناة user_id")

@app.on_callback_query(filters.regex(r"^baaaaan$") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def ban_callback_vega(client, query):
    await query.message.edit("استخدم الأمر: حظر user_id")

@app.on_callback_query(filters.regex(r"^unbaaaaan$") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def unban_callback_vega(client, query):
    await query.message.edit("استخدم الأمر: الغاء حظر user_id")

@app.on_callback_query(filters.regex(r"^twasssolon$") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def enable_contact_callback_vega(client, query):
    await query.message.edit("عزيزي المطور قم بارسال فتح التواصل")

@app.on_callback_query(filters.regex(r"^twasssolof$") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def disable_contact_callback_vega(client, query):
    await query.message.edit("عزيزي المطور قم بارسال قفل التواصل")

@app.on_callback_query(filters.regex(r"^sharrrrrrei$") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def broadcast_callback_vega(client, query):
    await query.message.edit("عزيزي المطور قم بارسال شيير + النص المراد اذاعة")

@app.on_callback_query(filters.regex(r"^reeeeestart$") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def restart_callback_vega(client, query):
    await query.message.edit("عزيزي المطور قم بارسال تحديث مع العلم يجب تحديثي كل عند رفع مطور او اضافة اشتراك اجباري")

@app.on_callback_query(filters.regex(r"^view_menus$") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def view_menus_vega(client, query):
    menus = load_data(DATA_FILES["menus"])
    buttons = load_data(DATA_FILES["buttons"])
    response = "القوائم المتاحة:\n\n"
    for menu in menus:
        menu_buttons = [btn["title"] for btn in buttons if btn["menu_id"] == menu["id"]]
        response += f"{menu['name']} - الأزرار: {', '.join(menu_buttons)}\n\n"
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("رجوع", callback_data="back_to_control_panel")]])
    await query.message.edit(response, reply_markup=keyboard)

@app.on_callback_query(filters.regex(r"^delete_menu$") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def delete_menu_vega(client, query):
    menus = load_data(DATA_FILES["menus"])
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(menu["name"], callback_data=f"del_menu_{menu['id']}")]
        for menu in menus
    ] + [[InlineKeyboardButton("رجوع", callback_data="back_to_control_panel")]])
    await query.message.edit("اختر القائمة للحذف:", reply_markup=keyboard)

@app.on_callback_query(filters.regex(r"^del_menu_(\d+)$") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def confirm_delete_vega(client, query):
    menu_id = int(query.matches[0].group(1))
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("تأكيد", callback_data=f"confirm_del_{menu_id}")],
        [InlineKeyboardButton("إلغاء", callback_data="cancel_del")],
        [InlineKeyboardButton("رجوع", callback_data="delete_menu")]
    ])
    await query.message.edit("هل أنت متأكد من الحذف؟", reply_markup=keyboard)

@app.on_callback_query(filters.regex(r"^delete_button_from_menu$") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def delete_button_from_menu_vega(client, query):
    menus = load_data(DATA_FILES["menus"])
    if not menus:
        await query.message.edit("لا توجد قوائم متاحة.")
        return
    keyboard = []
    for menu in menus:
        keyboard.append([InlineKeyboardButton(menu["name"], callback_data=f"select_menu_to_delete_button_{menu['id']}")])
    keyboard.append([InlineKeyboardButton("رجوع", callback_data="back_to_control_panel")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit("اختر القائمة التي تريد حذف زر منها:", reply_markup=reply_markup)

@app.on_callback_query(filters.regex(r"^select_menu_to_delete_button_(\d+)$") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def select_menu_to_delete_button_vega(client, query):
    menu_id = int(query.matches[0].group(1))
    buttons = load_data(DATA_FILES["buttons"])
    menu_buttons = [btn for btn in buttons if btn["menu_id"] == menu_id]
    if not menu_buttons:
        await query.message.edit("هذه القائمة لا تحتوي على أزرار.")
        return
    keyboard = []
    for button in menu_buttons:
        keyboard.append([InlineKeyboardButton(button["title"], callback_data=f"delete_button_{button['id']}")])
    keyboard.append([InlineKeyboardButton("رجوع", callback_data="delete_button_from_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit("اختر الزر الذي تريد حذفه:", reply_markup=reply_markup)

@app.on_callback_query(filters.regex(r"^delete_button_(\d+)$") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def confirm_delete_button_vega(client, query):
    button_id = int(query.matches[0].group(1))
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("تأكيد الحذف", callback_data=f"confirm_delete_button_{button_id}")],
        [InlineKeyboardButton("إلغاء", callback_data="cancel_delete_button")],
        [InlineKeyboardButton("رجوع", callback_data="delete_button_from_menu")]
    ])
    await query.message.edit("هل أنت متأكد من حذف هذا الزر؟", reply_markup=keyboard)

@app.on_callback_query(filters.regex(r"^confirm_delete_button_(\d+)$") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def perform_delete_button_vega(client, query):
    button_id = int(query.matches[0].group(1))
    buttons = load_data(DATA_FILES["buttons"])
    buttons = [btn for btn in buttons if btn["id"] != button_id]
    save_data(DATA_FILES["buttons"], buttons)
    await query.message.edit("تم حذف الزر بنجاح!")

@app.on_callback_query(filters.regex(r"^cancel_delete_button$") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def cancel_delete_button_vega(client, query):
    await delete_button_from_menu_vega(client, query)

@app.on_callback_query(filters.regex(r"^confirm_del_(\d+)$") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def perform_delete_vega(client, query):
    menu_id = int(query.matches[0].group(1))
    menus = load_data(DATA_FILES["menus"])
    menus = [menu for menu in menus if menu["id"] != menu_id]
    save_data(DATA_FILES["menus"], menus)
    buttons = load_data(DATA_FILES["buttons"])
    buttons = [btn for btn in buttons if btn["menu_id"] != menu_id]
    save_data(DATA_FILES["buttons"], buttons)
    await query.message.edit("تم الحذف بنجاح!")

@app.on_callback_query(filters.regex(r"^add_content$") & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))))
async def start_adding_vega(client, query):
    user_data[query.from_user.id] = {}
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("إنشاء قائمة جديدة", callback_data="new_menu")],
        [InlineKeyboardButton("إضافة إلى قائمة موجودة", callback_data="existing_menu")],
        [InlineKeyboardButton("رجوع", callback_data="back_to_control_panel")]
    ])
    await query.message.edit("اختر الإجراء:", reply_markup=keyboard)
    user_data[query.from_user.id]['state'] = States.CHOOSE_ACTION

@app.on_callback_query(filters.regex(r"^(new_menu|existing_menu)$"))
async def handle_menu_choice_vega(client, query):
    user_id = query.from_user.id
    if query.data == "new_menu":
        await query.message.edit("أرسل صورة القائمة الجديدة:")
        user_data[user_id]['state'] = States.GET_MENU_IMAGE
    else:
        menus = load_data(DATA_FILES["menus"])
        if not menus:
            await query.message.edit("لا توجد قوائم متاحة. يرجى إنشاء قائمة جديدة أولاً.")
            return
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(menu["name"], callback_data=f"select_menu_{menu['id']}")] for menu in menus
        ])
        await query.message.edit("اختر القائمة:", reply_markup=keyboard)
        user_data[user_id]['state'] = States.SELECT_MENU

@app.on_message(filters.private & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))) & filters.photo)
async def handle_photo_vega(client, message: Message):
    user_id = message.from_user.id
    state = user_data.get(user_id, {}).get('state')
    if state == States.GET_MENU_IMAGE:
        user_data[user_id]['image_id'] = message.photo.file_id
        user_data[user_id]['state'] = States.GET_MENU_NAME
        await message.reply("أرسل اسم القائمة الجديدة:")

@app.on_callback_query(filters.regex(r"^select_menu_(\d+)$"))
async def handle_selected_menu_vega(client, query):
    user_id = query.from_user.id
    menu_id = int(query.matches[0].group(1))
    user_data[user_id] = {
        'state': States.GET_VIDEO,
        'menu_id': menu_id
    }
    await query.message.edit("أرسل الفيديو الأول لهذه القائمة:")

@app.on_message(filters.private & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))) & filters.text)
async def handle_text_vega(client, message: Message):
    user_id = message.from_user.id
    state = user_data.get(user_id, {}).get('state')
    if state == States.GET_MENU_NAME:
        menus = load_data(DATA_FILES["menus"])
        images = load_data(DATA_FILES["images"])
        new_menu = {
            "id": len(menus) + 1,
            "name": message.text.strip(),
            "image_id": user_data[user_id].get('image_id', None)
        }
        menus.append(new_menu)
        save_data(DATA_FILES["menus"], menus)
        if user_data[user_id].get('image_id'):
            images[str(new_menu["id"])] = user_data[user_id]['image_id']
            save_data(DATA_FILES["images"], images)
        user_data[user_id] = {
            'state': States.GET_VIDEO,
            'menu_id': new_menu["id"]
        }
        await message.reply("أرسل الفيديو الأول لهذه القائمة:")
    elif state == States.GET_TITLE:
        if 'video_id' not in user_data[user_id]:
            await message.reply("حدث خطأ. يرجى البدء من جديد.")
            return
        buttons = load_data(DATA_FILES["buttons"])
        new_button = {
            "id": len(buttons) + 1,
            "title": message.text,
            "video_id": user_data[user_id]['video_id'],
            "menu_id": user_data[user_id]['menu_id']
        }
        buttons.append(new_button)
        save_data(DATA_FILES["buttons"], buttons)
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("إضافة زر آخر", callback_data="add_another")],
            [InlineKeyboardButton("إنهاء", callback_data="finish")]
        ])
        await message.reply("تم الحفظ! اختر الإجراء:", reply_markup=keyboard)
        user_data[user_id]['state'] = States.CHOOSE_ACTION

@app.on_message(filters.private & filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))) & filters.video)
async def handle_video_vega(client, message: Message):
    user_id = message.from_user.id
    state = user_data.get(user_id, {}).get('state')
    if state == States.GET_VIDEO:
        user_data[user_id]['video_id'] = message.video.file_id
        user_data[user_id]['state'] = States.GET_TITLE
        await message.reply("أرسل عنوان الزر لهذا الفيديو:")

@app.on_callback_query(filters.regex(r"^(add_another|finish)$"))
async def handle_additional_actions_vega(client, query):
    user_id = query.from_user.id
    if query.data == "add_another":
        user_data[user_id]['state'] = States.GET_VIDEO
        await query.message.edit("أرسل الفيديو التالي:")
    else:
        del user_data[user_id]
        await query.message.edit("تم الانتهاء من إضافة الأزرار.")

@app.on_message(filters.private & ~filters.user(OWNER_VEGA + list(load_data(DATA_FILES["settings"]).get("developers", []))) & ~filters.command("start"))
async def handle_user_messages_vega(client, message: Message):
    menus = load_data(DATA_FILES["menus"])
    buttons = load_data(DATA_FILES["buttons"])
    if message.text.startswith('/'):
        await message.reply("هذه الرسالة تحتوي على أمر ولا يمكن إعادة توجيهها.")
        return
    is_menu = any(menu["name"] == message.text for menu in menus)
    is_button = any(button["title"] == message.text for button in buttons)
    if is_menu or is_button:
        return
    user_id = message.from_user.id
    user_info = await app.get_users(user_id)
    user_name = user_info.first_name
    user_mention = user_info.mention(user_name)
    add_conversation(user_id)
    message_text = (
        f"رسالة جديدة من المستخدم:\n\n"
        f"المستخدم: {user_mention}\n"
        f"المعرف: `{user_id}`\n"
        f"الرسالة:\n{message.text}"
    )
    for OWNER_VEGA_id in OWNER_VEGA:
        try:
            await app.send_message(OWNER_VEGA_id, message_text)
        except Exception as e:
            print(f"فشل إرسال الرسالة إلى المطور {OWNER_VEGA_id}: {e}")
    await message.reply("تم إرسال رسالتك إلى المطور.")

async def notify_OWNER_VEGAs_vega(user, action_type):
    user_id = user["user_id"]
    first_name = user.get("first_name", "Unknown")
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if action_type == "دخول":
        message_text = (
            f"مستخدم جديد دخل البوت!\n\n"
            f"معرف المستخدم: `{user_id}`\n"
            f"الاسم: {first_name}\n"
            f"وقت التسجيل: `{current_time}`"
        )
    elif action_type == "حظر":
        message_text = (
            f"تم حظر المستخدم\n\n"
            f"المعرف: `{user_id}`\n"
            f"الاسم: {first_name}\n"
            f"وقت الحظر: `{current_time}`"
        )
    elif action_type == "إلغاء حظر":
        message_text = (
            f"تم إلغاء حظر المستخدم\n\n"
            f"المعرف: `{user_id}`\n"
            f"الاسم: {first_name}\n"
            f"وقت الإلغاء: `{current_time}`"
        )
    for OWNER_VEGA_id in OWNER_VEGA:
        try:
            await app.send_message(OWNER_VEGA_id, message_text)
        except Exception as e:
            print(f"فشل إرسال التنبيه إلى المطور {OWNER_VEGA_id}: {e}")

@app.on_message(filters.command("start") & filters.private)
async def start_vega(client, message: Message):
    user_id = message.from_user.id
    if is_banned(user_id):
        await message.reply("تم حظرك من استخدام البوت.")
        return
    users = load_data(DATA_FILES["users"])
    user_exists = any(user["user_id"] == user_id for user in users)
    if not user_exists:
        new_user = {"user_id": user_id, "joined_at": int(time.time())}
        users.append(new_user)
        save_data(DATA_FILES["users"], users)
        await notify_OWNER_VEGAs_vega(new_user, "دخول")
    subscribed = await check_subscription_vega(user_id)
    if not subscribed:
        await message.reply_text(
            "عذرآ عزيزي المستخدم يرجي الاشتراك في في القنوات اولا",
            reply_markup=await show_channels_menu_vega(user_id)
        )
        return
    await show_main_menu_vega(message)

@app.on_callback_query(filters.regex("^check_subscription$"))
async def check_subscription_callback_vega(client, query):
    subscribed = await check_subscription_vega(query.from_user.id)
    if subscribed:
        await query.message.delete()
        await show_main_menu_vega(query.message)
    else:
        await query.answer("لم تنضم لجميع القنوات بعد!", show_alert=True)

async def show_main_menu_vega(message: Message):
    try:
        menus = load_data(DATA_FILES["menus"])
        if not menus:
            return await message.reply("لا توجد قوائم متاحة حالياً")
        keyboard = []
        for i in range(0, len(menus), 2):
            row = []
            if i < len(menus):
                row.append(InlineKeyboardButton(menus[i]["name"], callback_data=f"menu_{menus[i]['id']}"))
            if i + 1 < len(menus):
                row.append(InlineKeyboardButton(menus[i + 1]["name"], callback_data=f"menu_{menus[i + 1]['id']}"))
            if row:
                keyboard.append(row)
        reply_markup = InlineKeyboardMarkup(keyboard)
        await message.reply(
            "مرحبا بك في بوت المسلسلات اختر من القائمة\nمقدم من سورس فيجا t.me/vegaone",
            reply_markup=reply_markup
        )
    except Exception as e:
        await message.reply(f"حدث خطأ: {e}")

@app.on_callback_query(filters.regex(r"^menu_(\d+)$"))
async def handle_menu_selection_vega(client, query):
    menu_id = int(query.matches[0].group(1))
    menus = load_data(DATA_FILES["menus"])
    buttons = load_data(DATA_FILES["buttons"])
    images = load_data(DATA_FILES["images"])
    menu = next((menu for menu in menus if menu["id"] == menu_id), None)
    if not menu:
        await query.message.edit("هذه القائمة غير موجودة!")
        return
    menu_buttons = [btn for btn in buttons if btn["menu_id"] == menu_id]
    if not menu_buttons:
        await query.message.edit("هذه القائمة فارغة!")
        return
    keyboard = []
    for i in range(0, len(menu_buttons), 2):
        row = []
        if i < len(menu_buttons):
            row.append(InlineKeyboardButton(menu_buttons[i]["title"], callback_data=f"button_{menu_buttons[i]['id']}"))
        if i + 1 < len(menu_buttons):
            row.append(InlineKeyboardButton(menu_buttons[i + 1]["title"], callback_data=f"button_{menu_buttons[i + 1]['id']}"))
        if row:
            keyboard.append(row)
    keyboard.append([InlineKeyboardButton("رجوع", callback_data="back_to_main_menu")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    image_id = images.get(str(menu_id))
    if image_id:
        await query.message.reply_photo(
            photo=image_id,
            caption=f"{menu['name']}\n\nاختر زرًا:",
            reply_markup=reply_markup
        )
    else:
        await query.message.edit(f"{menu['name']}\n\nاختر زرًا:", reply_markup=reply_markup)

@app.on_callback_query(filters.regex(r"^button_(\d+)$"))
async def handle_button_selection_vega(client, query):
    button_id = int(query.matches[0].group(1))
    buttons = load_data(DATA_FILES["buttons"])
    button = next((btn for btn in buttons if btn["id"] == button_id), None)
    if button:
        sent_message = await app.send_video(
            chat_id=query.message.chat.id,
            video=button["video_id"],
            caption="\nتم تنزيل الحلقة المطلوبة \nt.me/vegaone",
            protect_content=True
        )
        await query.message.reply("سيتم حذف الفيديو تلقائيًا بعد ساعة.")
        asyncio.create_task(delete_video_after_delay_vega(query.message.chat.id, sent_message.id))
    else:
        await query.message.reply("هذا الزر غير موجود!")

@app.on_callback_query(filters.regex(r"^back_to_main_menu$"))
async def back_to_main_menu_vega(client, query):
    await show_main_menu_vega(query.message)

if __name__ == "__main__":
    app.start()
    print("Bot Started!")
    idle()
    app.stop()