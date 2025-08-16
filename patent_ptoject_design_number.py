from PyQt5 import QtWidgets, QtGui, QtCore
import os


class Ui_SecondWindow(object):
    def __init__(self):
        self.adapter_box = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("SecondWindow")
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

        # ==== Кнопка "Назад" ====
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

        # ==== Прямоугольник "Путь к вебдрайверу" ====
        self.adapter_box = QtWidgets.QFrame(self.centralwidget)
        self.adapter_box.setGeometry(30, 189, 326, 140)
        self.adapter_box.setStyleSheet("background-color: #F4F4F4; border-radius: 16px;")

        label_adapter = QtWidgets.QLabel("Путь к вебдрайверу", self.adapter_box)
        label_adapter.setFont(QtGui.QFont(font_family_semibold, 12))
        label_adapter.setStyleSheet("color: #383535;")
        label_adapter.move(30, 10)

        self.adapter_btn = QtWidgets.QPushButton("Выбрать файл", self.adapter_box)
        self.adapter_btn.setGeometry(30, 56, 266, 36)
        self.adapter_btn.setFont(QtGui.QFont(font_family_bold, 10))
        self.adapter_btn.setStyleSheet("""
        QPushButton {
            background-color: #FFFFFF;
            color: #C4C3C3;
            border-radius: 10px;
        }
        QPushButton:hover {
            background-color: #F8F8F8;
            color: #949393;
        }
        """)

        self.adapter_path_edit = QtWidgets.QLineEdit(self.adapter_box)
        self.adapter_path_edit.setReadOnly(True)
        self.adapter_path_edit.setFont(QtGui.QFont(font_family_regular, 7))
        self.adapter_path_edit.setGeometry(30, 102, 266, 30)
        self.adapter_path_edit.setStyleSheet("""
        QLineEdit {
            border-radius: 10px;
            padding-left: 10px;
            color: #383535;
        }
        """)

        # ==== Прямоугольник "Путь к входящим данным" ====
        self.input_box = QtWidgets.QFrame(self.centralwidget)
        self.input_box.setGeometry(30, 349, 326, 140)
        self.input_box.setStyleSheet("background-color: #F4F4F4; border-radius: 16px;")

        label_input = QtWidgets.QLabel("Путь к входящим данным", self.input_box)
        label_input.setFont(QtGui.QFont(font_family_semibold, 12))
        label_input.setStyleSheet("color: #383535;")
        label_input.move(30, 10)

        self.input_btn = QtWidgets.QPushButton("Выбрать файл", self.input_box)
        self.input_btn.setGeometry(30, 56, 266, 36)
        self.input_btn.setFont(QtGui.QFont(font_family_bold, 10))
        self.input_btn.setStyleSheet("""
        QPushButton {
            background-color: #FFFFFF;
            color: #C4C3C3;
            border-radius: 10px;
        }
        QPushButton:hover {
            background-color: #F8F8F8;
            color: #949393;
        }
        """)

        self.input_path_edit = QtWidgets.QLineEdit(self.input_box)
        self.input_path_edit.setReadOnly(True)
        self.input_path_edit.setFont(QtGui.QFont(font_family_regular, 7))
        self.input_path_edit.setGeometry(30, 102, 266, 30)
        self.input_path_edit.setStyleSheet("""
        QLineEdit {
            border-radius: 10px;
            padding-left: 10px;
            color: #383535;
        }
        """)

        # ==== Прямоугольник "Браузер" ====
        self.browser_box = QtWidgets.QFrame(self.centralwidget)
        self.browser_box.setGeometry(30, 509, 326, 114)
        self.browser_box.setStyleSheet("background-color: #F4F4F4; border-radius: 16px;")

        label_browser = QtWidgets.QLabel("Браузер", self.browser_box)
        label_browser.setFont(QtGui.QFont(font_family_semibold, 12))
        label_browser.setStyleSheet("color: #383535;")
        label_browser.move(30, 10)

        radio_style = f"QRadioButton {{ color: #C4C3C3; font-family: '{font_family_bold}'; font-size: 10pt; }}"

        self.radio_google = QtWidgets.QRadioButton("Google", self.browser_box)
        self.radio_google.move(30, 40)
        self.radio_google.setStyleSheet(radio_style)
        self.radio_google.setChecked(True)

        self.radio_edge = QtWidgets.QRadioButton("Microsoft Edge", self.browser_box)
        self.radio_edge.move(30, 70)
        self.radio_edge.setStyleSheet(radio_style)

        # ==== Кнопка "СТАРТ" ====
        self.start_btn = QtWidgets.QPushButton("СТАРТ", self.centralwidget)
        self.start_btn.setGeometry(376, 553, 618, 70)
        self.start_btn.setFont(QtGui.QFont(font_family_black, 14))
        self.start_btn.setStyleSheet("""
        QPushButton {
            background-color: #0011FF;
            color: #FFFFFF;
            border-radius: 16px;
        }
        QPushButton:hover {
            background-color: rgba(0, 17, 200, 1);
        }
        """)

        # ==== Прямоугольник "База данных" ====
        self.db_box = QtWidgets.QFrame(self.centralwidget)
        self.db_box.setGeometry(376, 189, 618, 344)
        self.db_box.setStyleSheet("background-color: #F4F4F4; border-radius: 16px;")

        layout = QtWidgets.QVBoxLayout(self.db_box)
        layout.setContentsMargins(30, 10, 0, 0)
        layout.setSpacing(0)

        label_db = QtWidgets.QLabel(self.db_box)
        label_db.setStyleSheet("background: transparent; color: #383535;")
        label_db.setFont(QtGui.QFont(font_family_semibold, 12))
        label_db.setText("""<p style="line-height:77%; margin:0;">База данных (для поисковой<br>системы ФИПС)</p>""")
        label_db.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        label_db.setWordWrap(True)
        layout.addWidget(label_db)

        layout.addSpacing(15)

        checkbox_style = f"""
        QCheckBox {{
            color: #C4C3C3;
            font-family: '{font_family_bold}';
            font-size: 10pt;
        }}
        QCheckBox::indicator {{
            width: 14px;
            height: 14px;
        }}
        """

        self.cb1 = QtWidgets.QCheckBox("Рефераты российских изобретений")
        self.cb2 = QtWidgets.QCheckBox("Заявки на российские изобретения")
        self.cb3 = QtWidgets.QCheckBox("Тексты российских изобретений из 3-х последних бюллетеней")
        self.cb4 = QtWidgets.QCheckBox("Формулы российских изобретений")
        self.cb5 = QtWidgets.QCheckBox("Формулы российских ПМ из 3-х последних бюллетеней")
        self.cb6 = QtWidgets.QCheckBox("Перспективные российские изобретения")
        self.cb7 = QtWidgets.QCheckBox("ВЫДЕЛИТЬ ВСЁ")

        for cb in [self.cb1, self.cb2, self.cb3, self.cb4, self.cb5, self.cb6, self.cb7]:
            cb.setStyleSheet(checkbox_style)
            layout.addWidget(cb)

        layout.addStretch()

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
    ui = Ui_SecondWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
