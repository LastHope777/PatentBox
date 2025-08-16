from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFontDatabase
import os


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 768)
        MainWindow.setWindowFlags(QtCore.Qt.Window |
                                  QtCore.Qt.WindowCloseButtonHint |
                                  QtCore.Qt.WindowMinimizeButtonHint)
        MainWindow.setFixedSize(MainWindow.size())
        MainWindow.setWindowTitle("Патент Бокс")
        MainWindow.setStyleSheet("background-color: white;")

        # Загружаем кастомные шрифты
        font_path_black = os.path.join(os.getcwd(), "Geologica-Black.ttf")
        font_path_bold = os.path.join(os.getcwd(), "Geologica-Bold.ttf")
        font_path_semibold = os.path.join(os.getcwd(), "Geologica-SemiBold.ttf")

        QFontDatabase.addApplicationFont(font_path_black)
        QFontDatabase.addApplicationFont(font_path_bold)
        QFontDatabase.addApplicationFont(font_path_semibold)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")



        # Верхний подзаголовок
        self.label_top = QtWidgets.QLabel(self.centralwidget)
        self.label_top.setGeometry(QtCore.QRect(288, 100, 455, 80))
        self.label_top.setTextFormat(QtCore.Qt.RichText)
        self.label_top.setText("""
        <p style='line-height:60%; margin:0; text-align:center;'>
            <span style='color:#3C4189;'>Ваш умный помощник в мире интеллектуальной собственности</span>
        </p>
        """)
        self.label_top.setWordWrap(True)
        self.label_top.setAlignment(QtCore.Qt.AlignCenter)

        # ✅ Применяем Semibold
        font = QtGui.QFont("Geologica Semibold", 10)
        self.label_top.setFont(font)

        # Стиль
        self.label_top.setStyleSheet("""
            background-color:#BEC2FF;
            padding-right: 15px;
            padding-left: 15px;
            padding-top: 8px;
            padding-bottom: 15px;
            border-radius: 16px;
        """)

        # Шрифт
        font = QtGui.QFont("Geologica Semibold", 12)
        self.label_top.setFont(font)

        # Отступы: добавляем +4 пикселя снизу для выравнивания
        self.label_top.setStyleSheet("""
            background-color:#BEC2FF;
            padding-right: 15px;
            padding-left: 15px;
            padding-top: 2px;
            padding-bottom: 20px;   /* увеличено на 4px */
            border-radius: 16px;
        """)

        # Основной заголовок
        self.label_title = QtWidgets.QLabel(self.centralwidget)
        self.label_title.setGeometry(QtCore.QRect(126, 120, 773, 252))
        self.label_title.setTextFormat(QtCore.Qt.RichText)
        self.label_title.setText("""
        <p style='line-height:60%; margin:0;'>
            <span style='color:#383535;'>Добро пожаловать в </span>
            <span style='color:#0011FF;'>Патент Бокс!</span>
        </p>
        """)
        self.label_title.setWordWrap(True)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        font = QtGui.QFont("Geologica Black", 44)
        self.label_title.setFont(font)

        # ✅ Убираем белый фон
        self.label_title.setStyleSheet("background-color: transparent;")

        # Кнопка "НАЧАТЬ РАБОТУ"
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setGeometry(QtCore.QRect(342, 492, 340, 70))
        self.pushButton_start.setText("НАЧАТЬ РАБОТУ")
        self.pushButton_start.setFont(QtGui.QFont("Geologica Black", 14))
        self.pushButton_start.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 17, 255, 1);
                color: white;
                border-radius: 16px;
            }
            QPushButton:hover {
                background-color: rgba(0, 17, 200, 1);
            }
        """)

        # Кнопка "ИНСТРУКЦИЯ"
        self.pushButton_help = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_help.setGeometry(QtCore.QRect(342, 570, 340, 70))
        self.pushButton_help.setText("ИНСТРУКЦИЯ")
        self.pushButton_help.setFont(QtGui.QFont("Geologica Black", 14))
        self.pushButton_help.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 183, 230, 1);
                color: white;
                border-radius: 16px;
            }
            QPushButton:hover {
                background-color: rgba(255, 150, 200, 1);
            }
        """)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        # Нижняя надпись
        self.label_title = QtWidgets.QLabel(self.centralwidget)
        self.label_title.setGeometry(QtCore.QRect(310, 690, 405, 50))
        self.label_title.setTextFormat(QtCore.Qt.RichText)
        self.label_title.setText("""
                <p style='line-height:60%; margin:0;'>
                    <span style='color:#383535;'>© 2025 ПатентБокс. Все права защищены.
                    Контакты: nikita_pishk@rambler.ru </span>
                </p>
                """)
        self.label_title.setWordWrap(True)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        font = QtGui.QFont("Geologica Semibold", 9)
        self.label_title.setFont(font)

        # ✅ Убираем белый фон
        self.label_title.setStyleSheet("background-color: transparent;")



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
