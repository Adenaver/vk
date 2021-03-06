import vk_api
import os
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import psycopg2
hostname = os.environ.get('hosting')
username = os.environ.get('user')
password = os.environ.get('password')
database = os.environ.get('bdname')
tok=os.environ.get('vk_token')
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
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button('Мой профиль', color=VkKeyboardColor.PRIMARY)
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
                keyboard1 = VkKeyboard(one_time=True)
                keyboard1.add_button('Мой профиль', color=VkKeyboardColor.PRIMARY)
                keyboard1.add_button('Отказаться от рассылки', color=VkKeyboardColor.NEGATIVE)
                con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
                cur = con.cursor()
                full_link="https://vk.com/id"+str(event.obj.from_id)
                cur.execute("UPDATE users SET mailing = true WHERE vk = %s",(full_link,))
                con.commit()
                con.close()
                vk.messages.send(
                    user_id=event.obj.from_id,
                    random_id=ms_key,
                    message="Вы успешно подписались на рассылку новостей. В любой момент вы можете от неё отказатся нажав на кнопку 'Отказаться от рассылки'",
                    keyboard=keyboard1.get_keyboard()
                )

            elif event.obj.text=="Отказаться от рассылки":
                keyboard2 = VkKeyboard(one_time=True)
                keyboard2.add_button('Мой профиль', color=VkKeyboardColor.PRIMARY)
                keyboard2.add_button('Подписаться на рассылку новостей', color=VkKeyboardColor.POSITIVE)
                con = psycopg2.connect( host=hostname, user=username, password=password, dbname=database )
                cur = con.cursor()
                full_link="https://vk.com/id"+str(event.obj.from_id)
                cur.execute("UPDATE users SET mailing = false WHERE vk = %s",(full_link,))
                con.commit()
                con.close()
                vk.messages.send(
                    user_id=event.obj.from_id,
                    random_id=ms_key,
                    message="Вы успешно отказались от рассылки новостей. В любой момент вы можете подписаться на рассылку нажав на кнопку 'Подписаться на рассылку новостей'",
                    keyboard=keyboard2.get_keyboard()
                )
                #invoice_message(event.obj.from_id,event.obj.text,firstName,lastName)
            elif event.obj.text=="Мой профиль":
                try:
                    if bd_data[10]=="null" or bd_data[10]=="false":
                        keyboard.add_button('Подписаться на рассылку новостей', color=VkKeyboardColor.POSITIVE)
                    elif bd_data[10]=="true":
                        keyboard.add_button('Отказаться от рассылки', color=VkKeyboardColor.NEGATIVE)
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
if __name__ == '__main__':
    main()
