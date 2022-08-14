# Fine_dust_data_visualization_koss4week


* 구현 영상

https://user-images.githubusercontent.com/104904309/183557590-e68a869e-2d9e-4be8-88f0-168034867f3c.mp4



https://user-images.githubusercontent.com/104904309/183557591-722ab7ef-7df1-4a7b-a446-290406c040eb.mp4



https://user-images.githubusercontent.com/104904309/183557679-9592e765-c710-46cd-8a1e-5554a55b35b6.mp4



https://user-images.githubusercontent.com/104904309/183557682-2ffcfee3-af6a-4a7a-ae65-456ec44c0d0f.mp4



* 파이썬 코드 line by line

```python
from pymongo import MongoClient # python에서 mongodb로 데이터를 보내고 받을 때 쓰기 위함
import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas # PyQt5 어플리케이션에서 그림이 그려질 캔버스 불러옴
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar # 툴바 불러오기
from matplotlib.figure import Figure

# <@> - @ 부분에 내 정보 입력, cluser0의 안의 데이터베이스를 이용
client = MongoClient("mongodb+srv://<my name>:<my password>@cluster0.grmlkbb.mongodb.net/Cluster0?retryWrites=true&w=majority")
   

db = client['test'] # test라는 이름의 데이터베이스에 접속
result = db['dust'].find().sort("_id", -1) # "dust"라는 콜렉션 이름에서 "_id"라는 키값으로 최근값부터 가져오기

ls = [] # 미세먼지 데이터를 저장할 빈 리스트 생성
ls1 = [] # 미세먼지 데이터를 저장할 빈 리스트 생성
ls2 = [] # 미세먼지 데이터를 저장할 빈 리스트 생성
for d, cnt in zip(result, range(100)):
    print(int(d['pm25']))
    ls.append(int(d['pm25'])) # empty list ls에 'pm25'값을 int형식으로 추가
    ls1.append(int(d['pm1'])) # empty list ls1에 'pm1'값을 int형식으로 추가
    ls2.append(int(d['pm10'])) # empty list ls2에 'pm10'값을 int형식으로 추가
              
class MyApp(QMainWindow): # QMainWindow 클래스를 상속받은 MtApp 클래스 생성
    def __init__(self):
        super().__init__() # 다른 클래스의 속성, 메소드를 불러옴
        self.initUI()

        self.main_widget = QWidget() # 프로그램의 메인 위젯 설정
        self.setCentralWidget(self.main_widget) # 메인 위젯 가운데 정렬 설정

        canvas = FigureCanvas(Figure(figsize=(4, 3)))
        vbox = QVBoxLayout(self.main_widget)
        vbox.addLayout(self.vbox1) # 수직 layout 추가
        vbox.addLayout(self.vbox2) # 수직 layout 추가
        vbox.addWidget(canvas) # addWidget 메서드로 위젯 등록
        
        self.ax = canvas.figure.subplots()  # 좌표축 준비
        self.timer = canvas.new_timer(  #0.1초마다 그래프 업데이트
          100, [(self.update_canvas, (), {})]
        )     
        self.timer.start() # 타이머 시작
      
        #self.ax.plot([i for i in range(100, 0, -1)], ls, '-')

        self.setWindowTitle('실내 미세먼지 농도 측정기') # 타이틀바에 나타나는 창의 제목 설정
        self.setGeometry(300, 100, 600, 400) # 창의 크기 설정
        self.show() # 창 띄우기
        
    def update_canvas(self):
        self.ax.clear() # 그래프 figure 초기화
        test = db['dust'].find().sort("_id", -1) # "dust"라는 콜렉션 이름에서 "_id"라는 키값으로 최근값부터 가져오기
        for d, cnt in zip(test, range(1)):
            print(float(d['pm25']))
            ls.append(float(d['pm25'])) # empty list ls에 'pm25'값을 float형식으로 추가
            ls1.append(float(d['pm1'])) # empty list ls에 'pm1'값을 float형식으로 추가
            ls2.append(float(d['pm10']))# empty list ls에 'pm10'값을 float형식으로 추가
        print(ls[-100:-1])
        self.ax.plot(ls[-100:-1], color="blue") # 'pm25'값을 파란색으로 최근값부터 그래프 나타냄
        self.ax.plot(ls1[-100:-1], color="red") # 'pm1'값을 빨간색으로  최근값부터 그래프 나타냄
        self.ax.plot(ls2[-100:-1], color="yellow") # 'pm10'값을 노란색으로  최근값부터 그래프 나타냄
        
        self.ax.figure.canvas.draw() # 그래프 그리기
        self.current.setText(f'현재 실내 미세먼지 농도는 {int(ls[-1])} 입니다.') # 실시간 실내 미세먼지 농도 업데이트 
        
        # 실시간 미세먼지 농도 임의로 값 설정하여 4단계로 나누는 조건문
        if ls[-1] < 3:
            self.icon.setPixmap(QPixmap('매우좋음.png')) # 현재 미세먼지 상태 사진 업데이트
            self.label.setText('매우좋음') # 현재 미세먼지 상태 업데이트
            self.label.setAlignment(Qt.AlignVCenter) # 라벨의 배치 중앙으로
            self.icon.setAlignment(Qt.AlignRight) # 사진의 배치 중앙으로
        elif 3 <= ls[-1] <= 5:
            self.icon.setPixmap(QPixmap('좋음.png')) # 현재 미세먼지 상태 사진 업데이트
            self.label.setText('좋음') # 현재 미세먼지 상태 업데이트
            self.label.setAlignment(Qt.AlignVCenter) # 라벨의 배치 중앙으로
            self.icon.setAlignment(Qt.AlignRight) # 사진의 배치 중앙으로
        elif 6 <= ls[-1] <= 8:
            self.icon.setPixmap(QPixmap('나쁨.png')) # 현재 미세먼지 상태 사진 업데이트
            self.label.setText('나쁨') # 현재 미세먼지 상태 업데이트
            self.label.setAlignment(Qt.AlignVCenter) # 라벨의 배치 중앙으로
            self.icon.setAlignment(Qt.AlignRight) # 사진의 배치 중앙으로
        else:
            self.icon.setPixmap(QPixmap('매우나쁨.png')) # 현재 미세먼지 상태 사진 업데이트
            self.label.setText('매우나쁨') # 현재 미세먼지 상태 업데이트
            self.label.setAlignment(Qt.AlignVCenter) # 라벨의 배치 중앙으로
            self.icon.setAlignment(Qt.AlignRight)  # 사진의 배치 중앙으로
      
    def initUI(self): # 초기 UI함수
        self.img()      
        
        self.vbox1 = QHBoxLayout() # 위젯 가로방향 나열
        self.vbox2 = QHBoxLayout() # 위젯 가로방향 나열
        self.vbox3 = QHBoxLayout() # 위젯 가로방향 나열
        
        self.vbox1.addWidget(self.current) # vbox1에 현재 미세먼지 상태 등록
        self.vbox2.addWidget(self.icon) # vbox2에 현재 미세먼지 상태 사진 등록
        self.vbox2.addWidget(self.label) # vbox2에 현재 미세먼지 상태 등록
 
    #  값과 사진이 업데이트되는 데이터에 따라 다른 update_canvas() 함수와 별개로 기본값으로 설정
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
        
        self.icon.move(100, 50) # 사진 위치 설정


app = QApplication(sys.argv) # QApplication의 생성자 호출,  QT 응용 프로그램을 초기화하기 위해 sys.argv 사용
ex = MyApp()
app.exec_() # 프로그램이 꺼지지않도록 무한 루프상태로 만들어 대기 상태에 머무름
```
