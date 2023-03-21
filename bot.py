# pip install python-telegram-bot v13
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from secret import bot_token
import matplotlib.pyplot as plt

data = {}

#update contiene l'informazione che deriva dal chatbot
#context contiene l'informazione di contesto su di chi è il cellulare che ha mandato il messaggio
def welcome(update, context):
    msg = '''Welcome in <b>My Es2 Bot</b>'''

def process_chat(update, context):
    print(context)
    msg= update.message.text.lower()
    if msg.startswith('newdata'):
        cmd, city, valore = msg.split(' ')
        if city in data:
            data[city].append(float(valore))
        else:
            data[city] = [float(valore)]
        update.message.reply_text("dati ricevuti", parse_mode='HTML')
    elif msg.startswith('getdata'):
        cmd, city = msg.split(' ')
        plt.bar(range(len(data[city])), data[city])
        plt.savefig(city+'.png')
        chat_id = update.message.chat.id
        context.bot.send_document(chat_id=chat_id, document=open(city+'.png', 'rb'))
    else:
        welcome(update, context)

def process_location(update, context):
    # in telegram si può condividere la posizione puntuale o per un periodo di tempo.
    # a seconda del tipo di condivisione fatta arrivano dei messaggi diversi che si possono gestire entrambi
    if update.edited_message:
        message = update.edited_message
    else:
        message = update.message

    user_location = message.location

    user = message.from_user
    print(user)
    print(f"You talk with user {user['first_name']} and his user ID: {user['id']}")

    msg = f'Ti trovi presso lat={user_location.latitude}&lon={user_location.longitude}'
    print(msg)
    message.reply_text(msg)

def photo_handler(update, context):
    file = context.bot.getFile(update.message.photo[-1].file_id)
    file.download('photo.jpg') #salva il file che arriva dalla chat e lo chiama 'photo.jpg'
    update.message.reply_text('photo received')

def main():
   print('bot started....')
   upd= Updater(bot_token, use_context=True)
   disp=upd.dispatcher

   disp.add_handler(CommandHandler("start", welcome))
   disp.add_handler(MessageHandler(Filters.regex('^.*$'), process_chat))
   disp.add_handler(MessageHandler(Filters.location, process_location))
   disp.add_handler(MessageHandler(Filters.photo, photo_handler))


   upd.start_polling()
   upd.idle()



if __name__=='__main__':
   main()