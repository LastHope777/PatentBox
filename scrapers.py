"""
Сбор данных о патенте с сайтов: ФИПС, Платформа Роспатента, WIPO Patentscope.

Каждая функция scrape_*(driver, request, ...) открывает поиск, находит документ
с точно таким номером, как в запросе, и возвращает Patent. Если документа нет —
бросает ExactResultNotFound (из result_picker), остальные ошибки пробрасываются
как есть: их ловит и записывает в таблицу patent_search.process_document().

Все XPath собраны в константы в начале каждого раздела. Если сайт поменяет
вёрстку, править нужно только их. Для важных элементов указано несколько XPath:
первый — по тексту/устойчивому признаку, следующие — старые позиционные пути
как запасной вариант.
"""

import re
import time
from dataclasses import dataclass

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait

from holder_parser import get_patent_holder
from result_picker import find_exact_result, parse_request

WAIT_TIMEOUT = 10  # сек., сколько ждать появления элемента


@dataclass
class Patent:
    number: str  # вид и номер охранного документа (для ФИПС — ещё и режим действия)
    name: str    # название
    holder: str  # патентообладатель, а если его нет — заявитель (НЕ авторы)
    mpk: str     # классификационные рубрики
    date: str    # дата приоритета / публикации


# ============================== Браузер ==============================

_BROWSERS = {
    "google": (webdriver.Chrome, ChromeService),
    "edge": (webdriver.Edge, EdgeService),
}


def create_driver(browser, driver_path):
    """Запускает браузер: browser = "google" или "edge", driver_path — путь к chromedriver/msedgedriver."""
    try:
        driver_class, service_class = _BROWSERS[browser]
    except KeyError:
        raise ValueError(f"Неизвестный браузер: {browser!r}") from None
    return driver_class(service=service_class(executable_path=driver_path))


def quit_driver(driver):
    """Закрывает браузер, не падая, если он уже закрыт."""
    try:
        driver.quit()
    except WebDriverException:
        pass


# ============================== Общие помощники ==============================

def find_first(driver, xpaths):
    """Первый найденный элемент по списку XPath (от основного к запасным)."""
    for xpath in xpaths:
        found = driver.find_elements(By.XPATH, xpath)
        if found:
            return found[0]
    raise NoSuchElementException(f"Не найден элемент ни по одному из XPath: {list(xpaths)}")


def text_of(driver, xpaths, default=None):
    """Текст первого найденного элемента. Если ничего не найдено — default
    (а если default не задан — NoSuchElementException)."""
    try:
        return find_first(driver, xpaths).text
    except NoSuchElementException:
        if default is None:
            raise
        return default


def wait_for(driver, xpaths, clickable=False, timeout=WAIT_TIMEOUT):
    """Ждёт появления элемента по любому из XPath (clickable=True — ещё и видимого/активного)."""
    def _find(drv):
        for xpath in xpaths:
            for element in drv.find_elements(By.XPATH, xpath):
                if not clickable or (element.is_displayed() and element.is_enabled()):
                    return element
        return False

    return WebDriverWait(driver, timeout).until(_find, message=f"Не дождались элемента: {list(xpaths)}")


# ============================== ФИПС ==============================

FIPS_URL = "https://www.fips.ru/iiss/"
FIPS_ALL_DATABASES = "all"

# JSF-идентификаторы вида j_idt74 у ФИПС меняются (то j_idt74, то j_idt81),
# поэтому группу баз и кнопки ищем по тексту.
FIPS_DB_GROUP = (
    '//div[contains(@class, "title")][contains(normalize-space(text()), "Патентные документы РФ (рус")]',
    '//*[@id="db-selection-form:j_idt74"]',
    '//*[@id="db-selection-form:j_idt81"]',
)
# Галочки баз в группе «Патентные документы РФ (рус.)»; index = 0, 1, 2...
FIPS_DB_CHECKBOX = '//*[@id="db-selection-form:dbsGrid1:{index}:dbsGrid1checkbox"]'
FIPS_SELECT_ALL = ('//*[@id="db-selection-form:button-set1"]//input[@value="выделить все"]',)
FIPS_GO_TO_SEARCH = (
    '//*[@id="db-selection-form:button-set1"]//input[@value="перейти к поиску"]',
    '//*[@id="db-selection-form:button-set1"]/div[1]/input',
)
FIPS_NUMBER_FIELD = (  # поле «(11) Номер документа»
    '//div[contains(@class, "oneblock")][.//span[starts-with(normalize-space(.), "(11)")]]'
    '//div[contains(@class, "input")]/input',
    '//*[@id="fields:1:j_idt109"]',
)
FIPS_SEARCH_BUTTON = (
    '//*[@id="searchForm"]//input[@value="Поиск"]',
    '//*[@id="searchForm"]/div[1]/div[1]/div[3]/div[1]/input',
)
FIPS_RESULT_ITEMS = (
    '//a[@data-index]',
    '/html/body/div[3]/div/div/div[1]/div[2]/div/form/div[3]/div/div/a',
)
FIPS_STATUS = ('//*[@id="StatusR"]', '//*[@id="StatusRAP"]')
FIPS_NUMBER_PARTS = ('//*[@id="top2"]', '//*[@id="top4"]', '//*[@id="top6"]')  # RU / номер / код вида
FIPS_NAME = ('/html/body/div[3]/div/div/div[1]/div[2]/form/div/div/div[2]/div/div/p/b',)
FIPS_MPK = ('//*[@id="mainDoc"]/table[1]/tbody/tr/td[2]/table/tbody/tr[2]/td[1]/div/ul/li/a/span',)
FIPS_DATE = ('//*[@id="bib"]/tbody/tr/td[1]/p[2]/b',)
FIPS_NO_STATUS = "Не удалось найти информацию о режиме действия патента"


def fips_query(request):
    """ФИПС ищет по номеру без страны и кода вида: «RU 2 848 852 C1» -> «2848852»."""
    try:
        return parse_request(request)[1]
    except ValueError:
        words = request.split()
        return words[0] if words else request


def _fips_select_databases(driver, databases):
    """Отмечает базы данных. databases — FIPS_ALL_DATABASES или список индексов (0 — первая галочка)."""
    wait_for(driver, FIPS_DB_GROUP, clickable=True).click()  # раскрываем группу
    if databases == FIPS_ALL_DATABASES:
        wait_for(driver, FIPS_SELECT_ALL, clickable=True).click()
    else:
        for index in databases:
            xpath = FIPS_DB_CHECKBOX.format(index=index)
            if not driver.find_elements(By.XPATH, xpath):
                print(f"[ФИПС] базы №{index + 1} на сайте нет — пропускаю")
                continue
            checkbox = wait_for(driver, (xpath,), clickable=True)
            if not checkbox.is_selected():
                checkbox.click()
    time.sleep(1)  # даём AJAX перерисовать кнопки под списком баз
    wait_for(driver, FIPS_GO_TO_SEARCH, clickable=True).click()


def scrape_fips(driver, request, databases):
    driver.get(FIPS_URL)
    _fips_select_databases(driver, databases)

    field = wait_for(driver, FIPS_NUMBER_FIELD, clickable=True)
    field.click()
    field.send_keys(fips_query(request))
    wait_for(driver, FIPS_SEARCH_BUTTON, clickable=True).click()

    # из всей выдачи — документ с точно таким же номером, а не первый в списке
    find_exact_result(driver, request, FIPS_RESULT_ITEMS, link_xpaths=None).click()
    wait_for(driver, FIPS_NUMBER_PARTS[:1])

    status = text_of(driver, FIPS_STATUS, default=FIPS_NO_STATUS)
    number = " ".join(text_of(driver, (xpath,)) for xpath in FIPS_NUMBER_PARTS) + "\n" + status
    return Patent(
        number=number,
        name=text_of(driver, FIPS_NAME),
        holder=get_patent_holder(driver),
        mpk=text_of(driver, FIPS_MPK),
        date=text_of(driver, FIPS_DATE),
    )


# ============================== Платформа Роспатента ==============================

PLATFORM_URL = "https://openstat.rospatent.gov.ru/patents"
PLATFORM_SEARCH_INPUT = (
    '//*[@id="layout"]/div[3]/div/div[3]/div[1]/div[1]/div[1]/div[2]/input',
    '//*[@id="layout"]/div[3]/div/div[3]/div[1]/div[1]/div[1]/input',
    '//input[@placeholder="Что вы ищете?"]',
)
PLATFORM_SEARCH_BUTTON = (
    '//*[@id="layout"]/div[3]/div/div[2]/div/div/button',
    '//button[normalize-space(.)="Поиск"]',
)
PLATFORM_RESULT_ITEMS = (
    '//*[@id="layout"]/div[3]/div/div[4]/div[5]/div/div[2]/div/div/div/ul/li',
    '//*[@id="layout"]//ul/li[.//a]',
)
PLATFORM_RESULT_LINK = ('./div[2]/div/div[1]/div/a', './/a')

_PLATFORM_BIBLIO = '//*[@id="doc-biblio"]/div[2]'
PLATFORM_COUNTRY = (_PLATFORM_BIBLIO + '/div[1]/div[1]/div[2]',)
PLATFORM_NUMBER = (_PLATFORM_BIBLIO + '/div[1]/div[2]/div[2]',)
PLATFORM_KIND = (_PLATFORM_BIBLIO + '/div[1]/div[3]/div[2]',)
PLATFORM_MPK_LABEL = (_PLATFORM_BIBLIO + '/div[3]/div[2]',)
PLATFORM_MPK = (_PLATFORM_BIBLIO + '/div[3]/div[3]',)          # если подпись в div[3] — «МПК»
PLATFORM_MPK_SHIFTED = (_PLATFORM_BIBLIO + '/div[4]/div[3]',)  # иначе МПК строкой ниже

_PLATFORM_DOC = '/html/body/div/div/div[3]/div/div/div[2]/div[1]/div[3]/div/div[1]/div/div[1]/div[1]'
PLATFORM_NAME = (_PLATFORM_DOC + '/h1',)
PLATFORM_DATE = (_PLATFORM_DOC + '/div[5]/div[4]', _PLATFORM_DOC + '/div[4]/div[4]')


def scrape_platform(driver, request):
    driver.get(PLATFORM_URL)
    search_input = wait_for(driver, PLATFORM_SEARCH_INPUT)
    search_input.clear()
    search_input.send_keys(request)
    find_first(driver, PLATFORM_SEARCH_BUTTON).click()

    # из всей выдачи — документ с точно таким же номером, а не первый в списке
    find_exact_result(driver, request, PLATFORM_RESULT_ITEMS, link_xpaths=PLATFORM_RESULT_LINK).click()
    wait_for(driver, PLATFORM_COUNTRY)

    number = " ".join(text_of(driver, xpaths) for xpaths in (PLATFORM_COUNTRY, PLATFORM_NUMBER, PLATFORM_KIND))
    if text_of(driver, PLATFORM_MPK_LABEL) == "МПК":
        mpk = text_of(driver, PLATFORM_MPK)
    else:
        mpk = text_of(driver, PLATFORM_MPK_SHIFTED)
    return Patent(
        number=number,
        name=text_of(driver, PLATFORM_NAME),
        holder=get_patent_holder(driver),
        mpk=mpk,
        date=text_of(driver, PLATFORM_DATE),
    )


# ============================== WIPO Patentscope ==============================

WIPO_URL = "https://patentscope.wipo.int/search/ru/search.jsf"
WIPO_RESULTS_DELAY = 5  # сек.: после поиска сайт открывает либо список, либо сразу карточку
WIPO_SEARCH_FIELD = ('//*[@id="simpleSearchForm:fpSearch:input"]',)
WIPO_SEARCH_BUTTON = (
    '/html/body/div[2]/div[5]/div/div[2]/form/div/div[1]/div[2]/div/div/div[1]/div[2]/button',
    '//*[@id="simpleSearchForm:fpSearch:input"]/following::button[1]',
)
WIPO_RESULT_ITEMS = (
    '//*[starts-with(@id, "resultListForm:resultTable:") and contains(@id, ":patentResult")]',
)
WIPO_RESULT_LINK = ('./div[1]/div[1]/a', './/a')
WIPO_HEADER = ('//*[@id="headerForm:headerFormContent"]/h1/div/div[1]',)  # «1. CN103900678 - Название»

_WIPO_BIBLIO = '/html/body/div[2]/div[5]/div/div[1]/div[2]/form/div/div/div/div[1]/div/div/div[2]/div/div[1]'
WIPO_MPK = (
    _WIPO_BIBLIO + '/div[9]/span[2]/div/div[1]',
    _WIPO_BIBLIO + '/div[5]/span[2]/div/div[1]',
    _WIPO_BIBLIO + '/div[7]/span[2]/div/div[1]/div',
)
WIPO_DATE = (_WIPO_BIBLIO + '/div[5]/span[2]',)
# У части документов поля сдвинуты: тогда «МПК» совпадает с «датой», и берём другие строки
WIPO_MPK_SHIFTED = (_WIPO_BIBLIO + '/div[5]/span[2]/div/div[1]',)
WIPO_DATE_SHIFTED = (_WIPO_BIBLIO + '/div[2]/span[2]',)
WIPO_KIND_LABEL = (_WIPO_BIBLIO + '/div[6]/span[1]/span',)
WIPO_KIND_IF_LABEL = (_WIPO_BIBLIO + '/div[8]/span[2]',)   # если в div[6] подпись «Вид публикации»
WIPO_KIND_OTHERWISE = (_WIPO_BIBLIO + '/div[6]/span[2]',)


def _wipo_number_from_header(header):
    """«12. CN103900678 - Название» -> «CN103900678»."""
    before_dash = header.split(" - ", 1)[0]
    return re.sub(r"^\s*\d+\.\s*", "", before_dash).strip()


def _wipo_kind(driver):
    try:
        if text_of(driver, WIPO_KIND_LABEL) == "Вид публикации":
            return text_of(driver, WIPO_KIND_IF_LABEL)
        return text_of(driver, WIPO_KIND_OTHERWISE)
    except NoSuchElementException:
        return ""


def scrape_wipo(driver, request):
    driver.get(WIPO_URL)
    wait_for(driver, WIPO_SEARCH_FIELD, clickable=True).send_keys(request)
    find_first(driver, WIPO_SEARCH_BUTTON).click()
    time.sleep(WIPO_RESULTS_DELAY)

    if driver.find_elements(By.XPATH, WIPO_HEADER[0]):
        # по номеру сразу открылась карточка документа
        header = text_of(driver, WIPO_HEADER)
        number = request
    else:
        # открылся список — выбираем документ с точно таким же номером
        find_exact_result(driver, request, WIPO_RESULT_ITEMS, link_xpaths=WIPO_RESULT_LINK).click()
        header = wait_for(driver, WIPO_HEADER).text
        number = " ".join(part for part in (_wipo_number_from_header(header), _wipo_kind(driver)) if part)

    mpk = text_of(driver, WIPO_MPK)
    date = text_of(driver, WIPO_DATE)
    if mpk == date:
        mpk = text_of(driver, WIPO_MPK_SHIFTED)
        date = text_of(driver, WIPO_DATE_SHIFTED)
    return Patent(
        number=number,
        name=header.split(" - ", 1)[1] if " - " in header else header,
        holder=get_patent_holder(driver),
        mpk=mpk,
        date=date,
    )
