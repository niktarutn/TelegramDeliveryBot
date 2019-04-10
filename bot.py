import telebot
from telebot import types
from telebot.types import Message
import requests
import restaurants

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
    rest_list =  restaurants.show_rests()
    if call.message:
        if call.data == "rst": #shows list of restaurants
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                for rest in rest_list:
                    keyboard.add(types.InlineKeyboardButton(text=str(rest), callback_data=str(rest)))
                bot.send_message(call.message.chat.id,"Step 1: choose the restaurant!",reply_markup=keyboard)

        elif call.data == "menu": #shows menu
                food_list = restaurants.show_menu()
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                for item in food_list:
                    keyboard = types.InlineKeyboardMarkup(row_width=2)
                    keyboard.add(types.InlineKeyboardButton(text= 'Add 1 to the cart', callback_data=str(item)))
                    bot.send_message(call.message.chat.id,item)
                    bot.send_photo(call.message.chat.id, restaurants.show_photo(item))
                    bot.send_message(call.message.chat.id,restaurants.show_descr(item))
                    bot.send_message(call.message.chat.id,'Price: ' + str(restaurants.show_price(item)) + 'eur',reply_markup=keyboard)

        elif call.data in restaurants.show_menu(): #adds items to the cart
            id = call.from_user.id
            price = restaurants.show_price(call.data)
            restaurants.addtocart(id, call.data,price)
            x = str(call.data) + '(1) added to the cart'
            bot.send_message(call.message.chat.id,x)

        elif call.data == 'pay':
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(types.InlineKeyboardButton(text="Confirm and pay", callback_data='confirmed'))
            bot.send_message(call.message.chat.id, "Click to pay and confirm the order", reply_markup=keyboard)

        elif call.data == 'confirmed':
            restaurants.save_order(call.from_user.id, 'Confirmed')
            bot.send_message(call.message.chat.id, "Thank you for your order!")
            restaurants.empty_cart(call.from_user.id)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    bot.send_message(message.from_user.id, "Chosen location is saved. The order is on the way.")



@bot.message_handler(commands=["checkout"]) #shows cart by user id
def handle_checkout(message):
    restaurants.showcart(message.from_user.id)
    order = restaurants.showcart(message.from_user.id)
    bot.send_message(message.from_user.id, "Your order:")
    for item in order:
            bot.send_message(message.from_user.id, item[0])
    bot.send_message(message.from_user.id, "Your summary: " + str(restaurants.summary(message.from_user.id)) + ' eur')
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton(text='Proceed to checkout', callback_data='pay'))
    bot.send_message(message.chat.id,'Would you like to finish your order?',reply_markup=keyboard)

@bot.message_handler(commands=["empty"]) #empties user's cart
def empty(message):
    restaurants.empty_cart(message.from_user.id)
    bot.send_message(message.from_user.id, "Your cart is empty now.")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text=="Check out":
        restaurants.showcart(message.from_user.id)
        order = restaurants.showcart(message.from_user.id)
        bot.send_message(message.from_user.id, "Your order:")
        for item in order:
                bot.send_message(message.from_user.id, item[0])
        bot.send_message(message.from_user.id, "Your summary: " + str(restaurants.summary(message.from_user.id)) + ' eur')
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(types.InlineKeyboardButton(text='Proceed to checkout', callback_data='pay'))
        bot.send_message(message.chat.id,'Would you like to finish your order?',reply_markup=keyboard)

    elif message.text=="Start again":
        handle_start(message)


if __name__ == '__main__':
    bot.polling(none_stop=True)
