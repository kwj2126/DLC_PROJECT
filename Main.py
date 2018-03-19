from Kiwoom import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys

form = uic.loadUiType("GUI.ui")[0]


class GUI(QMainWindow, form):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.kiwoom = Kiwoom()
        self.kiwoom.log_in()

        code_list = self.kiwoom.get_code_list(0)  # 코스피
        code_list += self.kiwoom.get_code_list(10)  # 코스닥

        screen_no = 1000
        reg_cnt = 0
        for code in code_list:  # 호가정보 실시간 등록
            fid_list = ''
            for i in range(41, 81):
                if i != 41:
                    fid_list += ';'
                fid_list += str(i)

            reg_cnt += 1
            if reg_cnt == 100:
                reg_cnt = 0
                screen_no += 1

            self.kiwoom.set_real_reg(screen_no, code, fid_list, 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    app.exec_()
