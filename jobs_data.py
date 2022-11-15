import csv
import datetime
import os


class JobItem():

    def __init__(self) -> None:
        self.init_data()

    def init_data(self) -> None:
        self._date = datetime.datetime.date(datetime.datetime.strptime('2022-11-01', '%Y-%m-%d'))
        self._id = '0'
        self._sender_id = '0'
        self._text_lower = ''
        self._price = '0'
        self._url = ''
        self._email = ''
        self._sender_nickname = ''

    def get_item_dict(self) -> dict:
        """ return data dict for current object :
        {...data...} """

        return {
            'date': self._date,
            'id': self._id,
            'sender_id': self._sender_id,
            'text_lower': self._text_lower,
            'price': self._price,
            'url': self._url,
            'email': self._email,
            'sender_nickname': self._sender_nickname,
        }


class Jobs(JobItem):
    def __init__(self,
                 profile_name: str) -> None:
        super().__init__()
        self._delimiter = ','
        self._quotechar = '"'
        self._profile_name = profile_name
        self._data_file_name = profile_name + '_data.csv'
        self._jobs = {}  # { date: [ {}, ...{}]
        self._days_before_delete_a_job = 30

    def get_jobs(self):
        return self._jobs

    def get_delimiter(self):
        return self._delimiter

    def get_quotechar(self):
        return self._quotechar

    def get_profile_name(self):
        return self._profile_name

    def load_data(self) -> dict:
        self._jobs = {}
        try:
            with open(self._data_file_name, 'r') as csv_file:
                csv_dict_reader = csv.DictReader(csv_file,
                                                 delimiter=self._delimiter,
                                                 quotechar=self._quotechar)
                for row_dict in csv_dict_reader:
                    this_date = datetime.datetime.date(datetime.datetime.strptime(row_dict['date'], '%Y-%m-%d'))
                    row_dict.pop('date')
                    if this_date not in self._jobs.keys():
                        self._jobs[this_date] = []
                    self._jobs[this_date].append(row_dict)

        except Exception as e:
            print(e)

    def save_data(self) -> bool:
        try:
            data_file_name_tmp = self._data_file_name + '.tmp'
            self.delete_file_silently(data_file_name_tmp)

            with open(data_file_name_tmp, 'w') as csv_file:
                dict_writer = csv.DictWriter(csv_file,
                                             fieldnames=self.get_item_dict().keys(),
                                             delimiter=self._delimiter,
                                             quotechar=self._quotechar)
                dict_writer.writeheader()
                today_date = datetime.datetime.date(datetime.datetime.now())
                for this_date in self._jobs.keys():
                    if abs((today_date - this_date).days) < self._days_before_delete_a_job:
                        list_of_dicts = self._jobs[this_date]
                        for item_dict in list_of_dicts:
                            item_dict['date'] = this_date
                            dict_writer.writerow(item_dict)

            # remove old data file
            self.delete_file_silently(self._data_file_name)
            # rename tmp data file to current data file
            try:
                os.rename(data_file_name_tmp, self._data_file_name)
            except Exception as e:
                print(e)
                return False

        except Exception as e:
            print(e)
            return False
        return True

    def delete_file_silently(self,
                             file_name: str):
        try:
            os.remove(file_name)
        except Exception as e:
            print(e)

    def save_data_for_date_to_file(self,
                                   for_date,
                                   file_name: str) -> bool:

        self.delete_file_silently(file_name)
        try:
            with open(file_name, 'w') as csv_file:
                dict_writer = csv.DictWriter(csv_file,
                                             fieldnames=self.get_item_dict().keys(),
                                             delimiter=self.get_delimiter(),
                                             quotechar=self.get_quotechar())
                dict_writer.writeheader()
                for item_dict in self.get_jobs()[for_date]:
                    item_dict['date'] = for_date
                    dict_writer.writerow(item_dict)


        except Exception as e:
            print(e)
            return False
        return True

#########################
if __name__ == "__main__":
    jobs = Jobs('andrei_jobs')
    jobs.load_data()
    print(jobs._jobs)
    jobs.save_data()
