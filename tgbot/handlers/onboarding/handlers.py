import datetime

from django.utils import timezone
from telegram import ParseMode, Update
from telegram.ext import (
    ConversationHandler,
    CallbackContext,
)
from tgbot.handlers.onboarding import static_text
from tgbot.handlers.utils.info import extract_user_data_from_update
from users.models import User
from tgbot.handlers.onboarding.keyboards import make_keyboard_for_start_command

NAME, SURNAME, PHOTO, VIDEO, VOICE, DOCUMENT, LOCATION, CONTACT = range(8)

def command_start(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)

    if created:
        text = static_text.start_created.format(first_name=u.first_name)
    else:
        text = static_text.start_not_created.format(first_name=u.first_name)

    update.message.reply_text(text=text,
                              reply_markup=make_keyboard_for_start_command())


def secret_level(update: Update, context: CallbackContext) -> None:
    # callback_data: SECRET_LEVEL_BUTTON variable from manage_data.py
    """ Pressed 'secret_level_button_text' after /start command"""
    user_id = extract_user_data_from_update(update)['user_id']
    text = static_text.unlock_secret_room.format(
        user_count=User.objects.count(),
        active_24=User.objects.filter(updated_at__gte=timezone.now() - datetime.timedelta(hours=24)).count()
    )

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML
    )


def registration(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(text="Send your name please")

    return NAME

def user_name(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    context.user_data["name"] = text
    update.message.reply_text(text="Send your lastname please")

    return CONTACT
    
def user_surname(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    context.user_data["surname"] = text
    update.message.reply_text(text="Send your photo please")

    return PHOTO

def user_photo(update: Update, context: CallbackContext) -> None:
    image = update.message.photo[-1]
    context.user_data["photo"] = image.file_id

    update.message.reply_photo(photo=image.file_id, caption="I gotcha!\nSend your video please")

    return  VIDEO

def user_video(update: Update, context: CallbackContext) -> None:
    video = update.message.video
    context.user_data["video"] = video.file_id

    update.message.reply_video(video=video, caption="I gotcha!\nSend your voice pleace")

    return VOICE

def user_voice(update: Update, context: CallbackContext) -> None:
    voice = update.message.voice
    context.user_data["voice"] = voice.file_id

    update.message.reply_voice(voice=context.user_data["voice"], caption="I gotcha!\nSend your document please")

    return DOCUMENT

def user_document(update: Update, context: CallbackContext) -> None:
    document = update.message.document
    context.user_data["document"] = document.file_id

    update.message.reply_document(document=document, caption="I gotcha!\nSend your location please")


    return LOCATION

def user_location(update: Update, context: CallbackContext) -> None:
    location = update.message.location
    context.user_data["location"] = {
        "latitude": location.latitude,
        "longitude": location.longitude,
    }
    
    update.message.reply_location(location=location)
    update.message.reply_text(text="I gotcha!\nSend your contact please")

    return CONTACT

def user_contact(update: Update, context: CallbackContext) -> None:
    contact = update.message.contact
    context.user_data["contact"] = contact.phone_number

    update.message.reply_contact(contact=contact)
    update.message.reply_text(text="Well done. You are registered!!!")

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> None:
    pass

"""             user detail end             """