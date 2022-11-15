from jobs_criteria import *
from jobs_data import *
from items_from_telegram import *
import datetime

###################################
if __name__ == "__main__":
    jobs_criteria = JobsCriteria('andrei_jobs')
    # load prev jobs
    jobs_criteria.load_data()

    # get new jobs from telegram
    items_telegram = ItemsFromTelegram()

    today = datetime.datetime.date(datetime.datetime.now())
    yesterday = today - datetime.timedelta(days=1)

    items_telegram.run(
        jobs_criteria.get_profile()['telegram channels'],
        yesterday,
        jobs_criteria)

    # save collected jobs
    jobs_criteria.save_data()

    # save jobs for yesterday to file
    file_name = jobs_criteria.get_profile_name() + '_' + \
                datetime.datetime.strftime(yesterday, '%Y-%m-%d') + \
                '.csv'

    jobs_criteria.save_data_for_date_to_file(
        yesterday,
        file_name
    )

    # send yesterday jobs file to telegram group
    items_telegram.send_file_to_telegram(file_name, 1)
    jobs_criteria.delete_file_silently(file_name)

    items_telegram.client_stop()