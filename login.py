from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
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

        if entered_username == '' and entered_password == '':
            error_label.text = 'Empty username and password!'
        elif entered_username == '':
            error_label.text = 'Empty username!'
        elif entered_password == '':
            error_label.text = 'Empty password!'
        elif entered_username == username and entered_password == password:
            # Open the main.py application
            subprocess.Popen(["python", "main.py"])

            # Close the login.py application
            os._exit(0)
        elif entered_username != 'DL' or entered_password != '123':
            error_label.text = 'Wrong username or password!'
        else:
            error_label.text = 'Failed.'

if __name__ == "__main__":
    app = Login()
    app.run()
