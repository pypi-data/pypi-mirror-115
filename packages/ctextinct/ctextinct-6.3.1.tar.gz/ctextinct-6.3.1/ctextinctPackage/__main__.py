from ctextinctPackage.controller import Controller


def main():
    cyber_chatbot = Controller()
    print("main object initialised")
    cyber_chatbot.main()


if __name__ == "__main__":
    main()
else:
    print('This module cannot be imported or used by another module. Please run code from app.py file')
