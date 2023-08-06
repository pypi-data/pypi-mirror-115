import ctypes
import datetime
import glob
import subprocess
import threading
import time
import socket
import serial
import sys
from PySide2.QtCore import QTimer
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import QDateTime
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtGui import QColor
from PySide2.QtWidgets import *
from Sylvac import DataBase
from Sylvac.ui_main import Ui_MainDis
import argparse
# import qdarkstyle
# import matplotlib



from PySide2 import QtCore, QtWidgets
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import pandas as pd

# matplotlib.use('Qt5Agg')

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class GetCom(threading.Thread):

    def __init__(self, LsrData, LstCom):
        threading.Thread.__init__(self)
        self.Data = LsrData
        self.LstCom = LstCom

    def serial_ports(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def run(self):
        if len(self.LstCom) == 0:
            for item in self.serial_ports():
                self.LstCom.append(item)
        else:
            self.LstCom.clear()
            for item in self.serial_ports():
                self.LstCom.append(item)
        print('Hoan Thanh')


def UpdateDict(dictupdate, di):
    di.update(dictupdate)


def is_connected():
    try:
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        print('Khong co ket noi Internet')
        pass
    return False


def restart():
    print("restarting Pi")
    command = "/usr/bin/sudo /sbin/shutdown -r now"
    import subprocess
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)
    pass


def CapNhat():
    if is_connected():
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'Sylvac'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'Sylvac'])
        restart()
        print('Hoan Thanh')


class ThreadReadvalue(threading.Thread):
    def __init__(self, Serial, Com, threadLock, dataReader, gui, nameThread, dtaCsdl, lstIdUpdate):
        threading.Thread.__init__(self)
        self.Serial = Serial
        self.Com = Com
        self.ThreadLock = threadLock
        self.DataReader = dataReader
        self.Gui = gui
        self.NameThread = nameThread
        self.DtaCsdl = dtaCsdl
        self.LstIdUpdate = lstIdUpdate
        self.iDNgay = 0

    @property
    def SetId(self):
        return self.iDNgay

    @SetId.setter
    def SetId(self, idgay):
        self.iDNgay = idgay

    def run(self):
        num = 0
        if not self.Serial.isOpen():

            self.Serial = serial.Serial(port=self.Com,
                                        baudrate=4800,
                                        bytesize=7,
                                        timeout=1,
                                        stopbits=serial.STOPBITS_TWO,
                                        parity=serial.PARITY_EVEN
                                        )

            self.Serial.setDTR(True)
            self.Serial.setRTS(True)

            requet = 'TOL?' + chr(13)

            self.Serial.write(requet.encode('ASCII'))

            while num < 2:
                if self.Serial.in_waiting > 0 and self.Serial.isOpen():
                    Maxmin = self.Serial.readline().decode('utf-8')
                    lsrMaxmin = Maxmin.split()
                    Min = lsrMaxmin[0]
                    Max = lsrMaxmin[1]
                    if self.NameThread == 'Thou1':
                        self.Gui.lbDlimit1.setText(
                            '<p align="right"><span style=" color:#ffaa7f;">' + Min + '</span></p>')
                        self.Gui.lbuplimit1.setText(
                            '<p align="right"><span style=" color:#55ff00;">' + Max + '</span></p>')
                    if self.NameThread == 'Thou2':
                        self.Gui.lbDlimit2.setText(
                            '<p align="right"><span style=" color:#ffaa7f;">' + Min + '</span></p>')
                        self.Gui.lbuplimit2.setText(
                            '<p align="right"><span style=" color:#55ff00;">' + Max + '</span></p>')
                time.sleep(0.5)
                num += 1
            sic1 = {'Thou1': [0.0, 0.0, 0.0]}
            sic2 = {'Thou2': [0.0, 0.0, 0.0]}
            SolanDoThuoc = 0
            SolanDoThuoc2 = 0

            while 1:
                try:
                    if self.Serial.in_waiting > 0 and self.Serial.isOpen():
                        self.ThreadLock.acquire()
                        value = self.Serial.readline().decode('utf-8')
                        if num == 0:
                            print(self.Serial.readline().decode('utf-8'))
                            num = 1
                        else:
                            num = 1
                            lstva = value.split()
                            valuedt = float(lstva[0].split('+0')[1])
                            if self.NameThread == 'Thou1' and SolanDoThuoc <= 2:
                                if lstva[1] == '=':
                                    sic1['Thou1'][SolanDoThuoc] = valuedt
                                    self.Gui.lbvalue.setText(
                                        '<p align="center"><span style=" font-size:36pt; color:#55ff00;">' + str(
                                            valuedt) + '</span></p>')
                                else:
                                    sic1['Thou1'][SolanDoThuoc] = valuedt
                                    self.Gui.lbvalue.setText(
                                        '<p align="center"><span style=" font-size:36pt; color:#ff5500;">' + str(
                                            valuedt) + '</span></p>')
                                SolanDoThuoc += 1
                                self.Gui.lbsoluong.setText('<p align="center"><span style=" color:#0000ff;">'+str(SolanDoThuoc)+'-'+str(SolanDoThuoc2)+'-' + str(self.SetId) + '</span></p>')
                            elif self.NameThread == 'Thou2' and SolanDoThuoc2 == 0:
                                if lstva[1] == '=':
                                    sic2['Thou2'][SolanDoThuoc2] = valuedt
                                    self.Gui.lbvalue_2.setText('<p align="center"><span style=" font-size:36pt; '
                                                               'color:#55ff00;">' + str(valuedt) + '</span></p>')
                                else:
                                    sic2['Thou2'][SolanDoThuoc2] = valuedt
                                    self.Gui.lbvalue_2.setText('<p align="center"><span style=" font-size:36pt; '
                                                               'color:#ff5500;">' + str(valuedt) + '</span></p>')
                                SolanDoThuoc2 += 1

                            if SolanDoThuoc2 >= 1:
                                UpdateDict(sic2, self.DataReader)
                                SolanDoThuoc2 = 0
                                if self.DataReader['Thou2'][0] != 0.0:
                                    if len(self.LstIdUpdate) > 0:
                                        for idUpdate in self.LstIdUpdate:
                                            sql = "UPDATE DBML01_V02 SET Phi_42_00 =%s, Phi_42_45 =%s, Phi_42_90 =%s WHERE Id=%s"
                                            val = (self.DataReader['Thou2'][0], self.DataReader['Thou2'][1], self.DataReader['Thou2'][2], idUpdate)
                                            self.DtaCsdl.UpdateData(query=sql, lstParameter=val)
                                            up = {'Thou2': [0.0, 0.0, 0.0]}
                                            UpdateDict(up, self.DataReader)
                                            self.LstIdUpdate.remove(idUpdate)
                                            self.Gui.lbsoluong.setText('<p align="center"><span style=" color:#0000ff;">'+str(SolanDoThuoc)+'-'+str(SolanDoThuoc2)+'-' + str(self.SetId) + '</span></p>')
                                            break

                            if SolanDoThuoc == 3:
                                UpdateDict(sic1, self.DataReader)
                                SolanDoThuoc = 0
                                if 0.0 not in self.DataReader['Thou1']:
                                    # Insert dữ liệu lên Sql
                                    Ngay = datetime.date.today()
                                    Times = datetime.datetime.now().strftime("%H:%M:%S")
                                    # Lấy số thứ tự đếm số lượng
                                    query = "SELECT MAX(STT) FROM DBML01_V02 WHERE Ngay = %s"
                                    val = (str(Ngay),)
                                    dta = self.DtaCsdl.GetData(query, val)[0]
                                    if dta[0] is None:
                                        self.SetId = 1
                                    else:
                                        self.SetId = dta[0] + 1

                                    idDta = str(Ngay) + '|' + str(Times)

                                    sql = "INSERT INTO DBML01_V02 () VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

                                    val = (idDta, str(Ngay), Times, self.SetId, self.DataReader['Thou1'][0],
                                           self.DataReader['Thou1'][1], self.DataReader['Thou1'][2], 0.0, 0.0, 0.0, '')

                                    self.DtaCsdl.InsertData(query=sql, lstValue=val)
                                    self.LstIdUpdate.append(idDta)
                                    up = {'Thou1': [0.0, 0.0, 0.0]}
                                    UpdateDict(up, self.DataReader)
                                self.Gui.lbsoluong.setText('<p align="center"><span style=" color:#0000ff;">'+str(SolanDoThuoc)+'-'+str(SolanDoThuoc2)+'-' + str(self.SetId) + '</span></p>')
                            pass

                        self.ThreadLock.release()
                except Exception as e:
                    print(str(e))
                    self.ThreadLock.release()
                    pass
                time.sleep(0.1)
            pass

    def ClostCom(self):
        if self.Serial.isOpen():
            self.Serial.close()
            print('Da ngat ket noi')
            pass
        pass

    def get_id(self):
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for idThread, thread in threading._active.items():
            if thread is self:
                return idThread
            pass
        pass

    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')
            pass
        pass


class Thuoc:
    def __init__(self, name, thread):
        self.Name = name
        self.Thread = thread


class MainWindown(QMainWindow):
    lstThuoc = []

    def __init__(self, Dulieudoc, lstCOM, threadLock, dtaCsdl):
        QMainWindow.__init__(self)
        self.ui = Ui_MainDis()
        self.ui.setupUi(self)


        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 92, 157,125))

        self.ui.centralwidget.setGraphicsEffect(self.shadow)
        self.setWindowIcon((QtGui.QIcon(u":/icons/github.svg")))
        self.setWindowTitle("DEVICES MEASUREMENTS")

        # # Create Chart
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        #
        # df = pd.DataFrame([
        #    [0, 10], [5, 15], [2, 20], [15, 25], [4, 10],
        # ], columns=['A', 'B'])
        #
        # df.plot(ax=sc.axes)
        #
        # # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        #
        toolbar = NavigationToolbar(sc, self)
        toolbar.zoom(True)

        self.ui.LayoutChart.addWidget(toolbar)
        self.ui.LayoutChart.addWidget(sc)

        self.ui.cb1.addItems(lstCOM)
        self.ui.cb2.addItems(lstCOM)

        self.ThreadLock = threadLock
        self.DuLieu = Dulieudoc
        self.DtaCsdl = dtaCsdl
        self.LstIdUpdate = []
        self.serialPort = serial.Serial()

        self.ui.btnMain.clicked.connect(lambda: self.Dlsmain())

        self.ui.btnChart.clicked.connect(lambda: self.DlsChart())

        self.ui.btnKetNoi.clicked.connect(lambda: self.Connect_Com())
        self.ui.btnThoat.clicked.connect(lambda: self.Dongketnoi('Thou1'))
        # self.ui.btnChart.actions()

        self.serialPort2 = serial.Serial()
        self.ui.btnKetNoi_2.clicked.connect(lambda: self.Connect_Com2())
        self.ui.btnThoat_2.clicked.connect(lambda: self.Dongketnoi('Thou2'))

        self.ui.lbsoluong.setText('<p align="center"><span style=" color:#0000ff;">0</span></p>')

        # Thoat phần mềm bằng nút Exit
        self.ui.btnExit.clicked.connect(self.Exit)

        # Cập nhật phần mềm
        self.ui.btnUpdate.clicked.connect(self.UpdateSoftware)

        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

        # self.showMaximized()
        # self.showMaximized()
        self.showNormal()

    def Dlsmain(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Page_misure)
        pass

    def DlsChart(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.Page_chart)
        pass

    def showTime(self):
        times = QDateTime.currentDateTime()
        timeDisplay = times.toString('yyyy-MM-dd hh:mm:ss dddd')
        self.ui.lbTime.setText(
            '<html><head/><body><p align="center"><span style=" color:#00CBff;">' + timeDisplay + '</span></p></body></html>')

    def Connect_Com2(self):
        content = self.ui.cb2.currentText()
        self.ui.cb2.setDisabled(True)
        self.ui.btnKetNoi_2.setDisabled(True)
        th1 = ThreadReadvalue(self.serialPort2, content, threadLock=self.ThreadLock, dataReader=self.DuLieu,
                              gui=self.ui,
                              nameThread='Thou2', dtaCsdl=self.DtaCsdl, lstIdUpdate=self.LstIdUpdate)
        thuoc = Thuoc(name='Thou2', thread=th1)

        if len(self.lstThuoc) == 0:
            self.lstThuoc.append(thuoc)
            th1.setDaemon(True)
            th1.start()
        else:
            for th in self.lstThuoc:
                if th.Name != thuoc.Name:
                    self.lstThuoc.append(thuoc)
                    th1.setDaemon(True)
                    th1.start()

    def Connect_Com(self):
        content = self.ui.cb1.currentText()
        self.ui.cb1.setDisabled(True)
        self.ui.btnKetNoi.setDisabled(True)
        th1 = ThreadReadvalue(self.serialPort, content, threadLock=self.ThreadLock,
                              dataReader=self.DuLieu, gui=self.ui,
                              nameThread='Thou1', dtaCsdl=self.DtaCsdl,
                              lstIdUpdate=self.LstIdUpdate)
        thou = Thuoc(name='Thou1', thread=th1)

        if len(self.lstThuoc) == 0:
            self.lstThuoc.append(thou)
            th1.setDaemon(True)
            th1.start()
        else:
            for th in self.lstThuoc:
                if th.Name != thou.Name:
                    self.lstThuoc.append(thou)
                    th1.setDaemon(True)
                    th1.start()

    def Dongketnoi(self, namethread):
        if namethread == 'Thou1':
            self.ui.cb1.setDisabled(False)
            self.ui.btnKetNoi.setDisabled(False)
        elif namethread == 'Thou2':
            self.ui.cb2.setDisabled(False)
            self.ui.btnKetNoi_2.setDisabled(False)

        for th in self.lstThuoc:
            if th.Name == namethread:
                th.Thread.ClostCom()
                th.Thread.raise_exception()
                self.lstThuoc.remove(th)
                print('Thoat thread ', th.Name)

    def Exit(self):
        self.DtaCsdl.Closed()
        app.quit()

    def UpdateSoftware(self):
        th = threading.Thread(target=CapNhat)
        th.start()
        time.sleep(1)
        self.Exit()
        pass

    def closeEvent(self, event) -> None:
        close = QtWidgets.QMessageBox.question(self,
                                               "Thoát ứng dụng?",
                                               "Bạn muốn thoát ứng dụng???",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if close == QtWidgets.QMessageBox.Yes:
            sys.exit()
            self.DtaCsdl.Closed()
        else:
            self.DtaCsdl.Closed()
            pass
        pass


threadlock = []  # có 2 phần tử, chứa giá trị của thước thứ 1 và thứ 2
app = QApplication(sys.argv)
Dta = {'Thou1': [0.0, 0.0, 0.0], 'Thou2': [0.0, 0.0, 0.0]}

lstCom = []
# try:
DtaCsdl = DataBase()
# except Exception as e:
#     print(str(e))
#     th = threading.Thread(target=CapNhat)
#     th.start()

threadlock = threading.Lock()


def Run():
    # try:
    ThreadValue = GetCom(LsrData=Dta, LstCom=lstCom)
    ThreadValue.run()
    print(lstCom)
    windown = MainWindown(Dulieudoc=Dta, lstCOM=lstCom, threadLock=threadlock, dtaCsdl=DtaCsdl)
    # except Exception as e:
    #     print("Loi nay ne: " + str(e))
    #     windown.UpdateSoftware()

    # windown.setStyleSheet(qdarkstyle._load_stylesheet())

    sys.exit(app.exec_())


if __name__ == '__main__':
    Run()

