import calendar
import datetime
from calendar import HTMLCalendar
import flet as ft
from dateutil.relativedelta import relativedelta


# FletCalendar class is an interface for displaying calendar,
# which is as a part of interface for creating a record in RecordCreatorView class
class FletCalendar(ft.UserControl):
    def __init__(self):
        super().__init__()

        self.current_day, self.current_month, self.current_year = self.get_current_date()

        self.calendar_container = ft.Container(width=355, height=300,
                                               padding=ft.padding.all(2),
                                               border=ft.border.all(1, # self.border_color
                                                                    ),
                                               border_radius=ft.border_radius.all(10),
                                               alignment=ft.alignment.bottom_center)
        self.selected_date = False
        self.build()  # Build the calendar.

    @staticmethod
    def get_current_date():
        """get the initial current date"""
        today = datetime.datetime.today()
        current_day = today.day
        current_month = today.month
        current_year = today.year
        return current_day, current_month, current_year

    def select_date(self, e):
        """user selected the date"""
        self.selected_date = e.control.data
        self.set_date()

    def set_current_date(self):
        """setting the calendar to the current date"""
        today = datetime.datetime.today()
        self.current_month = today.month
        self.current_day = today.day
        self.current_year = today.year
        self.build()
        self.calendar_container.update()

    def set_date(self):
        """setting the calendar to the selected date"""
        self.current_day, self.current_month, self.current_year = self.selected_date
        self.build()
        self.calendar_container.update()

    def get_next(self, e):
        """moving to the next month"""
        current = datetime.date(self.current_year, self.current_month, self.current_day)
        add_month = relativedelta(months=1)
        next_month = current + add_month

        self.current_year = next_month.year
        self.current_month = next_month.month
        self.current_day = next_month.day
        self.build()
        self.calendar_container.update()

    def get_prev(self, e):
        """moving to the previous month"""
        current = datetime.date(self.current_year, self.current_month, self.current_day)
        add_month = relativedelta(months=1)
        next_month = current - add_month
        self.current_year = next_month.year
        self.current_month = next_month.month
        self.current_day = next_month.day
        self.build()
        self.calendar_container.update()

    def get_calendar(self):
        """get the calendar from the calendar module"""
        cal = HTMLCalendar()
        return cal.monthdayscalendar(self.current_year, self.current_month)
#
    def build(self):
        """build the calendar"""
        current_calendar = self.get_calendar()

        str_date = '{0} {1}, {2}'.format(self.current_day,
                                         calendar.month_name[self.current_month],
                                         self.current_year)

        date_display = ft.Text(str_date,
                               text_align=ft.TextAlign.CENTER,
                               size=20)
        next_button = ft.Container(ft.Text('>', text_align=ft.TextAlign.RIGHT, size=20),
                                   on_click=self.get_next)
        div = ft.Divider(height=1, thickness=2.0)
        prev_button = ft.Container(ft.Text('<', text_align=ft.TextAlign.LEFT, size=20),
                                   on_click=self.get_prev)

        calendar_column = ft.Column(
            [ft.Row([prev_button, date_display, next_button],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    height=40,
                    expand=False),
             div],
            spacing=2, width=355, height=330, alignment=ft.MainAxisAlignment.START, expand=False)
        # loop weeks and add row
        for week in current_calendar:
            week_row = ft.Row(alignment=ft.MainAxisAlignment.CENTER)
            # Loop days and add days to row.
            for day in week:
                if day > 0:
                    is_current_day_font = ft.FontWeight.W_300
                    display_day = str(day)
                    if len(str(display_day)) == 1: display_day = '0%s' % display_day
                    if day == self.current_day:
                        is_current_day_font = ft.FontWeight.BOLD

                    day_button = ft.Container(
                        content=ft.Text(str(display_day), weight=is_current_day_font),
                        on_click=self.select_date, data=(day, self.current_month, self.current_year),
                        width=40, height=40, ink=True, alignment=ft.alignment.center,
                        border_radius=ft.border_radius.all(10))
                else:
                    day_button = ft.Container(width=40, height=40, border_radius=ft.border_radius.all(10))

                week_row.controls.append(day_button)

            # adding the weeks to the main column
            calendar_column.controls.append(week_row)
        # adding the column to the page container
        self.calendar_container.content = calendar_column
        return ft.Column([self.calendar_container])