# 📦 ПатентБокс

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
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

## 📸 Скриншоты

### Главный экран
<img width="1041" height="816" alt="Главный экран" src="https://github.com/user-attachments/assets/88b616b5-cfe6-4061-a610-55b47db289bc" />

### Второй экран
<img width="1041" height="816" alt="Второй экран" src="https://github.com/user-attachments/assets/55f390f0-563c-4820-8444-454e60f06cb0" />

---

## 🛠️ Технологии
- [Python 3.10+](https://www.python.org/)  
- [PyQt5](https://pypi.org/project/PyQt5/)  
- [Selenium](https://www.selenium.dev/) (для автоматизации браузера)  

---

## 📦 Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/patentbox.git
   cd patentbox
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

## 🤝 Вклад в проект

Если хотите помочь в развитии проекта:
1. Сделайте форк 
2. Создайте ветку:
   ```bash
   git checkout -b feature/my-feature
   ```
3. Сделайте коммит:
   ```bash
   git commit -m "Добавлена новая функция"
   ```
4. Отправьте Pull Request 🚀

---

## 📜 Лицензия
Проект распространяется по лицензии **MIT**. Подробнее см. в файле [LICENSE](LICENSE).

---

## 📬 Контакты
👤 Автор: **Никита Пишков**  
📧 Email: [nikita_pishk@rambler.ru](mailto:nikita_pishk@rambler.ru)
