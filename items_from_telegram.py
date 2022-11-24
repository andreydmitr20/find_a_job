import csv
import requests
from find_a_job import *
from telethon import TelegramClient, events
import datetime


class ItemsFromTelegram():
    def __init__(self):
        self.__credentials = self.load_credentials('private_info.json')
        self.__client = None

    def client_start(self):
        if self.get_client() is None:
            self.set_client(
                TelegramClient(
                    'session',
                    int(self.__credentials['api_id']),
                    self.__credentials['api_hash'],
                ))
            self.get_client().start(phone=self.__credentials['phone'])

    def client_stop(self):
        if self.get_client() is None:
            return
        try:
            self.get_client().disconnect()
        finally:
            self.set_client(None)

    def get_client(self):
        return self.__client

    def set_client(self,
                   client):
        self.__client = client

    def load_credentials(self,
                         file_name: str) -> dict:
        try:
            with open(file_name, 'r') as json_file:
                return json.loads(json_file.read())
        except Exception as e:
            print(e)
            return {}

    def read_msgs_from_channel_for_date(self,
                                        this_channel: str,
                                        this_date,
                                        jobs_criteria: JobsCriteria):
        # get msg_id fo tomorrow date
        try:
            msg = self.get_client().iter_messages(this_channel,
                                                  limit=1,
                                                  reverse=True,
                                                  offset_date=this_date + datetime.timedelta(days=1)).__next__()
            this_max_id = msg.id
        except:
            # no msgs
            this_max_id = 0
        print(f'^^^^^^^^^^^^^^Channel: {this_channel}')
        try:
            for msg in self.get_client().iter_messages(this_channel,
                                                       max_id=this_max_id,
                                                       reverse=True,
                                                       offset_date=this_date):
                if isinstance(msg.sender_id, int) and isinstance(msg.text, str):
                    text = msg.text # .replace('\n',' ')

                    if (jobs_criteria is None):
                        print((str(msg), str(msg.sender_id), text[50]))
                    elif jobs_criteria.criteria_function(text.lower()):
                        if self.store_item(jobs_criteria, this_date, msg, text):
                            print('\nACCEPTED >>>>>>>>>>>>>>>>>>>>',str(msg.id), str(msg.sender_id), text)
        except Exception as e:
            print(e)
            print(f'!!! Wrong channel {this_channel}')
    def store_item(self,
                   jobs_criteria: JobsCriteria,
                   this_date,
                   message,
                   text: str) -> bool:
        if jobs_criteria is None:
            return True
        jobs = jobs_criteria.get_jobs()
        if this_date not in jobs.keys():
            jobs[this_date] = []
        # check if found same msg
        for item_dict in jobs[this_date]:
            if item_dict['id'] == str(message.id) and \
                    item_dict['sender_id'] == str(message.sender_id):
                # skip
                return False
        jobs[this_date].append({
            'id': str(message.id),
            'sender_id': str(message.sender_id),
            'text_lower': text,
            'price': '0',
            'url': '',
            'email': '',
            'sender_nickname': '',
        })
        return True

    def run(self,
            channels: list,
            this_date,
            jobs_criteria: JobsCriteria):
        self.client_start()

        print(this_date, ':')
        for this_channel in channels:
            self.read_msgs_from_channel_for_date(this_channel,
                                                 this_date,
                                                 jobs_criteria)
        self.client_stop()

    # send file
    def send_file_to_telegram(self,
                              file_name: str,
                              do_send=False) -> None:
        if not do_send:
            return
        try:

            with open(file_name, 'r') as file:
                url = f"https://api.telegram.org/bot{self.__credentials['bot_token']}/sendDocument"
                # print(
                requests.post(url, data={'chat_id': self.__credentials['group_id']}, files={'document': file})
                # )
        except Exception as e:
            print(e)
            print('Can\'t send file to Telegram.')

        # send to telegram

    def send_message_to_telegram(self,
                                 message: str,
                                 do_send=False) -> None:
        if not do_send:
            return
        try:

            url = f"https://api.telegram.org/bot{self.__credentials['bot_token']}/sendMessage?chat_id={self.__credentials['group_id']}&text={message}"
            # print(
            requests.get(url).json()
            # )
        except Exception as e:
            print(e)
            print('Can\t send message to Telegram.')


####################
if __name__ == "__main__":
    items_telegram = ItemsFromTelegram()
    items_telegram.send_message_to_telegram('test', 1)
    quit()
    items_telegram.run([
        "@qa_jobs",
        "@it_vacancyN1",
    ], None)
