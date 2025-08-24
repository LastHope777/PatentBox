from PyQt5 import QtWidgets, QtGui, QtCore
import os
import sys


class Ui_InstructionSlider(object):
    def __init__(self):
        self.adapter_box = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Ui_InstructionSlider")
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
        self.label_title.setGeometry(QtCore.QRect(30, 130, 800, 100))
        self.label_title.setTextFormat(QtCore.Qt.RichText)
        self.label_title.setText("""
        <p style='line-height:100%; margin:0;'>
            <span style='color:#383535;'>Работа с приложением</span>
        </p>
        """)
        self.label_title.setWordWrap(True)
        self.label_title.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        font = QtGui.QFont("Geologica Black", 38)
        self.label_title.setFont(font)
        # ✅ Убираем белый фон
        self.label_title.setStyleSheet("background-color: transparent;")

        # Слайдер
        self.slider = SliderWidget(self.centralwidget)
        self.slider.setGeometry(30, 264, 964, 420)  # Размещение и размер слайдера

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


class ImageWindow(QtWidgets.QMainWindow):

    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.setFixedSize(600, 400)  # Размер увеличенного окна
        self.setStyleSheet("background-color: white;")

        pixmap = QtGui.QPixmap(image_path)
        pixmap_scaled = pixmap.scaled(600, 400, QtCore.Qt.KeepAspectRatio)

        label = QtWidgets.QLabel(self)
        label.setPixmap(pixmap_scaled)
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.setCentralWidget(label)


class SliderWidget(QtWidgets.QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #F4F4F4; border-radius: 16px;")

        # Виджет для содержимого слайдера
        self.stacked_widget = QtWidgets.QStackedWidget(self)
        self.stacked_widget.setGeometry(0, 0, 964, 420)  # Занимает всю площадь контейнера

        # Кнопка "Влево"
        # Для стрелки влево используем два изображения: обычное и для ховера
        self.left_btn = QtWidgets.QPushButton("", self)  # Пустой текст
        self.left_btn.setFixedSize(24, 24)  # Размер кнопки
        self.left_btn.setGeometry(422, 375, 24, 24)
        self.left_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-image: url(arrow_left_regular.svg);
                background-repeat: no-repeat;
                background-position: center;
            }
            QPushButton:hover {
                background-image: url(arrow_left_hover.svg);
            }
        """)
        self.left_btn.clicked.connect(self.prev_page)

        def load_font(path, fallback="Arial"):
            font_id = QtGui.QFontDatabase.addApplicationFont(path)
            if font_id == -1:
                return fallback
            return QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]

        font_family_black = load_font(os.path.join(os.getcwd(), "Geologica-Black.ttf"))
        font_family_bold = load_font(os.path.join(os.getcwd(), "Geologica_Auto-Bold.ttf"))
        font_family_semibold = load_font(os.path.join(os.getcwd(), "Geologica-SemiBold.ttf"))
        font_family_regular = load_font(os.path.join(os.getcwd(), "Geologica-Regular.ttf"))

        # Добавляем страницы в слайдер
        # Страница 1
        page1 = QtWidgets.QWidget()

        label1_text = QtWidgets.QLabel("Шаг 1.", page1)
        label1_text.setGeometry(QtCore.QRect(30, 30, 90, 25))
        label1_text.setFont(QtGui.QFont(font_family_semibold, 14))

        label2_text = QtWidgets.QLabel(page1)
        label2_text.setGeometry(QtCore.QRect(30, 50, 600, 100))
        label2_text.setText("""
        <p style='line-height:60%; margin:0;'>
            <span style='color:#383535;'>Для начала работы необходимо запустить приложение «Патент<br></span>
            <span style='color:#383535;'>Бокс» после чего откроется главное меню.<br><br></span>
            <span style='color:#383535;'>После этого необходимо нажать на кнопку «НАЧАТЬ РАБОТУ».</span>
        </p>
        """)
        label2_text.setFont(QtGui.QFont(font_family_regular, 10))
        label2_text.setStyleSheet("background-color: transparent;")
        label3_text = QtWidgets.QLabel("1/5", page1)
        label3_text.setGeometry(QtCore.QRect(450, 380, 30, 15))
        label3_text.setFont(QtGui.QFont(font_family_semibold, 10))

        # Изображение
        self.image_label = QtWidgets.QLabel(page1)
        self.image_label.setGeometry(QtCore.QRect(592, 70, 340, 240))
        self.image_label.setScaledContents(True) # Масштабирование
        pixmap = QtGui.QPixmap("slider_1.1.jpg")
        if pixmap.isNull():
            pixmap = QtGui.QPixmap(200, 150)
            pixmap.fill(QtCore.Qt.lightGray)
        self.image_label.setPixmap(pixmap)
        self.image_label.setCursor(QtCore.Qt.PointingHandCursor)
        self.image_label.mousePressEvent = lambda event: self.show_image_window("slider_1.1.jpg")


        self.stacked_widget.addWidget(page1)

        # Страница 2
        page2 = QtWidgets.QWidget()
        label1_slider2_text = QtWidgets.QLabel("Шаг 2.", page2)
        label1_slider2_text.setGeometry(QtCore.QRect(30, 30, 90, 25))
        label1_slider2_text.setFont(QtGui.QFont(font_family_semibold, 14))

        label2_slider2_text = QtWidgets.QLabel(page2)
        label2_slider2_text.setGeometry(QtCore.QRect(30, 60, 600, 234))
        label2_slider2_text.setText("""
                <p style='line-height:60%; margin:0;'>
                    <span style='color:#383535;'>В появившемся окне необходимо указать путь к вебрайверу <br></span>
                    <span style='color:#383535;'>для браузера, который вы собираетесь использовать: Google<br></span>
                    <span style='color:#383535;'>или Microsoft Edge.<br><br></span>
                    <span style='color:#383535;'>Вебдрайвер можно скачать в интернете по запросу: «WebDriver<br></span>
                    <span style='color:#383535;'>для {Ваш браузер}»<br><br></span>
                    <span style='color:#383535;'>Указывать путь необходимо к файлу с расширением.exe<br><br></span>
                    <span style='color:#383535;'>Далее необходимо указать путь к входящим данным<br></span>
                    <span style='color:#383535;'>в формате.docx, выбрать браузер, который хотите использовать<br></span>
                    <span style='color:#38355;'>и указать базы данных, если будет использоваться поисковая<br></span>
                    <span style='color:#383535;'>система ФИПС</span>
                </p>
                """)
        label2_slider2_text.setFont(QtGui.QFont(font_family_regular, 10))

        label3_slider2_text = QtWidgets.QLabel("2/5", page2)
        label3_slider2_text.setGeometry(QtCore.QRect(450, 380, 30, 15))
        label3_slider2_text.setFont(QtGui.QFont(font_family_semibold, 10))

        # Изображение
        self.image_label_slider2 = QtWidgets.QLabel(page2)
        self.image_label_slider2.setGeometry(QtCore.QRect(592, 70, 340, 240))
        self.image_label_slider2.setScaledContents(True) # Масштабирование
        pixmap = QtGui.QPixmap("slider_2.1.jpg")
        if pixmap.isNull():
            pixmap = QtGui.QPixmap(200, 150)
            pixmap.fill(QtCore.Qt.lightGray)
        self.image_label_slider2.setPixmap(pixmap)
        self.image_label_slider2.setCursor(QtCore.Qt.PointingHandCursor)
        self.image_label_slider2.mousePressEvent = lambda event: self.show_image_window("slider_2.1.jpg")


        self.stacked_widget.addWidget(page2)

        # Страница 3
        page3 = QtWidgets.QWidget()
        label1_slider3_text = QtWidgets.QLabel("Шаг 3. Правильное оформление входящих данных", page3)
        label1_slider3_text.setGeometry(QtCore.QRect(30, 30, 630, 25))
        label1_slider3_text.setFont(QtGui.QFont(font_family_semibold, 14))

        label2_slider3_text = QtWidgets.QLabel(page3)
        label2_slider3_text.setGeometry(QtCore.QRect(30, 60, 480, 105))
        label2_slider3_text.setText("""
                        <p style='line-height:60%; margin:0;'>
                            <span style='color:#383535;'>Приложение поддерживает работу с тремя платформами<br></span>
                            <span style='color:#383535;'>для управления интеллектуальной собственностью: Поисковая<br></span>
                            <span style='color:#383535;'>система ФИПС, Поисковая платформа Роспатента и Patenscope.<br><br></span>
                            <span style='color:#383535;'>Для корректной работы программы необходимо предоставлять<br></span>
                            <span style='color:#383535;'>данные в формате.docx</span>
                        </p>
                        """)
        label2_slider3_text.setFont(QtGui.QFont(font_family_regular, 9))

        label4_slider3_text = QtWidgets.QLabel(page3)
        label4_slider3_text.setGeometry(QtCore.QRect(30, 170, 500, 28))
        label4_slider3_text.setText("""
                        <p style='line-height:60%; margin:0;'>
                            <span style='color:#383535;'>Оформление входящих данных для поисковой системы ФИПС:</span>
                        </p>
                        """)
        label4_slider3_text.setFont(QtGui.QFont(font_family_semibold, 9))

        label5_slider3_text = QtWidgets.QLabel(page3)
        label5_slider3_text.setGeometry(QtCore.QRect(30, 203, 520, 89))
        label5_slider3_text.setText("""
                        <p style='line-height:60%; margin:0;'>
                            <span style='color:#383535;'>1. Необходимо создать таблицу с необходимым количеством строк<br></span>
                            <span style='color:#383535;'>&nbsp;&nbsp;&nbsp;&nbsp;и всего одним столбцом;<br></span>
                            <span style='color:#383535;'>2. В первой строке указать «ФИПС» или «Фипс» или «фипс»;<br></span>
                            <span style='color:#383535;'>3. Далее в каждой последующей ячейке указать номер документа <br></span>
                            <span style='color:#383535;'>&nbsp;&nbsp;&nbsp;&nbsp;(Только цифры).</span>
                        </p>
                        """)
        label5_slider3_text.setFont(QtGui.QFont(font_family_regular, 9))

        label6_slider3_text = QtWidgets.QLabel(page3)
        label6_slider3_text.setGeometry(QtCore.QRect(566, 170, 100, 27))
        label6_slider3_text.setText("""
                                <p style='line-height:60%; margin:0;'>
                                    <span style='color:#383535;'>Пример:</span>
                                </p>
                                """)
        label6_slider3_text.setFont(QtGui.QFont(font_family_semibold, 9))

        label3_slider3_text = QtWidgets.QLabel("3/5", page3)
        label3_slider3_text.setGeometry(QtCore.QRect(450, 380, 30, 15))
        label3_slider3_text.setFont(QtGui.QFont(font_family_semibold, 10))

        # Изображение
        self.image_label_slider3 = QtWidgets.QLabel(page3)
        self.image_label_slider3.setGeometry(QtCore.QRect(566, 201, 350, 60))
        self.image_label_slider3.setScaledContents(True)  # Масштабирование
        pixmap = QtGui.QPixmap("slider_3.1.jpg")
        if pixmap.isNull():
            pixmap = QtGui.QPixmap(200, 150)
            pixmap.fill(QtCore.Qt.lightGray)
        self.image_label_slider3.setPixmap(pixmap)
        self.image_label_slider3.setCursor(QtCore.Qt.PointingHandCursor)
        self.image_label_slider3.mousePressEvent = lambda event: self.show_image_window("slider_3.1.jpg")

        self.stacked_widget.addWidget(page3)

        # Страница 4
        page4 = QtWidgets.QWidget()
        label1_slider4_text = QtWidgets.QLabel("Шаг 3. Правильное оформление входящих данных", page4)
        label1_slider4_text.setGeometry(QtCore.QRect(30, 30, 630, 25))
        label1_slider4_text.setFont(QtGui.QFont(font_family_semibold, 14))

        label2_slider4_text = QtWidgets.QLabel(page4)
        label2_slider4_text.setGeometry(QtCore.QRect(30, 60, 560, 45))
        label2_slider4_text.setText("""
                                <p style='line-height:60%; margin:0;'>
                                    <span style='color:#383535;'>Оформление входящих данных для поисковой<br>платформы Роспатента:</span>
                                </p>
                                """)
        label2_slider4_text.setFont(QtGui.QFont(font_family_semibold, 9))

        label7_slider4_text = QtWidgets.QLabel(page4)
        label7_slider4_text.setGeometry(QtCore.QRect(30, 105, 520, 89))
        label7_slider4_text.setText("""
                                        <p style='line-height:60%; margin:0;'>
                                            <span style='color:#383535;'>1. Необходимо создать таблицу с необходимым количеством строк<br></span>
                                            <span style='color:#383535;'>&nbsp;&nbsp;&nbsp;&nbsp;и всего одним столбцом;<br></span>
                                            <span style='color:#383535;'>2. В первой строке указать «Платформа» или «платформа»;<br></span>
                                            <span style='color:#383535;'>3. Далее в каждой последующей ячейке указать номер документа <br></span>
                                            <span style='color:#383535;'>&nbsp;&nbsp;&nbsp;&nbsp;(Вместе с кодом страны и кодом типа документа).</span>
                                        </p>
                                        """)
        label7_slider4_text.setFont(QtGui.QFont(font_family_regular, 9))

        label4_slider4_text = QtWidgets.QLabel(page4)
        label4_slider4_text.setGeometry(QtCore.QRect(30, 200, 500, 28))
        label4_slider4_text.setText("""
                                <p style='line-height:60%; margin:0;'>
                                    <span style='color:#383535;'>Оформление входящих данных для Patentscope:</span>
                                </p>
                                """)
        label4_slider4_text.setFont(QtGui.QFont(font_family_semibold, 9))

        label5_slider4_text = QtWidgets.QLabel(page4)
        label5_slider4_text.setGeometry(QtCore.QRect(30, 233, 520, 89))
        label5_slider4_text.setText("""
                                <p style='line-height:60%; margin:0;'>
                                    <span style='color:#383535;'>1. Необходимо создать таблицу с необходимым количеством строк<br></span>
                                    <span style='color:#383535;'>&nbsp;&nbsp;&nbsp;&nbsp;и всего одним столбцом;<br></span>
                                    <span style='color:#383535;'>2. В первой строке указать «ФИПС» или «Фипс» или «фипс»;<br></span>
                                    <span style='color:#383535;'>3. Далее в каждой последующей ячейке указать номер документа <br></span>
                                    <span style='color:#383535;'>&nbsp;&nbsp;&nbsp;&nbsp;(Только цифры)</span>
                                </p>
                                """)
        label5_slider4_text.setFont(QtGui.QFont(font_family_regular, 9))

        label6_slider4_text = QtWidgets.QLabel(page4)
        label6_slider4_text.setGeometry(QtCore.QRect(566, 60, 100, 27))
        label6_slider4_text.setText("""
                                        <p style='line-height:60%; margin:0;'>
                                            <span style='color:#383535;'>Пример:</span>
                                        </p>
                                        """)
        label6_slider4_text.setFont(QtGui.QFont(font_family_semibold, 9))

        label3_slider4_text = QtWidgets.QLabel("4/5", page4)
        label3_slider4_text.setGeometry(QtCore.QRect(450, 380, 30, 15))
        label3_slider4_text.setFont(QtGui.QFont(font_family_semibold, 10))

        # Изображение
        self.image_label_slider4 = QtWidgets.QLabel(page4)
        self.image_label_slider4.setGeometry(QtCore.QRect(566, 90, 350, 60))
        self.image_label_slider4.setScaledContents(True)  # Масштабирование
        pixmap = QtGui.QPixmap("slider_4.1.jpg")
        if pixmap.isNull():
            pixmap = QtGui.QPixmap(200, 150)
            pixmap.fill(QtCore.Qt.lightGray)
        self.image_label_slider4.setPixmap(pixmap)
        self.image_label_slider4.setCursor(QtCore.Qt.PointingHandCursor)
        self.image_label_slider4.mousePressEvent = lambda event: self.show_image_window("slider_4.1.jpg")

        label6_slider7_text = QtWidgets.QLabel(page4)
        label6_slider7_text.setGeometry(QtCore.QRect(566, 200, 100, 27))
        label6_slider7_text.setText("""
                                                <p style='line-height:60%; margin:0;'>
                                                    <span style='color:#383535;'>Пример:</span>
                                                </p>
                                                """)
        label6_slider7_text.setFont(QtGui.QFont(font_family_semibold, 9))

        self.image_label_slider42 = QtWidgets.QLabel(page4)
        self.image_label_slider42.setGeometry(QtCore.QRect(566, 230, 350, 60))
        self.image_label_slider42.setScaledContents(True)  # Масштабирование
        pixmap = QtGui.QPixmap("slider_4.2.jpg")
        if pixmap.isNull():
            pixmap = QtGui.QPixmap(200, 150)
            pixmap.fill(QtCore.Qt.lightGray)
        self.image_label_slider42.setPixmap(pixmap)
        self.image_label_slider42.setCursor(QtCore.Qt.PointingHandCursor)
        self.image_label_slider42.mousePressEvent = lambda event: self.show_image_window("slider_4.2.jpg")

        self.stacked_widget.addWidget(page4)

        # Страница 5
        page5 = QtWidgets.QWidget()
        label1_slider5_text = QtWidgets.QLabel("Возможные ошибки", page5)
        label1_slider5_text.setGeometry(QtCore.QRect(30, 30, 250, 25))
        label1_slider5_text.setFont(QtGui.QFont(font_family_semibold, 14))

        label7_slider5_text = QtWidgets.QLabel(page5)
        label7_slider5_text.setGeometry(QtCore.QRect(30, 60, 520, 117))
        label7_slider5_text.setText("""
                                                <p style='line-height:60%; margin:0;'>
                                                    <span style='color:#383535;'>1. Если приложение перестало запускать браузер, то одной<br></span>
                                                    <span style='color:#383535;'>&nbsp;&nbsp;&nbsp;&nbsp;из самых частых причин возникновения данной ошибки<br></span>
                                                    <span style='color:#383535;'>&nbsp;&nbsp;&nbsp;&nbsp;является несовместимость версий вебдрайвера<br></span>
                                                    <span style='color:#383535;'>&nbsp;&nbsp;&nbsp;&nbsp;и браузера. Для устранения ошибки посмотрите версию<br></span>
                                                    <span style='color:#383535;'>&nbsp;&nbsp;&nbsp;&nbsp;вашего браузера после чего скачайте соответствующую<br></span>
                                                    <span style='color:#383535;'>&nbsp;&nbsp;&nbsp;&nbsp;ему версию вебдрайвера (Они должны совпадать<br></span>
                                                    <span style='color:#383535;'>&nbsp;&nbsp;&nbsp;&nbsp;или быть близкими).</span>
                                                </p>
                                                """)
        label7_slider5_text.setFont(QtGui.QFont(font_family_regular, 9))

        label4_slider5_text = QtWidgets.QLabel(page5)
        label4_slider5_text.setGeometry(QtCore.QRect(30, 190, 500, 90))
        label4_slider5_text.setText("""
                                        <p style='line-height:60%; margin:0;'>
                                             <span style='color:#383535;'>2. Если приложение не находит указанный вами патент,<br></span>
                                             <span style='color:#383535;'>&nbsp;&nbsp;&nbsp;&nbsp;то вероятно неправильно указан номер или он записан<br></span>
                                             <span style='color:#383535;'>&nbsp;&nbsp;&nbsp;&nbsp;в неправильном формате, обязательно сравните<br></span>
                                             <span style='color:#383535;'>&nbsp;&nbsp;&nbsp;&nbsp;написание номера с теми, что представлены<br></span>
                                             <span style='color:#383535;'>&nbsp;&nbsp;&nbsp;&nbsp;на скриншотах.</span>
                                        </p>
                                        """)
        label4_slider5_text.setFont(QtGui.QFont(font_family_regular, 9))

        label7_slider6_text = QtWidgets.QLabel(page5)
        label7_slider6_text.setGeometry(QtCore.QRect(520, 60, 420, 73))
        label7_slider6_text.setText("""
                                                                <p style='line-height:60%; margin:0;'>
                                                                    <span style='color:#383535;'>3. Если приложение указывает данные не того патента,<br></span>
                                                                    <span style='color:#383535;'>&nbsp;&nbsp;&nbsp;&nbsp;то вероятно был обнаружен ещё один патент с таким<br></span>
                                                                    <span style='color:#383535;'>&nbsp;&nbsp;&nbsp;&nbsp;номером и приложение выбрало не тот (Выбирается<br></span>
                                                                    <span style='color:#383535;'>&nbsp;&nbsp;&nbsp;&nbsp;первый из списка).</span>
                                                                </p>
                                                                """)
        label7_slider6_text.setFont(QtGui.QFont(font_family_regular, 9))

        label3_slider5_text = QtWidgets.QLabel("5/5", page5)
        label3_slider5_text.setGeometry(QtCore.QRect(450, 380, 30, 15))
        label3_slider5_text.setFont(QtGui.QFont(font_family_semibold, 10))

        label6_slider5_text = QtWidgets.QLabel(page5)
        label6_slider5_text.setGeometry(QtCore.QRect(520, 140, 250, 30))
        label6_slider5_text.setText("""
                                                <p style='line-height:60%; margin:0;'>
                                                    <span style='color:#383535;'>Пример такой ситуации:</span>
                                                </p>
                                                """)
        label6_slider5_text.setFont(QtGui.QFont(font_family_semibold, 9))

        # Изображение
        self.image_label_slider5 = QtWidgets.QLabel(page5)
        self.image_label_slider5.setGeometry(QtCore.QRect(520, 173, 240, 160))
        self.image_label_slider5.setScaledContents(True)  # Масштабирование
        pixmap = QtGui.QPixmap("slider_5.1.jpg")
        if pixmap.isNull():
            pixmap = QtGui.QPixmap(200, 150)
            pixmap.fill(QtCore.Qt.lightGray)
        self.image_label_slider5.setPixmap(pixmap)
        self.image_label_slider5.setCursor(QtCore.Qt.PointingHandCursor)
        self.image_label_slider5.mousePressEvent = lambda event: self.show_image_window("slider_5.1.jpg")

        self.stacked_widget.addWidget(page5)

        # Кнопка "Вправо"
        self.right_btn = QtWidgets.QPushButton("", self)
        self.right_btn.setFixedSize(24, 24)
        self.right_btn.setGeometry(480, 375, 24, 24)
        self.right_btn.setStyleSheet("""
                    QPushButton {
                        border: none;
                        background-image: url(arrow_right_regular.svg);
                        background-repeat: no-repeat;
                        background-position: center;
                    }
                    QPushButton:hover {
                        background-image: url(arrow_right_hover.svg);
                    }
                """)
        self.right_btn.clicked.connect(self.next_page)

        # Обновляем видимость кнопок при старте
        self.update_buttons()


    def show_image_window(self, image_path):
        """Обработчик события клика по изображению"""
        self.image_window = ImageWindow(image_path)
        self.image_window.show()

    def next_page(self):
        current_index = self.stacked_widget.currentIndex()
        if current_index < self.stacked_widget.count() - 1:
            self.stacked_widget.setCurrentIndex(current_index + 1)
            self.update_buttons()

    def prev_page(self):
        current_index = self.stacked_widget.currentIndex()
        if current_index > 0:
            self.stacked_widget.setCurrentIndex(current_index - 1)
            self.update_buttons()

    def update_buttons(self):
        current_index = self.stacked_widget.currentIndex()
        total_pages = self.stacked_widget.count()

        # Скрываем "Влево" на первом экране
        self.left_btn.setVisible(current_index > 0)

        # Скрываем "Вправо" на последнем экране
        self.right_btn.setVisible(current_index < total_pages - 1)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_InstructionSlider()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
