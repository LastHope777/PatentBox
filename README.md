# 📦 ПатентБокс

![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

**ПатентБокс** — настольное приложение на **PyQt5** для работы с патентной информацией и автоматизации поиска через веб-драйверы.  

## 🔑 Функциональность
- 📂 выбор пути к **веб-драйверу** (Google Chrome / Microsoft Edge);
- 📂 загрузка **входных данных**;
- 🌐 запуск поиска в выбранном браузере;
- 📊 работа с базами данных ФИПС (рефераты, формулы, заявки и др.);
- ⚡️ удобный интерфейс с управлением в один клик.

---
## 🌐 Поддерживаемые источники
- 🔍 **ФИПС** — поисковая система Федерального института промышленной собственности
- 🔍 **Платформа Роспатента** — поисковая платформа Роспатента
- 🔍 **WIPO Patentscope** — международная база патентов
---

## 📸 Скриншоты

### Главный экран
<img width="1041" height="816" alt="Главный экран" src="https://github.com/user-attachments/assets/88b616b5-cfe6-4061-a610-55b47db289bc" />

### Второй экран
<img width="1041" height="816" alt="Второй экран" src="https://github.com/user-attachments/assets/55f390f0-563c-4820-8444-454e60f06cb0" />

---

## 🛠️ Технологии
- [Python 3.11+](https://www.python.org/)  
- [PyQt5](https://pypi.org/project/PyQt5/)  
- [Selenium](https://www.selenium.dev/) (для автоматизации браузера)  
- [python-docx](https://python-docx.readthedocs.io/) (для работы с .docx файлами)

---

## 📦 Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/LastHope777/PatentBox.git
   cd PatentBox
   ```

2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/MacOS
   venv\Scripts\activate      # Windows
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

---
## 📁 Структура проекта
```
PatentBox/
├── main.py
├── requirements.txt
├── result.docx
├── assets/
│   ├── fonts/
│   └── images/
└── ui/
    ├── patent_ptoject_design_main_menu.py
    ├── patent_ptoject_design_number.py
    ├── page_instruction.py
    └── page_instruction_slider.py
```
---
## ▶️ Запуск

```bash
python main.py
```

---

## ⚙️ Настройки
- **Веб-драйвер**: путь к `chromedriver.exe` или `msedgedriver.exe` указывается через кнопку **Выбрать файл**.  
- **Файлы данных**: загружаются через отдельный блок интерфейса в формате `.docx`.  
- **Браузер**: выбирается радиокнопкой (**Google** или **Microsoft Edge**).

---

## 📜 Лицензия
Проект распространяется по лицензии **MIT**. Подробнее см. в файле [LICENSE](LICENSE).

---

## 📬 Контакты
👤 Автор: **Никита Пишков**  
📧 Email: [nikita_pishk@rambler.ru](mailto:nikita_pishk@rambler.ru)
