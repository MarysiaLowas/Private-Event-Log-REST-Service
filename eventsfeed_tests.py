import unittest

from event_handler import EventHandler


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
                'text': "It should be at the beginning but time is a strange animal #update @all-friends",
                'category': "update",
                'person': "all-friends",
                'time': 1420912461
            }
        ]

    def setUp(self):
        events = []
        self.myService = EventHandler(events)

    def test_get_last_with_empty_list(self):
        results = self.myService.get_last_ten()
        self.assertEquals(results, [])

    def test_add_event_parse_no_defaults(self):
        results = self.myService.add_event(self.feed_with_all)
        # make_time truncates milliseconds
        # risky if we are on a break of a second
        time = self.myService.make_time()
        expected = {
            'id': 1,
            'text': 'What a fantastic day #update @john',
            'category': 'update',
            'person': 'john',
            'time': time
        }
        self.assertDictEqual(results, expected)

    def test_add_event_parse_with_defaults(self):
        results = self.myService.add_event(self.feed_with_defaults)
        # make_time truncates milliseconds
        # risky if we are on a break of a second
        time = self.myService.make_time()
        expected = {
            'id': 1,
            'text': "It's empty",
            'category': 'update',
            'person': 'all',
            'time': time
        }
        self.assertDictEqual(results, expected)

    def test_add_event_append_list(self):
        results = self.myService.add_event(self.feed_with_all)
        self.assertListEqual(self.myService.event_list, [results])

    def test_get_last_with_nine_events(self):
        self.myService.event_list = self.sample_events[0:9]
        results = self.myService.get_last_ten()
        self.assertEqual(len(results), 9)
        self.assertListEqual(results, self.sample_events[0:9])

    def test_get_last_with_eleven_events(self):
        self.myService.event_list = self.sample_events
        results = self.myService.get_last_ten()
        self.assertEqual(len(results), 10)
        self.assertListEqual(results, self.sample_events[0:10])

    def test_get_last_by_field_category_below_ten(self):
        self.myService.event_list = self.sample_events
        results = self.myService.get_last_by_field('category', 'update')
        expected = [self.sample_events[1], self.sample_events[2], self.sample_events[6], self.sample_events[9],
                    self.sample_events[10]]
        self.assertEqual(len(results), 5)
        self.assertListEqual(results, expected)

    def test_get_last_by_field_category_above_ten(self):
        self.myService.event_list = self.sample_events
        for i in range(0, 6):
            self.myService.add_event(self.feed_with_all)
            i += 1
        results = self.myService.get_last_by_field('category', 'update')
        expected = self.myService.event_list[0:6] + [self.sample_events[1], self.sample_events[2],
                   self.sample_events[6], self.sample_events[9]]
        self.assertEqual(len(results), 10)
        self.assertListEqual(results, expected)

    def test_get_last_by_field_person_below_ten(self):
        self.myService.event_list = self.sample_events
        results = self.myService.get_last_by_field('person', 'all-friends')
        expected = [self.sample_events[0], self.sample_events[1], self.sample_events[5], self.sample_events[10]]
        self.assertEqual(len(results), 4)
        self.assertListEqual(results, expected)

    def test_get_last_by_field_person_above_ten(self):
        self.myService.event_list = self.sample_events
        for i in range(0, 7):
            self.myService.add_event(self.feed_with_all)
            i += 1
        results = self.myService.get_last_by_field('person', 'john')
        expected = self.myService.event_list[0:7] + [self.sample_events[2], self.sample_events[3],
                   self.sample_events[7]]
        self.assertEqual(len(results), 10)
        self.assertListEqual(results, expected)

    def test_get_last_by_field_time_below_ten(self):
        self.myService.event_list = self.sample_events
        results = self.myService.get_last_by_field('time', 1421604081)
        self.assertEqual(len(results), 9)
        self.assertListEqual(results, self.sample_events[2:])

    def test_get_last_by_field_time_above_ten(self):
        self.myService.event_list = self.sample_events
        results = self.myService.get_last_by_field('time', 1421604201)
        self.assertEqual(len(results), 10)
        self.assertListEqual(results, self.sample_events[0:10])


if __name__ == '__main__':
    unittest.main()

