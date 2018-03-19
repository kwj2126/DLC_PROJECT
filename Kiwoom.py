# 키움 통신 모듈

from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import csv
import time


class Kiwoom(QAxWidget):

    def __init__(self):
        super().__init__()
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")
        self._set_signal()
        self._open_file()

    def _set_signal(self):
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveRealData.connect(self._receive_real_data)

    # 키움 서버 로그인 함수
    def log_in(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def _event_connect(self, err_code):
        if err_code == 0:
            print('Successfully Connected')
        else:
            print('error : ' + str(err_code))
        self.login_event_loop.exit()

    # 종목코드 반환 함수
    # market : 0 = 장내 / 10 = 코스닥 / 3 = ELW / 8 = ETF / 50 = KONEX / 4 = 뮤추얼펀드 / 5 = 신주인수권 / 6 = 리츠
    def get_code_list(self, market):
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market)
        code_list = code_list.split(';')
        return code_list

    # 실시간 데이터 수신 설정 함수
    # screen_no = 화면번호 / code = 종목코드 / fid_list = 감시 리스트(string, ; 로 구별)
    # opt_type = 1 (0은 현재 등록하는 종목만 등록 / 1은 추가 등록)
    def set_real_reg(self, screen_no, code, fid_list, opt_type):
        screen_no = str(screen_no)
        code = str(code)
        fid_list = str(fid_list)
        opt_type = str(opt_type)

        self.dynamicCall("SetRealReg(QString, QString, QString, int", screen_no, code, fid_list, opt_type)

    def _receive_real_data(self, code, real_type, real_data):
        if real_type == '주식호가잔량':
            data = list()
            data.append(str(code))
            data.append(time.time())
            for i in range(10):
                data.append(str(abs(int(self._get_real_data(code, 51+i)))))  # 매수호가
                data.append(self._get_real_data(code, 71+i))  # 매수호가잔량
            for i in range(10):
                data.append(str(abs(int(self._get_real_data(code, 41+i)))))  # 매도호가
                data.append(self._get_real_data(code, 61+i))  # 매도호가잔량
            self.writer.writerow(data)

    def _get_real_data(self, code, fid):
        return self.dynamicCall("GetCommRealData(QString, QString)", code, fid)

    def _open_file(self):
        f = open('data.csv', 'a', encoding='utf-8', newline='')
        self.writer = csv.writer(f)
