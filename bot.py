import telebot
from telebot import types
from telebot.types import Message
import requests
import dbfunctions

bot = telebot.TeleBot("699888211:AAHL7pSV19gGWL5WkxXucax1_FXdZq8z5qg")

@bot.message_handler(commands=["start"]) #initializes the start
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True)
    user_markup.row('Start again')
    user_markup.row('Check out')
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    callback_button = types.InlineKeyboardButton(text="Click to see our menu", callback_data="menu")
    keyboard.add(callback_button)
    bot.send_message(message.chat.id, 'Welcome!', reply_markup=user_markup)
    bot.send_message(message.chat.id, "Please choose an option below to continue.", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def query_text(call):
    if call.message:
        if call.data == "menu": #shows menu
                food_list = dbfunctions.show_menu()
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                for item in food_list:
                    keyboard = types.InlineKeyboardMarkup(row_width=2)
                    keyboard.add(types.InlineKeyboardButton(text= 'Add 1 to the cart', callback_data=str(item)))
                    bot.send_message(call.message.chat.id,item)
                    bot.send_photo(call.message.chat.id, dbfunctions.show_photo(item))
                    bot.send_message(call.message.chat.id,dbfunctions.show_descr(item))
                    bot.send_message(call.message.chat.id,'Price: ' + str(dbfunctions.show_price(item)) + 'eur',reply_markup=keyboard)

        elif call.data in dbfunctions.show_menu(): #adds items to the cart
            id = call.from_user.id
            price = dbfunctions.show_price(call.data)
            dbfunctions.addtocart(id, call.data,price)
            x = str(call.data) + '(1) added to the cart'
            bot.send_message(call.message.chat.id,x)

        elif call.data == 'location':
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(types.InlineKeyboardButton(text="Send as a text", callback_data='confirmed'))
            bot.send_message(call.message.chat.id, "Send us location where you would like us to deliver your order.", reply_markup=keyboard)
            dbfunctions.save_order(call.from_user.id, 'loc')


        elif call.data == 'confirmed':
            dbfunctions.save_order(call.from_user.id, 'Confirmed')
            bot.send_message(call.message.chat.id, "Thank you for your order!")
            dbfunctions.empty_cart(call.from_user.id)

@bot.message_handler(content_types=['location'])  #hadles location
def handle_location(message):
    if dbfunctions.show_status(message.from_user.id) == 'loc':
        bot.send_message(message.from_user.id, "Chosen location is saved. The order is on the way.")
        print (message.location)
        dbfunctions.location(message.from_user.id, str(message.location))
        dbfunctions.status('Confirmed', message.chat.id)


@bot.message_handler(commands=["checkout"]) #shows cart by user id, to be initialized by the command '/checkout'
def handle_checkout(message):
    dbfunctions.showcart(message.from_user.id)
    order = dbfunctions.showcart(message.from_user.id)
    bot.send_message(message.from_user.id, "Your order:")
    for item in order:
            bot.send_message(message.from_user.id, item[0])
    bot.send_message(message.from_user.id, "Your summary: " + str(dbfunctions.summary(message.from_user.id)) + ' eur')
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text='Send location and pay', callback_data='location'))
    bot.send_message(message.chat.id,'Would you like to finish your order?',reply_markup=keyboard)

@bot.message_handler(commands=["empty"]) #empties user's cart
def empty(message):
    dbfunctions.empty_cart(message.from_user.id)
    bot.send_message(message.from_user.id, "Your cart is empty now.")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text=="Check out": #empties cart
        dbfunctions.showcart(message.from_user.id)
        order = dbfunctions.showcart(message.from_user.id)
        bot.send_message(message.from_user.id, "Your order:")
        for item in order:
                bot.send_message(message.from_user.id, item[0])
        bot.send_message(message.from_user.id, "Your summary: " + str(dbfunctions.summary(message.from_user.id)) + ' eur')
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text='Send location and pay', callback_data='location'))
        bot.send_message(message.chat.id,'Would you like to finish your order?',reply_markup=keyboard)

    elif message.text=="Start again": #restarts user's interaction with bot
        handle_start(message)
        dbfunctions.delete_order(message.from_user.id)


if __name__ == '__main__':
    bot.polling(none_stop=True)
