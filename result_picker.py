"""
Выбор в списке результатов поиска патента с ТОЧНО таким же номером, как в запросе.

Проблема: по номеру сайты часто возвращают несколько документов (тот же номер
в другой базе, документы, в тексте которых упоминается искомый номер, аналоги
из других стран и т.д.), а программа кликала по первому в списке.

Решение:
1. Из запроса выделяем номер: страну (RU, CN, WO...), цифры и код вида (C1, U1, A...).
   «RU 2 848 852 C1», «RU2848852C1», «2848852» -> ('RU', '2848852', 'C1').
2. У каждой строки выдачи берём СОБСТВЕННЫЙ номер документа — первый номер
   в начале строки (в первых строках текста), а не любые цифры из реферата:
   так документ, который лишь ссылается на искомый номер, не будет выбран.
3. Совпадение «точь-в-точь»: цифры равны целиком (2848852 != 28488521),
   страна и код вида сравниваются, если они указаны и в запросе, и в выдаче.
4. Если подходящих строк несколько — предпочитаем ту, где совпал код вида.
5. Если точного совпадения нет — бросаем ExactResultNotFound (а не кликаем
   по первому попавшемуся), и в таблицу пишется пометка.
"""

import re
import time

from selenium.common.exceptions import StaleElementReferenceException, WebDriverException
from selenium.webdriver.common.by import By

# Сколько первых строк текста результата считаем «заголовком» с номером документа.
HEADER_LINES = 3

# Номер документа: [страна]? цифры [код вида]?
# Пробелы внутри цифр («2 848 852») убираются заранее в _normalize().
_NUMBER_RE = re.compile(
    r"(?<![A-Z0-9])"
    r"(?:([A-Z]{2})[\s\-]?)?"          # страна: RU, CN, WO...
    r"(\d{4,13})"                       # сам номер
    r"(?:[\s\-]?([A-Z]\d?))?"           # код вида: C1, U1, A, B2...
    r"(?![A-Z0-9])"
)


class ExactResultNotFound(Exception):
    def __init__(self, request, seen):
        self.request = request
        self.seen = seen  # номера, которые были в выдаче
        shown = ", ".join(seen[:10]) if seen else "выдача пуста"
        super().__init__(f"В выдаче нет документа с номером «{request}». Найдены: {shown}")


def _normalize(text):
    text = (text or "").upper().replace(" ", " ")
    # «2 848 852» -> «2848852», «232 170» -> «232170»
    return re.sub(r"(?<=\d)[  ](?=\d)", "", text)


def parse_numbers(text):
    """Все номера документов в тексте в порядке появления: [(страна, цифры, вид), ...].
    Части дат («27.02.2025», «2025-02-27») пропускаются."""
    text = _normalize(text)
    found = []
    for m in _NUMBER_RE.finditer(text):
        start, end = m.start(2), m.end(2)
        before = text[start - 1] if start > 0 else ""
        after = text[end:end + 2]
        if (before and before in "./") or re.match(r"[./\-]\d", after):
            continue  # кусок даты
        country, digits, kind = m.group(1), m.group(2), m.group(3)
        found.append((country, digits, kind))
    return found


def parse_request(request):
    """Номер из запроса пользователя."""
    numbers = parse_numbers(request)
    if not numbers:
        raise ValueError(f"Не удалось распознать номер в запросе: {request!r}")
    return numbers[0]


def _fmt(num):
    country, digits, kind = num
    return " ".join(x for x in (country, digits, kind) if x)


def match_score(wanted, candidate):
    """0 — не совпадает; 1 — совпали страна/цифры; 2 — совпал ещё и код вида."""
    w_country, w_digits, w_kind = wanted
    c_country, c_digits, c_kind = candidate
    if w_digits.lstrip("0") != c_digits.lstrip("0"):
        return 0
    if w_country and c_country and w_country != c_country:
        return 0
    if w_kind and c_kind:
        if w_kind == c_kind:
            return 2
        # «A» в запросе подходит к «A1», но «C1» не подходит к «C2»
        if w_kind[0] != c_kind[0] or (len(w_kind) == 2 and len(c_kind) == 2):
            return 0
    return 1


def own_number(item_text, link_text=""):
    """Собственный номер документа строки выдачи.
    Смотрим только «заголовок» строки (первые HEADER_LINES строк) и текст ссылки —
    номера из реферата/цитирований ниже не учитываются. Номер с кодом страны
    («RU 2848852 C1», «CN103900678») важнее голых цифр (например, из названия)."""
    header = "\n".join((item_text or "").splitlines()[:HEADER_LINES])
    numbers = parse_numbers(header + "\n" + (link_text or ""))
    if not numbers:
        return None
    with_country = [n for n in numbers if n[0]]
    return with_country[0] if with_country else numbers[0]


def pick_exact(request, items):
    """Чистая логика выбора (без браузера), удобно тестировать.
    items: [(item_text, link_text), ...]. Возвращает индекс подходящего элемента."""
    wanted = parse_request(request)
    best_index, best_score, seen = None, 0, []
    for i, (item_text, link_text) in enumerate(items):
        num = own_number(item_text, link_text)
        if num is None:
            continue
        seen.append(_fmt(num))
        score = match_score(wanted, num)
        if score > best_score:
            best_index, best_score = i, score
            if score == 2:
                break
    if best_index is None:
        raise ExactResultNotFound(request, seen)
    return best_index


def find_exact_result(driver, request, items_xpath, link_xpaths=(".//a",), timeout=15):
    """
    Ждёт выдачу и возвращает элемент для клика по документу с точно таким номером.
      items_xpath — XPath ВСЕХ строк выдачи (без индекса [1]!) или кортеж XPath-ов
                    (точный, затем запасной широкий);
      link_xpaths — относительные XPath ссылки внутри строки, пробуются по порядку
                    (если ни один не нашёлся — кликаем саму строку).
    Строки без номера (меню, заголовки таблицы) просто пропускаются, поэтому
    items_xpath можно делать широким.
    """
    xpaths = (items_xpath,) if isinstance(items_xpath, str) else tuple(items_xpath)
    deadline = time.time() + timeout
    last_error, previous_seen = ExactResultNotFound(request, []), None
    while time.time() < deadline:
        try:
            rows = []
            for xp in xpaths:  # первый XPath, который что-то нашёл
                rows = driver.find_elements(By.XPATH, xp)
                if rows:
                    break
            items, links = [], []
            for row in rows:
                link = row
                for xp in link_xpaths or ():
                    found = row.find_elements(By.XPATH, xp)
                    if found:
                        link = found[0]
                        break
                items.append((row.text, link.text if link is not row else ""))
                links.append(link)
            if items:
                index = pick_exact(request, items)
                print(f"[result] «{request}»: выбран результат №{index + 1} из {len(items)}")
                return links[index]
        except ExactResultNotFound as exc:
            # Выдача могла ещё не догрузиться. Если два раза подряд видим одно и то же —
            # значит, она загрузилась, и нужного номера в ней действительно нет.
            if exc.seen and exc.seen == previous_seen:
                raise
            last_error, previous_seen = exc, exc.seen
        except (StaleElementReferenceException, WebDriverException):
            pass  # страница перерисовалась во время чтения
        time.sleep(0.7)
    raise last_error
