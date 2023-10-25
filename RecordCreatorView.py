import flet as ft
from flet_core import UserControl
import FletCalendar


# RecordCreatorView class is an interface for creating entries in a diary
class RecordCreatorView(UserControl):
    def __init__(self, recordlist, calendar: FletCalendar.FletCalendar):
        super().__init__()
        self.title_field = ft.TextField(label="Title",
                                        text_size=20)
        self.text_field = ft.TextField(label="Text",
                                       multiline=True,
                                       text_size=20)
        self.calendar = calendar
        self.mood_slider = 0
        self.list_of_symptoms = []
        self.list_of_symptoms_text = ft.Text()
        self.data = ['Headache', 'Abdominal pain', 'Blood in stool', 'Chest pain', 'Constipation', 'Cough', 'Diarrhea',
                     'Difficulty swallowing', 'Dizziness', 'Eye discomfort and redness', 'Eye problems', 'Foot pain',
                     'ankle pain', 'Foot swelling', 'leg swelling', 'Heart palpitations', 'Hip pain', 'Knee pain',
                     'Low back pain', 'Nasal congestion', 'Nausea or vomiting', 'Neck pain', 'Numbness', 'Tingling in hands',
                     'Pelvic pain', 'Shortness of breath', 'Shoulder pain', 'Sore throat', 'Urinary problems', 'Wheezing',
                     'Blurred vision', 'Brain fog', 'Choking when eating', 'Crossed eyed', 'Decreased responsiveness',
                     'Difficult to swallow', 'Difficulty speaking', 'Difficulty walking', 'Difficulty writing',
                     'Drooling from one side of the mouth', 'Alteration in mental status', 'Drooping eyelids',
                     'Face or mouth numbness', 'Fine tremors in hands', 'Lost interest in people', 'Limb spasms',
                     'Limb weakness', 'Seizure', 'Sensitive to sound', 'Sensitive to light', 'Stuttering', 'Tics',
                     'Trembling of fingers or whole body', 'Hangover', 'Eye twitching', 'Double vision']
        self.txtsearch = ft.TextField(label='Search',
                                      text_size=20,
                                      on_change=self.search)
        self.resultdata = ft.ListView()

        self.resultcon = ft.Container(
            padding=10,
            margin=10,
            offset=ft.transform.Offset(-2, 0),
            animate_offset=ft.animation.Animation(600, curve=ft.AnimationCurve.EASE_IN),
            content=ft.Column(controls=[
                self.resultdata]))
        self.resultcon.visible = False
        self.recordlist = recordlist

    def create_button_clicked(self, e):
        """method create_button_clicked() collects all user input
         and initiates creating a record by calling add_record() method of the RecordList class"""
        if not self.calendar.selected_date:
            (day, month, year) = FletCalendar.FletCalendar.get_current_date()
        else:
            (day, month, year) = self.calendar.selected_date
        if len(str(day)) == 1:
            day = '0%s' % str(day)
        if len(str(month)) == 1:
            month = '0%s' % str(month)
        year = str(year)
        record_date = '{}-{}-{}'.format(year, month, day)
        self.recordlist.add_record(
            self.title_field.value,
            self.text_field.value,
            self.mood_slider,
            ','.join(self.list_of_symptoms),
            record_date)
        self.list_of_symptoms = []

    def slider_changed(self, e):
        self.mood_slider = e.control.value
        self.update()

    def create_resultdata_view(self, x):
        # creating an interface for adding symptom to the users's list if symptoms or removing it from the list
        icon_button = ft.IconButton(
            icon=ft.icons.ADD_CIRCLE_OUTLINE,
            icon_size=20,
            tooltip="Add/remove symptom",
            selected_icon=ft.icons.DONE_OUTLINE_ROUNDED)

        def icon_button_clicked(e):
            symptom = x
            if e.control.selected:
                self.remove_symptom(symptom)
                e.control.selected = False
                e.control.update()
            else:
                self.add_symptom(symptom)
                e.control.selected = True
                e.control.update()

        icon_button.on_click = icon_button_clicked
        view = ft.Row(controls=[
            ft.Text(x, size=20),
            icon_button])
        return view

    def search(self, e):
        """the search among the available list of symptoms"""
        mysearch = e.control.value
        result = []
        if not mysearch == '':
            self.resultcon.visible = True
            for item in self.data:
                if mysearch in item:
                    result.append(item)
        if len(result) > 0:
            self.resultcon.offset = ft.transform.Offset(0, 0)
            self.resultdata.controls.clear()
            for x in result:
                self.resultdata.controls.append(self.create_resultdata_view(x))
            self.update()
        else:
            self.resultcon.offset = ft.transform.Offset(-2, 0)
            self.resultdata.controls.clear()
            self.update()

    def add_symptom(self, x):
        if x not in self.list_of_symptoms:
            self.list_of_symptoms.append(x)

    def remove_symptom(self, x):
        self.list_of_symptoms.remove(x)

    def build(self):
        """build() method creates and returns a displayed view of RecordCreatorView class,
        which is used by the user for creating and modifying diary entries"""
        button = ft.ElevatedButton(text='Add record',
                                   style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)),
                                   expand=True,
                                   width=355,

                                   on_click=self.create_button_clicked)
        slider = ft.Slider(min=0,
                           max=10,
                           divisions=10,
                           label="{value}",
                           on_change_end=self.slider_changed)
        text_slider = ft.Text(
            '''Use the slider to pick a number from 1 to 10 that best reflects your mood level.''',
            size=15)
        search_column = ft.Column([
            ft.Text('Find the symptoms that bother you by entering their name and add them to your entry.',
                    size=15),
            self.txtsearch,
            self.resultcon
        ])
        content_column = ft.Column([self.title_field, self.text_field, text_slider, slider, search_column],
                                   alignment=ft.alignment.top_left,
                                   expand=True)
        content_container = ft.Container(content=content_column, expand=True, margin=5, padding=5)
        calendar_column = ft.Column([self.calendar, button],
                                    expand=False,
                                    spacing=10,
                                    width=355, height=355
                                    )
        row = ft.Row(controls=[content_container, calendar_column],
                     expand=2)
        return row