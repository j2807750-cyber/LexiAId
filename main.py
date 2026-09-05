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

GROUPS = {"risk": "Қауіп тобы", "neuro": "Нейротипикалық"}

SESSION_DEFS = [
    {
        "key": "A",
        "label": "А сессиясы",
        "format": "standard",
        "audio": False,
        "desc": "Стандартты форматтау, аудиоқолдаусыз",
    },
    {
        "key": "B",
        "label": "Б сессиясы",
        "format": "optimized",
        "audio": False,
        "desc": "WCAG 2.2 бойынша оңтайландырылған формат, аудиоқолдаусыз",
    },
    {
        "key": "V",
        "label": "В сессиясы",
        "format": "optimized",
        "audio": True,
        "desc": "Оңтайландырылған формат + синхронды ЖИ-дыбыстау",
    },
]

DEFAULT_TEXTS = [
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
]

# ----------------------------------------------------------------------
# сақтау (JSON файлдар — «ортақ» дерек ретінде)
# ----------------------------------------------------------------------


def load_texts():
    if TEXTS_FILE.exists():
        try:
            data = json.loads(TEXTS_FILE.read_text(encoding="utf-8"))
            if isinstance(data, list) and len(data) == 3:
                return data
        except Exception:
            pass
    return json.loads(json.dumps(DEFAULT_TEXTS))  # deep copy


def save_texts(texts):
    TEXTS_FILE.write_text(json.dumps(texts, ensure_ascii=False, indent=2), encoding="utf-8")


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
# форматтау стильдері (WCAG 2.2 талаптары)
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


def tts_widget(text, lang_pref=("kk", "ru")):
    """Speech Synthesis + сөзбе-сөз бөлектеу — өз алдына JS компонент."""
    words = words_of(text)
    words_json = json.dumps(words, ensure_ascii=False)
    text_json = json.dumps(text, ensure_ascii=False)
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
        cursor:pointer;">Дыбыстауды бастау</button>
      <button id="lexiaid-stop" style="font-family:'Manrope',sans-serif; font-weight:600;
        padding:10px 20px; border-radius:8px; border:1.5px solid #1B2A4A; background:transparent;
        color:#1B2A4A; cursor:pointer;">Тоқтату</button>
    </div>
    <script>
      const words = {words_json};
      const fullText = {text_json};
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
        const kk = voices.find(v => v.lang && v.lang.toLowerCase().startsWith('kk'));
        const ru = voices.find(v => v.lang && v.lang.toLowerCase().startsWith('ru'));
        if (kk) utter.voice = kk; else if (ru) utter.voice = ru;
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
# streamlit баптаулары мен стилі
# ----------------------------------------------------------------------

st.set_page_config(page_title="LexiAid", page_icon="📖", layout="centered")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700&family=Unbounded:wght@600;700&family=Atkinson+Hyperlegible:wght@400;700&display=swap');

    :root {
        --lx-navy: #1B2A4A;
        --lx-navy-hover: #263a63;
        --lx-gold: #C9A227;
        --lx-bg: #EEF1F4;
        --lx-panel: #FFFFFF;
        --lx-border: #e3e0d6;
        --lx-text: #24304a;
        --lx-muted: #5b5748;
    }

    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: var(--lx-bg) !important;
        color: var(--lx-text) !important;
        font-family: 'Manrope', sans-serif !important;
    }

    /* headings */
    h1, h2, h3, h4 {
        font-family: 'Unbounded', sans-serif !important;
        color: var(--lx-navy) !important;
    }

    /* every bit of plain text Streamlit renders (markdown, captions, labels) */
    p, span, label, li,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] span,
    [data-testid="stCaptionContainer"],
    [data-testid="stWidgetLabel"] p,
    .stRadio label, .stRadio p,
    .stCheckbox label {
        color: var(--lx-text) !important;
    }
    [data-testid="stCaptionContainer"] { color: var(--lx-muted) !important; }

    .lexiaid-eyebrow {
        font-family: 'Manrope', sans-serif;
        font-size: 12px; font-weight: 700;
        color: var(--lx-gold) !important;
        letter-spacing: 0.02em; margin-bottom: 2px;
    }

    .lexiaid-panel {
        background: var(--lx-panel) !important;
        border: 1.5px solid var(--lx-border);
        border-radius: 14px;
        padding: 28px;
        margin-top: 10px;
        color: var(--lx-text) !important;
    }

    /* buttons */
    div.stButton > button {
        font-family: 'Manrope', sans-serif !important;
        font-weight: 600;
        border-radius: 8px;
        background: var(--lx-navy) !important;
        color: #F7F4EE !important;
        border: none !important;
        padding: 0.55em 1.4em;
    }
    div.stButton > button:hover { background: var(--lx-navy-hover) !important; color: #F7F4EE !important; }
    div.stButton > button:disabled { opacity: 0.45; color: #F7F4EE !important; }
    div.stButton > button[kind="primary"] { background: var(--lx-gold) !important; color: var(--lx-navy) !important; }
    div.stButton > button[kind="primary"]:hover { background: #b8901f !important; }

    /* text inputs / text areas */
    .stTextInput input, .stTextArea textarea {
        background: #FFFFFF !important;
        color: var(--lx-text) !important;
        border: 1.5px solid #d8d3c4 !important;
        border-radius: 7px !important;
    }
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: #9a9584 !important;
    }

    /* radio buttons: label text + option text */
    .stRadio [role="radiogroup"] label p { color: var(--lx-text) !important; }
    .stRadio [role="radiogroup"] label div { color: var(--lx-text) !important; }

    /* tables */
    [data-testid="stTable"] table { background: #FFFFFF !important; color: var(--lx-text) !important; }
    [data-testid="stTable"] th { color: var(--lx-navy) !important; border-bottom: 2px solid var(--lx-border) !important; }
    [data-testid="stTable"] td { color: var(--lx-text) !important; border-bottom: 1px solid #ececec !important; }

    /* containers used for admin question cards */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FBFAF7 !important;
        border-color: var(--lx-border) !important;
    }

    hr { border-color: var(--lx-border) !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


def header(subtitle):
    st.markdown('<div class="lexiaid-eyebrow">Дарын РҒПО · биология бағыты</div>', unsafe_allow_html=True)
    st.markdown("# 📖 LexiAid")
    st.markdown(f"<div style='color:#5b5748; font-size:15px;'>{subtitle}</div>", unsafe_allow_html=True)
    st.markdown(
        "<div style='height:3px; width:64px; background:#C9A227; border-radius:2px; margin:14px 0 18px;'></div>",
        unsafe_allow_html=True,
    )


def results_table(rows):
    st.table(
        [
            {"Сессия": r["session"], "WPM": r["wpm"], "ER (%)": r["er"],
             "CI (%)": r["ci"], "Уақыт (с)": r["seconds"]}
            for r in rows
        ]
    )


# ----------------------------------------------------------------------
# session_state инициализациясы
# ----------------------------------------------------------------------

defaults = {
    "stage": "setup",
    "texts": load_texts(),
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
# навигация
# ----------------------------------------------------------------------

nav_col1, nav_col2, nav_col3 = st.columns(3)
with nav_col1:
    if st.button("🔄 Жаңа сессия", use_container_width=True):
        reset_all()
        st.rerun()
with nav_col2:
    if st.button("📝 Мәтіндерді баптау", use_container_width=True):
        st.session_state.stage = "admin"
        st.rerun()
with nav_col3:
    if st.button("📊 Пилоттық нәтижелер", use_container_width=True):
        st.session_state.stage = "dashboard"
        st.rerun()

stage = st.session_state.stage
current_session = SESSION_DEFS[st.session_state.session_idx] if st.session_state.session_idx < 3 else None
current_text = st.session_state.texts[st.session_state.session_idx] if st.session_state.session_idx < 3 else None

# ----------------------------------------------------------------------
# ЭКРАН: баптау (қатысушыны тіркеу)
# ----------------------------------------------------------------------

if stage == "setup":
    header("Дислексия қаупін ерте анықтауға арналған бейімделгіш оқу құралы")
    st.markdown('<div class="lexiaid-panel">', unsafe_allow_html=True)

    name = st.text_input("Қатысушының аты (немесе кодтық нөмірі)", placeholder="мыс. P-06 немесе Айгерім Қ.")
    group = st.radio("Топ", options=list(GROUPS.keys()), format_func=lambda k: GROUPS[k], horizontal=True)

    st.write(
        "Қатысушы кроссовер-дизайн бойынша үш сессиядан өтеді: А (стандартты формат), "
        "Б (WCAG 2.2 форматы), В (WCAG 2.2 форматы + ЖИ-дыбыстау). Әр сессиядан кейін "
        "5 бақылау сұрағына жауап беріледі."
    )

    if st.button("Сессияларды бастау", disabled=not name.strip()):
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
    header("3-тарау: практикалық эксперимент — кроссовер-дизайн")
    st.markdown('<div class="lexiaid-panel">', unsafe_allow_html=True)

    label = "Келесі сессия" if st.session_state.session_results else "Бірінші сессия"
    st.markdown(f'<div class="lexiaid-eyebrow">{label}</div>', unsafe_allow_html=True)
    st.markdown(f"### {current_session['label']}")
    st.write(current_session["desc"])
    st.write(f"Мәтін: «{current_text['title']}»")

    if st.session_state.session_results:
        results_table(st.session_state.session_results)

    btn_label = "Дыбыстауды бастау" if current_session["audio"] else "Оқуды бастау"
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
    header("3-тарау: практикалық эксперимент — кроссовер-дизайн")
    st.markdown('<div class="lexiaid-panel">', unsafe_allow_html=True)

    st.markdown(f"### {current_session['label']} — «{current_text['title']}»")
    st.caption(f"⏱ Таймер жүріп тұр · қате саны: {st.session_state.error_count}")

    if current_session["audio"]:
        st.write(
            "Төмендегі дыбыстау виджеті мәтінді дауыстап оқиды және оқылып жатқан "
            "сөзді бөлектейді. Оқу уақыты мен қателерді бақылаушы жеке белгілейді."
        )
        tts_widget(current_text["content"])
    else:
        st.markdown(
            f'<div style="{format_css(current_session["format"])}">{current_text["content"]}</div>',
            unsafe_allow_html=True,
        )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Қате белгілеу"):
            st.session_state.error_count += 1
            st.rerun()
    with col2:
        if st.button("Оқуды аяқтадым", type="primary"):
            st.session_state.elapsed = time.time() - st.session_state.timer_start
            st.session_state.timer_running = False
            st.session_state.stage = "quiz"
            st.session_state.answers = {}
            st.rerun()

    st.caption(
        "Бақылаушы: қатысушы сөзді дұрыс оқымаған, түсіріп алған немесе ауыстырған "
        "сәтте «Қате белгілеу» батырмасын басыңыз."
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# ЭКРАН: түсінік сұрақтары
# ----------------------------------------------------------------------

elif stage == "quiz":
    header("3-тарау: практикалық эксперимент — кроссовер-дизайн")
    st.markdown('<div class="lexiaid-panel">', unsafe_allow_html=True)
    st.markdown("### Мазмұнды түсіну сұрақтары")

    qs = current_text["questions"]
    for qi, q in enumerate(qs):
        key = f"q_{st.session_state.session_idx}_{qi}"
        choice = st.radio(f"{qi + 1}. {q['q']}", options=list(range(len(q["options"]))),
                           format_func=lambda oi, opts=q["options"]: opts[oi],
                           key=key, index=None)
        st.session_state.answers[qi] = choice

    all_answered = all(st.session_state.answers.get(qi) is not None for qi in range(len(qs)))

    if st.button("Жауаптарды растау", disabled=not all_answered):
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
    header("3-тарау: практикалық эксперимент — кроссовер-дизайн")
    st.markdown('<div class="lexiaid-panel">', unsafe_allow_html=True)

    p = st.session_state.participant
    st.markdown(f"### {p['name']} — эксперимент аяқталды")
    st.write(f"Топ: {GROUPS[p['group']]}")
    results_table(st.session_state.session_results)
    st.caption("Нәтиже жалпы пилоттық база кестесіне сақталды (барлық қатысушыларға ортақ).")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Жаңа қатысушы"):
            reset_all()
            st.rerun()
    with col2:
        if st.button("Пилоттық кестені көру"):
            st.session_state.stage = "dashboard"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# ЭКРАН: пилоттық нәтижелер тақтасы
# ----------------------------------------------------------------------

elif stage == "dashboard":
    header("3-тарау: практикалық эксперимент — кроссовер-дизайн")
    st.markdown('<div class="lexiaid-panel">', unsafe_allow_html=True)
    st.markdown("### Пилоттық сынақ нәтижелері")
    st.caption("Бұл кесте барлық қатысушылар үшін ортақ.")

    all_results = load_all_results()

    if not all_results:
        st.write("Әзірге сақталған нәтиже жоқ.")
    else:
        rows = []
        pairs = []
        for r in all_results:
            by_session = {x["session"]: x for x in r["results"]}
            a, b, v = by_session.get("A"), by_session.get("B"), by_session.get("V")
            rows.append({
                "Қатысушы": r["name"],
                "Топ": GROUPS.get(r["group"], r["group"]),
                "А: WPM/ER": f"{a['wpm']} / {a['er']}%" if a else "—",
                "Б: WPM/ER": f"{b['wpm']} / {b['er']}%" if b else "—",
                "В: WPM/ER": f"{v['wpm']} / {v['er']}%" if v else "—",
                "ER өзгерісі (А→В)": f"{round_(v['er'] - a['er'], 1)} п.п." if a and v else "—",
            })
            if a and v:
                pairs.append(a["er"] - v["er"])

        st.table(rows)

        ttest = paired_t_test(pairs)
        if ttest:
            st.markdown(
                f"""
                <div style="margin-top:20px; padding:16px; background:#F5F5F5; border-radius:8px;">
                  <b style="color:#1B2A4A;">Жұптық t-критерийі (А мен В сессиялары арасындағы ER)</b><br>
                  <span style="color:#5b5748; font-size:13.5px;">
                    n = {ttest['n']}, орташа айырма d̄ = {ttest['mean']} п.п., s_d = {ttest['sd']}
                    {f", t = {ttest['t']}" if ttest['t'] is not None else ""}
                  </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if st.button("Жаңарту"):
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# ЭКРАН: мәтіндерді баптау
# ----------------------------------------------------------------------

elif stage == "admin":
    header("3-тарау: практикалық эксперимент — кроссовер-дизайн")
    st.markdown('<div class="lexiaid-panel">', unsafe_allow_html=True)
    st.markdown("### Сессия мәтіндерін баптау")
    st.caption(
        "Үш мәтін сәйкесінше А, Б, В сессияларында қолданылады. Өзгерістер барлық "
        "қатысушылар үшін ортақ сақталады."
    )

    draft = json.loads(json.dumps(st.session_state.texts))  # deep copy

    for ti, t in enumerate(draft):
        st.markdown(f"**{SESSION_DEFS[ti]['label']} мәтіні**")
        t["title"] = st.text_input(f"Тақырып ({ti + 1})", value=t["title"], key=f"title_{ti}")
        t["content"] = st.text_area(f"Мәтін мазмұны ({ti + 1})", value=t["content"], key=f"content_{ti}", height=140)

        for qi, q in enumerate(t["questions"]):
            with st.container(border=True):
                q["q"] = st.text_input(f"Сұрақ {qi + 1}", value=q["q"], key=f"q_{ti}_{qi}")
                for oi in range(len(q["options"])):
                    q["options"][oi] = st.text_input(
                        f"Вариант {oi + 1}", value=q["options"][oi], key=f"opt_{ti}_{qi}_{oi}"
                    )
                q["correct"] = st.radio(
                    "Дұрыс жауап", options=list(range(len(q["options"]))),
                    format_func=lambda oi, opts=q["options"]: opts[oi],
                    index=q["correct"], key=f"correct_{ti}_{qi}", horizontal=True,
                )
        st.markdown("---")

    if st.button("Сақтау"):
        save_texts(draft)
        st.session_state.texts = draft
        st.success("Сақталды.")

    st.markdown("</div>", unsafe_allow_html=True)
