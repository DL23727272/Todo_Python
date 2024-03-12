from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextFieldRect
from kivy.lang import Builder
import subprocess
import os

class Login(MDApp):
    def build(self):
        return Builder.load_file("login.kv")

    def login(self):
        entered_username = self.root.ids.username_input.text
        entered_password = self.root.ids.password_input.text
        error_label = self.root.ids.error_label

        username = 'DL'
        password = '123'

        if entered_username == username and entered_password == password:
            error_label.text = 'GO!'
            # Open the main.py application
            subprocess.Popen(["python", "main.py"])

            # Close the login.py application
            os._exit(0)
        elif username == '' and password == '':
            error_label.text = 'Empty!'
        elif username != 'DL' or password != '123':
            error_label.text = 'Wrong input!'
        else:
            error_label.text = 'Failed.'

if __name__ == "__main__":
    app = Login()
    app.run()
