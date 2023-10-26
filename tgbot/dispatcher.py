"""
    Telegram event handlers
"""
from telegram.ext import (
    Dispatcher, Filters,
    CommandHandler, MessageHandler,
    CallbackQueryHandler,
)

from dtb.settings import DEBUG
from tgbot.handlers.broadcast_message.manage_data import CONFIRM_TEST,CONFIRM_DECLINE_BROADCAST
from tgbot.handlers.broadcast_message.static_text import broadcast_command
from tgbot.handlers.onboarding.manage_data import SECRET_LEVEL_BUTTON

from tgbot.handlers.utils import files, error
from tgbot.handlers.admin import handlers as admin_handlers
from tgbot.handlers.location import handlers as location_handlers
from tgbot.handlers.onboarding import handlers as onboarding_handlers
from tgbot.handlers.broadcast_message import handlers as broadcast_handlers
from tgbot.main import bot


from tgbot.states import *
from tgbot import static_text as menu_text
from tgbot.handlers.menu import handlers as menu_handlers
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)




        # Grant permission to the user with the given user_id
        # You can store the granted permission in a database or other storage



def setup_dispatcher(dp):
    """
    Adding handlers for events from Telegram
    """
    # onboarding
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", onboarding_handlers.command_start)],
        states={
            CHOOSE: [
                CommandHandler("start", onboarding_handlers.command_start),
                CommandHandler("admin", admin_handlers.admin),
                CommandHandler("stats", admin_handlers.stats),
                CommandHandler("change_id", menu_handlers.change_channel_id),
                CommandHandler('export_users', admin_handlers.export_users),
                CommandHandler('refresh_reg', menu_handlers.Registeration),


                MessageHandler(Filters.regex(f"^{menu_text.About_comp}$"),  menu_handlers.About_camp),
                # MessageHandler(Filters.regex(f"^{menu_text.test_ber}$"),  menu_handlers.Prepare_testing),
                MessageHandler(Filters.regex(f"^{menu_text.test_ber}$"),  menu_handlers.before_give_test),
                MessageHandler(Filters.regex(f"^{menu_text.Litsey}$"),  menu_handlers.About_litsey),
                MessageHandler(Filters.regex(f"^{menu_text.Register_users}$"),  menu_handlers.Registeration),

                # MessageHandler(Filters.photo,   menu_handlers.image_handler),
                MessageHandler(Filters.video,   menu_handlers.video_handler),
                MessageHandler(Filters.document, menu_handlers.files_handler),

            ],

            BEFORE_START_test: [               
                CallbackQueryHandler(menu_handlers.Give_test),
                                
            ],


            CHECK_BEFORE_TEST: [               
                CallbackQueryHandler(menu_handlers.Prepare_testing),
                                
            ],
            WAITING_ANSWER: [  
            MessageHandler(Filters.text, menu_handlers.Get_answers),
            CallbackQueryHandler(menu_handlers.Checking_answers),                               
            ],

            GET_Full_name: [
                MessageHandler(Filters.text,  menu_handlers.Name_Handler),
                                
            ],  
            GET_numer: [
                MessageHandler(Filters.text,  menu_handlers.Phone_number_handler),                                
            ],  
            
        },
        fallbacks=[MessageHandler(Filters.text & ~Filters.command, onboarding_handlers.command_start)],
    )

    dp.add_handler(conv_handler)
    

    # dp.add_handler(CommandHandler("start", onboarding_handlers.command_start))

    # admin commands
    

    # # location
    # dp.add_handler(CommandHandler("ask_location", location_handlers.ask_for_location))
    # dp.add_handler(MessageHandler(Filters.location, location_handlers.location_handler))

    # secret level
    dp.add_handler(CallbackQueryHandler(onboarding_handlers.secret_level, pattern=f"^{SECRET_LEVEL_BUTTON}"))

    # broadcast message
    # SEND massages for USERs

    dp.add_handler(
        MessageHandler(Filters.regex(rf'^{broadcast_command}(/s)?.*'), broadcast_handlers.broadcast_command_with_message)
    )
    

    dp.add_handler(
        CallbackQueryHandler(broadcast_handlers.broadcast_decision_handler, pattern=f"^{CONFIRM_DECLINE_BROADCAST}")
    )




    # files
    dp.add_handler(MessageHandler(
        Filters.animation, files.show_file_id,
    ))

    # handling errors
    dp.add_error_handler(error.send_stacktrace_to_tg_chat)

    # EXAMPLES FOR HANDLERS
    # dp.add_handler(MessageHandler(Filters.text, <function_handler>))
    # dp.add_handler(MessageHandler(
    #     Filters.document, <function_handler>,
    # ))
    # dp.add_handler(CallbackQueryHandler(<function_handler>, pattern="^r\d+_\d+"))
    # dp.add_handler(MessageHandler(
    #     Filters.chat(chat_id=int(TELEGRAM_FILESTORAGE_ID)),
    #     # & Filters.forwarded & (Filters.photo | Filters.video | Filters.animation),
    #     <function_handler>,
    # ))

    return dp


n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True))
