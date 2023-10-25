import sqlite3
from datetime import datetime
from statistics import mean


# create Record class with record's attributes
class Record:
    def __init__(self, record_id: int, title: str, text: str, mood: int, symptoms: str, date: str):
        self.title = title
        self.text = text
        self.mood = mood
        self.symptoms = symptoms
        self.date = date
        self.record_id = record_id


# create RecordList class for storing records in a Python list object
class RecordList:
    def __init__(self):
        super().__init__()
        self.Records = []
        # implement observer pattern here by creating a list of subscribers
        self.subscribers = []

    def add_record(self, title, text, mood: int, symptoms, date):
        """in add_record() method a new instance of the Record class is created
        and added to Python list object for storing"""
        if len(self.Records) > 0:
            new_id = max([self.Records[x].record_id for x in range(len(self.Records))]) + 1
        else:
            new_id = 1
        record = Record(new_id, title, text, mood, symptoms, date)
        self.Records.append(record)
        self.notify_subscribers()

    def remove_record(self, record: Record):
        """remove_record() method is called to remove an instance of the Record class passed into it
        from the Python list object, and then notify all subscribers in the list of subscribers about it"""
        self.Records.remove(record)
        self.notify_subscribers()

    def add_subscriber(self, callback):
        self.subscribers.append(callback)

    def remove_subscriber(self, callback):
        self.subscribers.remove(callback)

    def notify_subscribers(self):
        """notify_subscribers() method is called by remove_record() method
        and notify all subscribers in the list of subscribers about deleting a record"""
        for callback in self.subscribers:
            callback()

    def get_records(self):
        """get_records() return all records, stored in the Python list object"""
        return self.Records

    def get_records_between_dates(self, start_date, end_date):
        """get_records_between_dates() method returns a list of records,
        where every record date is between dates, that user specified
        in date selection view"""
        records = []
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
        for record in self.Records:
            record_date_obj = datetime.strptime(record.date, '%Y-%m-%d')
            if (start_date_obj <= record_date_obj) and (record_date_obj <= end_date_obj):
                records.append(record)
        return records


# create RecordList class for storing records in a database file
class RecordListDB(RecordList):
    def __init__(self, database_path: str):
        super().__init__()
        # a database file path must be specified when creating an instance of the class RecordListDB
        # to create a database file in the current directory, if it doesn't exist,
        # and to be able to connect to the database
        self.database_path = database_path
        # create a new database, if it doesn't exist, and open a database connection
        db = sqlite3.connect(self.database_path)
        # create a database cursor to be able to execute SQL statements and fetch results from SQL queries
        cur = db.cursor()
        # create database table with title, text, mood, symptoms and date columns
        cur.execute('CREATE TABLE IF NOT EXISTS entries(title TEXT, text TEXT, mood INT, symptoms TEXT, date TEXT)')
        # implement observer pattern here by creating a list of subscribers
        db.commit()
        db.close()
        self.subscribers = []

    def add_record(self, title, text, mood, symptoms, date):
        """add_record() method connects to the database and inserts new row into it,
        using user input passed into the method, and then notifies all subscribers in the list of subscribers,
        that list of records is changed"""
        db = sqlite3.connect(self.database_path)
        cur = db.cursor()
        cur.execute('INSERT INTO entries VALUES(?, ?, ?, ?, ?)', (title, text, mood, symptoms, date))
        db.commit()
        db.close()
        self.notify_subscribers()

    def remove_record(self, record: Record):
        """remove_record() method gets an id of the instance of Record class, passed into it,
        and deletes corresponding row in the database table,
        and then notifies all subscribers in the list of subscribers, that list of records is changed"""
        db = sqlite3.connect(self.database_path)
        cur = db.cursor()
        cur.execute('DELETE FROM entries WHERE rowid = ?', (record.record_id,))
        db.commit()
        db.close()
        self.notify_subscribers()

    def add_subscriber(self, callback):
        self.subscribers.append(callback)

    def remove_subscriber(self, callback):
        if callback in self.subscribers:
            self.subscribers.remove(callback)

    def notify_subscribers(self):
        """notify_subscribers() notifies all subscribers in the list of subscribers, when specific event is happened"""
        for callback in self.subscribers:
            callback()

    def get_records(self):
        """get_records() method connects to the database, gets all data from it,
        creates instances of Record class using the data from database,
        and return list of these instances"""
        records = []
        db = sqlite3.connect(self.database_path)
        cur = db.cursor()
        res = cur.execute('SELECT rowid, * FROM entries')
        for row in res:
            record = Record(row[0], row[1], row[2], row[3], row[4], row[5])
            records.append(record)
        db.close()
        return records

    def get_records_between_dates(self, start_date, end_date):
        """get_records_between_dates() method returns a list of records,
        where every record date is between dates, that user specified
        in date selection view"""
        records = []
        db = sqlite3.connect(self.database_path)
        cur = db.cursor()
        for row in cur.execute('SELECT rowid, * FROM entries WHERE date >= "%s" AND date <= "%s"'
                               % (start_date, end_date)):
            record = Record(row[0], row[1], row[2], row[3], row[4], row[5])
            records.append(record)
        db.close()
        return records


# create Analytics class to analyze records for summary view
class Analytics:
    @staticmethod
    def average_mood(records):
        """average_mood() collects mood values and calculates average mood level"""
        if len(records) >= 1:
            mood = []
            for record in records:
                mood.append(record.mood)
            average = round(mean(mood), 1)
            return average
        else:
            return 0

    @staticmethod
    def symptoms(records):
        """symptoms() method collects and transform list of symptoms to text type suitable for displaying summary view"""
        text = ''
        for record in records:
            if record.symptoms != '':
                if text == '':
                    text = record.symptoms
                else:
                    text = text + ',' + record.symptoms
        lst = text.split(',')
        symptoms = ''
        dct = {}
        for x in lst:
            if x not in dct.keys():
                dct[x] = 1
            elif x in dct.keys():
                dct[x] += 1
        sorted_lst = sorted(dct.items(), key=lambda y: y[1], reverse=True)

        def di(ls, d):
            d = dict(ls)
            return d

        symptoms_dict = {}
        symptoms_dict = di(sorted_lst, symptoms_dict)
        for key, value in symptoms_dict.items():
            symptoms = symptoms + key + ' (' + str(dct[key]) + '),'
        symptoms = symptoms[:-1]
        return symptoms


if __name__ == '__main__':
    pass

