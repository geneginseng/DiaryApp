import flet as ft
from DiaryRecords import RecordListDB
from ViewModel import ViewModel
from FletCalendar import FletCalendar
from RecordCreatorView import RecordCreatorView


def main(page: ft.Page):
    # specify the page's design (title, alignment, color scheme)
    page.title = "The diary"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(color_scheme_seed="#21005D")
    # create class's instances to run app's logic
    my_calendar = FletCalendar()  # create instance of calendar view
    record_list = RecordListDB('records.db')  # create instance of records storage (Python object or database file)
    creator = RecordCreatorView(record_list, my_calendar)  # create an interface for creating records in a diary
    # create an interface for displaying list of entries, summary view, and date selection view.
    # ViewModel class's attributes date_selection_view, record_list_view, and summary_view indicate
    # whether corresponding elements will be added to the page
    model = ViewModel(record_list, date_selection_view=True, record_list_view=True, summary_view=True)

    # add view elements on the page
    page.add(creator)
    page.add(model)


# create a page with specified properties, adds view elements on it
# and call main() function with a page instance passed into it for creating a user session
if __name__ == "__main__":
    # run the created page in separate window, starting user session
    ft.app(target=main)
