import tkinter as tk
from tkinter import ttk, END, CENTER, tix
from PIL import ImageTk, Image
import time
from tkinter.tix import Balloon


class Splash(tk.Toplevel):
    def __init__(self, main_window):
        tk.Toplevel.__init__(self, main_window)
        self.wm_attributes('-fullscreen', 'true')
        logo_img = Image.open("docs/images/transparent_ardonagh.png")
        logo_img = logo_img.resize((562, 202), Image.ANTIALIAS)
        splash_logo = ImageTk.PhotoImage(logo_img)
        logo_label = tk.Label(self, image=splash_logo)
        logo_label.image = splash_logo
        logo_label.place(relx=0.5, rely=0.5, anchor=CENTER)
        # required to make window show before the program gets to the mainloop
        self.update()


# The view inherits from tk.Tk() class so I could have access to all its attributes & methods
class View(tk.Tk):
    PAD = 10  # constant, a class variable, which can be different for each instance of this class
    FONT = "helvetica 14"  # reduces repetition and allows me tso control font for all my app from one place
    COMPANY_COLOR = "#003428"

    def __init__(self, controller):
        super().__init__()  # super() function used to get access to the methods of tk.Tk class.
        # It returns a temp object of the parent class
        # remove main_window
        self.withdraw()
        # show splash screen
        splash_screen = Splash(self)
        # setup Main Window
        self.controller = controller
        self.frames_dict = {}
        self.news_buttons = []
        self.nav = False
        time.sleep(3)  # simulating a delay while loading
        # loading finished so splash screen destroyed
        splash_screen.destroy()
        # show main_window again
        self.deiconify()
        print("View Initialised")

    def main(self):
        self.title("CT Extinct")
        print("title added")
        self.iconbitmap("docs/images/individualLogo.ico")
        app_width = 600
        app_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_axis = (screen_width / 2) - (app_width / 2)
        y_axis = (screen_height / 2) - (app_height / 2)
        self.geometry(f'{app_width}x{app_height}+{int(x_axis)}+{int(y_axis)}')
        self.create_menu()
        self._make_all_frames()
        self._make_cyber_news_widgets()
        self._make_cyber_bot_widgets()
        print("before frame shown")
        print(self.winfo_screenheight())
        print(self.winfo_screenheight())
        self.show_frame_type("cyber_bot_frame")
        self.mainloop()  # allows me to includes events in this application as it creates an infinite loop which can
        # be stopped by closing the window

    def _make_all_frames(self):
        self.maincontainer = tk.Frame(self, bg="black")
        self.maincontainer.pack(side="top", fill="both", expand="True")
        # setting main container dimensions and making it dynamic with size of window
        tk.Grid.grid_rowconfigure(self.maincontainer, 0, weight=1)
        tk.Grid.grid_columnconfigure(self.maincontainer, 0, weight=1)
        # creating empty dictionary and initialising an instance of each class inside main container
        # then linking them to dictionary keys and positioning them so they can fill the whole window
        self.cyber_bot_frame = tk.Frame(self.maincontainer, bg="white")
        self.cyber_news_frame = tk.Frame(self.maincontainer, bg="black")
        self.feedback_form_frame = tk.Frame(self.maincontainer, bg=self.COMPANY_COLOR)
        self.cyber_incident_frame = tk.Frame(self.maincontainer, bg="yellow")
        self.cyber_bot_frame.grid(row=0, column=0, sticky="nsew")
        self.cyber_news_frame.grid(row=0, column=0, sticky="nsew")
        self.feedback_form_frame.grid(row=0, column=0, sticky="nsew")
        self.cyber_incident_frame.grid(row=0, column=0, sticky="nsew")
        # self.frames_dict["splash_frame"] = self.splash_frame
        self.frames_dict["cyber_bot_frame"] = self.cyber_bot_frame
        self.frames_dict["cyber_news_frame"] = self.cyber_news_frame
        self.frames_dict["feedback_form_frame"] = self.feedback_form_frame
        self.frames_dict["cyber_incident_frame"] = self.cyber_incident_frame
        # nav frame
        self.nav_frames = []

    def create_menu(self):
        main_menu = tk.Menu(self)
        self.config(menu=main_menu)
        file_menu = tk.Menu(main_menu)
        main_menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Sign Out", command=self.controller.restart_program)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.controller.restart_program)

        navigate_menu = tk.Menu(main_menu)
        main_menu.add_cascade(label="Navigate To", menu=navigate_menu)
        navigate_menu.add_command(label="Cyber Bot", command=lambda: self.show_frame_type("cyber_bot_frame"))
        navigate_menu.add_separator()
        navigate_menu.add_command(label="Cyber News", command=lambda: self.show_frame_type("cyber_news_frame"))
        navigate_menu.add_separator()
        navigate_menu.add_command(label="Feedback Form", command=lambda: self.show_frame_type("feedback_form_frame"))
        navigate_menu.add_separator()
        navigate_menu.add_command(label="Security Incident",
                                  command=lambda: self.show_frame_type("cyber_incident_frame"))

        help_menu = tk.Menu(main_menu)
        main_menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Help on Our Site",
                              command=lambda: self.controller.visit_site("https://kunet.kingston.ac.uk/k1739510"
                                                                         "/ctExtinct/view/index.php"))
        help_menu.add_separator()
        help_menu.add_command(label="Version", command=lambda: print("Version 1.0"))

    def show_frame_type(self, frame_type):
        visible_frame = self.frames_dict[frame_type]
        if frame_type == "cyber_news_frame":
            self.controller.on_button_click("news_b")
        visible_frame.tkraise()

    def delete_news_buttons(self):
        for i in range((len(self.news_buttons) - 1)):
            self.news_buttons.remove(self.news_buttons[i])

    def create_news_buttons(self):
        for k, v in self.controller.cache.items():
            temp = tk.Button(self.cyber_news_frame, text=k, command=lambda: self.controller.visit_site(v))
            temp.pack(pady=self.PAD, padx=self.PAD)
            self.news_buttons.append(temp)

    def _make_cyber_news_widgets(self):
        title_l = tk.Label(self.cyber_news_frame, text="Top 20 Cyber Headlines")
        title_l.pack(padx=self.PAD, pady=self.PAD)

    def next_question(self, response):
        self.chatbot_entry.delete(0, END)
        print(response + "= responsE")
        self.output_field.configure(text=response)

    def _make_cyber_bot_widgets(self):
        self.input_frame = tk.Frame(self.cyber_bot_frame, bg=self.COMPANY_COLOR)
        self.output_frame = tk.Frame(self.cyber_bot_frame, bg=self.COMPANY_COLOR)
        self.output_frame.pack(padx=self.PAD, pady=self.PAD, side="top")
        self.input_frame.pack(padx=self.PAD, pady=self.PAD, side="bottom")

        self.chatbot_entry = tk.Entry(self.input_frame, font=self.FONT)
        self.entry_label = tk.Label(self.input_frame, text="Ask Cyber Security Question: ", font=self.FONT,
                                    bg=self.COMPANY_COLOR, fg="white")
        self.output_field = tk.Label(self.output_frame, text="Chatbot: Hey my name is Janine. You can ask me anything!",
                                     height=20, width=50, justify="left", anchor="n",
                                     bg=self.COMPANY_COLOR, wraplength=550, fg="white", font=self.FONT)
        self.entry_label.pack(padx=self.PAD, pady=self.PAD, side="left")
        self.chatbot_entry.pack(padx=self.PAD, pady=self.PAD, side="left")
        self.output_field.pack(padx=self.PAD, pady=self.PAD, fill='both')

        self.entry_b = ttk.Button(self.input_frame, text="Go",
                                  command=lambda: self.controller.on_enter_key_pressed(self.chatbot_entry.get()))
        self.entry_b.pack(padx=self.PAD, pady=self.PAD, side="right")

        # tip = Balloon(self))
        # tip.config(bd=10, bg="blue")
        # tip.label.config(bg="red", fg="white", bd=20)
        # tip.message.config(bg="red", fg="white")
        # tip.bind_widget(self.chatbot_entry, balloonmsg="Please press enter")

# I only used self. when I needed to use that particular variable from outside its method.
# the use of _ at the start  in the naming of a method means that the method wont be called outside the class,
# it is not required, it is a convention and  is recognised by everyone
