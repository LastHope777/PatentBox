"""
ПатентБокс — точка входа и окна приложения.

Логика поиска вынесена в отдельные модули:
  patent_search.py — чтение входного .docx и запись таблиц в result.docx;
  scrapers.py      — работа с сайтами ФИПС, Платформы Роспатента и WIPO;
  holder_parser.py — поиск патентообладателя на странице патента;
  result_picker.py — выбор в выдаче документа с точно таким номером.
"""

import os
import sys
import traceback

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from paths import IMG_LOGO
from patent_search import FIPS_ALL_DATABASES, process_document
from ui.fonts import load_app_fonts
from ui.page_instruction import Ui_InstructionWindow
from ui.page_instruction_slider import Ui_InstructionSlider
from ui.patent_project_design_main_menu import Ui_MainWindow
from ui.patent_project_design_number import Ui_SecondWindow


class BaseWindow(QtWidgets.QMainWindow):
    """Окно с UI-классом из папки ui и переходом на другое окно."""

    ui_class = None

    def __init__(self):
        super().__init__()
        self.ui = self.ui_class()
        self.ui.setupUi(self)
        self.next_window = None

    def switch_to(self, window_class):
        self.next_window = window_class()
        self.next_window.show()
        self.close()


class MainMenuWindow(BaseWindow):
    """Главный экран: «Начать работу» и «Инструкция»."""

    ui_class = Ui_MainWindow

    def __init__(self):
        super().__init__()
        self.ui.pushButton_start.clicked.connect(lambda: self.switch_to(SearchWindow))
        self.ui.pushButton_help.clicked.connect(lambda: self.switch_to(InstructionWindow))


class InstructionWindow(BaseWindow):
    """Первая страница инструкции."""

    ui_class = Ui_InstructionWindow

    def __init__(self):
        super().__init__()
        self.ui.back_btn.clicked.connect(lambda: self.switch_to(MainMenuWindow))
        self.ui.continue_btn.clicked.connect(lambda: self.switch_to(InstructionSliderWindow))


class InstructionSliderWindow(BaseWindow):
    """Слайдер с подробной инструкцией."""

    ui_class = Ui_InstructionSlider

    def __init__(self):
        super().__init__()
        self.ui.back_btn.clicked.connect(lambda: self.switch_to(InstructionWindow))


class SearchWindow(BaseWindow):
    """Второй экран: выбор файлов, браузера, баз ФИПС и запуск поиска."""

    ui_class = Ui_SecondWindow

    def __init__(self):
        super().__init__()
        # Порядок важен: индекс галочки = номер базы в группе «Патентные документы РФ (рус.)» на ФИПС
        self.fips_checkboxes = [self.ui.cb1, self.ui.cb2, self.ui.cb3,
                                self.ui.cb4, self.ui.cb5, self.ui.cb6]

        self.ui.input_btn.clicked.connect(
            lambda: self.choose_file(self.ui.input_path_edit, "Документы (*.docx)"))
        self.ui.adapter_btn.clicked.connect(
            lambda: self.choose_file(self.ui.adapter_path_edit, "Программы (*.exe)"))
        self.ui.cb7.stateChanged.connect(self.toggle_all_databases)
        self.ui.start_btn.clicked.connect(self.run_search)
        self.ui.back_btn.clicked.connect(lambda: self.switch_to(MainMenuWindow))

    def choose_file(self, line_edit, file_filter):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите файл", "", file_filter)
        if file_path:
            line_edit.setText(file_path)

    def toggle_all_databases(self):
        for checkbox in self.fips_checkboxes:
            checkbox.setChecked(self.ui.cb7.isChecked())

    def selected_fips_databases(self):
        if self.ui.cb7.isChecked():
            return FIPS_ALL_DATABASES
        return [index for index, checkbox in enumerate(self.fips_checkboxes) if checkbox.isChecked()]

    def run_search(self):
        input_path = self.ui.input_path_edit.text().strip()
        driver_path = self.ui.adapter_path_edit.text().strip()
        if not os.path.isfile(input_path):
            QMessageBox.warning(self, "Не хватает данных", "Выберите файл с входными данными (.docx).")
            return
        if not os.path.isfile(driver_path):
            QMessageBox.warning(self, "Не хватает данных", "Укажите путь к веб-драйверу (.exe).")
            return

        self.ui.start_btn.setEnabled(False)
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        summary, error = None, None
        try:
            summary = process_document(input_path, driver_path,
                                       self.ui.get_selected_browser(),
                                       self.selected_fips_databases())
        except PermissionError:
            error = "Не удалось сохранить result.docx — закройте его в Word и запустите поиск снова."
        except Exception as exc:  # показываем ошибку, а не роняем приложение
            traceback.print_exc()
            error = f"Поиск остановлен из-за ошибки:\n{exc}"
        finally:
            QtWidgets.QApplication.restoreOverrideCursor()
            self.ui.start_btn.setEnabled(True)

        if error:
            QMessageBox.critical(self, "Ошибка", error)
        else:
            QMessageBox.information(self, "Готово", summary.message())


def main():
    app = QtWidgets.QApplication(sys.argv)
    load_app_fonts()  # регистрируем шрифты Geologica один раз, до создания окон
    app.setWindowIcon(QtGui.QIcon(IMG_LOGO))
    window = MainMenuWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
