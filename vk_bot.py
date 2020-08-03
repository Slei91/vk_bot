import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
try:
    from group_token import token
except Exception as err:
    print('Ошибка токена')
    print(err)


GROUP_ID = 197388508


class Bot:
    def __init__(self):
        self.vk_session = vk_api.VkApi(token=token)
        self.long_poll = vk_api.bot_longpoll.VkBotLongPoll(vk=self.vk_session, group_id=GROUP_ID)
        self.vk_api = self.vk_session.get_api()

    def on_event(self):
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.WALL_POST_NEW and abs(event.object.from_id) == GROUP_ID:
                for user_id in self.vk_api.groups.getMembers(group_id=GROUP_ID, filter='friends')['items']:
                    self.vk_api.messages.send(user_id=user_id, random_id=get_random_id(), peer_id=GROUP_ID,
                                              message=event.object.text)
            else:
                print(f'Событие типа {event.type} еще не обрабатываются')


if __name__ == '__main__':
    bot = Bot()
    try:
        bot.on_event()
    except KeyboardInterrupt:
        print('Завершение работы бота')
    except Exception as error:
        print(f'Непредвиденная ошибка {error}')
