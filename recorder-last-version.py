import sys
from PyQt5.QtWidgets import  QMainWindow, QApplication
from PyQt5 import QtCore, QtGui, QtWidgets 
import dxcam,cv2,os
import threading


fps = 0
pause_state = False
exit_state = False
record_state = False
video_name = 'video'
def grab():
    global fps
    global pause_state
    global exit_state
    global video_name
    global record_state
    TOP = 0
    LEFT = 0
    RIGHT = 1920
    BOTTOM = 1080
    region = (LEFT, TOP, RIGHT, BOTTOM)
    title = "[DXcam] Capture benchmark"
    # print(fps)
    fps = 8
    # print(fps)
    camera = dxcam.create(output_idx=0, output_color="BGR")
    camera.start(target_fps=fps, video_mode=True)
    writer = cv2.VideoWriter(
        f"{video_name}.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (1920, 1080)
    )
    a = 0
    while True:
        # print(a)
        writer.write(camera.get_latest_frame())
        a = a+1
        # print(a)
        if pause_state == True:
            while True:
                if pause_state == False or exit_state == True:
                    break
        if pause_state == False and exit_state == True:
             break
        elif exit_state == True:
            break
    camera.stop()
    writer.release()

class MyWindow(QMainWindow): 

    def __init__(self):
        super(MyWindow,self).__init__()
        self.resize(687,478)
        self.setObjectName("Hy-Recorder")
        self.setWindowTitle('Hy-Recorder')
        self.gridLayoutWidget = QtWidgets.QWidget(self)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(130, 110, 311, 81))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.name = QtWidgets.QLineEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name.sizePolicy().hasHeightForWidth())
        self.name.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.name.setFont(font)
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        
        self.fps = QtWidgets.QLineEdit(self)
        self.fps.setGeometry(QtCore.QRect(450, 140, 121, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fps.sizePolicy().hasHeightForWidth())
        self.fps.setSizePolicy(sizePolicy)
        self.fps.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.fps.setFont(font)
        self.fps.setObjectName("fps")
        
        self.record = QtWidgets.QPushButton(self)
        self.record.setGeometry(QtCore.QRect(130, 210, 101, 81))
        self.record.setObjectName("pushButton")
        
        self.pause = QtWidgets.QPushButton(self)
        self.pause.setGeometry(QtCore.QRect(240, 210, 101, 81))
        self.pause.setObjectName("pushButton_2")
        
        self.continue_btn = QtWidgets.QPushButton(self)
        self.continue_btn.setGeometry(QtCore.QRect(350, 210, 101, 81))
        self.continue_btn.setObjectName("pushButton_3")
        
        self.exit = QtWidgets.QPushButton(self)
        self.exit.setGeometry(QtCore.QRect(470, 210, 101, 81))
        self.exit.setObjectName("pushButton_4")
       

    
        _translate = QtCore.QCoreApplication.translate
        self.label_2.setText(_translate("MainWindow", "FPS:"))
        self.label.setText(_translate("MainWindow", "Video Name:"))
        self.record.setText(_translate("MainWindow", "Record"))
        self.pause.setText(_translate("MainWindow", "Pause"))
        self.continue_btn.setText(_translate("MainWindow", "Continue"))
        self.exit.setText(_translate("MainWindow", "Exit & Save"))

        
        self.pause.clicked.connect(self.pause_stream)
        self.exit.clicked.connect(self.exit_stream)
        self.continue_btn.clicked.connect(self.con_stream)
        self.record.clicked.connect(self.recorder)

        self.continue_btn.setStyleSheet("color : rgba(0, 0, 0, 100)")
        self.pause.setStyleSheet("color : rgba(0, 0, 0, 100)")
        self.exit.setStyleSheet("color : rgba(0, 0, 0, 100)")

        self.pause.setEnabled(False)
        self.exit.setEnabled(False)
        self.continue_btn.setEnabled(False)
        
    def recorder(self):
        global video_name,fps
        # global record_state
        video_name = str(self.name.text())
        fps= int(self.fps.text())
        self.record.setEnabled(False)
        self.pause.setEnabled(True)
        self.pause.setStyleSheet("color :color: #fff;")
        self.exit.setStyleSheet("color :color: #fff;")
        self.exit.setEnabled(True)
        # record_state = True
        th.start()
       
    def pause_stream(self):
        global pause_state
        pause_state = True
        self.continue_btn.setStyleSheet("color :color: #fff;")
        self.continue_btn.setEnabled(True)

    def con_stream(self):
        global pause_state
        pause_state = False

    def exit_stream(self):
        global exit_state
        exit_state = True
        self.record.setEnabled(True)
        self.name.clear()
        # record_state =False
        print(sys.executable)
        print(sys.argv)
        self.close()
        QtCore.QCoreApplication.quit()
        os.system("recorder_interface.py 1")
       
th = threading.Thread(target=grab)

def window():
    app = QApplication(sys.argv) # bir app oluşturup sistemdeki arg leri attık # zetcode da bak
    win = MyWindow()
    
    style = """


QWidget
{
    color: #fff;
    background-color: #323232;
    
}

QWidget:item:hover
{
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #D1DBCB, stop: 1 #b2b6af);
    color: #000000;
}

QWidget:item:selected
{
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #D1DBCB, stop: 1 #b2b6af);
}

QMenuBar::item
{
    background: transparent;
}

QMenuBar::item:selected
{
    background: transparent;
    border: 1px solid #fdf6e3;
}

QMenuBar::item:pressed
{
    background: #444;
    border: 1px solid #000;
    background-color: QLinearGradient(
        x1:0, y1:0,
        x2:0, y2:1,
        stop:1 #212121,
        stop:0.4 #343434/*,
        stop:0.2 #343434,
        stop:0.1 #fdf6e3*/
    );
    margin-bottom:-1px;
    padding-bottom:1px;
}

QMenu
{
    border: 1px solid #000;
}

QMenu::item
{
    padding: 2px 20px 2px 20px;
}

QMenu::item:selected
{
    color: #000000;
}

QWidget:disabled
{
    color: #404040;
    background-color: #323232;
}

QAbstractItemView
{
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0.1 #646464, stop: 1 #5d5d5d);
}

QWidget:focus
{
    /*border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0
     #D1DBCB, stop: 1 #b2b6af);*/
}

QLineEdit
{
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);
    padding: 1px;
    border-style: solid;
    border: 1px solid #1e1e1e;
    border-radius: 5;
}

QPushButton
{
    color: #fff;
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);
    border-width: 1px;
    border-color: #1e1e1e;
    border-style: solid;
    border-radius: 6;
    font-size: 20px;
    
}

QPushButton:pressed
{
    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);
}


QTextEdit
{
    background-color: #242424;
}

QPlainTextEdit
{
    background-color: #242424;
}

QHeaderView::section
{
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #616161, stop: 0.5 #505050, stop: 0.6 #434343, stop:1 #656565);
    color: white;
    padding-left: 4px;
    border: 1px solid #6c6c6c;
}




QMainWindow::separator
{
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);
    color: white;
    padding-left: 4px;
    border: 1px solid #4c4c4c;
    spacing: 3px; /* spacing between items in the tool bar */
}

QMainWindow::separator:hover
{

    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #b2b6af,
    stop:0.5 #b56c17 stop:1 #D1DBCB);
    color: white;
    padding-left: 4px;
    border: 1px solid #6c6c6c;
    spacing: 3px; /* spacing between items in the tool bar */
}

QToolBar {
    border: 1px transparent #323232;
    background: 1px solid #323232;
}

QToolBar::handle
{
     spacing: 3px; /* spacing between items in the tool bar */
     background: url(:/images/handle.png);
}

QMenu::separator
{
    height: 2px;
    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);
    color: white;
    padding-left: 4px;
    margin-left: 10px;
    margin-right: 5px;
}



"""
    app.setStyleSheet(style)
    win.show() # pencereyi başlattık
    sys.exit(app.exec_()) # pencereyi kapatabilmek için x tuşunu aktif hale getirdik

window()

    
