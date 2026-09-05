"""
LexiAid — дислексия қаупін диагностикалауға арналған адаптивті оқу құралы.
Дарын РҒПО (биология бағыты) жобасы — 3-тарау: практикалық эксперимент.

Іске қосу:
    pip install -r requirements.txt
    streamlit run lexiaid_streamlit.py
"""

import json
import math
import time
import uuid
from datetime import datetime
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

# ----------------------------------------------------------------------
# тұрақтылар
# ----------------------------------------------------------------------

DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
TEXTS_FILE = DATA_DIR / "texts_config.json"
RESULTS_FILE = DATA_DIR / "results.json"

LANGS = ["kk", "ru", "en"]
LANG_NAMES = {"kk": "ҚАЗ", "ru": "РУС", "en": "ENG"}
LANG_SPEECH_TAG = {"kk": "kk-KZ", "ru": "ru-RU", "en": "en-US"}

GROUPS_T = {
    "risk": {"kk": "Қауіп тобы", "ru": "Группа риска", "en": "At-risk group"},
    "neuro": {"kk": "Нейротипикалық", "ru": "Нейротипичная", "en": "Neurotypical"},
}

SESSION_DEFS = [
    {
        "key": "A",
        "format": "standard",
        "audio": False,
        "label": {"kk": "А сессиясы", "ru": "Сессия А", "en": "Session A"},
        "desc": {
            "kk": "Стандартты форматтау, аудиоқолдаусыз",
            "ru": "Стандартное форматирование, без аудиоподдержки",
            "en": "Standard formatting, no audio support",
        },
    },
    {
        "key": "B",
        "format": "optimized",
        "audio": False,
        "label": {"kk": "Б сессиясы", "ru": "Сессия Б", "en": "Session B"},
        "desc": {
            "kk": "WCAG 2.2 бойынша оңтайландырылған формат, аудиоқолдаусыз",
            "ru": "Оптимизированный формат по WCAG 2.2, без аудиоподдержки",
            "en": "WCAG 2.2 optimized format, no audio support",
        },
    },
    {
        "key": "V",
        "format": "optimized",
        "audio": True,
        "label": {"kk": "В сессиясы", "ru": "Сессия В", "en": "Session C"},
        "desc": {
            "kk": "Оңтайландырылған формат + синхронды ЖИ-дыбыстау",
            "ru": "Оптимизированный формат + синхронная ИИ-озвучка",
            "en": "Optimized format + synchronized AI narration",
        },
    },
]

# ----------------------------------------------------------------------
# UI мәтіндері (kk / ru / en)
# ----------------------------------------------------------------------

UI = {
    "app_title": {"kk": "LexiAid", "ru": "LexiAid", "en": "LexiAid"},
    "eyebrow": {
        "kk": "Дарын РҒПО · биология бағыты",
        "ru": "Дарын НОО · направление биологии",
        "en": "Daryn Youth Science Society · Biology track",
    },
    "subtitle_setup": {
        "kk": "Дислексия қаупін ерте анықтауға арналған бейімделгіш оқу құралы",
        "ru": "Адаптивный инструмент для раннего выявления риска дислексии",
        "en": "An adaptive tool for early detection of dyslexia risk",
    },
    "subtitle_exp": {
        "kk": "3-тарау: практикалық эксперимент — кроссовер-дизайн",
        "ru": "Глава 3: практический эксперимент — кроссовер-дизайн",
        "en": "Chapter 3: practical experiment — crossover design",
    },
    "nav_reset": {"kk": "🔄 Жаңа сессия", "ru": "🔄 Новая сессия", "en": "🔄 New session"},
    "nav_admin": {"kk": "📝 Мәтіндерді баптау", "ru": "📝 Настройка текстов", "en": "📝 Configure texts"},
    "nav_dashboard": {"kk": "📊 Пилоттық нәтижелер", "ru": "📊 Пилотные результаты", "en": "📊 Pilot results"},
    "theme_toggle": {"kk": "🌗 Тема", "ru": "🌗 Тема", "en": "🌗 Theme"},
    "participant_name": {
        "kk": "Қатысушының аты (немесе кодтық нөмірі)",
        "ru": "Имя участника (или код)",
        "en": "Participant name (or code)",
    },
    "participant_placeholder": {
        "kk": "мыс. P-06 немесе Айгерім Қ.",
        "ru": "напр. P-06 или Айгерим К.",
        "en": "e.g. P-06 or John D.",
    },
    "group_label": {"kk": "Топ", "ru": "Группа", "en": "Group"},
    "setup_desc": {
        "kk": "Қатысушы кроссовер-дизайн бойынша үш сессиядан өтеді: А (стандартты формат), "
              "Б (WCAG 2.2 форматы), В (WCAG 2.2 форматы + ЖИ-дыбыстау). Әр сессиядан кейін "
              "5 бақылау сұрағына жауап беріледі.",
        "ru": "Участник проходит три сессии по кроссовер-дизайну: А (стандартный формат), "
              "Б (формат WCAG 2.2), В (формат WCAG 2.2 + ИИ-озвучка). После каждой сессии "
              "участник отвечает на 5 контрольных вопросов.",
        "en": "The participant goes through three sessions in a crossover design: A (standard "
              "format), B (WCAG 2.2 format), C (WCAG 2.2 format + AI narration). After each "
              "session the participant answers 5 comprehension questions.",
    },
    "start_sessions": {"kk": "Сессияларды бастау", "ru": "Начать сессии", "en": "Start sessions"},
    "next_session": {"kk": "Келесі сессия", "ru": "Следующая сессия", "en": "Next session"},
    "first_session": {"kk": "Бірінші сессия", "ru": "Первая сессия", "en": "First session"},
    "text_label": {"kk": "Мәтін: «{title}»", "ru": "Текст: «{title}»", "en": "Text: “{title}”"},
    "start_audio": {"kk": "Дыбыстауды бастау", "ru": "Начать озвучивание", "en": "Start narration"},
    "start_reading": {"kk": "Оқуды бастау", "ru": "Начать чтение", "en": "Start reading"},
    "timer_caption": {
        "kk": "⏱ Таймер жүріп тұр · қате саны: {n}",
        "ru": "⏱ Таймер идёт · количество ошибок: {n}",
        "en": "⏱ Timer running · error count: {n}",
    },
    "audio_desc": {
        "kk": "Төмендегі дыбыстау виджеті мәтінді дауыстап оқиды және оқылып жатқан сөзді "
              "бөлектейді. Оқу уақыты мен қателерді бақылаушы жеке белгілейді.",
        "ru": "Виджет озвучивания ниже читает текст вслух и выделяет читаемое слово. Время "
              "чтения и ошибки отмечает наблюдатель отдельно.",
        "en": "The narration widget below reads the text aloud and highlights the word being "
              "read. Reading time and errors are marked separately by the observer.",
    },
    "mark_error": {"kk": "Қате белгілеу", "ru": "Отметить ошибку", "en": "Mark error"},
    "finish_reading": {"kk": "Оқуды аяқтадым", "ru": "Чтение завершено", "en": "Finished reading"},
    "observer_note": {
        "kk": "Бақылаушы: қатысушы сөзді дұрыс оқымаған, түсіріп алған немесе ауыстырған "
              "сәтте «Қате белгілеу» батырмасын басыңыз.",
        "ru": "Наблюдатель: нажимайте «Отметить ошибку», когда участник неправильно "
              "прочитал, пропустил или заменил слово.",
        "en": "Observer: press “Mark error” whenever the participant misreads, skips, or "
              "substitutes a word.",
    },
    "quiz_title": {
        "kk": "Мазмұнды түсіну сұрақтары",
        "ru": "Вопросы на понимание содержания",
        "en": "Comprehension questions",
    },
    "confirm_answers": {"kk": "Жауаптарды растау", "ru": "Подтвердить ответы", "en": "Confirm answers"},
    "finished_title": {
        "kk": "{name} — эксперимент аяқталды",
        "ru": "{name} — эксперимент завершён",
        "en": "{name} — experiment completed",
    },
    "group_display": {"kk": "Топ: {group}", "ru": "Группа: {group}", "en": "Group: {group}"},
    "saved_note": {
        "kk": "Нәтиже жалпы пилоттық база кестесіне сақталды (барлық қатысушыларға ортақ).",
        "ru": "Результат сохранён в общей пилотной базе (общей для всех участников).",
        "en": "The result has been saved to the shared pilot database (common to all participants).",
    },
    "new_participant": {"kk": "Жаңа қатысушы", "ru": "Новый участник", "en": "New participant"},
    "view_pilot_table": {
        "kk": "Пилоттық кестені көру",
        "ru": "Посмотреть пилотную таблицу",
        "en": "View pilot table",
    },
    "dashboard_title": {
        "kk": "Пилоттық сынақ нәтижелері",
        "ru": "Результаты пилотного испытания",
        "en": "Pilot test results",
    },
    "dashboard_caption": {
        "kk": "Бұл кесте барлық қатысушылар үшін ортақ.",
        "ru": "Эта таблица общая для всех участников.",
        "en": "This table is shared across all participants.",
    },
    "no_results": {
        "kk": "Әзірге сақталған нәтиже жоқ.",
        "ru": "Пока нет сохранённых результатов.",
        "en": "No saved results yet.",
    },
    "col_participant": {"kk": "Қатысушы", "ru": "Участник", "en": "Participant"},
    "col_group": {"kk": "Топ", "ru": "Группа", "en": "Group"},
    "col_a": {"kk": "А: WPM/ER", "ru": "А: WPM/ER", "en": "A: WPM/ER"},
    "col_b": {"kk": "Б: WPM/ER", "ru": "Б: WPM/ER", "en": "B: WPM/ER"},
    "col_v": {"kk": "В: WPM/ER", "ru": "В: WPM/ER", "en": "C: WPM/ER"},
    "col_delta": {
        "kk": "ER өзгерісі (А→В)",
        "ru": "Изменение ER (А→В)",
        "en": "ER change (A→C)",
    },
    "pp_unit": {"kk": "п.п.", "ru": "п.п.", "en": "pp"},
    "ttest_title": {
        "kk": "Жұптық t-критерийі (А мен В сессиялары арасындағы ER)",
        "ru": "Парный t-критерий (ER между сессиями А и В)",
        "en": "Paired t-test (ER between sessions A and C)",
    },
    "refresh": {"kk": "Жаңарту", "ru": "Обновить", "en": "Refresh"},
    "admin_title": {
        "kk": "Сессия мәтіндерін баптау",
        "ru": "Настройка текстов сессий",
        "en": "Configure session texts",
    },
    "admin_caption": {
        "kk": "Үш мәтін сәйкесінше А, Б, В сессияларында қолданылады. Өзгерістер осы тіл "
              "нұсқасы үшін сақталады.",
        "ru": "Три текста используются соответственно в сессиях А, Б, В. Изменения "
              "сохраняются для текущей версии языка.",
        "en": "The three texts are used in sessions A, B, C respectively. Changes are saved "
              "for the current language version.",
    },
    "session_text_header": {
        "kk": "**{label} мәтіні**",
        "ru": "**Текст сессии {label}**",
        "en": "**Text for {label}**",
    },
    "title_field": {"kk": "Тақырып ({n})", "ru": "Заголовок ({n})", "en": "Title ({n})"},
    "content_field": {
        "kk": "Мәтін мазмұны ({n})",
        "ru": "Содержание текста ({n})",
        "en": "Text content ({n})",
    },
    "question_field": {"kk": "Сұрақ {n}", "ru": "Вопрос {n}", "en": "Question {n}"},
    "option_field": {"kk": "Вариант {n}", "ru": "Вариант {n}", "en": "Option {n}"},
    "correct_answer": {"kk": "Дұрыс жауап", "ru": "Правильный ответ", "en": "Correct answer"},
    "save": {"kk": "Сақтау", "ru": "Сохранить", "en": "Save"},
    "saved_ok": {"kk": "Сақталды.", "ru": "Сохранено.", "en": "Saved."},
    "col_session": {"kk": "Сессия", "ru": "Сессия", "en": "Session"},
    "col_wpm": {"kk": "WPM", "ru": "WPM", "en": "WPM"},
    "col_er": {"kk": "ER (%)", "ru": "ER (%)", "en": "ER (%)"},
    "col_ci": {"kk": "CI (%)", "ru": "CI (%)", "en": "CI (%)"},
    "col_time": {"kk": "Уақыт (с)", "ru": "Время (с)", "en": "Time (s)"},
    "tts_play": {"kk": "Дыбыстауды бастау", "ru": "Начать озвучивание", "en": "Start narration"},
    "tts_stop": {"kk": "Тоқтату", "ru": "Остановить", "en": "Stop"},
}


def T(key, lang, **kwargs):
    template = UI[key][lang]
    return template.format(**kwargs) if kwargs else template


# ----------------------------------------------------------------------
# оқу мәтіндері — үш тілде
# ----------------------------------------------------------------------

DEFAULT_TEXTS_BY_LANG = {
    "kk": [
        {
            "id": "text1",
            "title": "Дала мен көш",
            "content": (
                "Ерте көктемде дала кең байтақ жасыл кілемге оранады. Қой үстінде "
                "қалықтаған бозторғайдың үні ауылдың ұйқысын ашады. Шопандар малын "
                "жаңа жайылымға қарай ертемен айдайды. Жолда кездескен әрбір бұлақ "
                "малға да, адамға да қуат береді. Балалар үйірімен өзен жағасына "
                "түсіп, тастан тас секіріп ойнайды. Кешкісін от басына жиналған "
                "үлкендер ескі аңыздарды баяндайды, ал жастар оны тыңдап, өз "
                "тілінің байлығын түсінеді. Түн түскенде аспанда жұлдыздар молайып, "
                "дала тыныштыққа бөленеді. Ертеңгі күн тағы да жаңа шаруамен "
                "басталады. Осылайша, дала өмірі жыл мезгіліне қарай өзгеріп, әр "
                "отбасының тағдырымен тығыз байланысады. Ауыл адамдарының "
                "бір-біріне деген қамқорлығы мен ынтымағы осындай қарапайым "
                "күндерде көрінеді."
            ),
            "questions": [
                {"q": "Дала қай мезгілде жасыл кілемге оранады?",
                 "options": ["Қыста", "Ерте көктемде", "Күзде", "Жаздың соңында"], "correct": 1},
                {"q": "Ауылдың ұйқысын не ашады?",
                 "options": ["Қораздың дауысы", "Бозторғайдың үні", "Жел дауысы", "Ит үруі"], "correct": 1},
                {"q": "Балалар қайда ойнайды?",
                 "options": ["Тау басында", "Өзен жағасында", "Үй ішінде", "Мектеп ауласында"], "correct": 1},
                {"q": "Кешкісін от басында не істейді?",
                 "options": ["Ән айтады", "Аңыз баяндайды", "Мал сойды", "Ұйықтайды"], "correct": 1},
                {"q": "Мәтін бойынша ауыл адамдарын не сипаттайды?",
                 "options": ["Бір-біріне қамқорлық пен ынтымақ", "Бір-бірімен бәсекелестік",
                             "Оқшаулану", "Немқұрайлылық"], "correct": 0},
            ],
        },
        {
            "id": "text2",
            "title": "Кітапхана сыры",
            "content": (
                "Қаланың орталығында үлкен әрі көне кітапхана орналасқан. Оның "
                "есігінен кірген сәтте кітаптың ерекше иісі мұрынға келеді. "
                "Оқырмандар тыныш бұрыштарда өз әлеміне беріліп, беттерді ақырын "
                "ашады. Кітапханашы әрбір келушіге қажетті кітапты тез тауып "
                "береді, себебі ол мыңдаған кітаптың орналасуын жатқа біледі. "
                "Балалар бөлімінде түрлі-түсті суретті кітаптар қатар тұр, ал "
                "үлкен адамдар ғылыми еңбектерді парақтайды. Демалыс күндері "
                "мұнда жас жазушылардың кездесуі өтеді, олар өз шығармаларынан "
                "үзінді оқып, оқырмандармен пікір алысады. Кешке қарай кітапхана "
                "жарығы жылы сарғыш түске боялып, ерекше ұйқы басар сезім "
                "тудырады. Осы жерде әр адам өзінің қызығушылығына сай жаңа "
                "білім табады. Кітапхана - тек кітап сақтайтын орын емес, ол "
                "қалалықтардың рухани демалыс алаңы."
            ),
            "questions": [
                {"q": "Кітапхана қала бойынша қай жерде орналасқан?",
                 "options": ["Шетінде", "Орталықта", "Су жағасында", "Тау бөктерінде"], "correct": 1},
                {"q": "Кітапханашы неге кітапты тез табады?",
                 "options": ["Компьютер көмегімен", "Орналасуын жатқа білгендіктен",
                             "Кездейсоқ", "Басқа қызметкерден сұрап"], "correct": 1},
                {"q": "Демалыс күндері кітапханада не өтеді?",
                 "options": ["Спорт жарысы", "Жас жазушылардың кездесуі", "Базар", "Концерт"], "correct": 1},
                {"q": "Кешке кітапхана жарығы қандай түске боялады?",
                 "options": ["Көк", "Жасыл", "Жылы сарғыш", "Қызыл"], "correct": 2},
                {"q": "Мәтін кітапханны немен сипаттайды?",
                 "options": ["Тек кітап сақтайтын орын", "Қалалықтардың рухани демалыс алаңы",
                             "Сауда орталығы", "Спорт залы"], "correct": 1},
            ],
        },
        {
            "id": "text3",
            "title": "Теңіз жағасындағы таң",
            "content": (
                "Атырау қаласының маңындағы өзен жағасында таң ерте оянған "
                "балықшылар қайығын дайындайды. Су бетінде әлі де таң "
                "шапағының қызғылт сәулесі шағылысады. Балықшылар жылдар бойы "
                "жинақтаған тәжірибесімен ауа райын дәл болжайды. Қайық суға "
                "түскен сәтте, толқындар жайлап оны алысқа қарай итереді. "
                "Жағада қалған балалар торларды ретке келтіріп, үлкендерге "
                "көмектеседі. Түскі уақытта ауылға оралған балықшылар өз "
                "олжасын ортаға салып, көршілерімен бөліседі. Кешкі ас кезінде "
                "отбасылар өзен туралы әңгіме қозғап, оның маңыздылығын жас "
                "ұрпаққа жеткізеді. Өзен тек тамақ көзі ғана емес, ол осы "
                "өңір тұрғындарының тарихымен тығыз байланысты киелі орын. "
                "Жыл сайын су деңгейінің өзгеруі тұрғындарды алаңдатады, "
                "сондықтан олар өзенді қорғауға ерекше мән береді."
            ),
            "questions": [
                {"q": "Балықшылар қайығын қашан дайындайды?",
                 "options": ["Түсте", "Таң ерте", "Кешке", "Түн ортасында"], "correct": 1},
                {"q": "Балықшылар ауа райын немен болжайды?",
                 "options": ["Радио арқылы", "Жинақтаған тәжірибесімен", "Кітаптан оқып", "Болжамайды"], "correct": 1},
                {"q": "Жағада қалған балалар не істейді?",
                 "options": ["Торларды ретке келтіреді", "Ойнап жүреді", "Ұйықтайды", "Мектепке барады"], "correct": 0},
                {"q": "Балықшылар олжасын не істейді?",
                 "options": ["Сатады", "Ортаға салып бөліседі", "Жасырады", "Тастайды"], "correct": 1},
                {"q": "Тұрғындарды не алаңдатады?",
                 "options": ["Су деңгейінің өзгеруі", "Жол құрылысы", "Базар бағасы", "Ауа температурасы"], "correct": 0},
            ],
        },
    ],
    "ru": [
        {
            "id": "text1",
            "title": "Степь и кочевье",
            "content": (
                "Ранней весной степь укутывается в широкий зелёный ковёр. Голос "
                "жаворонка, парящего над отарой, будит аул. Пастухи рано утром гонят "
                "скот на новое пастбище. Каждый родник, встреченный по пути, даёт "
                "силы и скоту, и людям. Дети всей гурьбой спускаются к реке и "
                "прыгают с камня на камень. Вечером старшие собираются у костра и "
                "рассказывают старинные легенды, а молодёжь слушает их и постигает "
                "богатство родного языка. Когда наступает ночь, на небе становится "
                "всё больше звёзд, и степь погружается в тишину. Новый день снова "
                "начинается с новых забот. Так жизнь степи меняется по временам "
                "года и тесно связана с судьбой каждой семьи. Забота и единство "
                "аульчан друг о друге проявляются именно в такие простые дни."
            ),
            "questions": [
                {"q": "В какое время года степь укутывается в зелёный ковёр?",
                 "options": ["Зимой", "Ранней весной", "Осенью", "В конце лета"], "correct": 1},
                {"q": "Что будит аул?",
                 "options": ["Крик петуха", "Голос жаворонка", "Шум ветра", "Лай собаки"], "correct": 1},
                {"q": "Где играют дети?",
                 "options": ["На вершине горы", "На берегу реки", "Дома", "Во дворе школы"], "correct": 1},
                {"q": "Что делают вечером у костра?",
                 "options": ["Поют песни", "Рассказывают легенды", "Режут скот", "Спят"], "correct": 1},
                {"q": "Что подчёркивает текст об аульчанах?",
                 "options": ["Заботу и единство друг о друге", "Соперничество друг с другом",
                             "Обособленность", "Равнодушие"], "correct": 0},
            ],
        },
        {
            "id": "text2",
            "title": "Тайна библиотеки",
            "content": (
                "В центре города расположена большая и старая библиотека. Как "
                "только входишь в её двери, в нос ударяет особый запах книг. "
                "Читатели в тихих уголках погружаются в свой мир и медленно "
                "переворачивают страницы. Библиотекарь быстро находит нужную книгу "
                "для каждого посетителя, ведь он наизусть знает расположение тысяч "
                "книг. В детском отделе рядами стоят яркие книги с картинками, а "
                "взрослые листают научные труды. По выходным здесь проходят встречи "
                "с молодыми писателями, которые читают отрывки из своих произведений "
                "и обмениваются мнениями с читателями. К вечеру свет в библиотеке "
                "окрашивается в тёплый жёлтый оттенок, создавая особое сонное "
                "настроение. Здесь каждый человек находит новые знания по своим "
                "интересам. Библиотека — не просто место хранения книг, это духовное "
                "пространство отдыха для горожан."
            ),
            "questions": [
                {"q": "Где расположена библиотека по отношению к городу?",
                 "options": ["На окраине", "В центре", "На берегу реки", "У подножия горы"], "correct": 1},
                {"q": "Почему библиотекарь быстро находит книгу?",
                 "options": ["С помощью компьютера", "Знает расположение наизусть",
                             "Случайно", "Спрашивает у другого сотрудника"], "correct": 1},
                {"q": "Что проходит в библиотеке по выходным?",
                 "options": ["Спортивные соревнования", "Встречи с молодыми писателями", "Рынок", "Концерт"], "correct": 1},
                {"q": "В какой оттенок окрашивается вечером свет библиотеки?",
                 "options": ["Синий", "Зелёный", "Тёплый жёлтый", "Красный"], "correct": 2},
                {"q": "Чем текст характеризует библиотеку?",
                 "options": ["Просто место хранения книг", "Духовное пространство отдыха горожан",
                             "Торговый центр", "Спортзал"], "correct": 1},
            ],
        },
        {
            "id": "text3",
            "title": "Рассвет на берегу реки",
            "content": (
                "На берегу реки близ города Атырау рано проснувшиеся рыбаки "
                "готовят свою лодку. На поверхности воды всё ещё отражаются "
                "розовые отблески зари. Рыбаки, накопившие опыт за долгие годы, "
                "точно предсказывают погоду. В момент, когда лодка спускается на "
                "воду, волны медленно уносят её вдаль. Оставшиеся на берегу дети "
                "приводят в порядок сети и помогают взрослым. Днём вернувшиеся в "
                "аул рыбаки делятся своим уловом с соседями. За вечерней трапезой "
                "семьи заводят разговор о реке и передают её значимость молодому "
                "поколению. Река — не просто источник пищи, это священное место, "
                "тесно связанное с историей жителей этого края. Ежегодное изменение "
                "уровня воды беспокоит жителей, поэтому они уделяют особое внимание "
                "защите реки."
            ),
            "questions": [
                {"q": "Когда рыбаки готовят свою лодку?",
                 "options": ["Днём", "Рано утром", "Вечером", "В полночь"], "correct": 1},
                {"q": "Чем рыбаки предсказывают погоду?",
                 "options": ["По радио", "Накопленным опытом", "Читая книги", "Не предсказывают"], "correct": 1},
                {"q": "Что делают оставшиеся на берегу дети?",
                 "options": ["Приводят в порядок сети", "Играют", "Спят", "Идут в школу"], "correct": 0},
                {"q": "Что делают рыбаки со своим уловом?",
                 "options": ["Продают", "Делятся с соседями", "Прячут", "Выбрасывают"], "correct": 1},
                {"q": "Что беспокоит жителей?",
                 "options": ["Изменение уровня воды", "Строительство дорог", "Цены на рынке", "Температура воздуха"], "correct": 0},
            ],
        },
    ],
    "en": [
        {
            "id": "text1",
            "title": "The Steppe and the Migration",
            "content": (
                "In early spring, the steppe wraps itself in a wide green carpet. "
                "The voice of a lark soaring above the flock wakes the village. "
                "Herders drive their livestock to new pastures early in the "
                "morning. Every spring they meet along the way gives strength to "
                "both animals and people. Children go down to the riverbank "
                "together and jump from stone to stone. In the evening, elders "
                "gather around the fire and tell old legends, while the young "
                "listen and come to understand the richness of their language. "
                "When night falls, the stars multiply in the sky, and the steppe "
                "settles into silence. A new day always begins with new tasks. "
                "Thus the life of the steppe changes with the seasons and is "
                "closely tied to the fate of every family. The care and unity of "
                "the villagers for one another show through in such simple days."
            ),
            "questions": [
                {"q": "In what season does the steppe wrap itself in a green carpet?",
                 "options": ["Winter", "Early spring", "Autumn", "Late summer"], "correct": 1},
                {"q": "What wakes the village?",
                 "options": ["A rooster's crow", "The lark's voice", "The sound of wind", "A dog barking"], "correct": 1},
                {"q": "Where do the children play?",
                 "options": ["On a mountaintop", "By the riverbank", "At home", "In the school yard"], "correct": 1},
                {"q": "What do people do by the fire in the evening?",
                 "options": ["Sing songs", "Tell legends", "Slaughter livestock", "Sleep"], "correct": 1},
                {"q": "What does the text say about the villagers?",
                 "options": ["Care and unity for one another", "Rivalry with each other",
                             "Isolation", "Indifference"], "correct": 0},
            ],
        },
        {
            "id": "text2",
            "title": "The Secret of the Library",
            "content": (
                "In the center of the city stands a large, old library. The "
                "moment you step through its doors, the distinct smell of books "
                "greets you. Readers settle into quiet corners, lost in their own "
                "world, slowly turning the pages. The librarian quickly finds the "
                "right book for every visitor, since he knows the location of "
                "thousands of books by heart. In the children's section, colorful "
                "picture books stand in rows, while adults leaf through scholarly "
                "works. On weekends, meetings with young writers are held here, "
                "where they read excerpts from their work and exchange views with "
                "readers. Toward evening, the library's light takes on a warm, "
                "golden hue, creating a special drowsy feeling. Here, every person "
                "finds new knowledge suited to their interests. The library is "
                "not merely a place to store books — it is a spiritual space of "
                "rest for the city's people."
            ),
            "questions": [
                {"q": "Where is the library located relative to the city?",
                 "options": ["On the outskirts", "In the center", "By the riverside", "At the foot of a mountain"], "correct": 1},
                {"q": "Why does the librarian find books quickly?",
                 "options": ["With a computer", "Knows the layout by heart", "By chance", "Asks another staff member"], "correct": 1},
                {"q": "What happens at the library on weekends?",
                 "options": ["Sports competitions", "Meetings with young writers", "A market", "A concert"], "correct": 1},
                {"q": "What hue does the library's light take on in the evening?",
                 "options": ["Blue", "Green", "Warm golden", "Red"], "correct": 2},
                {"q": "How does the text characterize the library?",
                 "options": ["Merely a place to store books", "A spiritual space of rest for city dwellers",
                             "A shopping center", "A gym"], "correct": 1},
            ],
        },
        {
            "id": "text3",
            "title": "Dawn by the Riverside",
            "content": (
                "By the riverbank near the city of Atyrau, fishermen who woke "
                "early prepare their boat. Pink reflections of dawn still shimmer "
                "on the water's surface. Fishermen, drawing on years of "
                "accumulated experience, predict the weather precisely. The "
                "moment the boat is launched, the waves slowly carry it away. "
                "Children who stay on shore tidy up the nets and help the "
                "adults. At midday, fishermen returning to the village share "
                "their catch with their neighbors. Over the evening meal, "
                "families talk about the river and pass its importance on to the "
                "younger generation. The river is not merely a source of food — "
                "it is a sacred place closely tied to the history of the "
                "region's people. The yearly change in water level worries the "
                "residents, so they pay special attention to protecting the "
                "river."
            ),
            "questions": [
                {"q": "When do the fishermen prepare their boat?",
                 "options": ["Midday", "Early morning", "Evening", "Midnight"], "correct": 1},
                {"q": "How do fishermen predict the weather?",
                 "options": ["By radio", "Through accumulated experience", "By reading books", "They don't predict it"], "correct": 1},
                {"q": "What do the children who stay on shore do?",
                 "options": ["Tidy up the nets", "Play", "Sleep", "Go to school"], "correct": 0},
                {"q": "What do fishermen do with their catch?",
                 "options": ["Sell it", "Share it with neighbors", "Hide it", "Throw it away"], "correct": 1},
                {"q": "What worries the residents?",
                 "options": ["Change in water level", "Road construction", "Market prices", "Air temperature"], "correct": 0},
            ],
        },
    ],
}

# ----------------------------------------------------------------------
# сақтау (JSON файлдар — «ортақ» дерек ретінде)
# ----------------------------------------------------------------------


def load_all_texts():
    """Барлық тілдердегі мәтіндерді қайтарады, сақталған өзгерістермен біріктіріп."""
    data = {}
    saved = {}
    if TEXTS_FILE.exists():
        try:
            saved = json.loads(TEXTS_FILE.read_text(encoding="utf-8"))
        except Exception:
            saved = {}
    for lang in LANGS:
        entry = saved.get(lang) if isinstance(saved, dict) else None
        if isinstance(entry, list) and len(entry) == 3:
            data[lang] = entry
        else:
            data[lang] = json.loads(json.dumps(DEFAULT_TEXTS_BY_LANG[lang]))  # deep copy
    return data


def save_texts_for_lang(lang, texts):
    saved = {}
    if TEXTS_FILE.exists():
        try:
            saved = json.loads(TEXTS_FILE.read_text(encoding="utf-8"))
        except Exception:
            saved = {}
    if not isinstance(saved, dict):
        saved = {}
    saved[lang] = texts
    TEXTS_FILE.write_text(json.dumps(saved, ensure_ascii=False, indent=2), encoding="utf-8")


def load_all_results():
    if RESULTS_FILE.exists():
        try:
            return json.loads(RESULTS_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []


def save_participant_result(record):
    all_results = load_all_results()
    all_results = [r for r in all_results if r["id"] != record["id"]]
    all_results.append(record)
    RESULTS_FILE.write_text(json.dumps(all_results, ensure_ascii=False, indent=2), encoding="utf-8")


# ----------------------------------------------------------------------
# метрикалар
# ----------------------------------------------------------------------


def words_of(text):
    return text.strip().split()


def round_(n, d=1):
    f = 10 ** d
    return round(n * f) / f


def compute_metrics(total_words, error_count, seconds, correct_answers, total_questions):
    safe_seconds = max(seconds, 1)
    wpm = ((total_words - error_count) / safe_seconds) * 60
    er = (error_count / total_words) * 100
    ci = (correct_answers / total_questions) * 100
    return {
        "wpm": round_(max(wpm, 0)),
        "er": round_(er),
        "ci": round_(ci),
        "seconds": round_(seconds),
    }


def paired_t_test(diffs):
    n = len(diffs)
    if n < 2:
        return None
    mean = sum(diffs) / n
    variance = sum((d - mean) ** 2 for d in diffs) / (n - 1)
    sd = math.sqrt(variance)
    if sd == 0:
        return {"t": None, "mean": round_(mean, 2), "sd": 0, "n": n}
    t = mean / (sd / math.sqrt(n))
    return {"t": round_(t, 3), "mean": round_(mean, 2), "sd": round_(sd, 2), "n": n}


# ----------------------------------------------------------------------
# форматтау стильдері (WCAG 2.2 талаптары) — тақырыптан тәуелсіз, эксперимент
# шарттарының бір бөлігі болғандықтан ашық/қараңғы тақырыпқа өзгермейді
# ----------------------------------------------------------------------


def format_css(fmt):
    if fmt == "standard":
        return """
            font-family: Arial, Helvetica, sans-serif;
            font-size: 16px;
            line-height: 1.0;
            letter-spacing: normal;
            word-spacing: normal;
            text-align: justify;
            color: #000000;
            background: #FFFFFF;
            padding: 24px;
            border-radius: 4px;
            border: 1px solid #d8d8d8;
        """
    return """
        font-family: 'Atkinson Hyperlegible', Verdana, Arial, sans-serif;
        font-size: 18px;
        line-height: 1.5;
        letter-spacing: 0.12em;
        word-spacing: 0.16em;
        text-align: left;
        color: #1A1A1A;
        background: #F5F5F5;
        padding: 28px;
        border-radius: 10px;
        border: 1px solid #e3e0d6;
    """


def tts_widget(text, lang, ui_lang):
    """Speech Synthesis + сөзбе-сөз бөлектеу — өз алдына JS компонент.

    `lang` — мәтіннің тілі (дыбыс синтезін таңдау үшін),
    `ui_lang` — интерфейс тілі (батырма жазулары үшін).
    """
    words = words_of(text)
    words_json = json.dumps(words, ensure_ascii=False)
    text_json = json.dumps(text, ensure_ascii=False)
    speech_tag = LANG_SPEECH_TAG.get(lang, "kk-KZ")
    speech_prefix = lang
    play_label = T("tts_play", ui_lang)
    stop_label = T("tts_stop", ui_lang)
    html = f"""
    <div id="lexiaid-tts" style="font-family:'Atkinson Hyperlegible',Verdana,Arial,sans-serif;
         font-size:18px; line-height:1.5; letter-spacing:0.12em; word-spacing:0.16em;
         text-align:left; color:#1A1A1A; background:#F5F5F5; padding:28px;
         border-radius:10px; border:1px solid #e3e0d6;">
      <div id="lexiaid-words"></div>
    </div>
    <div style="margin-top:14px; display:flex; gap:10px;">
      <button id="lexiaid-play" style="font-family:'Manrope',sans-serif; font-weight:600;
        padding:10px 20px; border-radius:8px; border:none; background:#1B2A4A; color:#F7F4EE;
        cursor:pointer;">{play_label}</button>
      <button id="lexiaid-stop" style="font-family:'Manrope',sans-serif; font-weight:600;
        padding:10px 20px; border-radius:8px; border:1.5px solid #1B2A4A; background:transparent;
        color:#1B2A4A; cursor:pointer;">{stop_label}</button>
    </div>
    <script>
      const words = {words_json};
      const fullText = {text_json};
      const preferredTag = {json.dumps(speech_tag)};
      const preferredPrefix = {json.dumps(speech_prefix)};
      const container = document.getElementById('lexiaid-words');
      container.innerHTML = words.map((w, i) => `<span id="w${{i}}">${{w}} </span>`).join('');

      function clearHighlight() {{
        words.forEach((_, i) => {{
          const el = document.getElementById('w' + i);
          if (el) {{ el.style.background = 'transparent'; el.style.color = 'inherit'; }}
        }});
      }}

      document.getElementById('lexiaid-play').onclick = function() {{
        window.speechSynthesis.cancel();
        const utter = new SpeechSynthesisUtterance(fullText);
        const voices = window.speechSynthesis.getVoices();
        const exact = voices.find(v => v.lang && v.lang.toLowerCase() === preferredTag.toLowerCase());
        const byPrefix = voices.find(v => v.lang && v.lang.toLowerCase().startsWith(preferredPrefix));
        const fallbackRu = voices.find(v => v.lang && v.lang.toLowerCase().startsWith('ru'));
        const chosen = exact || byPrefix || fallbackRu;
        if (chosen) utter.voice = chosen;
        utter.lang = preferredTag;
        utter.rate = 0.95;
        utter.onboundary = function(e) {{
          const upto = fullText.slice(0, e.charIndex);
          const idx = Math.max(upto.trim().split(/\\s+/).length - 1, 0);
          clearHighlight();
          const el = document.getElementById('w' + idx);
          if (el) {{ el.style.background = '#C9A227'; el.style.color = '#1B2A4A'; }}
        }};
        utter.onend = clearHighlight;
        window.speechSynthesis.speak(utter);
      }};

      document.getElementById('lexiaid-stop').onclick = function() {{
        window.speechSynthesis.cancel();
        clearHighlight();
      }};
    </script>
    """
    components.html(html, height=420, scrolling=True)


# ----------------------------------------------------------------------
# ашық / қараңғы тақырыптар (тек интерфейс қабығы үшін; WCAG эксперимент
# форматы жоғарыдағы format_css арқылы бөлек басқарылады)
# ----------------------------------------------------------------------

THEMES = {
    "light": {
        "accent": "#1B2A4A",
        "accent-hover": "#263a63",
        "gold": "#C9A227",
        "gold-hover": "#b8901f",
        "bg": "#EEF1F4",
        "panel": "#FFFFFF",
        "border": "#e3e0d6",
        "text": "#24304a",
        "muted": "#5b5748",
        "btn-text": "#F7F4EE",
        "primary-btn-text": "#1B2A4A",
        "input-bg": "#FFFFFF",
        "input-border": "#d8d3c4",
        "placeholder": "#9a9584",
        "table-border": "#ececec",
        "admin-bg": "#FBFAF7",
    },
    "dark": {
        "accent": "#8CA3D9",
        "accent-hover": "#A3B7E0",
        "gold": "#D4AF37",
        "gold-hover": "#c19d2e",
        "bg": "#10142A",
        "panel": "#1A1F3D",
        "border": "#2E3559",
        "text": "#E7E9F5",
        "muted": "#9AA0C0",
        "btn-text": "#0E1226",
        "primary-btn-text": "#1B140A",
        "input-bg": "#1E2442",
        "input-border": "#39406A",
        "placeholder": "#7A81A8",
        "table-border": "#2E3559",
        "admin-bg": "#181D38",
    },
}


# ----------------------------------------------------------------------
# streamlit баптаулары
# ----------------------------------------------------------------------

st.set_page_config(page_title="LexiAid", page_icon="📖", layout="centered")

defaults = {
    "stage": "setup",
    "lang": "kk",
    "theme": "light",
    "texts": load_all_texts(),
    "participant": {"id": "", "name": "", "group": "risk"},
    "session_idx": 0,
    "session_results": [],
    "error_count": 0,
    "timer_start": None,
    "timer_running": False,
    "elapsed": 0.0,
    "answers": {},
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

lang = st.session_state.lang
TH = THEMES[st.session_state.theme]
css_vars = "\n        ".join(f"--lx-{k}: {v};" for k, v in TH.items())

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700&family=Unbounded:wght@600;700&family=Atkinson+Hyperlegible:wght@400;700&display=swap');

    :root {{
        {css_vars}
    }}

    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
        background: var(--lx-bg) !important;
        color: var(--lx-text) !important;
        font-family: 'Manrope', sans-serif !important;
    }}

    /* headings */
    h1, h2, h3, h4 {{
        font-family: 'Unbounded', sans-serif !important;
        color: var(--lx-accent) !important;
    }}

    /* every bit of plain text Streamlit renders (markdown, captions, labels) */
    p, span, label, li,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stCaptionContainer"],
    [data-testid="stWidgetLabel"] p,
    .stRadio label, .stRadio p,
    .stCheckbox label {{
        color: var(--lx-text) !important;
    }}
    [data-testid="stCaptionContainer"] {{ color: var(--lx-muted) !important; }}

    .lexiaid-eyebrow {{
        font-family: 'Manrope', sans-serif;
        font-size: 12px; font-weight: 700;
        color: var(--lx-gold) !important;
        letter-spacing: 0.02em; margin-bottom: 2px;
    }}

    .lexiaid-panel {{
        background: var(--lx-panel) !important;
        border: 1.5px solid var(--lx-border);
        border-radius: 14px;
        padding: 28px;
        margin-top: 10px;
        color: var(--lx-text) !important;
    }}

    /* buttons */
    div.stButton > button {{
        font-family: 'Manrope', sans-serif !important;
        font-weight: 600;
        border-radius: 8px;
        background: var(--lx-accent) !important;
        color: var(--lx-btn-text) !important;
        border: none !important;
        padding: 0.55em 1.4em;
    }}
    div.stButton > button:hover {{ background: var(--lx-accent-hover) !important; color: var(--lx-btn-text) !important; }}
    div.stButton > button:disabled {{ opacity: 0.45; color: var(--lx-btn-text) !important; }}
    div.stButton > button[kind="primary"] {{ background: var(--lx-gold) !important; color: var(--lx-primary-btn-text) !important; }}
    div.stButton > button[kind="primary"]:hover {{ background: var(--lx-gold-hover) !important; }}

    /* the generic p/span text-color rule above wins over inherited button color
       (direct declarations beat inheritance), so force it back explicitly here */
    div.stButton > button p,
    div.stButton > button span,
    div.stButton > button div {{
        color: var(--lx-btn-text) !important;
    }}
    div.stButton > button[kind="primary"] p,
    div.stButton > button[kind="primary"] span,
    div.stButton > button[kind="primary"] div {{
        color: var(--lx-primary-btn-text) !important;
    }}

    /* text inputs / text areas */
    .stTextInput input, .stTextArea textarea {{
        background: var(--lx-input-bg) !important;
        color: var(--lx-text) !important;
        border: 1.5px solid var(--lx-input-border) !important;
        border-radius: 7px !important;
    }}
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {{
        color: var(--lx-placeholder) !important;
    }}

    /* radio buttons: label text + option text */
    .stRadio [role="radiogroup"] label p {{ color: var(--lx-text) !important; }}
    .stRadio [role="radiogroup"] label div {{ color: var(--lx-text) !important; }}

    /* tables */
    [data-testid="stTable"] table {{ background: var(--lx-panel) !important; color: var(--lx-text) !important; }}
    [data-testid="stTable"] th {{ color: var(--lx-accent) !important; border-bottom: 2px solid var(--lx-border) !important; }}
    [data-testid="stTable"] td {{ color: var(--lx-text) !important; border-bottom: 1px solid var(--lx-table-border) !important; }}

    /* containers used for admin question cards */
    [data-testid="stVerticalBlockBorderWrapper"] {{
        background: var(--lx-admin-bg) !important;
        border-color: var(--lx-border) !important;
    }}

    hr {{ border-color: var(--lx-border) !important; }}
    </style>
    """,
    unsafe_allow_html=True,
)


def header(subtitle):
    st.markdown(f'<div class="lexiaid-eyebrow">{T("eyebrow", lang)}</div>', unsafe_allow_html=True)
    st.markdown(f"# 📖 {T('app_title', lang)}")
    st.markdown(f"<div style='color:var(--lx-muted); font-size:15px;'>{subtitle}</div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='height:3px; width:64px; background:var(--lx-gold); border-radius:2px; margin:14px 0 18px;'></div>",
        unsafe_allow_html=True,
    )


def results_table(rows):
    st.table(
        [
            {
                T("col_session", lang): r["session"],
                T("col_wpm", lang): r["wpm"],
                T("col_er", lang): r["er"],
                T("col_ci", lang): r["ci"],
                T("col_time", lang): r["seconds"],
            }
            for r in rows
        ]
    )


def reset_all():
    st.session_state.stage = "setup"
    st.session_state.participant = {"id": "", "name": "", "group": "risk"}
    st.session_state.session_idx = 0
    st.session_state.session_results = []
    st.session_state.error_count = 0
    st.session_state.timer_start = None
    st.session_state.timer_running = False
    st.session_state.elapsed = 0.0
    st.session_state.answers = {}


# ----------------------------------------------------------------------
# тіл / тақырып таңдағыш + навигация
# ----------------------------------------------------------------------

top_col1, top_col2 = st.columns([2, 1])
with top_col1:
    chosen_lang = st.radio(
        "🌐",
        options=LANGS,
        format_func=lambda l: LANG_NAMES[l],
        index=LANGS.index(st.session_state.lang),
        horizontal=True,
        key="lang_radio",
        label_visibility="collapsed",
    )
    if chosen_lang != st.session_state.lang:
        st.session_state.lang = chosen_lang
        st.rerun()
with top_col2:
    theme_icon = "☀️" if st.session_state.theme == "dark" else "🌙"
    if st.button(f"{theme_icon} {T('theme_toggle', lang)}", use_container_width=True):
        st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
        st.rerun()

nav_col1, nav_col2, nav_col3 = st.columns(3)
with nav_col1:
    if st.button(T("nav_reset", lang), use_container_width=True):
        reset_all()
        st.rerun()
with nav_col2:
    if st.button(T("nav_admin", lang), use_container_width=True):
        st.session_state.stage = "admin"
        st.rerun()
with nav_col3:
    if st.button(T("nav_dashboard", lang), use_container_width=True):
        st.session_state.stage = "dashboard"
        st.rerun()

stage = st.session_state.stage
current_session = SESSION_DEFS[st.session_state.session_idx] if st.session_state.session_idx < 3 else None
current_text = (
    st.session_state.texts[lang][st.session_state.session_idx]
    if st.session_state.session_idx < 3
    else None
)

# ----------------------------------------------------------------------
# ЭКРАН: баптау (қатысушыны тіркеу)
# ----------------------------------------------------------------------

if stage == "setup":
    header(T("subtitle_setup", lang))
    st.markdown('<div class="lexiaid-panel">', unsafe_allow_html=True)

    name = st.text_input(T("participant_name", lang), placeholder=T("participant_placeholder", lang))
    group = st.radio(
        T("group_label", lang),
        options=list(GROUPS_T.keys()),
        format_func=lambda k: GROUPS_T[k][lang],
        horizontal=True,
    )

    st.write(T("setup_desc", lang))

    if st.button(T("start_sessions", lang), disabled=not name.strip()):
        st.session_state.participant = {
            "id": f"{name.strip().replace(' ', '_')}_{uuid.uuid4().hex[:8]}",
            "name": name.strip(),
            "group": group,
        }
        st.session_state.session_idx = 0
        st.session_state.session_results = []
        st.session_state.stage = "session_intro"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# ЭКРАН: сессия алдындағы кіріспе
# ----------------------------------------------------------------------

elif stage == "session_intro":
    header(T("subtitle_exp", lang))
    st.markdown('<div class="lexiaid-panel">', unsafe_allow_html=True)

    label = T("next_session", lang) if st.session_state.session_results else T("first_session", lang)
    st.markdown(f'<div class="lexiaid-eyebrow">{label}</div>', unsafe_allow_html=True)
    st.markdown(f"### {current_session['label'][lang]}")
    st.write(current_session["desc"][lang])
    st.write(T("text_label", lang, title=current_text["title"]))

    if st.session_state.session_results:
        results_table(st.session_state.session_results)

    btn_label = T("start_audio", lang) if current_session["audio"] else T("start_reading", lang)
    if st.button(btn_label):
        st.session_state.error_count = 0
        st.session_state.elapsed = 0.0
        st.session_state.timer_start = time.time()
        st.session_state.timer_running = True
        st.session_state.stage = "session"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# ЭКРАН: оқу сессиясы
# ----------------------------------------------------------------------

elif stage == "session":
    header(T("subtitle_exp", lang))
    st.markdown('<div class="lexiaid-panel">', unsafe_allow_html=True)

    st.markdown(f"### {current_session['label'][lang]} — «{current_text['title']}»")
    st.caption(T("timer_caption", lang, n=st.session_state.error_count))

    if current_session["audio"]:
        st.write(T("audio_desc", lang))
        tts_widget(current_text["content"], lang, lang)
    else:
        st.markdown(
            f'<div style="{format_css(current_session["format"])}">{current_text["content"]}</div>',
            unsafe_allow_html=True,
        )

    col1, col2 = st.columns(2)
    with col1:
        if st.button(T("mark_error", lang)):
            st.session_state.error_count += 1
            st.rerun()
    with col2:
        if st.button(T("finish_reading", lang), type="primary"):
            st.session_state.elapsed = time.time() - st.session_state.timer_start
            st.session_state.timer_running = False
            st.session_state.stage = "quiz"
            st.session_state.answers = {}
            st.rerun()

    st.caption(T("observer_note", lang))
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# ЭКРАН: түсінік сұрақтары
# ----------------------------------------------------------------------

elif stage == "quiz":
    header(T("subtitle_exp", lang))
    st.markdown('<div class="lexiaid-panel">', unsafe_allow_html=True)
    st.markdown(f"### {T('quiz_title', lang)}")

    qs = current_text["questions"]
    for qi, q in enumerate(qs):
        key = f"q_{lang}_{st.session_state.session_idx}_{qi}"
        choice = st.radio(f"{qi + 1}. {q['q']}", options=list(range(len(q["options"]))),
                           format_func=lambda oi, opts=q["options"]: opts[oi],
                           key=key, index=None)
        st.session_state.answers[qi] = choice

    all_answered = all(st.session_state.answers.get(qi) is not None for qi in range(len(qs)))

    if st.button(T("confirm_answers", lang), disabled=not all_answered):
        correct = sum(
            1 for qi, q in enumerate(qs) if st.session_state.answers.get(qi) == q["correct"]
        )
        total_words = len(words_of(current_text["content"]))
        metrics = compute_metrics(
            total_words, st.session_state.error_count, st.session_state.elapsed,
            correct, len(qs),
        )
        record = {"session": current_session["key"], **metrics, "correct": correct, "total": len(qs)}
        st.session_state.session_results.append(record)

        if st.session_state.session_idx < len(SESSION_DEFS) - 1:
            st.session_state.session_idx += 1
            st.session_state.stage = "session_intro"
        else:
            participant = st.session_state.participant
            save_participant_result({
                "id": participant["id"],
                "name": participant["name"],
                "group": participant["group"],
                "results": st.session_state.session_results,
                "savedAt": datetime.now().isoformat(),
            })
            st.session_state.stage = "finished"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# ЭКРАН: аяқталды
# ----------------------------------------------------------------------

elif stage == "finished":
    header(T("subtitle_exp", lang))
    st.markdown('<div class="lexiaid-panel">', unsafe_allow_html=True)

    p = st.session_state.participant
    st.markdown(f"### {T('finished_title', lang, name=p['name'])}")
    st.write(T("group_display", lang, group=GROUPS_T[p["group"]][lang]))
    results_table(st.session_state.session_results)
    st.caption(T("saved_note", lang))

    col1, col2 = st.columns(2)
    with col1:
        if st.button(T("new_participant", lang)):
            reset_all()
            st.rerun()
    with col2:
        if st.button(T("view_pilot_table", lang)):
            st.session_state.stage = "dashboard"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# ЭКРАН: пилоттық нәтижелер тақтасы
# ----------------------------------------------------------------------

elif stage == "dashboard":
    header(T("subtitle_exp", lang))
    st.markdown('<div class="lexiaid-panel">', unsafe_allow_html=True)
    st.markdown(f"### {T('dashboard_title', lang)}")
    st.caption(T("dashboard_caption", lang))

    all_results = load_all_results()

    if not all_results:
        st.write(T("no_results", lang))
    else:
        rows = []
        pairs = []
        for r in all_results:
            by_session = {x["session"]: x for x in r["results"]}
            a, b, v = by_session.get("A"), by_session.get("B"), by_session.get("V")
            group_name = GROUPS_T.get(r["group"], {}).get(lang, r["group"])
            rows.append({
                T("col_participant", lang): r["name"],
                T("col_group", lang): group_name,
                T("col_a", lang): f"{a['wpm']} / {a['er']}%" if a else "—",
                T("col_b", lang): f"{b['wpm']} / {b['er']}%" if b else "—",
                T("col_v", lang): f"{v['wpm']} / {v['er']}%" if v else "—",
                T("col_delta", lang): f"{round_(v['er'] - a['er'], 1)} {T('pp_unit', lang)}" if a and v else "—",
            })
            if a and v:
                pairs.append(a["er"] - v["er"])

        st.table(rows)

        ttest = paired_t_test(pairs)
        if ttest:
            st.markdown(
                f"""
                <div style="margin-top:20px; padding:16px; background:var(--lx-admin-bg); border-radius:8px;">
                  <b style="color:var(--lx-accent);">{T('ttest_title', lang)}</b><br>
                  <span style="color:var(--lx-muted); font-size:13.5px;">
                    n = {ttest['n']}, d̄ = {ttest['mean']} {T('pp_unit', lang)}, s_d = {ttest['sd']}
                    {f", t = {ttest['t']}" if ttest['t'] is not None else ""}
                  </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if st.button(T("refresh", lang)):
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# ЭКРАН: мәтіндерді баптау
# ----------------------------------------------------------------------

elif stage == "admin":
    header(T("subtitle_exp", lang))
    st.markdown('<div class="lexiaid-panel">', unsafe_allow_html=True)
    st.markdown(f"### {T('admin_title', lang)}")
    st.caption(T("admin_caption", lang))

    draft = json.loads(json.dumps(st.session_state.texts[lang]))  # deep copy

    for ti, t in enumerate(draft):
        st.markdown(T("session_text_header", lang, label=SESSION_DEFS[ti]["label"][lang]))
        t["title"] = st.text_input(T("title_field", lang, n=ti + 1), value=t["title"], key=f"title_{lang}_{ti}")
        t["content"] = st.text_area(
            T("content_field", lang, n=ti + 1), value=t["content"], key=f"content_{lang}_{ti}", height=140
        )

        for qi, q in enumerate(t["questions"]):
            with st.container(border=True):
                q["q"] = st.text_input(T("question_field", lang, n=qi + 1), value=q["q"], key=f"q_{lang}_{ti}_{qi}")
                for oi in range(len(q["options"])):
                    q["options"][oi] = st.text_input(
                        T("option_field", lang, n=oi + 1), value=q["options"][oi], key=f"opt_{lang}_{ti}_{qi}_{oi}"
                    )
                q["correct"] = st.radio(
                    T("correct_answer", lang), options=list(range(len(q["options"]))),
                    format_func=lambda oi, opts=q["options"]: opts[oi],
                    index=q["correct"], key=f"correct_{lang}_{ti}_{qi}", horizontal=True,
                )
        st.markdown("---")

    if st.button(T("save", lang)):
        save_texts_for_lang(lang, draft)
        st.session_state.texts[lang] = draft
        st.success(T("saved_ok", lang))

    st.markdown("</div>", unsafe_allow_html=True)
