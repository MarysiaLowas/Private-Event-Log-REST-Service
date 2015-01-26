from datetime import datetime
from calendar import timegm
import unittest

from flask import Flask, json

from eventhandler import EventHandler
import eventsfeed


class EventHandlerTestCase(unittest.TestCase):

    def __init__(self, methodName):
        unittest.TestCase.__init__(self, methodName)
        self.feed_with_all = "What a fantastic day #update @john"
        self.feed_with_defaults = "It's empty"
        self.sample_events = [
            {
                'id': 11,
                'text': "Will the slicing work? #poll @all-friends",
                'category': "poll",
                'person': "all-friends",
                'time': 1421604201
            },
            {
                'id': 10,
                'text': "It's almost Monday #update @all-friends",
                'category': "update",
                'person': "all-friends",
                'time': 1421604141
            },
            {
                'id': 9,
                'text': "Sunday night maybe better #update @john",
                'category': "update",
                'person': "john",
                'time': 1421604081
            },
            {
                'id': 8,
                'text': "The air is really bad today #warn @john",
                'category': "warn",
                'person': "john",
                'time': 1421603961
            },
            {
                'id': 7,
                'text': "Why so serious? #poll @all",
                'category': "poll",
                'person': "all",
                'time': 1421603901
            },
            {
                'id': 6,
                'text': "What do you think? #poll @all-friends",
                'category': "poll",
                'person': "all-friends",
                'time': 1421603841
            },
            {
                'id': 5,
                'text': "This can be empty",
                'category': "update",
                'person': "all",
                'time': 1421603781
            },
            {
                'id': 4,
                'text': "The forth message #warn @john",
                'category': "warn",
                'person': "john",
                'time': 1421603721
            },
            {
                'id': 2,
                'text': "It's fantastic!",
                'category': "warn",
                'person': "john",
                'time': 1421603661
            },
            {
                'id': 1,
                'text': "I just won a lottery #update @all",
                'category': "update",
                'person': "all",
                'time': 1421513660
            },
            {
                'id': 3,
                'text': "It should be at the beginning but time is a strange "
                        "animal #update @all-friends",
                'category': "update",
                'person': "all-friends",
                'time': 1420912461
            }
        ]

    def setUp(self):
        events = []
        self.my_service = EventHandler(events)

    def test_get_last_with_empty_list(self):
        results = self.my_service.get_last_ten()
        self.assertEqual(results, [])

    def test_get_last_by_field_empty(self):
        results = self.my_service.get_last_by_field('category', 'value')
        self.assertEqual(results, [])

    def test_add_event_parse_no_defaults(self):
        results = self.my_service.add_event(self.feed_with_all)
        # make_time truncates milliseconds
        # risky if we are on a break of a second
        time = self.my_service.make_time()
        expected = {
            'id': 1,
            'text': 'What a fantastic day #update @john',
            'category': 'update',
            'person': 'john',
            'time': time
        }
        self.assertDictEqual(results, expected)

    def test_add_event_parse_with_defaults(self):
        results = self.my_service.add_event(self.feed_with_defaults)
        # make_time truncates milliseconds
        # risky if we are on a break of a second
        time = self.my_service.make_time()
        expected = {
            'id': 1,
            'text': "It's empty",
            'category': 'update',
            'person': 'all',
            'time': time
        }
        self.assertDictEqual(results, expected)

    def test_add_event_append_list(self):
        results = self.my_service.add_event(self.feed_with_all)
        self.assertListEqual(self.my_service.event_list, [results])

    def test_get_last_with_nine_events(self):
        self.my_service.event_list = self.sample_events[0:9]
        results = self.my_service.get_last_ten()
        self.assertEqual(len(results), 9)
        self.assertListEqual(results, self.sample_events[0:9])

    def test_get_last_with_eleven_events(self):
        self.my_service.event_list = self.sample_events
        results = self.my_service.get_last_ten()
        self.assertEqual(len(results), 10)
        self.assertListEqual(results, self.sample_events[0:10])

    def test_get_last_by_field_category_below_ten(self):
        self.my_service.event_list = self.sample_events
        results = self.my_service.get_last_by_field('category', 'update')
        expected = [self.sample_events[1], self.sample_events[2],
                    self.sample_events[6], self.sample_events[9],
                    self.sample_events[10]]
        self.assertEqual(len(results), 5)
        self.assertListEqual(results, expected)

    def test_get_last_by_field_category_above_ten(self):
        self.my_service.event_list = self.sample_events
        for i in range(0, 6):
            self.my_service.add_event(self.feed_with_all)
        results = self.my_service.get_last_by_field('category', 'update')
        expected = self.my_service.event_list[0:6] + [self.sample_events[1],
                                                      self.sample_events[2],
                                                      self.sample_events[6],
                                                      self.sample_events[9]]
        self.assertEqual(len(results), 10)
        self.assertListEqual(results, expected)

    def test_get_last_by_field_person_below_ten(self):
        self.my_service.event_list = self.sample_events
        results = self.my_service.get_last_by_field('person', 'all-friends')
        expected = [self.sample_events[0], self.sample_events[1],
                    self.sample_events[5], self.sample_events[10]]
        self.assertEqual(len(results), 4)
        self.assertListEqual(results, expected)

    def test_get_last_by_field_person_above_ten(self):
        self.my_service.event_list = self.sample_events
        for i in range(0, 7):
            self.my_service.add_event(self.feed_with_all)
        results = self.my_service.get_last_by_field('person', 'john')
        expected = self.my_service.event_list[0:7] + [self.sample_events[2],
                                                      self.sample_events[3],
                                                      self.sample_events[7]]
        self.assertEqual(len(results), 10)
        self.assertListEqual(results, expected)

    def test_get_last_by_field_time_below_ten(self):
        self.my_service.event_list = self.sample_events
        results = self.my_service.get_last_by_field('time', 1421604081)
        self.assertEqual(len(results), 9)
        self.assertListEqual(results, self.sample_events[2:])

    def test_get_last_by_field_time_above_ten(self):
        self.my_service.event_list = self.sample_events
        results = self.my_service.get_last_by_field('time', 1421604201)
        self.assertEqual(len(results), 10)
        self.assertListEqual(results, self.sample_events[0:10])


class EventsFeedTestCaseEmptyList(unittest.TestCase):

    def __init__(self, methodName):
        unittest.TestCase.__init__(self, methodName)
        self.feed_with_all = "What a fantastic day #update @john"

    def setUp(self):
        eventsfeed.my_service.event_list = []
        self.app = eventsfeed.app.test_client()

    @staticmethod
    def make_time():
        # the method truncates milliseconds
        # to fit nicely in the URL
        time = datetime.utcnow()
        time = timegm(time.timetuple())
        return time

    def test_get_last_ten_empty_list(self):
        results = self.app.get('/feeds/api/v1.0/events')
        self.assertEqual(results.data, "No events yet")

    def test_get_last_by_field_empty_list(self):
        results = self.app.get('/feeds/api/v1.0/events/category/warn')
        self.assertEqual(results.data, "No events yet")

    def test_add_event(self):
        results = self.app.post('/feeds/api/v1.0/events',
                                data=self.feed_with_all)
        time = self.make_time()
        expected = {
            'id': 1,
            'text': 'What a fantastic day #update @john',
            'category': 'update',
            'person': 'john',
            'time': time
        }
        self.assertEqual(results.status, '201 CREATED')
        self.assertDictEqual(json.loads(results.data), {"event": expected})


class EventsFeedTestCaseFullList(unittest.TestCase):

    def __init__(self, methodName):
        unittest.TestCase.__init__(self, methodName)
        self.sample_events = [
            {
                'id': 17,
                'text': 'What a fantastic day #update @john',
                'category': 'update',
                'person': 'john',
                'time': 1421607501
            },
            {
                'id': 16,
                'text': 'What a fantastic day #update @john',
                'category': 'update',
                'person': 'john',
                'time': 1421606501
            },
            {
                'id': 15,
                'text': 'What a fantastic day #update @john',
                'category': 'update',
                'person': 'john',
                'time': 1421606401
            },
            {
                'id': 14,
                'text': 'What a fantastic day #update @john',
                'category': 'update',
                'person': 'john',
                'time': 1421605401
            },
            {
                'id': 13,
                'text': 'What a fantastic day #update @john',
                'category': 'update',
                'person': 'john',
                'time': 1421605301
            },
            {
                'id': 12,
                'text': 'What a fantastic day #update @john',
                'category': 'update',
                'person': 'john',
                'time': 1421604301
            },
            {
                'id': 11,
                'text': "Will the slicing work? #poll @all-friends",
                'category': "poll",
                'person': "all-friends",
                'time': 1421604201
            },
            {
                'id': 10,
                'text': "It's almost Monday #update @all-friends",
                'category': "update",
                'person': "all-friends",
                'time': 1421604141
            },
            {
                'id': 9,
                'text': "Sunday night maybe better #update @john",
                'category': "update",
                'person': "john",
                'time': 1421604081
            },
            {
                'id': 8,
                'text': "The air is really bad today #warn @john",
                'category': "warn",
                'person': "john",
                'time': 1421603961
            },
            {
                'id': 7,
                'text': "Why so serious? #poll @all",
                'category': "poll",
                'person': "all",
                'time': 1421603901
            },
            {
                'id': 6,
                'text': "What do you think? #poll @all-friends",
                'category': "poll",
                'person': "all-friends",
                'time': 1421603841
            },
            {
                'id': 5,
                'text': "This can be empty",
                'category': "update",
                'person': "all",
                'time': 1421603781
            },
            {
                'id': 4,
                'text': "The forth message #warn @john",
                'category': "warn",
                'person': "john",
                'time': 1421603721
            },
            {
                'id': 2,
                'text': "It's fantastic!",
                'category': "warn",
                'person': "john",
                'time': 1421603661
            },
            {
                'id': 1,
                'text': "I just won a lottery #update @all",
                'category': "update",
                'person': "all",
                'time': 1421513660
            },
            {
                'id': 3,
                'text': "It should be at the beginning but time is a strange "
                        "animal #update @all-friends",
                'category': "update",
                'person': "all-friends",
                'time': 1420912461
            }
        ]

    def setUp(self):
        eventsfeed.my_service.event_list = self.sample_events
        self.app = eventsfeed.app.test_client()

    def test_get_last_ten_full_list(self):
        results = self.app.get('/feeds/api/v1.0/events')
        self.assertDictEqual(json.loads(results.data), {
            "events": self.sample_events[0:10]
        })

    def test_get_last_ten_by_time_full_list(self):
        results = self.app.get('/feeds/api/v1.0/events/time/1421606501')
        self.assertDictEqual(json.loads(results.data), {
            "events": self.sample_events[1:11]
        })

    def test_get_last_ten_by_category_full_list(self):
        results = self.app.get('/feeds/api/v1.0/events/category/update')
        expected = self.sample_events[0:6] + [self.sample_events[7],
                                              self.sample_events[8],
                                              self.sample_events[12],
                                              self.sample_events[15]]
        self.assertDictEqual(json.loads(results.data), {"events": expected})

    def test_get_last_ten_by_person_full_list(self):
        results = self.app.get('/feeds/api/v1.0/events/person/john')
        expected = self.sample_events[0:6] + [self.sample_events[8],
                                              self.sample_events[9],
                                              self.sample_events[13],
                                              self.sample_events[14]]
        self.assertDictEqual(json.loads(results.data), {"events": expected})


if __name__ == '__main__':
    unittest.main()
