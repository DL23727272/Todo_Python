from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from main import MainApp
import subprocess
import os

Window.clearcolor = (1, 0, 0, 1)

username = "DL"
password = "123"

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(None, None))

        self.username_input = TextInput(hint_text='Username', multiline=False, size_hint=(None, None), size=(200, 40), pos_hint={'center_x': 0.5})
        self.password_input = TextInput(hint_text='Password', multiline=False, password=True, size_hint=(None, None), size=(200, 40), pos_hint={'center_x': 0.5})
        self.result_label = TextInput(hint_text='', disabled=True, size_hint=(None, None), size=(200, 40), pos_hint={'center_x': 0.5},
                                       foreground_color=(1, 1, 1, 1))

        login_btn = Button(text='Login', size_hint=(None, None), size=(100, 40), pos_hint={'center_x': 0.9, 'center_y': 0.8}, background_color=(1, 1, 0, 1))
        login_btn.bind(on_press=self.login)

        layout.add_widget(self.result_label)
        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_btn)

        self.add_widget(layout)
        self.successful_login = False

    def login(self, instance):
        entered_username = self.username_input.text
        entered_password = self.password_input.text

        if entered_username == username and entered_password == password:
            self.result_label.text = 'GO!'
            # Open the main.py application
            subprocess.Popen(["python", "main.py"])

            # Close the login.py application
            os._exit(0)
        elif username == '' and password == '':
            self.result_label.text = 'Empty!'
        elif username != 'DL' or password != '123':
            self.result_label.text = 'Wrong input!'
        else:
            self.result_label.text = 'Failed.'

class MainScreen(Screen):
    pass

class LoginApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login_screen'))
        sm.add_widget(MainScreen(name='main_screen'))
        return sm

if __name__ == '__main__':
    app = LoginApp()
    app.run()
