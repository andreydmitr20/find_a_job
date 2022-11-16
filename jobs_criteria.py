from jobs_data import *
import json
import os


class JobsCriteria(Jobs):
    def __init__(self,
                 profile_name: str):
        super().__init__(profile_name)
        self._profile_file_name = self.get_profile_name() + '.json'
        self._profile = None
        self.load_profile()

    def set_profile(self, profile):
        self._profile

    def get_profile(self):
        return self._profile

    def get_profile_file_name(self):
        return self._profile_file_name

    def load_profile(self) -> bool:
        try:
            with open(self._profile_file_name, 'r') as json_file:
                self._profile = json.loads(json_file.read())
                return True
        except Exception as e:
            print(e)
            return False

    def save_profile(self):
        try:
            with open(self._profile_file_name, 'w') as json_file:
                json_file.write(json.dumps(self._profile, ensure_ascii=False))
                return True
        except Exception as e:
            print(e)
            return False

    @staticmethod
    def find_any_keyword(text: str, key_list: list) -> bool:
        for key in key_list:
            if text.find(key) >= 0:
                print('\nDROPPED ---------------->',key,':',text)
                return True
        return False

    def criteria_function(self,
                          text: str):
        if len(text) < self._profile['min text length'] or \
                self.find_any_keyword(text, self._profile['stop phrases']):
            return False
        return True


def initial_profile_save(jobs_criteria: JobsCriteria):
    os.remove(jobs_criteria.get_profile_file_name())
    jobs_criteria.set_profile({
        'profile name': jobs_criteria.get_profile_name(),
        'min text length': 100,
        'stop phrases': [
            "middle", "senior", "lead ",
            "1+", "2+", "3+", "years of experience",
            "node", "nest", "#frontend", "#react",
            "с#", "c#", "#сишарп", "ios",
            "украина",
            '#дизайн', "#лектор",
            '#ищу', '# ищу',
            '1с', '1c', "cбер", "сбер", "wildberries", "ozon", "яндекс",
            "# office", "moscow", "москва", "#гибридный_график",
            'c1', 'с1',  # english
            "грумер", "менеджер по продажам", "менеджер в отдел", "личный помощник", "ассистент",
            "помощник", "менеджер по работе", "копирайтер", "педикюр",
            "расширение ассортимента", "телеоператор",
        ],

        'telegram channels': [
            "@qa_jobs",
            "@it_vacancyN1",
            "@theyseeku",
            "@jobGeeks",
            "@javadevjob",
            "@forallqa",
            "@jobforjunior",
            "@qaload_job",
            "@montework",

        ],

    })
    jobs_criteria.save_profile()


###################################
if __name__ == "__main__":
    jobs_criteria = JobsCriteria('andrei_jobs')

    # initial_profile_save(jobs_criteria)
    # quit()

    jobs_criteria.load_data()
    jobs_criteria.save_data()
