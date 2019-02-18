import telebot
from telebot import types
from telebot.types import Message
import requests
import restaurants

bot = telebot.TeleBot("699888211:AAHL7pSV19gGWL5WkxXucax1_FXdZq8z5qg")

chosen_rest = ""

@bot.message_handler(commands=["start"])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row('Start again')
    user_markup.row('Check out')
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    callback_button = types.InlineKeyboardButton(text="Restaurants", callback_data="rst")
    switch_button = types.InlineKeyboardButton(text="Hot Deals", callback_data="hd")
    keyboard.add(callback_button, switch_button)
    bot.send_message(message.chat.id, 'Welcome!', reply_markup=user_markup)
    bot.send_message(message.chat.id, "Please choose an option below to continue.", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def query_text(call):
    rest_list =  restaurants.show_rests()
    if call.message:
        if call.data == "rst": #shows list of restaurants
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                for rest in rest_list:
                    keyboard.add(types.InlineKeyboardButton(text=str(rest), callback_data=str(rest)))
                bot.send_message(call.message.chat.id,"Choose the restaurant!",reply_markup=keyboard)

        elif call.data in rest_list: #shows menu
                global chosen_rest
                chosen_rest = call.data
                food_list = restaurants.show_menu(chosen_rest)
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                for item in food_list:
                    keyboard = types.InlineKeyboardMarkup(row_width=2)
                    keyboard.add(types.InlineKeyboardButton(text='Add to Cart', callback_data=str(item)))
                    bot.send_message(call.message.chat.id,item)
                    bot.send_message(call.message.chat.id,restaurants.show_descr(chosen_rest,item),reply_markup=keyboard)

        elif call.data in restaurants.show_menu(chosen_rest): #adds items to the cart
            id = call.from_user.id
            restaurants.addtocart(id, call.data)
            x = str(call.data) + '(1) added to the cart'
            bot.send_message(call.message.chat.id,x)

        elif call.data == 'pay':
            pass

@bot.message_handler(content_types=['location'])
def handle_location(message):
    

@bot.message_handler(commands=["checkout"]) #shows cart by user id
def handle_start(message):
    print(message.from_user.id)
    order = restaurants.showcart(message.from_user.id)
    bot.send_message(message.from_user.id, "Your order:")
    for item in order:
            bot.send_message(message.from_user.id, item[0])
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text='Confirm and pay', callback_data='pay'))
    bot.send_message(call.message.chat.id,'Would you like to finish your order?',reply_markup=keyboard)


@bot.message_handler(commands=["empty"]) #empties user's cart
def handle_start(message):
    restaurants.empty_cart(message.from_user.id)
    bot.send_message(message.from_user.id, "Your cart is empty now.")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text=="Check out":
        order = restaurants.showcart(message.from_user.id)
        bot.send_message(message.from_user.id, "Your order:")
        for item in order:
                bot.send_message(message.from_user.id, item[0])
    elif message.text=="Start again":
        handle_start(message)


if __name__ == '__main__':
    bot.polling(none_stop=True)
