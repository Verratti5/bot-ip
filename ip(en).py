import requests
import time
import telebot
from telebot import types
from datetime import datetime


token = "" #token bot
bot = telebot.TeleBot(token)

owner = 6310618035  #id

admins = [owner]

mandatory_subscriptions = ["llllIllIIl"]

db = {}

def db_exists(user_id):
    return f"user_{user_id}" in db

def db_get(user_id):
    return db.get(f"user_{user_id}")

def db_set(user_id, lang):
    db[f"user_{user_id}"] = {"lang": lang}

def get_total_users():
    return len(open("ids.txt").readlines())

def sendN(msg, lang):
    total_users = get_total_users()
    bot.send_message(owner, f'''- New User:
Name: [{msg.from_user.first_name}]
ID: {msg.from_user.id}
Username: @{msg.from_user.username}
Input Language: {lang}
Total Bot Users: {total_users}
————————————'''.replace("@None", "Not available"))

def save_user_id(user_id):
    with open("ids.txt", "a") as file:
        file.write(f"{user_id}\n")

@bot.message_handler(commands=["start"])
def start(message):
    idd = message.from_user.id
    subscribed = True

    for ch in mandatory_subscriptions:
        url = f"https://api.telegram.org/bot{token}/getChatMember?chat_id=@{ch}&user_id={idd}"
        req = requests.get(url).json()
        if not ('member' in req.get("result", {}).get("status", '') or 
                'creator' in req.get("result", {}).get("status", '') or 
                'administrator' in req.get("result", {}).get("status", '')):
            subscribed = False
            break

    if idd == owner or subscribed:
        save_user_id(idd)
        if not db_exists(idd):
            db_set(idd, "Not set")
            sendN(message, "Not set")

        if idd == owner:
            btns = types.InlineKeyboardMarkup(row_width=1)
            btn1 = types.InlineKeyboardButton("Statistics", callback_data="stats")
            btn2 = types.InlineKeyboardButton("Broadcast", callback_data="brod")
            btn3 = types.InlineKeyboardButton("Send Storage File", callback_data="file")
            btn4 = types.InlineKeyboardButton("Add Admin", callback_data="add_admin")
            btn5 = types.InlineKeyboardButton("Remove Admin", callback_data="remove_admin")
            btn6 = types.InlineKeyboardButton("Add Mandatory Subscription", callback_data="add_mandatory_sub")
            btn7 = types.InlineKeyboardButton("Remove Mandatory Subscription", callback_data="remove_mandatory_sub")
            btn8 = types.InlineKeyboardButton("Show Admins", callback_data="show_admins")
            btn9 = types.InlineKeyboardButton("Show User Panel", callback_data="show_users")
            btns.row(btn2, btn1)
            btns.row(btn3)
            btns.row(btn4, btn5)
            btns.row(btn6, btn7)
            btns.row(btn8, btn9)
            bot.send_message(message.chat.id, "Welcome, dear owner, please choose one of the options:", reply_markup=btns)
    
        else:
            markup = types.InlineKeyboardMarkup()
            btn_arabic = types.InlineKeyboardButton(text=" 🇮🇶 - العربية", callback_data="set_language_ar")
            btn_english = types.InlineKeyboardButton(text=" 🇺🇸 - English", callback_data="set_language_en")
            btn_french = types.InlineKeyboardButton(text=" 🇫🇷 - Français", callback_data="set_language_fr")
            btn_russian = types.InlineKeyboardButton(text=" 🇷🇺 - Русский", callback_data="set_language_ru")
            btn_kurdish = types.InlineKeyboardButton(text=" 🇹🇷 - Kurdî", callback_data="set_language_ku")
            btn_persian = types.InlineKeyboardButton(text=" 🇮🇷 - فارسی", callback_data="set_language_fa")
            markup.add(btn_arabic, btn_english, btn_french, btn_russian, btn_kurdish, btn_persian)

            message_text = """
اختر اللغة:
--------------------
Choose your language:
--------------------
Choisissez votre langue:
--------------------
Выберите язык:
--------------------
Zimanê xwe hilbijêre:
--------------------
زبان خود را انتخاب کنید:
            """

            bot.send_message(message.chat.id, message_text, reply_markup=markup)


    else:
        message_text = (
            "*أهلا عزيزي يجب عليك الاشتراك في قنوات المطورين:*\n\n"
            f"- *مــعرف القـنوات*: {' و '.join([f'@{ch}' for ch in mandatory_subscriptions])}\n\n"
            "‼️*| اشترك ثم ارسل /start*\n"
            "--------------------\n\n"
            "*Dear user, you must subscribe to the developer's channels:*\n\n"
            f"- *Channel IDs*: {' and '.join([f'@{ch}' for ch in mandatory_subscriptions])}\n\n"
            "‼️*| Subscribe and then send /start*\n"
            "--------------------\n\n"
            "*Cher utilisateur, vous devez vous abonner aux chaînes des développeurs :*\n\n"
            f"- *Identifiants des chaînes*: {' et '.join([f'@{ch}' for ch in mandatory_subscriptions])}\n\n"
            "‼️*| Abonnez-vous puis envoyez /start*\n"
            "--------------------\n\n"
            "*Уважаемый пользователь, вы должны подписаться на каналы разработчиков:*\n\n"
            f"- *Идентификаторы каналов*: {' и '.join([f'@{ch}' for ch in mandatory_subscriptions])}\n\n"
            "‼️*| Подпишитесь, а затем отправьте /start*\n"
            "--------------------\n\n"
            "*Bikarhênerê hêja, divê hûn bi kanalan pêşandinê yên pêşkêşkaran re binivîsin:*\n\n"
            f"- *ID-yên kanalê*: {' û '.join([f'@{ch}' for ch in mandatory_subscriptions])}\n\n"
            "‼️*| Bi kanalê binivîse û paşê /start bişînin*\n"
            "--------------------\n\n"
            "*کاربر عزیز، شما باید در کانال های توسعه دهنده مشترک شوید:*\n\n"
            f"- *شناسه های کانال*: {' و '.join([f'@{ch}' for ch in mandatory_subscriptions])}\n\n"
            "‼️*| مشترک شوید و سپس /start ارسال کنید*\n"
        )
        
        bot.send_message(message.chat.id, message_text, parse_mode="Markdown")



@bot.callback_query_handler(func=lambda call: call.data.startswith("set_language_"))
def set_language(call):
    user_id = call.from_user.id
    lang = call.data.split("_")[-1]

    db_set(user_id, lang)

    privateline = types.InlineKeyboardMarkup()
    ip_btn = types.InlineKeyboardButton(text="📱 - Info IP", callback_data="ip_tracker")
    privateline.add(ip_btn)

    language_texts = {
    "ar": "تم اختيار اللغة العربية. لاستخراج معلومات الـ IP، يُرجى الضغط على الزر الذي في الأسفل.",
    "en": "Language set to English. To extract IP information, please click the button below.",
    "fr": "Langue définie sur le français. Pour extraire les informations de l'IP, veuillez cliquer sur le bouton ci-dessous.",
    "ru": "Язык установлен на русский. Чтобы извлечь информацию об IP, пожалуйста, нажмите кнопку ниже.",
    "ku": "Ziman li Kurdî hat saz kirin. Ji bo hilanînê agahdariyên IPê, ji kerema xwe bişînin li pêlka jêrîn.",
    "fa": "زبان به فارسی تنظیم شد. برای استخراج اطلاعات آی‌پی، لطفا دکمه زیر را فشار دهید."
}


    bot.send_message(call.message.chat.id, language_texts.get(lang, language_texts["en"]), reply_markup=privateline, parse_mode="markdown")

@bot.callback_query_handler(func=lambda call: call.data == "ip_tracker")
def handle_ip_tracker(call):
    user_id = call.from_user.id
    lang = db_get(user_id)["lang"] if db_exists(user_id) else "en"

    ip_texts = {
        "ar": "أرسل الايبي الذي تريد البحث عنه وسوف أرسل إليك جميع معلوماته مع الخارطة",
        "en": "Send the IP you want to look up and I will send you all the details with the map",
        "fr": "Envoyez l'IP que vous souhaitez rechercher et je vous enverrai tous les détails avec la carte",
        "ru": "Отправьте IP, который вы хотите узнать, и я отправлю вам все детали с картой",
        "ku": "IP-ya ku hûn dixwazin lêkolînê bişînin û ez hemî agahdariyên bi nexşeyê ji we re şandinê",
        "fa": "آی‌پی که می‌خواهید جستجو کنید را ارسال کنید و من تمام جزئیات آن را همراه با نقشه برایتان ارسال خواهم کرد"
    }




    bot.send_message(call.message.chat.id, ip_texts.get(lang, ip_texts["en"]))

    bot.register_next_step_handler(call.message, IP_Track)

import re

def IP_Track(message):
    try:
        idu = message.from_user.id
        ip = message.text
        
        # Regular expression to validate IP address format
        valid_ip = re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip)
        if not valid_ip:
            user_data = db_get(idu) if db_exists(idu) else None
            if user_data and user_data.get("lang") == "ar":
                bot.send_message(message.chat.id, "هذا أيبي غير صالح، يرجى إرسال أيبي صالح.")
            elif user_data and user_data.get("lang") == "en":
                bot.send_message(message.chat.id, "This is an invalid IP, please send a valid IP.")
            elif user_data and user_data.get("lang") == "fr":
                bot.send_message(message.chat.id, "Ceci est une IP invalide, veuillez envoyer une IP valide.")
            elif user_data and user_data.get("lang") == "ru":
                bot.send_message(message.chat.id, "Это недействительный IP-адрес, пожалуйста, отправьте действительный IP.")
            elif user_data and user_data.get("lang") == "ku":
                bot.send_message(message.chat.id, "Ev IP nederas e, ji kerema xwe IP nederast bike.")
            elif user_data and user_data.get("lang") == "fa":
                bot.send_message(message.chat.id, "این یک آی‌پی نامعتبر است، لطفا آی‌پی معتبر ارسال کنید.")
            else:
                bot.send_message(message.chat.id, "هذا أيبي غير صالح، يرجى إرسال أيبي صالح.")
            return
        
        # Proceed with IP info retrieval if IP is valid
        rq = requests.get(f'http://ip-api.com/json/{ip}?fields=60551167', timeout=3)
        data = rq.json()

        if data["status"] == "success":
            lat = data["lat"]
            lon = data["lon"]
            loc = f"{lat}, {lon}"
            user_data = db_get(idu) if db_exists(idu) else None
            if user_data and user_data.get("lang") == "ar":
                bot.send_location(message.chat.id, latitude=lat, longitude=lon, horizontal_accuracy=data["offset"])
                bot.reply_to(message, f'''معلومات الأيبي {ip} :
القارة: {data["continent"]}.
الدولة: {data["country"]}.
المحافظة: {data["regionName"]}.
المدينة: {data["city"]}.
خطوط الطول والعرض: {loc}.
المنطقة الزمنية: {data["timezone"]}.
شركة الإتصالات: {data['org']}.
هل الايبي تابع لاستضافة: {data["hosting"]}.
هل الايبي بروكسي: {data['proxy']}.
------ ------- ------- -------
[حساب المطور وقناة المطور](By - @llllIllIIl and By -@llllIllIIl)'''.replace("False", "لا").replace("True", "نعم"))
            elif user_data and user_data.get("lang") == "en":
                bot.send_location(message.chat.id, latitude=lat, longitude=lon, horizontal_accuracy=data["offset"])
                bot.reply_to(message, f'''IP information {ip} :
Continent: {data["continent"]}.
Country: {data["country"]}.
Region: {data["regionName"]}.
City: {data["city"]}.
Lat & Lon: {loc}.
Timezone: {data["timezone"]}.
Telecom Company: {data['org']}.
Is Host: {data["hosting"]}.
Is Proxy: {data['proxy']}.
------ ------- ------- -------
[Developer account and developer channel](By - @llllIllIIl and By -@llllIllIIl)'''.replace("False", "No").replace("True", "Yes"))
            elif user_data and user_data.get("lang") == "fr":
                bot.send_location(message.chat.id, latitude=lat, longitude=lon, horizontal_accuracy=data["offset"])
                bot.reply_to(message, f'''Informations IP {ip} :
Continent: {data["continent"]}.
Pays: {data["country"]}.
Région: {data["regionName"]}.
Ville: {data["city"]}.
Lat & Lon: {loc}.
Fuseau horaire: {data["timezone"]}.
Compagnie télécom: {data['org']}.
Est-ce un hébergement: {data["hosting"]}.
Est-ce un proxy: {data['proxy']}.
------ ------- ------- -------
[Suivez-nous](By - @llllIllIIl and By -@llllIllIIl)'''.replace("False", "Non").replace("True", "Oui"))
            elif user_data and user_data.get("lang") == "ru":
                bot.send_location(message.chat.id, latitude=lat, longitude=lon, horizontal_accuracy=data["offset"])
                bot.reply_to(message, f'''Информация IP {ip} :
Континент: {data["continent"]}.
Страна: {data["country"]}.
Регион: {data["regionName"]}.
Город: {data["city"]}.
Широта и долгота: {loc}.
Часовой пояс: {data["timezone"]}.
Телекоммуникационная компания: {data['org']}.
Хост: {data["hosting"]}.
Прокси: {data['proxy']}.
------ ------- ------- -------
[Следите за нами](By - @llllIllIIl and By -@llllIllIIl)'''.replace("False", "Нет").replace("True", "Да"))
            elif user_data and user_data.get("lang") == "ku":
                bot.send_location(message.chat.id, latitude=lat, longitude=lon, horizontal_accuracy=data["offset"])
                bot.reply_to(message, f'''Agahdariyên IP {ip} :
Kontinent: {data["continent"]}.
Welat: {data["country"]}.
Herêm: {data["regionName"]}.
Bajar: {data["city"]}.
Lat & Lon: {loc}.
Demjimêr: {data["timezone"]}.
Şirketa telekom: {data['org']}.
Host e: {data["hosting"]}.
Proxy e: {data['proxy']}.
------ ------- ------- -------
[Meşgulî](By - @llllIllIIl and By -@llllIllIIl)'''.replace("False", "Na").replace("True", "Erê"))
            elif user_data and user_data.get("lang") == "fa":
                bot.send_location(message.chat.id, latitude=lat, longitude=lon, horizontal_accuracy=data["offset"])
                bot.reply_to(message, f'''اطلاعات IP {ip} :
قاره: {data["continent"]}.
کشور: {data["country"]}.
استان: {data["regionName"]}.
شهر: {data["city"]}.
عرض و طول جغرافیایی: {loc}.
منطقه زمانی: {data["timezone"]}.
شرکت ارتباطات: {data['org']}.
آیا هاست است: {data["hosting"]}.
آیا پروکسی است: {data['proxy']}.
------ ------- ------- -------
[دنبال کنید](By - @llllIllIIl and By -@llllIllIIl)'''.replace("False", "خیر").replace("True", "بله"))
            else:
                bot.send_message(message.chat.id, "لم يتم العثور على معلومات ال IP." if lang == "ar" else "No information found for the IP.")
        else:
            bot.send_message(message.chat.id, "لم يتم العثور على معلومات ال IP." if lang == "ar" else "No information found for the IP.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Error: {str(e)}")


@bot.callback_query_handler(func=lambda call: call.data == "stats")
def handle_stats(call):
    total_users = len(db)

    language_stats = {lang: sum(1 for user in db.values() if user["lang"] == lang) for lang in ["ar", "en", "fr", "ru", "ku", "fa"]}

    today_users = sum(1 for user in db.values() if user.get("join_date") == datetime.now().date())

    stats_message = (f"👥 *Statistics*\n"
                     f"• Total number of users: {total_users}\n"
                     f"• Number of users with Arabic language: {language_stats.get('ar', 0)}\n"
                     f"• Number of users with English language: {language_stats.get('en', 0)}\n"
                     f"• Number of users with French language: {language_stats.get('fr', 0)}\n"
                     f"• Number of users with Russian language: {language_stats.get('ru', 0)}\n"
                     f"• Number of users with Kurdish language: {language_stats.get('ku', 0)}\n"
                     f"• Number of users with Persian language: {language_stats.get('fa', 0)}\n"
                     f"• Number of users who joined today: {today_users}")

    bot.send_message(call.message.chat.id, stats_message, parse_mode="markdown")


@bot.callback_query_handler(func=lambda call: call.data == "brod")
def handle_broadcast(call):
    bot.send_message(call.message.chat.id, "Please send the message to be broadcast to all members:")
    bot.register_next_step_handler(call.message, broadcast_message)


def broadcast_message(message):
    start_time = time.time()  
    text = message.text
    user_ids = list(db.keys())

    try:
        with open('ids.txt', 'r') as file:
            file_user_ids = [line.strip() for line in file.readlines()]
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred while reading the ids.txt file: {e}")
        return

    all_user_ids = set(user_ids + file_user_ids)  

    total_count = len(all_user_ids)
    success_count = 0
    fail_count = 0
    batch_size = 50  
    broadcast_msg = bot.send_message(message.chat.id, "Broadcast started...")

    for i in range(0, total_count, batch_size):
        batch_ids = list(all_user_ids)[i:i + batch_size]
        failed = []
        for user_id in batch_ids:
            try:
                bot.send_message(user_id, text)
                success_count += 1
            except Exception:
                failed.append(user_id)
                fail_count += 1

        if (i // batch_size) % 2 == 0:  
            bot.edit_message_text(
                chat_id=broadcast_msg.chat.id,
                message_id=broadcast_msg.message_id,
                text=f"""Broadcast progress:
    Total users: {total_count}
    Success: {success_count}/{total_count}  -  {round((success_count / total_count) * 100, 2)}%
    Failure: {fail_count}/{total_count}  -  {round((fail_count / total_count) * 100, 2)}%
    Sent to: {round(((i + batch_size) / total_count) * 100, 2)}%"""
            )

    end_time = time.time()  
    total_time = end_time - start_time

    bot.edit_message_text(
        chat_id=broadcast_msg.chat.id,
        message_id=broadcast_msg.message_id,
        text=f"""Broadcast finished:
    Total users: {total_count}
    Success: {success_count}/{total_count}  -  {round((success_count / total_count) * 100, 2)}%
    Failure: {fail_count}/{total_count}  -  {round((fail_count / total_count) * 100, 2)}%
    Sent to: 100%
    Total time: {round(total_time, 2)} seconds"""
    )

@bot.callback_query_handler(func=lambda call: call.data == "file")
def handle_file(call):
    try:
        with open('ids.txt', 'rb') as f: 
            bot.send_document(call.message.chat.id, f, caption="User file")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"An error occurred while sending the file: {e}")

    
    bot.polling(none_stop=True)

@bot.callback_query_handler(func=lambda call: call.data.startswith("add_admin"))
def add_admin(call):
    bot.send_message(call.message.chat.id, "Send the user ID you want to add as admin:")
    bot.register_next_step_handler(call.message, process_add_admin)

def process_add_admin(message):
    try:
        user_id = int(message.text)
        chat_id = message.chat.id  
        if user_id not in admins:
            admins.append(user_id)
            bot.send_message(chat_id, f"User {user_id} has been added as an admin.")
        else:
            bot.send_message(chat_id, "The user is already an admin.")
    except Exception as e:
        bot.send_message(chat_id, f"An error occurred while adding the admin: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith("remove_admin"))
def remove_admin(call):
    bot.send_message(call.message.chat.id, "Send the user ID you want to remove from admins:")
    bot.register_next_step_handler(call.message, process_remove_admin)

def process_remove_admin(message):
    try:
        user_id = int(message.text)
        if user_id in admins and user_id != owner:
            admins.remove(user_id)
            bot.send_message(message.chat.id, f"User {user_id} has been removed from admins.")
        else:
            bot.send_message(message.chat.id, "The user is not an admin or is the owner.")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred while removing the admin: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith("add_mandatory_sub"))
def add_mandatory_sub(call):
    bot.send_message(call.message.chat.id, "Send the channel username without @ to add it to mandatory subscriptions:")
    bot.register_next_step_handler(call.message, process_add_mandatory_sub)

def process_add_mandatory_sub(message):
    try:
        channel = message.text
        if channel not in mandatory_subscriptions:
            mandatory_subscriptions.append(channel)
            bot.send_message(message.chat.id, f"Channel {channel} has been added to the mandatory subscriptions list.")
        else:
            bot.send_message(message.chat.id, "The channel is already in the mandatory subscriptions list.")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred while adding the mandatory subscription: {e}")

@bot.callback_query_handler(func=lambda call: call.data.startswith("remove_mandatory_sub"))
def remove_mandatory_sub(call):
    bot.send_message(call.message.chat.id, "Send the channel username without @ to remove it from mandatory subscriptions:")
    bot.register_next_step_handler(call.message, process_remove_mandatory_sub)

def process_remove_mandatory_sub(message):
    try:
        channel = message.text
        if channel in mandatory_subscriptions:
            mandatory_subscriptions.remove(channel)
            bot.send_message(message.chat.id, f"Channel {channel} has been removed from the mandatory subscriptions list.")
        else:
            bot.send_message(message.chat.id, "The channel is not in the mandatory subscriptions list.")
    except Exception as e:
        bot.send_message(message.chat.id, f"An error occurred while removing the mandatory subscription: {e}")

@bot.callback_query_handler(func=lambda call: call.data == "show_admins")
def show_admins(call):
    admin_list = "\n".join([str(admin) for admin in admins])
    bot.send_message(call.message.chat.id, f"Admin list:\n{admin_list}")

@bot.callback_query_handler(func=lambda call: call.data == "show_users")
def show_users(call):
    user_list = "\n".join([str(user_id) for user_id in db])
    bot.send_message(call.message.chat.id, f"User list:\n{user_list}")

print("-- Bot Started...")
bot.polling(none_stop=True)

