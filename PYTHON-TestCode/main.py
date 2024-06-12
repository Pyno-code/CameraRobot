import os
from os.path import abspath, dirname
from process import ManagerController

if __name__ == "__main__":
    os.chdir(dirname(abspath(__file__)))
    manager = ManagerController()

    manager.launch()
    manager.join()
    print('End of the program')