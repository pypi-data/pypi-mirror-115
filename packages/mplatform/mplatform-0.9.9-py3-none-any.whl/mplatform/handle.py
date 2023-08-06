from datetime import datetime
import numpy as np
import os

class Time:
    """
    handle Time: get_current_time, save_current_time
    """

    @staticmethod
    
    def date_time():
        """return: type -> str"""
        return (datetime.now()).strftime("\n%X\n%A, %B %d, %Y\n")

    # @staticmethod
    # def save_data_time():
        """return: type -> str"""
        # print(os.getcwd())
        # with open(file='.\history\log.txt',mode="a",encoding = 'utf-8') as file:
        #     file.write(handleTime.date_time())

class Folder:
    """
    handle Folder: get path,...
    """

    @staticmethod
    def list_file_dir(path=None):
        """
        path = 'C:\\'\n
        return: type('numpy.ndarray'), 2-D\n
        """        
        return np.transpose(np.array(os.listdir(path),ndmin=2))

    @staticmethod
    def show_list_file_dir(variable=None):
        """
        Show list when call def list_files_subfolders()
        return: None
        """
        if str(type(variable)) == str("<class 'numpy.ndarray'>"):
            if variable.ndim == 2:
                for i in range(0,len(variable)): print(variable[i][0])
            else: print('variable can only be 2 dimensional')
        else: print("type(variable) -> <class 'numpy.ndarray'>")

class File:
    """
    handle File: get path,...
    return: type -> str
    """
    @staticmethod
    def current_file(): return os.path.abspath(__file__)


def main(): pass
if __name__ == '__main__': main()