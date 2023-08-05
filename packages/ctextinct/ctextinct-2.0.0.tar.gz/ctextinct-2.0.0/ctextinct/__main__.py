from ctextinct.controller import Controller


def main():
    cyber_chatbot = Controller()
    print("main object initialised")
    # cyber_chatbot.parse_cyber_security_forum_and_replace_training_data("https://cybersecurityforum.com/cybersecurity"
    #                                                                   "-faq/")
    #cyber_chatbot.train_model("../Assets/Files/intents.json")
    cyber_chatbot.main()


if __name__ == "__main__":
    main()
else:
    print('This module cannot be imported or used by another module. Please run code from app.py file')





