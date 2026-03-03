import os

# Корень проекта — всегда правильный путь независимо от того откуда запускается
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Папки
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")

# Шрифты
FONT_BLACK = os.path.join(FONTS_DIR, "Geologica-Black.ttf")
FONT_BOLD = os.path.join(FONTS_DIR, "Geologica-Bold.ttf")
FONT_SEMIBOLD = os.path.join(FONTS_DIR, "Geologica-SemiBold.ttf")
FONT_REGULAR = os.path.join(FONTS_DIR, "Geologica-Regular.ttf")
FONT_AUTO_BOLD = os.path.join(FONTS_DIR, "Geologica_Auto-Bold.ttf")

# Изображения
IMG_LOGO = os.path.join(IMAGES_DIR, "logo.png")
IMG_VECTOR = os.path.join(IMAGES_DIR, "Vector.png")
IMG_ARROW_READ = os.path.join(IMAGES_DIR, "Arrow_read.png")
IMG_ARROW_LEFT_HOVER = os.path.join(IMAGES_DIR, "arrow_left_hover.svg")
IMG_ARROW_LEFT_REG = os.path.join(IMAGES_DIR, "arrow_left_regular.svg")
IMG_ARROW_RIGHT_HOVER = os.path.join(IMAGES_DIR, "arrow_right_hover.svg")
IMG_ARROW_RIGHT_REG = os.path.join(IMAGES_DIR, "arrow_right_regular.svg")
IMG_SLIDER_1 = os.path.join(IMAGES_DIR, "slider_1.1.jpg")
IMG_SLIDER_2 = os.path.join(IMAGES_DIR, "slider_2.1.jpg")
IMG_SLIDER_3 = os.path.join(IMAGES_DIR, "slider_3.1.jpg")
IMG_SLIDER_4_1 = os.path.join(IMAGES_DIR, "slider_4.1.jpg")
IMG_SLIDER_4_2 = os.path.join(IMAGES_DIR, "slider_4.2.jpg")
IMG_SLIDER_5 = os.path.join(IMAGES_DIR, "slider_5.1.jpg")

# Файлы результата
RESULT_DOCX = os.path.join(BASE_DIR, "result.docx")