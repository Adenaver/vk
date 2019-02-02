import vk_api
import os
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from flask import Flask, request
import random
import psycopg2
server = Flask(__name__)
hostname = os.environ.get('hosting')
username = os.environ.get('user')
password = os.environ.get('password')
database = os.environ.get('bdname')
tok=os.environ.get('vk_token')
keyboard = VkKeyboard(one_time=True)
keyboard.add_button('Мой профиль', color=VkKeyboardColor.PRIMARY)
def main():

    vk_session = vk_api.VkApi(token=tok)

    longpoll = VkBotLongPoll(vk_session, '168490072')
    vk = vk_session.get_api()
    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            print('Новое сообщение:')

            print('Для меня от: ', end='')

            print(event.obj.from_id)

            print('Текст:', event.obj.text)
            print()
            response = vk.users.get(user_id=event.obj.from_id)
            print(response[0]['first_name'])
            firstName=response[0]['first_name']
            lastName=response[0]['last_name']
            ms_key=random.randint(1,99999999)
            con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
            cur = con.cursor()
            full_link="https://vk.com/id"+str(event.obj.from_id)
            cur.execute("SELECT * FROM users WHERE vk = %s",(full_link,))
            bd_data=cur.fetchone()
            if event.obj.text=="/start":
                if bd_data[10]=="null" or bd_data[10]=="false":
                    keyboard.add_button('Подписаться на рассылку новостей', color=VkKeyboardColor.POSITIVE)
                elif bd_data[10]=="true":
                    keyboard.add_button('Отказаться от рассылки', color=VkKeyboardColor.NEGATIVE)
                vk.messages.send(
                    user_id=event.obj.from_id,
                    random_id=ms_key,
                    message="Вы можете получить информацию о своем пользователе. Нажав на кнопку 'Мой профиль'",
                    keyboard=keyboard.get_keyboard()
                )
                con.close()
            elif event.obj.text=="Подписаться на рассылку новостей":
                keyboard1.add_button('Мой профиль', color=VkKeyboardColor.PRIMARY)
                keyboard1.add_button('Отказаться от рассылки', color=VkKeyboardColor.NEGATIVE)
                con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
                cur = con.cursor()
                full_link="https://vk.com/id"+str(event.obj.from_id)
                cur.execute("UPDATE users SET status = true WHERE vk = %s",(id,))
                vk.messages.send(
                    user_id=event.obj.from_id,
                    random_id=ms_key,
                    message="Вы успешно подписались на рассылку новостей. В любой момент вы можете от неё отказатся нажав на кнопку 'Отказаться от рассылки'",
                    keyboard=keyboard1.get_keyboard()
                )

            elif event.obj.text=="Отказаться от рассылки":
                keyboard2.add_button('Мой профиль', color=VkKeyboardColor.PRIMARY)
                keyboard2.add_button('Подписаться на рассылку новостей', color=VkKeyboardColor.POSITIVE)
                con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
                cur = con.cursor()
                full_link="https://vk.com/id"+str(event.obj.from_id)
                cur.execute("UPDATE users SET status = false WHERE vk = %s",(id,))
                vk.messages.send(
                    user_id=event.obj.from_id,
                    random_id=ms_key,
                    message="Вы успешно отказались от рассылки новостей. В любой момент вы можете от неё отказатся нажав на кнопку 'Отказаться от рассылки'",
                    keyboard=keyboard2.get_keyboard()
                )
                #invoice_message(event.obj.from_id,event.obj.text,firstName,lastName)
            elif event.obj.text=="Мой профиль":
                try:
                    con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
                    cur = con.cursor()
                    full_link="https://vk.com/id"+str(event.obj.from_id)
                    print(full_link)
                    cur.execute("SELECT * FROM users WHERE vk = %s",(full_link,))
                    bd_data=cur.fetchone()
                    vk.messages.send(
                        user_id=event.obj.from_id,
                        random_id=ms_key,
                        message="Профиль\nИмя: "+str(bd_data[1])+"\nSTEAMID: "+str(bd_data[0])+"\nСтатус: "+str(bd_data[5])+"\n\nДоступные ПС: "+str(bd_data[7])+"\nДоступные звания: "+str(bd_data[8])+"\nТалон: "+str(bd_data[9]),
                        keyboard=keyboard.get_keyboard()
                    )
                    con.close()
                except Exception as e:
                    vk.messages.send(
                        user_id=event.obj.from_id,
                        random_id=ms_key,
                        message="Информации по вашему аккаунту нет.\nВозможно вы не подали анкету на участие в проекте. Или же ваш аккаунт ещё не добавили в базу.",
                        keyboard=keyboard.get_keyboard()
                    )
            else:
                con.close()
        elif event.type == VkBotEventType.MESSAGE_REPLY:
            print('Новое сообщение:')

            print('От меня для: ', end='')

            print(event.obj.peer_id)

            print('Текст:', event.obj.text)
            print()

        elif event.type == VkBotEventType.MESSAGE_TYPING_STATE:
            print('Печатает ', end='')

            print(event.obj.from_id, end=' ')

            print('для ', end='')

            print(event.obj.to_id)
            print()

        elif event.type == VkBotEventType.GROUP_JOIN:
            print(event.obj.user_id, end=' ')

            print('Вступил в группу!')
            print()

        elif event.type == VkBotEventType.GROUP_LEAVE:
            print(event.obj.user_id, end=' ')

            print('Покинул группу!')
            print()

        else:
            print(event.type)
            print()
@server.route("/alive")
def webhook():
    main()
@server.route("/")
def webhook():
    return "!", 200
if __name__ == '__main__':
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
main()
