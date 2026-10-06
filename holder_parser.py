"""
Универсальный поиск патентообладателя на странице патента.

Идея: не привязываться к абсолютным XPath (они ломаются при любом изменении
вёрстки), а искать поле по его ПОДПИСИ — коду INID и/или названию поля.
Коды INID — международный стандарт ВОИС (ST.9), они одинаковы на ФИПС,
Платформе Роспатента и в большинстве баз:

    (71) — заявитель
    (72) — автор (изобретатель)
    (73) — патентообладатель
    (75) — автор, являющийся заявителем
    (76) — автор, являющийся заявителем и патентообладателем

Алгоритм:
1. JS-скрипт (один вызов execute_script) обходит DOM и находит все элементы,
   чей собственный текст НАЧИНАЕТСЯ с подписи поля («(73) Патентообладатель(и):»,
   «Заявители», «Applicants» и т.п.). Длинные абзацы описания («Заявитель
   апробировал...») отсекаются: подпись должна быть короткой.
2. Для каждой подписи берётся значение: либо текст в том же элементе после
   подписи (ФИПС: <p>(73) ...:<b>значение</b></p>), либо следующий соседний
   элемент (Платформа, WIPO: <div>подпись</div><div>значение</div>),
   при необходимости — сосед родителя.
3. Python выбирает результат строго по приоритету:
   патентообладатель -> заявитель. Поля авторов/изобретателей НИКОГДА
   не попадают в результат, даже если других полей не нашлось.
"""

import re
import time

HOLDER_NOT_FOUND = "Патентообладатель не найден"

# True  — брать актуального патентообладателя (с учётом извещений ФИПС
#         о смене наименования / отчуждении права, они идут ниже библиографии);
# False — брать патентообладателя из библиографии (на дату публикации).
PREFER_CURRENT_HOLDER = True

_FIELD_JS = r"""
const INID_RE = /^\(\s*(\d{2})\s*\)/;
const KIND_BY_CODE = {'73': 'holder', '76': 'holder',
                      '71': 'applicant', '75': 'applicant',
                      '72': 'author'};
// Порядок важен: сначала патентообладатель, затем заявитель, затем автор.
// «Автор(ы) и патентообладатель(и)» -> holder.
const KIND_BY_WORD = [
  ['holder',    /(патентообладател|правообладател|приобретател|владел|patentee|proprietor|owner|assignee|grantee|holder)/i],
  ['applicant', /(заявител|applicant)/i],
  ['author',    /(автор|изобретател|inventor)/i],
];
const SKIP_TAGS = new Set(['SCRIPT', 'STYLE', 'NOSCRIPT', 'INPUT', 'TEXTAREA',
                           'SELECT', 'OPTION', 'BUTTON', 'svg']);
const FORM_TAGS = new Set(['INPUT', 'SELECT', 'TEXTAREA']);

const norm = s => (s || '').replace(/ /g, ' ').replace(/[ \t\r\f\v]+/g, ' ')
                           .split('\n').map(x => x.trim()).filter(Boolean).join('\n');

function ownText(el) {
  let t = '';
  for (const n of el.childNodes) if (n.nodeType === 3) t += n.textContent;
  return norm(t).replace(/\n/g, ' ');
}

// Возвращает {kind, code, label} или null, если текст — не подпись поля.
function classifyLabel(text) {
  if (!text) return null;
  const colon = text.indexOf(':');
  const label = (colon >= 0 ? text.slice(0, colon) : text).trim();
  if (!label || label.length > 60) return null;         // абзац описания, а не подпись
  let rest = label, code = null;
  const m = rest.match(INID_RE);
  if (m) { code = m[1]; rest = rest.slice(m[0].length).trim(); }
  let kind = code ? (KIND_BY_CODE[code] || null) : null;
  if (rest) {
    // слово-подпись должно стоять В НАЧАЛЕ (отсекаем «Нормализованное
    // наименование патентообладателя», «PD4A Изменение ... патентообладателя»)
    let wordKind = null;
    for (const [k, re] of KIND_BY_WORD) {
      const mm = rest.match(re);
      if (mm && mm.index === 0) { wordKind = k; break; }
    }
    if (!wordKind && !code) return null;
    if (!kind) kind = wordKind;
    else if (wordKind === 'holder') kind = 'holder';    // (75)/(76) «... и патентообладатель»
  }
  if (!kind) return null;
  return {kind, code, label};
}

function textOf(el) { return norm(el.innerText || el.textContent || ''); }

function valueAfter(el) {
  // 1) значение внутри того же элемента после подписи (ФИПС)
  const full = textOf(el);
  const own = ownText(el);
  if (el.children.length) {
    let v = full;
    const colon = v.indexOf(':');
    if (own && colon >= 0 && colon <= own.length + 2) v = v.slice(colon + 1);
    else if (own && v.startsWith(own)) v = v.slice(own.length);
    v = norm(v);
    if (v && !classifyLabel(v.split('\n')[0])) return v;
  } else if (own.includes(':')) {
    const v = norm(own.slice(own.indexOf(':') + 1));
    if (v) return v;
  }
  // 2) следующий соседний элемент; если сосед сам подпись («(73)» -> «Патентообладатель»
  //    -> значение) — пропускаем его. 3) Не нашли — поднимаемся к родителю (до 3 уровней).
  let cur = el;
  for (let up = 0; up < 3 && cur; up++, cur = cur.parentElement) {
    let sib = cur.nextElementSibling;
    if (sib) {
      while (sib) {
        // подпись поля формы поиска (рядом input) — это не данные патента
        if (FORM_TAGS.has(sib.tagName) || sib.querySelector('input,select,textarea')) return null;
        const t = textOf(sib);
        // пустые элементы (иконки) и элементы, начинающиеся с подписи
        // другого поля, значением не считаем
        if (t && !classifyLabel(t.split('\n')[0])) return t.length <= 3000 ? t : null;
        sib = sib.nextElementSibling;
      }
      return null;   // соседи на этом уровне были, но значения среди них нет — выше не лезем
    }
    // соседей нет (подпись обёрнута, как в WIPO: <span><span>Заявители</span></span>) — поднимаемся
  }
  return null;
}

const root = arguments[0] || document;
const out = [];
const seen = new Set();
let order = 0;
for (const el of root.querySelectorAll('*')) {
  order++;
  if (SKIP_TAGS.has(el.tagName)) continue;
  const info = classifyLabel(ownText(el));
  if (!info) continue;
  const value = valueAfter(el);
  if (!value) continue;
  const key = info.kind + '|' + value;
  if (seen.has(key)) continue;          // «(73)» и «Патентообладатель» в соседних div
  seen.add(key);
  out.push({kind: info.kind, code: info.code, label: info.label, value, order});
}
return out;
"""


def extract_party_fields(driver, root=None):
    """Все найденные на странице поля «автор/заявитель/патентообладатель»."""
    return driver.execute_script(_FIELD_JS, root) or []


def _clean(value):
    """Склеивает строки значения, убирает пустые и повторы."""
    lines = []
    for line in re.split(r"[\n;]+", value or ""):
        line = line.strip(" ,\t")
        if line and line not in lines:
            lines.append(line)
    return "\n".join(lines)


def choose_holder(fields, prefer_current=PREFER_CURRENT_HOLDER):
    """
    Выбирает патентообладателя из списка полей.
    Возвращает (значение, вид_поля) — вид: 'holder' / 'applicant' / None.

    Проверки:
      * поля авторов (72, «Автор», «Изобретатели», «Inventors») отбрасываются всегда;
      * сначала ищем патентообладателя (73/76, «Патентообладатель», «Правообладатель»,
        «Приобретатель исключительного права», «Owner», «Assignee»...);
      * если его нет (заявка, PCT-публикация) — берём заявителя (71/75);
      * если нет и его — возвращаем HOLDER_NOT_FOUND, а НЕ авторов.
    """
    fields = sorted(fields, key=lambda f: f.get("order", 0))
    authors = {_clean(f["value"]) for f in fields if f["kind"] == "author"}

    for kind in ("holder", "applicant"):
        candidates = [f for f in fields if f["kind"] == kind]
        if not candidates:
            continue
        # ФИПС: извещения о смене патентообладателя идут ниже библиографии,
        # поэтому актуальный — последний по порядку в документе.
        picked = candidates[-1] if (kind == "holder" and prefer_current) else candidates[0]
        value = _clean(picked["value"])
        if value and value != HOLDER_NOT_FOUND:
            if value in authors and kind == "applicant":
                # Заявитель-физлицо совпадает с автором — это нормально,
                # но пусть будет видно в логе.
                print(f"[holder] заявитель совпадает с авторами: {value!r}")
            return value, kind
    return HOLDER_NOT_FOUND, None


def get_patent_holder(driver, timeout=10, root=None):
    """
    Ждёт (до timeout секунд), пока на странице появится патентообладатель
    или заявитель, и возвращает строку для колонки «Заявитель (правообладатель)».
    Работает одинаково для ФИПС, Платформы Роспатента и WIPO Patentscope.
    """
    deadline = time.time() + timeout
    fields, previous = [], None
    while True:
        try:
            fields = extract_party_fields(driver, root)
        except Exception as exc:  # страница ещё грузится / перерисовывается
            print(f"[holder] ошибка разбора страницы: {exc}")
            fields = []
        if any(f["kind"] == "holder" for f in fields):
            break
        # Патентообладателя нет (например, у заявки только заявитель) —
        # ждём, пока страница «устаканится», чтобы не выйти раньше времени.
        snapshot = [(f["kind"], f["value"]) for f in fields]
        if fields and snapshot == previous:
            break
        if time.time() >= deadline:
            break
        previous = snapshot
        time.sleep(0.5)
    value, kind = choose_holder(fields)
    if kind is None:
        print("[holder] патентообладатель не найден, найденные поля:",
              [(f["kind"], f["label"]) for f in fields])
    return value
