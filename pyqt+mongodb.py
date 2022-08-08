from pymongo import MongoClient
import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

# <@> - @ 부분에 내 정보 입력
client = MongoClient("mongodb+srv://<my name>:<my password>@cluster0.grmlkbb.mongodb.net/Cluster0?retryWrites=true&w=majority")
   

db = client['test'] # test라는 이름의 데이터베이스에 접속
result = db['dust'].find().sort("_id", -1)

ls = []
ls1 = []
ls2 = []
for d, cnt in zip(result, range(100)):
    print(int(d['pm25']))
    ls.append(int(d['pm25']))
    ls1.append(int(d['pm1']))
    ls2.append(int(d['pm10']))
              
class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        canvas = FigureCanvas(Figure(figsize=(4, 3)))
        vbox = QVBoxLayout(self.main_widget)
        vbox.addLayout(self.vbox1)
        vbox.addLayout(self.vbox2)
        vbox.addWidget(canvas)
        
        self.ax = canvas.figure.subplots()  # 좌표축 준비
        self.timer = canvas.new_timer(
          100, [(self.update_canvas, (), {})]
        )     
        self.timer.start()
      
        #self.ax.plot([i for i in range(100, 0, -1)], ls, '-')

        self.setWindowTitle('실내 미세먼지 농도 측정기')
        self.setGeometry(300, 100, 600, 400)
        self.show()
        
    def update_canvas(self):
        self.ax.clear()
        test = db['dust'].find().sort("_id", -1)
        for d, cnt in zip(test, range(1)):
            print(float(d['pm25']))
            ls.append(float(d['pm25']))
            ls1.append(float(d['pm1']))
            ls2.append(float(d['pm10']))
        print(ls[-100:-1])
        self.ax.plot(ls[-100:-1], color="blue")
        self.ax.plot(ls1[-100:-1], color="red")
        self.ax.plot(ls2[-100:-1], color="yellow")
        
        self.ax.figure.canvas.draw()
        self.current.setText(f'현재 실내 미세먼지 농도는 {int(ls[-1])} 입니다.')
        
        if ls[-1] < 3:
            self.icon.setPixmap(QPixmap('매우좋음.png'))
            self.label.setText('매우좋음')
            self.label.setAlignment(Qt.AlignVCenter)
            self.icon.setAlignment(Qt.AlignRight)
        elif 3 <= ls[-1] <= 5:
            self.icon.setPixmap(QPixmap('좋음.png'))
            self.label.setText('좋음')
            self.label.setAlignment(Qt.AlignVCenter)
            self.icon.setAlignment(Qt.AlignRight)
        elif 6 <= ls[-1] <= 8:
            self.icon.setPixmap(QPixmap('나쁨.png'))
            self.label.setText('나쁨')
            self.label.setAlignment(Qt.AlignVCenter)
            self.icon.setAlignment(Qt.AlignRight)
        else:
            self.icon.setPixmap(QPixmap('매우나쁨.png'))
            self.label.setText('매우나쁨')
            self.label.setAlignment(Qt.AlignVCenter) 
            self.icon.setAlignment(Qt.AlignRight) 
      
    def initUI(self):
        self.img()      
        
        self.vbox1 = QHBoxLayout()
        self.vbox2 = QHBoxLayout()
        self.vbox3 = QHBoxLayout()
        
        self.vbox1.addWidget(self.current)
        self.vbox2.addWidget(self.icon)
        self.vbox2.addWidget(self.label)

    def img(self):
        self.icon = QLabel(self)
        self.current = QLabel('현재 실내 미세먼지 농도는 %d 입니다.' %(ls[0]), self)
        self.current.setAlignment(Qt.AlignCenter)
        
        if ls[-1] < 3:
            self.icon.setPixmap(QPixmap('매우좋음.png'))
            self.label = QLabel('매우좋음', self)
            self.label.setAlignment(Qt.AlignVCenter)
            self.icon.setAlignment(Qt.AlignRight)
        elif 3 <= ls[-1] <= 5:
            self.icon.setPixmap(QPixmap('좋음.png'))
            self.label = QLabel('좋음', self)
            self.label.setAlignment(Qt.AlignVCenter)
            self.icon.setAlignment(Qt.AlignRight)
        elif 6 <= ls[-1] <= 8:
            self.icon.setPixmap(QPixmap('나쁨.png'))
            self.label = QLabel('나쁨', self)
            self.label.setAlignment(Qt.AlignVCenter)
            self.icon.setAlignment(Qt.AlignRight)
        else:
            self.icon.setPixmap(QPixmap('매우나쁨.png'))
            self.label = QLabel('매우나쁨', self) 
            self.label.setAlignment(Qt.AlignVCenter) 
            self.icon.setAlignment(Qt.AlignRight) 
        
        self.icon.move(100, 50)


app = QApplication(sys.argv)
ex = MyApp()
app.exec_()
