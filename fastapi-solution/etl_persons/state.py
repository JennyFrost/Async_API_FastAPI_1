import os
import json
import datetime


class State:
    def __init__(self, file_path):
        self.file_path = file_path

    def _create_state(self):
        default_state = {
            "last_request": datetime.datetime.now().timestamp(),
            "first_request_bool": False
        }
        with open(self.file_path, 'w') as file_state:
            json.dump(default_state, file_state, indent=4)

    def _save_state(self, data):
        with open(self.file_path, 'w') as file_state:
            json.dump(data, file_state, indent=4)

    def check_exists(self):
        if not os.path.exists(self.file_path):
            self._create_state()

    def read_state(self):
        with open(self.file_path, 'r') as file_state:
            state = json.load(file_state)
        return state

    def update_state(self, data):
        state = self.read_state()
        state.update(data)
        self._save_state(state)

    def get_datetime_last_request(self):
        state = self.read_state()
        date = state.get('last_request')
        date = datetime.datetime.utcfromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
        return date

    def update_datetime_last_request(self):
        date = datetime.datetime.now().timestamp()
        self.update_state({'last_request': date})

    def add_last_id_person(self, last_id):
        self.update_state({'last_id_person': last_id})

    def get_last_id_person(self):
        state = self.read_state()
        last_id_person = state.get('last_id_person', None)
        if last_id_person is not None:
            last_id_person = [[last_id_person]]
        return last_id_person
