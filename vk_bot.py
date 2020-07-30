import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
try:
    from group_token import token
except Exception as err:
    print('Ошибка токена')
    print(err)


group_id = 197388508


class Bot:
    def __init__(self):
        self.vk_session = vk_api.VkApi(token=token)
        self.long_poll = vk_api.bot_longpoll.VkBotLongPoll(vk=self.vk_session, group_id=group_id)
        self.vk_api = self.vk_session.get_api()

    def on_event(self):
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.WALL_POST_NEW:
                for user_id in self.vk_api.groups.getMembers(group_id=group_id)['items']:
                    self.vk_api.messages.send(user_id=user_id, random_id=get_random_id(), peer_id=group_id,
                                              message=event.object.text)
            else:
                print(f'Событие типа {event.type} еще не обрабатываются')


if __name__ == '__main__':
    bot = Bot()
    bot.on_event()

# TODO дописать проверку на администратора
# TODO Дописать обработчики ошибок