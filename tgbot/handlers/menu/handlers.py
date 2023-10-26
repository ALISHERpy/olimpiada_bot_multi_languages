from telegram import ParseMode, Update
from telegram.ext import CallbackContext
from tgbot.states import *
from tgbot.handlers.menu import keyboards as menu_keyboard
import re
from django.db.models import Q



from files.models import IMAGES, VIDEOS, TestFile, ChannelId
from users.models import User



from dtb.settings import ADMINS
ADMINS=str(ADMINS)
ADMINS=ADMINS.split(",")
import random



from django.utils import timezone
import datetime

from tgbot.static_text import desciption_of_OLM,uzbekcha,ruscha
def About_camp(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text=desciption_of_OLM)


def About_litsey(update: Update, context: CallbackContext) -> None:
    

    obj=VIDEOS.objects.all()
    for i in obj:
            
            if i.description:
                update.message.bot.send_video(chat_id=update.message.chat_id, video=i.file_id, caption=i.description)
            else:
                update.message.bot.send_video(chat_id=update.message.chat_id, video=i.file_id)

    update.message.reply_text(text="""🗺 Manzil:  Navoiy shahar G‘alaba shoh ko‘chasi 186-uy 
➡️ Mo'ljal: Yangi bozor yonginasida""")
    return CHOOSE

def Get_answers(update: Update, context: CallbackContext) -> None:

    msg = update.message.text
    # Regular expression pattern
    pattern = re.compile(r'^\d+\*[A-Za-z]+$')

    if pattern.match(msg):        
        msg=msg.split('*')
        update.message.reply_text(text=f"Tekshirib Chiqqaninggizga Ishonchingiz komilmi ?\nTest kodi: {msg[0]}\nJavobingiz: {msg[1]}",
        reply_markup=menu_keyboard.Answers_confirm(),)
        context.user_data['msg'] = update.message.text

    else:
        update.message.reply_text(text="Javoblaringiz namuna singari emas\nQayta tekshirib yuboring!")
    
    return WAITING_ANSWER  

def Checking_answers(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    context.bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)

    if query.data == "not_confirmed":
        context.bot.send_message(chat_id=query.message.chat_id,
                                 text="Tekshirib olib qayta yuboring !")
        return WAITING_ANSWER
    else:
        xabar = ''

        current_local_time = timezone.localtime(timezone.now())
        u = User.objects.get_or_none(user_id=query.message.chat_id)

        if current_local_time.time() > u.Expired_time:
            xabar = "🙁Sizning 2 soat vaqtinggiz o'z nihoyasiga yitganligi tufayli Test ko'rsatgichingiz Nol ga tenglashtirildi🗣"

            context.bot.send_message(chat_id=query.message.chat_id,
                                     text=xabar)
            context.bot.send_message(chat_id=query.message.chat_id,
                                     text="Bosh sahifa.", reply_markup=menu_keyboard.main_keys())
            u.Answer_rate = "\n💀Test vaqtiga ulgura olmagan !"
            u.save()


        else:

            context.bot.send_message(chat_id=query.message.chat_id,
                                     text="🔍Tekshirildi !")

            msg_answer = context.user_data['msg'].split('*')

            right_answer_qs = TestFile.objects.filter(Q(description__iregex=rf'\b{msg_answer[0]}\*'))
            right_answer_obj = right_answer_qs.first()

            if right_answer_obj:  # Check if the object exists
                right_answer_description = right_answer_obj.description
            else:
                right_answer_description = None
            if right_answer_description:
                right_answer = right_answer_description.split('*')

            #
            user_answers = str(msg_answer[1]).lower()
            correct_answers = str(right_answer[1]).lower()
            correct_count = 0
            incorrect_count = 0

            ###Uzunligini tekshirish
            if len(user_answers) != len(correct_answers):
                context.bot.send_message(chat_id=query.message.chat_id,
                                         text=f"Testlar soni {len(correct_answers)}ta edi,lekin siz {len(user_answers)}ta Javob yubordinnigz !\nTekshirib qayta yuboring !")
                return WAITING_ANSWER

            for user_answer, correct_answer in zip(user_answers, correct_answers):
                if user_answer == correct_answer:
                    correct_count += 1
                else:
                    incorrect_count += 1

            total_questions = len(correct_answers)

            # Calculate the user's score as a percentage
            user_percentage = (correct_count / total_questions) * 100
            xabar = (f"Ko'rsatgich: {user_percentage:.1f}%")
            xabar += (
                f"\n\n🔷Savollar soni: {total_questions} ta\n✅To'g'rilari soni: {correct_count} ta\n❌Xatolar soni: {incorrect_count} ta")
            #
            context.bot.send_message(chat_id=query.message.chat_id,
                                     text=xabar)
            context.bot.send_message(chat_id=query.message.chat_id,
                                     text='Test yakunlandi⌛️\nEtiboringiz uchun Rahmat❗️\nSiz bosh Sahifadasiz.',
                                     reply_markup=menu_keyboard.main_keys())

            xabar += (f"\nTest raqami: {right_answer[0]}\nJavobingiz: {msg_answer[1]}")

            User.objects.filter(user_id=query.message.chat_id).update(Answer_rate=xabar)

        # Adminga yuborish

        try:
            u = User.objects.get_or_none(user_id=query.message.chat_id)
            kanal_id=ChannelId.objects.get(id=99)
            msg = f"👤User Test ishladi🔻\n\nkim:{u.first_name} {u.last_name}\nUsername: @{u.username}\nTel 📱 +{u.phone_number}\nTugagan vaqt: 🕰 {u.Expired_time}\n\n"
            # print('-100' + kanal_id)
            kanal_id=int('100' + str(kanal_id.channel_id))

            context.bot.send_message(chat_id=-kanal_id,
                                     text=msg + xabar)

        except Exception as inst:
            pass


        return CHOOSE




def Prepare_testing(update: Update, context: CallbackContext) -> None:

    query = update.callback_query
    context.bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id) 
    u=User.objects.get(user_id=query.from_user.id)

#####
    
    if query.data=="get_back":
        query.answer("Bosh menyu")

        context.bot.send_message(chat_id=query.message.chat_id,
                                 text="Siz bosh menyudasiz!",reply_markup=menu_keyboard.main_keys())

        return CHOOSE

    elif query.data=="uz":
        query.answer("✅Uzbekcha")
        User.objects.filter(user_id=query.message.chat_id).update(language_code='uz')

    elif query.data=="ru":
        query.answer("✅Ruscha")
        User.objects.filter(user_id=query.message.chat_id).update(language_code='ru')
        

#####
    if u.Expired_time != None:
        context.bot.send_message(chat_id=query.message.chat_id,text=f"🔴Siz Avval Test ishlagansiz!\nNatijangiz•\n{u.Answer_rate}",reply_markup=menu_keyboard.main_keys())
        return CHOOSE
                  
    elif u.phone_number:
        context.bot.send_message(chat_id=query.message.chat_id,
                text="Demak sizga hozir test taqdim etamiz.\n⏰2 soat beriladi,shu vaqtda javoblarni yubormasanggiz,natijanggiz Nol ga tenglashtiriladi!",
                reply_markup=menu_keyboard.inline_keys_start())
        return BEFORE_START_test
    else:
        context.bot.send_message(chat_id=query.message.chat_id,text="🔻Siz Avval Ro'yxatdan o'tishinggiz kerak🔻" ,reply_markup=menu_keyboard.main_keys())
        return CHOOSE


   

def before_give_test(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text='🧐Qaysi tildagi test savollarini ishlamoqchisiz ? ',reply_markup=menu_keyboard.inline_language_keyboard())
    
    return CHECK_BEFORE_TEST
def Give_test(update: Update, context: CallbackContext) -> None:
    
    query = update.callback_query
    context.bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    if query.data=="get_back":
        query.answer("Bosh menyu")

        context.bot.send_message(chat_id=query.message.chat_id,
                                 text="Siz bosh menyudasiz!",reply_markup=menu_keyboard.main_keys())

        return CHOOSE

    else:

        usercha=User.objects.get(user_id=query.from_user.id)        
        # print(usercha.language_code) ishladi

        selected_images = list(TestFile.objects.filter(language_code=usercha.language_code))
        

        if len(selected_images) >= 1:
            random_images = random.sample(selected_images, 1)
            for test_doc in random_images:
                file_id = test_doc.file_id
                if test_doc.description:
                    text = str(test_doc.description)
                    parts = text.split('*')

                    context.bot.send_document(chat_id=query.message.chat_id, document=file_id, caption=f"‼️ESLAB QOLING ‼️\nSizning Testinggiz🔢kodi: {parts[0]}")
                    context.bot.send_message(chat_id=query.message.chat_id, text=f"2 soat ichida javoblarini Namunadagidek yuborishingiz kerak\n(Namuna: {parts[0]}*AABDBBABCBCDBBB)")

                    current_local_time = timezone.localtime(timezone.now())
                    at_expired=current_local_time + datetime.timedelta(hours=2)

                    User.objects.filter(user_id=query.message.chat_id).update(
                    Expired_time=at_expired)


                    at_expired = at_expired.strftime('%Y-%m-%d %H:%M')
                    context.bot.send_message(chat_id=query.message.chat_id, text=f"⏳sizning vaqting {at_expired} da tugaydi !")
                    return WAITING_ANSWER

        else:
            context.bot.send_message(chat_id=query.message.chat_id, text="Not enough File available.")

        return CHOOSE




# def some_videos(update: Update, context: CallbackContext) -> None:
#     obj=VIDEOS.objects.all()
#     for i in obj:
#             file_id = i.link

#             if i.description:
#                 update.message.bot.send_video(chat_id=update.message.chat_id, video=file_id, caption=i.description)
#             else:
#                 update.message.bot.send_video(chat_id=update.message.chat_id, video=file_id)

#     return CHOOSE



# def some_videos(update: Update, context: CallbackContext) -> None:
#     selected_videos = list(VIDEOS.objects.all())
#     random.shuffle(selected_videos)  # Shuffle the order of videos
    
#     if len(selected_videos) >= 1:
#         random_videos = selected_videos[:1]  # Select the first 3 videos from the shuffled list
#         for video in random_videos:
#             file_id = video.file_id
#             if video.description:
#                 update.message.bot.send_video(chat_id=update.message.chat_id, video=file_id, caption=video.description)
#             else:
#                 update.message.bot.send_video(chat_id=update.message.chat_id, video=file_id)
#     else:
#         update.message.bot.send_message(chat_id=update.message.chat_id, text="Not enough videos available.")

#     return CHOOSE


     


def video_handler(update, context):
    message = update.message
    u = User.get_user(update, context)

    file_id = message.video.file_id

    if u.is_admin:
        if message.caption:
            caption = message.caption
            vv = VIDEOS(file_id=file_id,description=caption)
            
        else:
            vv = VIDEOS(file_id=file_id)
        
        vv.save()
        update.message.reply_text(text="Saved !")

    return CHOOSE


def files_handler(update, context):
    message = update.message
    u = User.get_user(update, context)

    file_id = message.document.file_id

    if u.is_admin:
        if message.caption:

            caption = message.caption.split('*')
            test_tili=caption[2]
            caption =caption[0]+"*"+caption[1]

            vv = TestFile(file_id=file_id,description=caption,language_code=test_tili)
            vv.save()   
            update.message.reply_text(text="Saved !")

        else:
            update.message.reply_text(text="Document file tagida(description) javoblarini yozib qoldirishinggiz kerak !")
            update.message.reply_text(text="Not Saved !")

    return CHOOSE




#     return CHOOSE
def change_channel_id(update, context):
    """ Show help info about all secret admins commands """
    u = User.get_user(update, context)
    message = update.message.text.split(" ")
    # print(message)
    if u.is_admin:
        the_id=ChannelId.objects.get(id=99)
        the_id.channel_id=message[1]
        the_id.save()
        update.message.reply_text(f"{message[1]} ga O'zgardi !\n ")
        # update.message.reply_text(text="Saved !")

    return CHOOSE

def Registeration(update: Update, context: CallbackContext) -> None:
    u = User.objects.get(user_id=update.message.chat_id)
    if update.message.text=="/refresh_reg":        
        update.message.bot.send_message(chat_id=update.message.chat_id, text="♻️Siz eski Ma'lumotlaringizni yangilamoqdasiz.\nTo'liq Isminggizni kiriting...\n(namuna:Alisher Axmadov)")
        return GET_Full_name
    
    if u.phone_number:
        update.message.reply_text(f"⚠️Siz Avval Malumotlarni to'ldirgansiz:\nIsm: {u.first_name}\nfam: {u.last_name}\nphone num: {u.phone_number}\n\nYangilashni istasanggiz /refresh_reg ni bosing!")
        return CHOOSE
    else:
        update.message.bot.send_message(chat_id=update.message.chat_id, text="🛃To'liq Isminggizni kiriting...\n(namuna:Alisher Axmadov)")
        return GET_Full_name


def Name_Handler(update, context):
    full_name = update.message.text.strip() 
    name_parts = full_name.split()
    if len(name_parts) == 2:
        first_name = name_parts[0]
        last_name = ' '.join(name_parts[1:]) 
        
        context.user_data['FIRST_NAME'] = first_name
        context.user_data['LAST_NAME'] = last_name
        
        update.message.reply_text(text=f"{full_name} Saqlandi !\n📞Bog'lanish uchun telefon raqamingizni yozing..\n(namuna: 998903332211)")
        
        return GET_numer
    else:
        update.message.reply_text("Xato! Ism va familiyangizni to'liq kiriting (namuna: Alisher Axmadov).")
        return GET_Full_name



def Phone_number_handler(update, context):
    
    message_text = update.message.text

    if re.match(r"^\d{12}$", message_text):
        context.user_data["NUMBER"] = message_text
        update.message.reply_text(f"☎️ +{message_text} Saqlandi !\n✔️Ro'yxatdan o'tish yakunlandi.\nSiz bosh menyudasiz!", 
                              reply_markup=menu_keyboard.main_keys())

        User.objects.filter(user_id=update.message.chat_id).update(
        phone_number=context.user_data["NUMBER"],
        first_name=context.user_data['FIRST_NAME'],
        last_name=context.user_data['LAST_NAME']
    ) 
    else:
        update.message.reply_text("Xato!\nQaytadan uruning,Telefon raqamni to'g'ri kiriting \n(12 ta raqam,masalan: 998903332211).")
        return GET_numer
    return CHOOSE

# CHOOSE is the state to proceed to after a valid phone number is entered.

