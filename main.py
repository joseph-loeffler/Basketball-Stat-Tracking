"""
Created on 5/12/23
@author: josephloeffler
"""
from model import Model
from view import View
from controller import Controller


def main():
    model = Model()
    controller = Controller(model, view=View(controller=Controller))
    controller.view.controller = controller

    controller.view.main()


if __name__ == '__main__':
    main()
