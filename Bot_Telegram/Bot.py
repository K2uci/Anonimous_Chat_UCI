from Config.Config import *
from Utils.Tools import *
from telebot.types import Message

# Funcion para darle un descanso al usuario
@bot.message_handler(commands=['descanso'])
def cmd_breack(message : Message):
    my_id = message.chat.id
    take_breack(my_id)
    info = 'Estas de descanso para volver presione /start'
    bot.send_message(my_id,info,parse_mode='html') 

# Funcion par abuscar un usuario libre
@bot.message_handler(commands=['buscar'])
def cmd_search(message : Message):
    my_id = message.chat.id
    if not search_by_id(my_id):
        info = '✅Te he emparejado con un usuario✅\nA partir de este mensaje todo lo que escribas se le enviara🔰'
        bot.send_message(my_id,info) 
    else:
        info = '❌No hay usuarios disponibles actualmente❌'
        bot.send_message(my_id,info) 

# Funcion inicial del bot
@bot.message_handler(commands=['start'])
def cmd_start(message : Message):
    info = '<b>👋¡Bienvenido a Anonimos Chat UCI!👋</b>'
    info += '\n\n🔥 Conéctate de forma anónima y atrevida. Explora nuevas relaciones y encuentra a esa persona'
    info += ' especial que hará latir tu corazón. 💖✨ ¡Atrévete!'
    info += '\n\nLos comandos de uso del bot son los siguientes: \n/buscar   <code>Para emparejar con otra persona</code>'
    info += '\n/descanso   <code>Elimina tu registro (no podras buscar ni ser buscado)</code>\n'
    bot.send_message(message.chat.id,info,parse_mode='html') 
    register(message.chat.id,message.chat.username)
    
# Función para enviar mensajes de entre usuarios
@bot.message_handler(content_types=['text'])
def handle_text(message: Message):
    id_user_recived = send_message_own(message.chat.id,message.text)
    if id_user_recived:
        bot.send_message(id_user_recived,message.text)
        # bot.send_message(MY_ID,message.text)

if __name__ == '__main__':
    bot.infinity_polling()