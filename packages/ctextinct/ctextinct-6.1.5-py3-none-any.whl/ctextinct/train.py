from ctextinct.controller import Controller
import argparse

trainUpdate = argparse.ArgumentParser(description="Train specific file")
trainUpdate.add_argument("-f", "--fileName", type=str, metavar="",
                         help="Please specify the exact name of the jason file containing the training data")
args = trainUpdate.parse_args()


def train(fileName):
    train_bot = Controller()
    train_bot.train_model(fileName)


if __name__ == "train":
    train(args.fileName)
else:
    print('This module cannot be imported or used by another module. Please run code from app.py file')
