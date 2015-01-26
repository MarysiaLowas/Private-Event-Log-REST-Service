from datetime import datetime
from calendar import timegm
from operator import itemgetter


class EventHandler(object):

    def __init__(self, event_list):
        self.event_list = self.sort_events(event_list)

    @staticmethod
    def sort_events(list_to_sort):
        sorted_list = sorted(list_to_sort, key=itemgetter('time'),
                             reverse=True)
        return sorted_list

    @staticmethod
    def parse_string(text):
        words_list = text.split()
        # defaults
        person = "all"
        category = "update"
        for i in words_list:
            if i.startswith("#"):
                category = i.strip("#")
            elif i.startswith("@"):
                person = i.strip("@")
        return category, person

    @staticmethod
    def make_time():
        # the method truncates milliseconds
        # to fit nicely in the URL
        time = datetime.utcnow()
        time = timegm(time.timetuple())
        return time

    def find_element_by_id(self, element_id):
        for i in self.event_list:
            if i['id'] == element_id:
                return i
        return None

    def select_events(self, field=None, value=None, count=10):
        selected_list = []
        if field is None:
            return self.event_list[0:count]
        elif field == "time":
            value = int(value)
            for i in self.event_list:
                if i[field] <= value:
                    selected_list.append(i)
                if len(selected_list) == count:
                    break
        else:
            for i in self.event_list:
                if i[field] == value:
                    selected_list.append(i)
                if len(selected_list) == count:
                    break
        return selected_list

    def get_all_events(self):
        return self.event_list

    def get_last_ten(self):
        return self.select_events()

    def get_last_by_field(self, event_field, event_value):
        return self.select_events(event_field, event_value)

    def add_event(self, feed):
        category, person = self.parse_string(feed)
        time = self.make_time()
        event = {
            'id': len(self.event_list) + 1,
            'text': feed,
            'category': category,
            'person': person,
            'time': time
        }
        self.event_list.append(event)
        self.event_list = self.sort_events(self.event_list)
        return event

    def get_event_by_id(self, event_id):
        event = self.find_element_by_id(event_id)
        return event
