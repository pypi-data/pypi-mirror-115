from ctextinctPackage.model_ import Model
from ctextinctPackage.view import View
import webbrowser
import os
import sys


# OOP (Controller) -> View() then return controller

class Controller:
    # i used *args and **kwargs here because this is the main class with many features and I do not want to limit its
    # functionality. Also to reduce errors as the project increases in size.
    def __init__(self, *args, **kwargs):
        #  __init__ method is the constructor of the class. "self" can be named anything, similar to "this" in Java.
        #  *args allows me to add as many arguments/variables as i want when i initialised an instance of class (object)
        #  **kwargs allows me to add as many keyword arguments/ dictionaries as I want into the class constructor
        self.counter = 0
        self.cache = False
        self.model_c = Model()  # model not aware of controller or view
        self.view_c = View(self)  # view aware of controller but not model so takes controller as argument

        print("Controller Initialised")

    def main(self):
        self.view_c.main()

    def restart_program(self):
        # Restarts the current program
        self.view_c.destroy()

    def on_button_click(self, button_name):
        if button_name == "news_b":
            if self.counter == 1:
                self.view_c.delete_news_buttons()
            if self.counter == 0:
                self.grab_top_twenty_news_headlines()
        print("END: on_button_click")

    def on_enter_key_pressed(self, user_question):
        response = self.model_c.ask_question(user_question)
        print("response from controller" + response)
        self.view_c.next_question(response)
        print("END: on_enter_key_pressed")

    def submit_feedback_form(self):
        pass

    def submit_cyber_incident(self):
        pass

    def grab_top_twenty_news_headlines(self):
        # if statement to prevent grabbing the top headlines if grabbed already
        if not self.cache:
            self.cache = self.model_c.connect_to_news_api()
        self.view_c.create_news_buttons()

    @staticmethod
    def visit_site(v):
        webbrowser.open_new_tab(v)

    def train_model(self, file):
        self.model_c.training_model(file)

    def parse_cyber_security_forum_and_replace_training_data(self, url):
        self.model_c.cyber_security_forum_parser(url)
        self.train_model(f'../docs/files/{url.split("/")[2].split(".")[0]}.json')
        #  F-string used as it allowed me to embed the filename formatting required inside a string with minimal syntax
