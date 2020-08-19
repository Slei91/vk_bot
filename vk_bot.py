import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
try:
    from group_token import token
except ImportError as err:
    token = None
    print(f'Ошибка токена, токен = {token}')
    print(err)
try:
    from data_base import timetable
except ImportError as err:
    timetable = None
    print('Ошибка расписания')
    print(err)


GROUP_ID = 197388508

price_words_list = ['цена', 'стоимость']
timetable_words_list = ['расписание']


class Bot:
    def __init__(self):
        self.vk_session = vk_api.VkApi(token=token)
        self.long_poll = vk_api.bot_longpoll.VkBotLongPoll(vk=self.vk_session, group_id=GROUP_ID)
        self.vk_api = self.vk_session.get_api()
        self.managers_id_list = [item['id'] for item in
                                 self.vk_api.groups.getMembers(group_id=GROUP_ID, filter='managers')['items']]

    def on_event(self):
        for event in self.long_poll.listen():
            try:
                self.send_post_from_wall_to_members_ls(event=event)
                self.get_info_from_bot_in_messages(event=event)
            except Exception as err:
                print(err)

    def send_post_from_wall_to_members_ls(self, event):
        if event.type == VkBotEventType.WALL_POST_NEW and abs(event.object.from_id) == GROUP_ID:
            for user_id in set(self.vk_api.groups.getMembers(group_id=GROUP_ID)['items']) - set(self.managers_id_list):
                self.vk_api.messages.send(user_id=user_id,
                                          random_id=get_random_id(),
                                          peer_id=GROUP_ID,
                                          message=event.object.text)

    def get_info_from_bot_in_messages(self, event):
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.object.text.lower() in timetable_words_list:
                self.vk_api.messages.send(user_id=event.object.from_id,
                                          random_id=get_random_id(),
                                          peer_id=GROUP_ID,
                                          message=self.data_base_format_to_message())

            elif event.object.text.lower() in price_words_list:
                self.vk_api.messages.send(user_id=event.object.from_id,
                                          random_id=get_random_id(),
                                          peer_id=GROUP_ID,
                                          message='''
                                          Первое групповое занятие - бесплатно
                                          Цена за групповое занятие - 500 рублей
                                          Персональная тренировка - 1000 рублей
                                          ''')
            else:
                self.vk_api.messages.send(user_id=event.object.from_id,
                                          random_id=get_random_id(),
                                          peer_id=GROUP_ID,
                                          message='''
                                          Я вас не понимаю =(
                                          'Цена' - чтобы узнать стоимость занятия
                                          'Расписание' - чтобы узнать расписание тренировок
                                          ''')

    @staticmethod
    def data_base_format_to_message():
        result_answer = ''
        for key, value in timetable.items():
            result_answer += f'{key} : {value} \n'

        return result_answer


if __name__ == '__main__':
    bot = Bot()
    try:
        bot.on_event()
    except KeyboardInterrupt:
        print('Завершение работы бота')
    except Exception as error:
        print(f'Непредвиденная ошибка {error}')
