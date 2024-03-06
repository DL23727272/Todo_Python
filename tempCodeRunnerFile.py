# Dependencies
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker

from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox

from datetime import datetime

# To be added after creating the database
from database import Database
# Initialize db instance
db = Database(host='localhost', user='root', password='', database='todo')


class DialogContent(MDBoxLayout):
    """OPENS A DIALOG BOX THAT GETS THE TASK FROM THE USER"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = str(datetime.now().strftime('%A %d %B %Y'))

    
    def show_date_picker(self):
        """Opens the date picker"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        date = value.strftime('%A %d %B %Y')
        self.ids.date_text.text = str(date)

# After creating the database.py
class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    '''Custom list item'''

    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        # state a pk which we shall use link the list items with the database primary keys
        self.pk = pk

    def mark(self, check, the_list_item):
        '''mark the task as complete or incomplete'''
        if check.active == True:
            the_list_item.text = '[s]'+the_list_item.text+'[/s]'
            db.mark_task_as_complete(the_list_item.pk)# here
        else:
            the_list_item.text = str(db.mark_task_as_incomplete(the_list_item.pk))# Here

    def delete_item(self, the_list_item):
        '''Delete the task'''
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)# Here
    
    def open_edit_dialog(self):
        app = MDApp.get_running_app()
        app.show_edit_dialog(self.pk, self.text, self.secondary_text)

class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    '''Custom left container'''

# Main App class
class MainApp(MDApp):
    task_list_dialog = None
    def build(self):
        # Setting theme to my favorite theme
        self.theme_cls.primary_palette = "Orange"
        
    # Showing the task dialog to add tasks 
    def show_task_dialog(self):
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(
                title="Create Task",
                type="custom",
                content_cls=DialogContent(),
            )

        self.task_list_dialog.open()

    def on_start(self):
        # Load the saved tasks and add them to the MDList widget when the application starts
        try:
            completed_tasks, incompleted_tasks = db.get_tasks()

            if incompleted_tasks != []:
                for task in incompleted_tasks:
                    add_task = ListItemWithCheckbox(pk=task[0],text=task[1], secondary_text=task[2])
                    self.root.ids.container.add_widget(add_task)

            if completed_tasks != []:
                for task in completed_tasks:
                    add_task = ListItemWithCheckbox(pk=task[0],text='[s]'+task[1]+'[/s]', secondary_text=task[2])
                    add_task.ids.check.active = True
                    self.root.ids.container.add_widget(add_task)
        except Exception as e:
            print(e)
            pass

    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()

    def add_task(self, task, task_date):
        '''Add task to the list of tasks'''
        # print(task.text, task_date)
        created_task = db.create_task(task.text, task_date)

        # return the created task details and create a list item
        self.root.ids['container'].add_widget(ListItemWithCheckbox(pk=created_task[0], text='[b]'+created_task[1]+'[/b]', secondary_text=created_task[2]))
        task.text = ''
        
    edit_task_dialog = None

    def show_edit_dialog(self, task_id, task_text, task_date):
        if not self.edit_task_dialog:
            self.edit_task_dialog = MDDialog(
                title="Edit Task",
                type="custom",
                content_cls=EditDialogContent(task_id, task_text, task_date),
            )

        self.edit_task_dialog.open()

    def update_task(self, task_id, new_task_text, new_task_date):
        db.update_task(task_id, new_task_text, new_task_date)
        self.refresh_task_list()
        self.edit_task_dialog.dismiss()

    def refresh_task_list(self):
        # Refresh the task list after editing or adding a new task
        self.root.ids.container.clear_widgets()
        completed_tasks, incompleted_tasks = db.get_tasks()

        if incompleted_tasks != []:
            for task in incompleted_tasks:
                add_task = ListItemWithCheckbox(pk=task[0], text=task[1], secondary_text=task[2])
                self.root.ids.container.add_widget(add_task)

        if completed_tasks != []:
            for task in completed_tasks:
                add_task = ListItemWithCheckbox(pk=task[0], text='[s]'+task[1]+'[/s]', secondary_text=task[2])
                add_task.ids.check.active = True
                self.root.ids.container.add_widget(add_task)   
                
class EditDialogContent(MDBoxLayout):
    def __init__(self, task_id, task_text, task_date, **kwargs):
        super().__init__(**kwargs)
        self.task_id = task_id

        self.ids.edit_task_text.text = task_text
        self.ids.edit_date_text.text = task_date

    def show_edit_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        date = value.strftime('%A %d %B %Y')
        self.ids.edit_date_text.text = str(date)

    def save_changes(self):
        app = MDApp.get_running_app()
        app.update_task(self.task_id, self.ids.edit_task_text.text, self.ids.edit_date_text.text)


if __name__ == '__main__':
    app = MainApp()
    app.run()
