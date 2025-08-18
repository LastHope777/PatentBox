from PyQt5 import QtWidgets, QtGui, QtCore
import os


class Ui_InstructionWindow(object):
    def __init__(self):
        self.adapter_box = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("InstructionWindow")
        MainWindow.resize(1024, 768)
        MainWindow.setWindowFlags(QtCore.Qt.Window |
                                  QtCore.Qt.WindowCloseButtonHint |
                                  QtCore.Qt.WindowMinimizeButtonHint)
        MainWindow.setFixedSize(MainWindow.size())
        MainWindow.setWindowTitle("Патент Бокс")
        MainWindow.setStyleSheet("background-color: white;")

        # === Подключение шрифтов ===
        def load_font(path, fallback="Arial"):
            font_id = QtGui.QFontDatabase.addApplicationFont(path)
            if font_id == -1:
                return fallback
            return QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]

        font_family_black = load_font(os.path.join(os.getcwd(), "Geologica-Black.ttf"))
        font_family_bold = load_font(os.path.join(os.getcwd(), "Geologica_Auto-Bold.ttf"))
        font_family_semibold = load_font(os.path.join(os.getcwd(), "Geologica-SemiBold.ttf"))
        font_family_regular = load_font(os.path.join(os.getcwd(), "Geologica-Regular.ttf"))


        # Центральный виджет
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Кнопка "Назад"
        self.back_btn = QtWidgets.QPushButton("Назад", self.centralwidget)
        self.back_btn.setGeometry(30, 30, 138, 50)
        self.back_btn.setFont(QtGui.QFont(font_family_semibold, 10))
        self.back_btn.setStyleSheet("""
        QPushButton {
            background-color: #BEC2FF;
            color: #3C4189;
            border-radius: 10px;
        }
        QPushButton:hover {
            background-color: #DDE0FF;
        }
        """)
        # Стрелочка
        icon_path = os.path.join(os.getcwd(), "Vector.png")
        icon = QtGui.QIcon(icon_path)
        self.back_btn.setIcon(icon)
        self.back_btn.setIconSize(QtCore.QSize(24, 24))

        # Основной заголовок
        self.label_title = QtWidgets.QLabel(self.centralwidget)
        self.label_title.setGeometry(QtCore.QRect(30, 130, 420, 95))
        self.label_title.setTextFormat(QtCore.Qt.RichText)
        self.label_title.setText("""
        <p style='line-height:100%; margin:0;'>
            <span style='color:#383535;'>Инструкция</span>
        </p>
        """)
        self.label_title.setWordWrap(True)
        self.label_title.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        font = QtGui.QFont("Geologica Black", 38)
        self.label_title.setFont(font)
        # ✅ Убираем белый фон
        self.label_title.setStyleSheet("background-color: transparent;")

        # Назначение (Заголовок)
        self.label_title_purposition = QtWidgets.QLabel(self.centralwidget)
        self.label_title_purposition.setGeometry(QtCore.QRect(30, 269, 200, 35))
        self.label_title_purposition.setTextFormat(QtCore.Qt.RichText)
        self.label_title_purposition.setText("""
        <p style='line-height:100%; margin:0;'>
            <span style='color:#383535;'>Назначение</span>
        </p>
        """)
        self.label_title_purposition.setWordWrap(True)
        self.label_title_purposition.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        font = QtGui.QFont("Geologica SemiBold", 16)
        self.label_title_purposition.setFont(font)
        # ✅ Убираем белый фон
        self.label_title_purposition.setStyleSheet("background-color: transparent;")

        # Назначение (Текст)
        self.label_title_text = QtWidgets.QLabel(self.centralwidget)
        self.label_title_text.setGeometry(QtCore.QRect(30, 304, 460, 125))
        self.label_title_text.setTextFormat(QtCore.Qt.RichText)
        self.label_title_text.setText("""
                       <p style='line-height:55%; margin:0;'>
                           <span style='color:#383535;'>«Патент Бокс» автоматизирует сбор <br>и структурирование\n</span>
                           <span style='color:#383535;'>данных по патентным документам из выбранных источников,\n</span>
                           <span style='color:#383535;'>формируя итоговые материалы <br>для «приложения В» к отчёту\n</span>
                           <span style='color:#383535;'>о патентном исследовании.</span>
                       </p>
                       """)
        self.label_title_text.setWordWrap(True)
        self.label_title_text.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        font = QtGui.QFont(font_family_regular, 12)
        self.label_title_text.setFont(font)
        # ✅ Убираем белый фон
        self.label_title_text.setStyleSheet("background-color: transparent;")

        # Поддерживаемые источники (Заголовок)
        self.label_title_source = QtWidgets.QLabel(self.centralwidget)
        self.label_title_source.setGeometry(QtCore.QRect(522, 269, 500, 40))
        self.label_title_source.setTextFormat(QtCore.Qt.RichText)
        self.label_title_source.setText("""
              <p style='line-height:100%; margin:0;'>
                  <span style='color:#383535;'>Поддерживаемые источники</span>
              </p>
              """)
        self.label_title_source.setWordWrap(True)
        self.label_title_source.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        font = QtGui.QFont("Geologica SemiBold", 16)
        self.label_title_source.setFont(font)
        # ✅ Убираем белый фон
        self.label_title_source.setStyleSheet("background-color: transparent;")

        # Поддерживаемые источники (Текст)
        self.label_title_source_text = QtWidgets.QLabel(self.centralwidget)
        self.label_title_source_text.setGeometry(QtCore.QRect(522, 304, 460, 70))
        self.label_title_source_text.setTextFormat(QtCore.Qt.RichText)
        self.label_title_source_text.setText("""
                        <p style='line-height:55%; margin:0;'>
                            <span style='color:#383535;'>&nbsp;&nbsp;• &nbsp;ФИПС (поисковая система);<br></span>
                            <span style='color:#383535;'>&nbsp;&nbsp;• &nbsp;Роспатент (поисковая платформа);<br></span>
                            <span style='color:#383535;'>&nbsp;&nbsp;• &nbsp;WIPO Patentscope.</span>
                        </p>
                        """)
        self.label_title_source_text.setWordWrap(True)
        self.label_title_source_text.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        font = QtGui.QFont(font_family_regular, 12)
        self.label_title_source_text.setFont(font)
        # ✅ Убираем белый фон
        self.label_title_source_text.setStyleSheet("background-color: transparent;")


        # Системные требования (Заголовок)
        self.label_title_requirements = QtWidgets.QLabel(self.centralwidget)
        self.label_title_requirements.setGeometry(QtCore.QRect(30, 455, 400, 39))
        self.label_title_requirements.setTextFormat(QtCore.Qt.RichText)
        self.label_title_requirements.setText("""
              <p style='line-height:100%; margin:0;'>
                  <span style='color:#383535;'>Системные требования</span>
              </p>
              """)
        self.label_title_requirements.setWordWrap(True)
        self.label_title_requirements.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        font = QtGui.QFont("Geologica SemiBold", 16)
        self.label_title_requirements.setFont(font)
        # ✅ Убираем белый фон
        self.label_title_requirements.setStyleSheet("background-color: transparent;")

        # Системные требования (Текст)
        self.label_title_requirements_text = QtWidgets.QLabel(self.centralwidget)
        self.label_title_requirements_text.setGeometry(QtCore.QRect(30, 489, 460, 150))
        self.label_title_requirements_text.setTextFormat(QtCore.Qt.RichText)
        self.label_title_requirements_text.setText("""
                        <p style='line-height:55%; margin:0;'>
                            <span style='color:#383535;'>&nbsp;&nbsp;• &nbsp;Операционная система: Windows 10/11;<br></span>
                            <span style='color:#383535;'>&nbsp;&nbsp;• &nbsp;Установленный браузер: Google Chrome<br></span>
                            <span style='color:#383535;'> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;или Microsoft Edge;<br></span>
                            <span style='color:#383535;'>&nbsp;&nbsp;• &nbsp;Соответствующий веб-драйвер:<br></span>
                            <span style='color:#383535;'> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ChromeDriver для Chrome <br></span>
                            <span style='color:#383535;'> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;либо MSEdgeDriver для Edge;<br></span>
                            <span style='color:#383535;'>&nbsp;&nbsp;• &nbsp;Стабильное интернет-соединение.</span>
                        </p>
                        """)
        self.label_title_requirements_text.setWordWrap(True)
        self.label_title_requirements_text.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        font = QtGui.QFont(font_family_regular, 12)
        self.label_title_requirements_text.setFont(font)
        # ✅ Убираем белый фон
        self.label_title_requirements_text.setStyleSheet("background-color: transparent;")

        # Кнопка "ЧИТАТЬ"
        self.continue_btn = QtWidgets.QPushButton("ЧИТАТЬ   ", self.centralwidget)
        self.continue_btn.setGeometry(522, 589, 264, 50)
        self.continue_btn.setFont(QtGui.QFont(font_family_bold, 12))
        self.continue_btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 183, 230, 1);
                    color: white;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 150, 200, 1);
                }
                """)
        # Стрелочка
        icon_path = os.path.join(os.getcwd(), "Arrow_read.png")
        icon = QtGui.QIcon(icon_path)
        self.continue_btn.setIcon(icon)
        self.continue_btn.setIconSize(QtCore.QSize(500, 1000))
        self.continue_btn.setLayoutDirection(QtCore.Qt.RightToLeft)


        # Нижняя надпись
        self.label_footer = QtWidgets.QLabel(self.centralwidget)
        self.label_footer.setGeometry(QtCore.QRect(310, 690, 405, 50))
        self.label_footer.setTextFormat(QtCore.Qt.RichText)
        self.label_footer.setText("""
        <p style='line-height:60%; margin:0;'>
        <span style='color:#383535;'>© 2025 ПатентБокс. Все права защищены.
        Контакты: nikita_pishk@rambler.ru </span>
        </p>
        """)
        self.label_footer.setWordWrap(True)
        self.label_footer.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.label_footer.setFont(QtGui.QFont(font_family_semibold, 9))
        self.label_footer.setStyleSheet("background-color: transparent;")

        MainWindow.setCentralWidget(self.centralwidget)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_InstructionWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
