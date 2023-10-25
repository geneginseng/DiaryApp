from collections import deque
import flet as ft
from flet_core import UserControl
from DiaryRecords import Record
from datetime import datetime


# RecordView class displays a view element of a created record
class RecordView(UserControl):
    def __init__(self, record: Record):
        super().__init__()
        self.value = record
        # implement observer pattern here by creating a list of subscribers
        self.subscribers = []
        self.view = None

    def build(self):
        """build() method creates and returns a view of all elements in a record"""
        title = ft.Text(size=15)
        text = ft.Text(size=15)
        date = ft.Text(size=15)
        mood = ft.Text(f'Level of mood: {self.value.mood}', size=15)
        symptoms = ft.Text(f'Your symptoms today: {self.value.symptoms}', size=15)
        title.value = self.value.title
        text.value = self.value.text
        date.value = self.value.date
        icon = ft.Icon(name=ft.icons.FAVORITE, color=ft.colors.PINK_700)
        # create a view element title_row containing icon and title to put them on the same line
        title_row = ft.Row(
            controls=[
                icon,
                title
            ])
        delete_button = ft.IconButton(
            icon=ft.icons.DELETE_FOREVER_ROUNDED,
            icon_color="pink700",
            icon_size=30,
            tooltip="Delete record",
            on_click=self.on_delete_click)
        date_delete_button_row = ft.Row(
            controls=[
                ft.Text('Date: ', size=15),
                date,
                delete_button
            ]
        )
        # create a column control for storing a record view
        column = ft.Column([
            title_row,
            text,
            mood,
            symptoms,
            date_delete_button_row])
        # create a container control with column control in it and add design elements
        self.view = ft.Container(content=column,
                                 border=ft.border.all(1),
                                 margin=5,
                                 padding=10,
                                 border_radius=10)
        return self.view

    def on_delete_click(self, e):
        """on_delete_click() method is called when on_click event of delete button of record view is happened"""
        self.notify_subscribers()

    def add_subscriber(self, callback):
        self.subscribers.append(callback)

    def remove_subscriber(self, callback):
        self.subscribers.remove(callback)

    def notify_subscribers(self):
        """notify_subscribers() method is called by on_delete_click() method
        and notify all subscribers in the list of subscribers about deleting a record view"""
        for callback in self.subscribers:
            callback(self.value)


class RecordListView(UserControl):
    def __init__(self, value=None, date=None):
        super().__init__()
        self._value = value
        if self._value is None:
            self._value = []
        self.date = date
        self.expand = True
        self.subscribers = []
        self.list_view = None
        self.view = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, list_of_entries):
        self._value = list_of_entries
        if self.page is not None:
            self.update_view()

    def build(self):
        self.list_view = ft.ListView(expand=1,
                                     auto_scroll=False)
        self.view = ft.Container(content=self.list_view,
                                 expand=True,
                                 alignment=ft.alignment.top_center)
        records = deque()
        for record in self._value:
            records.appendleft(record)
        for record in records:
            record_view = RecordView(record)
            self.list_view.controls.append(record_view)
            record_view.add_subscriber(lambda x: self.record_deleted(x))
        return self.view

    def did_mount(self):
        self.update_view()

    def update_view(self):
        self.list_view.clean()
        records = deque()
        for record in self._value:
            records.appendleft(record)
        for record in records:
            record_view = RecordView(record)
            self.list_view.controls.append(record_view)
            record_view.add_subscriber(lambda x: self.record_deleted(x))
        self.update()

    def record_deleted(self, record):
        self.notify_subscribers(record)

    def add_subscriber(self, callback):
        self.subscribers.append(callback)

    def remove_subscriber(self, callback):
        self.subscribers.remove(callback)

    def notify_subscribers(self, *args):
        for callback in self.subscribers:
            callback(*args)


class StatisticsView(UserControl):
    def __init__(self):
        super().__init__()
        self._entries_number = 0
        self._average_mood = 0
        self._symptoms = ''
        self.stat_text = ft.Text("", size=15)
        container = ft.Container(content=self.stat_text)

        self.view = ft.Container(content=container,
                                 expand=True,
                                 border=ft.border.all(1),
                                 padding=10,
                                 margin=5,
                                 border_radius=10,
                                 alignment=ft.alignment.top_left,)

    @property
    def entries_number(self):
        return self._entries_number

    @entries_number.setter
    def entries_number(self, number):
        self._entries_number = number
        if self.page is not None:
            self.update_view()

    @property
    def average_mood(self):
        return self._average_mood

    @average_mood.setter
    def average_mood(self, average_mood):
        self._average_mood = average_mood
        if self.page is not None:
            self.update_view()

    @property
    def symptoms(self):
        return self._symptoms

    @symptoms.setter
    def symptoms(self, symptoms):
        self._symptoms = symptoms
        if self.page is not None:
            self.update_view()

    def build(self):
        return self.view

    def build_stat_text(self):
        return f'''Here is a summary of the selected period.\r
You had entered {str(self._entries_number)} diary entries.\r
Your average mood level was {str(self._average_mood)}.\r
Your symptoms and the number of times each one has irritated you are listed here: {self._symptoms}.'''

    def did_mount(self):
        self.update_view()

    def update_view(self):
        self.stat_text.value = self.build_stat_text()
        self.update()


class DateSelectionView(UserControl):
    def __init__(self):
        super().__init__()
        self.select_start_date = None
        self.select_end_date = None
        self.view = None
        self.selected_date = None
        self.subscribers = []
        self.button = None

    def build(self):
        self.select_start_date = ft.TextField(label='Start date YYYY-MM-DD',
                                              text_size=15,
                                              width=230)
        self.select_end_date = ft.TextField(label='End date YYYY-MM-DD',
                                            text_size=15,
                                            width=230)
        button_entries = ft.ElevatedButton(text='Display entries',
                                           expand=True,
                                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                                                on_click=lambda e: self.date_selected('ent'))
        button_statistics = ft.ElevatedButton(text='Display statistics',
                                              expand=True,
                                                   style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                                                   on_click=lambda e: self.date_selected('stat'))
        self.view = ft.Row(controls=[self.select_start_date,
                                     self.select_end_date,
                                     button_entries,
                                     button_statistics],
                           alignment=ft.alignment.top_center)
        return self.view

    def date_selected(self, button):
        self.button = button
        try:
            datetime.strptime(self.select_start_date.value, '%Y-%m-%d')
            datetime.strptime(self.select_end_date.value, '%Y-%m-%d')
            self.selected_date = (self.select_start_date.value, self.select_end_date.value)
            self.notify_subscribers()
        except ValueError:
            self.selected_date = None
            self.notify_subscribers()

    def add_subscriber(self, callback):
        self.subscribers.append(callback)

    def remove_subscriber(self, callback):
        self.subscribers.remove(callback)

    def notify_subscribers(self):
        for callback in self.subscribers:
            callback()
