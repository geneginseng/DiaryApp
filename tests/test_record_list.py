import unittest
from DiaryRecords import RecordList, Record


class TestAddRecord(unittest.TestCase):
    def test_add_record(self):
        lst = RecordList()
        lst.add_record('record2', 'text', 6, 'pain', '2023-09-21')
        self.assertEqual(len(lst.Records), 1)
        record = lst.Records[0]
        self.assertEqual(record.title, "record2")
        self.assertEqual(record.text, "text")
        self.assertEqual(record.mood, 6)
        self.assertEqual(record.symptoms, 'pain')
        self.assertEqual(record.date, '2023-09-21')

    def test_add_record_wrong_data_type_of_argument(self):
        lst = RecordList()
        lst.add_record('record3', 'text', '6', 'pain', '2023-09-21')
        self.assertEqual(len(lst.Records), 1)
        record = lst.Records[0]
        self.assertEqual(record.title, "record3")
        self.assertEqual(record.text, "text")
        self.assertEqual(record.mood, '6')
        self.assertEqual(record.symptoms, 'pain')
        self.assertEqual(record.date, '2023-09-21')


class TestRemoveRecord(unittest.TestCase):
    def test_remove_record_in_list(self):
        lst = RecordList()
        lst.add_record('record', 'text', 6, 'pain', '2023-09-21')
        record = lst.Records[0]
        lst.remove_record(record)
        self.assertNotIn(record, lst.Records, 'The entry was not removed')

    def test_remove_record_not_in_list(self):
        lst = RecordList()
        record = Record(1, 'record4', 'text', 6, 'pain', '2023-09-21')
        try:
            lst.remove_record(record)
        except ValueError:
            self.fail('The ValueError was raised')


class TestAddSubscriber(unittest.TestCase):
    def test_add_subscriber(self):
        lst = RecordList()
        obj = lambda: 'Add me to the list of subscribers!'
        lst.add_subscriber(obj)
        self.assertIn(obj, lst.subscribers, "The subscriber isn't in the list!")


class TestRemoveSubscriber(unittest.TestCase):
    def test_remove_subscriber(self):
        lst = RecordList()
        obj = lambda: 'Add me to the list of subscribers!'
        lst.add_subscriber(obj)
        lst.remove_subscriber(obj)
        self.assertNotIn(obj, lst.subscribers, "The subscriber is in the list!")


class TestNotifySubscribers(unittest.TestCase):
    def test_notify_subscribers(self):
        lst = RecordList()
        count = 0

        def foo(num):
            nonlocal count
            count += num

        lst.add_subscriber(lambda: foo(1))
        lst.notify_subscribers()
        self.assertEqual(count, 1, "Subscribers were notified!")


class TestGetRecords(unittest.TestCase):
    def test_get_records(self):
        lst = RecordList()
        lst.add_record('record', 'text', 6, 'pain', '2023-09-21')
        lst.add_record('record2', 'text', 6, 'pain', '2023-09-21')
        records = lst.get_records()
        self.assertEqual(records, lst.Records)


class TestGetRecordsBetweenDates(unittest.TestCase):
    def test_get_records_between_dates(self):
        lst = RecordList()
        record1 = ('record1', 'text', 6, 'pain', '2023-09-21')
        record2 = ('record2', 'text', 6, 'pain', '2023-09-22')
        record3 = ('record3', 'text', 6, 'pain', '2023-09-23')
        record4 = ('record4', 'text', 6, 'pain', '2023-09-24')
        lst.add_record(*record1)
        lst.add_record(*record2)
        lst.add_record(*record3)
        lst.add_record(*record4)
        records = lst.get_records_between_dates('2023-09-22', '2023-09-24')
        l = len(records)
        self.assertEqual(l, 3)
        self.assertNotEqual(records[0].date, '2023-09-21')
        self.assertNotEqual(records[1].date, '2023-09-21')
        self.assertNotEqual(records[2].date, '2023-09-21')




if __name__ == '__main__':
    unittest.main()