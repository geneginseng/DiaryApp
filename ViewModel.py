import flet as ft
from flet_core import UserControl
from DiaryViews import RecordListView, DateSelectionView, StatisticsView
from DiaryRecords import Analytics


# ViewModel class is an integral component of the Model-View-ViewModel design pattern,
# serving as a controller responsible for generating and modifying UI elements in the View
# based on user-triggered events
class ViewModel(UserControl):
    def __init__(self,
                 record_list,
                 date_selection_view=False,
                 record_list_view=False,
                 summary_view=False):
        super().__init__()
        self.record_list = record_list
        self.list_view = ft.ListView(expand=1,
                                     auto_scroll=False,
                                     spacing=10,
                                     padding=10)
        self.view = ft.Container(expand=True,
                                 border_radius=10,
                                 alignment=ft.alignment.top_center,)
        self.expand = True
        self.list = False
        self.date = False
        self.sum = False
        self.displayed_view = None
        # create date selection view (if True) and subscribe instance of ViewModel class to notifications
        # associated with selection of a new date or switching the view between the list of entries and the summary view
        if date_selection_view:
            self.date = True
            self.date_selection_view = DateSelectionView()
            self.date_selection_view.add_subscriber(self.new_date_selected)
        # create summary view (if True)
        if summary_view:
            self.sum = True
            self.displayed_view = 'stat'
            self.summary_view = StatisticsView()
            records = self.record_list.get_records()
            records_number = len(records)
            self.summary_view.entries_number = records_number
            mood = Analytics.average_mood(records)
            self.summary_view.average_mood = mood
            symptoms = Analytics.symptoms(records)
            self.summary_view.symptoms = symptoms
        # create list of entries view (if True) and subscribe instance of ViewModel class to notifications
        # associated with deleting a record, triggered by user
        if record_list_view:
            self.list = True
            self.displayed_view = 'ent'
            list_of_entries = self.record_list.get_records()
            self.record_list_view = RecordListView()
            self.record_list_view.value = list_of_entries
            self.record_list_view.add_subscriber(self.delete_record)
        # subscribe instance of ViewModel class to notifications associated with any changes in the list of records
        self.record_list.add_subscriber(self.record_list_updated)
        self.new_date = None

    def build(self):
        if self.date_selection_view:
            self.list_view.controls.append(self.date_selection_view)
        if self.list:
            if self.list and self.displayed_view == 'ent':
                self.list_view.controls.append(self.record_list_view)
            if self.sum and self.displayed_view == 'stat':
                self.list_view.controls.append(self.summary_view)
        self.view.content = self.list_view
        return self.view

    def did_mount(self):
        """update views right after building them"""
        if self.list and self.displayed_view == 'ent':
            self.update_record_list_view()
        if self.sum and self.displayed_view == 'stat':
            self.update_summary_view()
        self.update()

    def record_list_updated(self):
        if self.list and self.displayed_view == 'ent':
            self.update_record_list_view()
        if self.sum and self.displayed_view == 'stat':
            self.update_summary_view()
        self.update()

    def new_date_selected(self):
        self.new_date = self.date_selection_view.selected_date
        self.displayed_view = self.date_selection_view.button
        if self.list:
            if self.summary_view in self.list_view.controls:
                self.list_view.controls.remove(self.summary_view)
            if self.record_list_view in self.list_view.controls:
                self.list_view.controls.remove(self.record_list_view)
            self.update()
            if self.sum and self.displayed_view == 'stat':
                self.list_view.controls.append(self.summary_view)
                self.update()
                self.update_summary_view()
            else:
                self.list_view.controls.append(self.record_list_view)
                self.update()
                self.update_record_list_view()
        self.update()

    def update_record_list_view(self):
        if self.new_date is None:
            list_of_entries = self.record_list.get_records()
        else:
            start_date = self.new_date[0]
            end_date = self.new_date[1]
            list_of_entries = []
            for record in self.record_list.get_records_between_dates(start_date, end_date):
                list_of_entries.append(record)
        self.record_list_view.value = list_of_entries

    def update_summary_view(self):
        if self.new_date is None:
            records = self.record_list.get_records()
        else:
            start_date = self.new_date[0]
            end_date = self.new_date[1]
            records = self.record_list.get_records_between_dates(start_date, end_date)
        records_number = len(records)
        mood = Analytics.average_mood(records)
        symptoms = Analytics.symptoms(records)
        self.summary_view.entries_number = records_number
        self.summary_view.average_mood = mood
        self.summary_view.symptoms = symptoms

    def delete_record(self, record):
        """after receiving notification from the record_list_view,
        delete_record() method calls the method of the RecordList/RecordListDB class
        to finally remove the record from the record store"""
        self.record_list.remove_record(record)

    def __del__(self):
        self.record_list.remove_subscriber(self.record_list_updated)
        if self.date:
            self.date_selection_view.remove_subscriber(self.new_date_selected)
        if self.list:
            self.record_list_view.remove_subscriber(self.delete_record)