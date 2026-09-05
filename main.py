import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="LexiAid",
    page_icon="\U0001F989",
    layout="wide",
)

st.markdown(
    """
    <style>
        .block-container {padding: 0 !important; max-width: 100% !important;}
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

HTML_CONTENT = r'''
<!DOCTYPE html>
<html lang="kk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LexiAid</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:wght@400;500;700;800&family=Noto+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  :root{
    /* -------- light theme (default) -------- */
    --bg: #F6F1E6;
    --bg-soft: #EFE8D8;
    --surface: #FFFDF6;
    --surface-2: #FBF6EA;
    --text: #2A2620;
    --text-muted: #6B6355;
    --border: #E2D8C1;
    --primary: #2F7A6F;
    --primary-strong: #1F5B52;
    --primary-tint: #E1F0EC;
    --amber: #D98E2B;
    --amber-tint: #FBEBD2;
    --coral: #D9603D;
    --coral-tint: #FBE3D8;
    --green: #3F8F5F;
    --green-tint: #E1F1E5;
    --shadow: 0 6px 16px rgba(42,38,32,0.08);
    --radius-sm: 10px;
    --radius-md: 16px;
    --radius-lg: 24px;

    --user-font-scale: 1;
    --user-letter-spacing: 0.01em;
    --user-line-height: 1.65;
  }
  html[data-theme="dark"]{
    --bg: #14171A;
    --bg-soft: #1B1F23;
    --surface: #20252A;
    --surface-2: #262B31;
    --text: #ECE7D9;
    --text-muted: #A7A196;
    --border: #333A41;
    --primary: #55B7AA;
    --primary-strong: #7FCFC4;
    --primary-tint: #1E332F;
    --amber: #E9AE55;
    --amber-tint: #34291A;
    --coral: #E58164;
    --coral-tint: #34211A;
    --green: #77C296;
    --green-tint: #1C3323;
    --shadow: 0 8px 20px rgba(0,0,0,0.35);
  }

  *{box-sizing:border-box;}
  html,body{margin:0;padding:0;}
  body{
    background:var(--bg);
    color:var(--text);
    font-family:'Atkinson Hyperlegible Next','Noto Sans',sans-serif;
    font-size:calc(16px * var(--user-font-scale));
    line-height:var(--user-line-height);
    letter-spacing:var(--user-letter-spacing);
    transition:background .25s ease,color .25s ease;
    min-height:100vh;
  }
  h1,h2,h3{
    font-weight:800;
    letter-spacing:0;
    line-height:1.25;
    margin:0;
  }
  p{margin:0;}
  button{
    font-family:inherit;
    font-size:inherit;
    letter-spacing:inherit;
    cursor:pointer;
    border:none;
    background:none;
    color:inherit;
  }
  button:focus-visible, a:focus-visible, [tabindex]:focus-visible{
    outline:3px solid var(--primary);
    outline-offset:2px;
  }
  .app{
    max-width:720px;
    margin:0 auto;
    padding:0 18px 64px;
  }

  /* ---------- header ---------- */
  .topbar{
    position:sticky; top:0; z-index:20;
    background:var(--bg);
    border-bottom:1px solid var(--border);
    padding:14px 0;
  }
  .topbar-inner{
    max-width:720px;margin:0 auto;padding:0 18px;
    display:flex; align-items:center; justify-content:space-between; gap:12px;
  }
  .brand{
    display:flex; align-items:center; gap:10px;
  }
  .brand-mark{
    width:38px;height:38px;border-radius:12px;
    background:var(--primary);
    display:flex;align-items:center;justify-content:center;
    font-size:20px;
    flex-shrink:0;
    box-shadow:var(--shadow);
  }
  .brand-name{
    font-weight:800; font-size:1.15rem; color:var(--text);
    position:relative;
  }
  .brand-name span{color:var(--primary);}
  .top-controls{display:flex; align-items:center; gap:8px;}
  .lang-switch{
    display:flex; background:var(--surface-2); border:1px solid var(--border);
    border-radius:999px; padding:3px; gap:2px;
  }
  .lang-switch button{
    padding:6px 10px; border-radius:999px; font-weight:700; font-size:0.78rem;
    color:var(--text-muted);
  }
  .lang-switch button.active{
    background:var(--primary); color:#fff;
  }
  .icon-btn{
    width:38px;height:38px;border-radius:999px;
    background:var(--surface-2); border:1px solid var(--border);
    display:flex;align-items:center;justify-content:center;font-size:18px;
    flex-shrink:0;
  }
  .stat-pill{
    display:flex; align-items:center; gap:5px;
    background:var(--amber-tint); color:var(--amber);
    border-radius:999px; padding:6px 11px; font-weight:800; font-size:0.85rem;
  }

  /* ---------- home / path ---------- */
  .hero{
    display:flex; gap:14px; align-items:flex-start;
    background:var(--surface); border:1px solid var(--border);
    border-radius:var(--radius-lg); padding:18px; margin:20px 0 8px;
    box-shadow:var(--shadow);
  }

  /* ---------- name entry screen ---------- */
  .name-wrap{
    max-width:420px; margin:10vh auto 0; text-align:center; padding:0 8px;
  }
  .name-mascot{font-size:3.6rem; margin-bottom:14px;}
  .name-title{font-size:1.3rem; margin-bottom:8px;}
  .name-sub{color:var(--text-muted); margin-bottom:26px;}
  .name-input{
    width:100%; padding:16px 18px; font-size:1.15rem; font-weight:700;
    border-radius:var(--radius-md); border:2px solid var(--border);
    background:var(--surface); color:var(--text); text-align:center;
    margin-bottom:14px;
  }
  .name-input:focus{outline:none; border-color:var(--primary);}
  .name-error{color:var(--coral); font-weight:700; font-size:0.85rem; min-height:20px; margin-bottom:6px;}
  .mascot{
    font-size:2.4rem; flex-shrink:0;
    background:var(--primary-tint); width:58px;height:58px;border-radius:16px;
    display:flex;align-items:center;justify-content:center;
  }
  .hero-text h2{font-size:1.05rem;margin-bottom:4px;}
  .hero-text p{color:var(--text-muted); font-size:0.92rem;}

  .settings-toggle{
    margin:14px 0; display:flex; justify-content:flex-end;
  }
  .settings-toggle button{
    display:flex; align-items:center; gap:6px;
    color:var(--primary-strong); font-weight:700; font-size:0.85rem;
    padding:6px 4px;
  }
  .settings-panel{
    background:var(--surface); border:1px solid var(--border);
    border-radius:var(--radius-md); padding:16px; margin-bottom:18px;
    display:none; gap:14px; flex-direction:column;
  }
  .settings-panel.open{display:flex;}
  .settings-row{display:flex; flex-direction:column; gap:6px;}
  .settings-row label{font-size:0.82rem; font-weight:700; color:var(--text-muted); display:flex; justify-content:space-between;}
  .settings-row input[type=range]{width:100%; accent-color:var(--primary);}

  .path{
    position:relative;
    padding:24px 0 8px;
  }
  .path::before{
    content:"";
    position:absolute; left:50%; top:10px; bottom:10px; width:3px;
    transform:translateX(-50%);
    background-image:linear-gradient(var(--border) 60%, rgba(0,0,0,0) 0%);
    background-position:left; background-size:3px 14px; background-repeat:repeat-y;
  }
  .lesson-row{
    position:relative; display:flex; margin:6px 0 26px; z-index:1;
  }
  .lesson-row.l0{justify-content:center;}
  .lesson-row.l1{justify-content:flex-start; padding-left:8%;}
  .lesson-row.l2{justify-content:flex-end; padding-right:8%;}
  .lesson-node{
    display:flex; flex-direction:column; align-items:center; gap:8px;
    width:96px;
  }
  .lesson-circle{
    width:76px;height:76px;border-radius:50%;
    display:flex;align-items:center;justify-content:center;
    font-size:2rem;
    background:var(--surface-2); border:3px solid var(--border);
    box-shadow:var(--shadow);
    transition:transform .15s ease;
  }
  .lesson-node.unlocked .lesson-circle{
    background:var(--primary-tint); border-color:var(--primary);
  }
  .lesson-node.done .lesson-circle{
    background:var(--green-tint); border-color:var(--green);
  }
  .lesson-node.locked .lesson-circle{opacity:0.5;}
  .lesson-node:not(.locked):active .lesson-circle{transform:scale(0.94);}
  .lesson-label{font-size:0.82rem; font-weight:700; text-align:center; color:var(--text-muted);}

  /* ---------- exercise screen ---------- */
  .screen{display:none;}
  .screen.active{display:block;}
  .ex-header{
    display:flex; align-items:center; gap:12px; padding:14px 0;
  }
  .progress-track{
    flex:1; height:12px; border-radius:999px; background:var(--surface-2);
    border:1px solid var(--border); overflow:hidden;
  }
  .progress-fill{
    height:100%; background:var(--primary); border-radius:999px;
    transition:width .3s ease;
  }
  .ex-card{
    background:var(--surface); border:1px solid var(--border);
    border-radius:var(--radius-lg); padding:24px 20px; margin-top:8px;
    box-shadow:var(--shadow);
  }
  .ex-kicker{
    font-size:0.82rem; font-weight:700; color:var(--primary-strong); margin-bottom:10px;
  }
  .ex-prompt{font-size:1.15rem; font-weight:700; margin-bottom:18px;}
  .emoji-display{
    font-size:3.4rem; text-align:center; margin-bottom:8px;
  }
  .listen-btn{
    display:flex; align-items:center; justify-content:center; gap:8px;
    margin:0 auto 20px; background:var(--primary); color:#fff;
    padding:10px 20px; border-radius:999px; font-weight:700;
    box-shadow:var(--shadow);
  }
  .listen-btn:active{transform:scale(0.97);}
  .options-grid{
    display:grid; grid-template-columns:1fr 1fr; gap:12px;
  }
  .opt-btn{
    background:var(--surface-2); border:2px solid var(--border);
    border-radius:var(--radius-sm); padding:14px 10px; font-weight:700;
    font-size:1.05rem; text-align:center;
  }
  .opt-btn:active{transform:scale(0.97);}
  .opt-btn.correct{background:var(--green-tint); border-color:var(--green); color:var(--green);}
  .opt-btn.incorrect{background:var(--coral-tint); border-color:var(--coral); color:var(--coral);}
  .opt-btn[disabled]{cursor:default;}

  .sentence-block{
    background:var(--surface-2); border:1px solid var(--border);
    border-radius:var(--radius-md); padding:16px; margin-bottom:16px;
    font-size:1.15rem; font-weight:600;
  }
  .blank-choice{display:flex; gap:12px; justify-content:center; margin-bottom:6px;}
  .blank-choice .opt-btn{min-width:70px; font-size:1.3rem;}

  .tile-row{display:flex; flex-wrap:wrap; gap:10px; margin-bottom:18px; min-height:52px;
    background:var(--surface-2); border:1px dashed var(--border); border-radius:var(--radius-sm); padding:10px;}
  .tile-bank{display:flex; flex-wrap:wrap; gap:10px;}
  .tile{
    background:var(--primary-tint); border:2px solid var(--primary);
    color:var(--primary-strong); font-weight:800; font-size:1.1rem;
    padding:10px 16px; border-radius:var(--radius-sm);
  }
  .tile.placed{opacity:0.35; pointer-events:none;}
  .tile.answer{background:var(--surface); border-color:var(--border); color:var(--text);}

  .feedback{
    margin-top:16px; padding:14px 16px; border-radius:var(--radius-sm);
    font-weight:700; display:none; align-items:center; gap:10px;
  }
  .feedback.show{display:flex;}
  .feedback.good{background:var(--green-tint); color:var(--green);}
  .feedback.bad{background:var(--coral-tint); color:var(--coral);}

  .primary-btn{
    width:100%; margin-top:20px; background:var(--primary); color:#fff;
    padding:15px; border-radius:var(--radius-md); font-weight:800; font-size:1.05rem;
    box-shadow:var(--shadow);
  }
  .primary-btn:disabled{opacity:0.45;}
  .primary-btn:active:not(:disabled){transform:scale(0.98);}
  .ghost-btn{
    width:100%; margin-top:10px; padding:14px; border-radius:var(--radius-md);
    font-weight:700; color:var(--text-muted); border:1px solid var(--border);
  }

  /* ---------- results screen ---------- */
  .result-wrap{text-align:center; padding:40px 10px;}
  .result-emoji{font-size:4rem; margin-bottom:10px;}
  .result-title{font-size:1.4rem; margin-bottom:6px;}
  .result-sub{color:var(--text-muted); margin-bottom:22px;}
  .result-stats{display:flex; gap:12px; justify-content:center; margin-bottom:26px;}
  .result-stat{
    background:var(--surface); border:1px solid var(--border); border-radius:var(--radius-md);
    padding:16px 20px; min-width:110px; box-shadow:var(--shadow);
  }
  .result-stat b{display:block; font-size:1.5rem; color:var(--primary-strong);}
  .result-stat span{font-size:0.8rem; color:var(--text-muted); font-weight:700;}

  @media (max-width:420px){
    .lesson-row.l1{padding-left:2%;}
    .lesson-row.l2{padding-right:2%;}
    .options-grid{grid-template-columns:1fr;}
  }
</style>
</head>
<body>
<div class="app">

  <div class="topbar">
    <div class="topbar-inner">
      <div class="brand">
        <div class="brand-mark">🦉</div>
        <div class="brand-name">Lexi<span>Aid</span></div>
      </div>
      <div class="top-controls">
        <div class="stat-pill">🔥 <span id="streakCount">0</span></div>
        <div class="stat-pill" style="background:var(--primary-tint);color:var(--primary-strong);">⭐ <span id="xpCount">0</span></div>
        <div class="lang-switch" id="langSwitch">
          <button data-lang="kk">ҚАЗ</button>
          <button data-lang="ru">РУС</button>
          <button data-lang="en">ENG</button>
        </div>
        <button class="icon-btn" id="themeToggle" aria-label="Toggle theme">🌙</button>
      </div>
    </div>
  </div>

  <!-- ================= NAME ENTRY SCREEN ================= -->
  <div class="screen active" id="screen-name">
    <div class="name-wrap">
      <div class="name-mascot">🦉</div>
      <h2 class="name-title" id="nameTitle"></h2>
      <p class="name-sub" id="nameSub"></p>
      <input type="text" class="name-input" id="nameInput" maxlength="40" autocomplete="off">
      <div class="name-error" id="nameError"></div>
      <button class="primary-btn" id="startBtn"></button>
    </div>
  </div>

  <!-- ================= HOME SCREEN ================= -->
  <div class="screen" id="screen-home">
    <div class="hero">
      <div class="mascot">🦉</div>
      <div class="hero-text">
        <h2 id="heroTitle"></h2>
        <p id="heroSub"></p>
      </div>
    </div>

    <div class="settings-toggle">
      <button id="settingsToggleBtn">⚙️ <span id="settingsLabel"></span></button>
    </div>
    <div class="settings-panel" id="settingsPanel">
      <div class="settings-row">
        <label><span id="lblFontSize"></span> <span id="valFontSize"></span></label>
        <input type="range" id="fontSizeRange" min="0.9" max="1.6" step="0.05" value="1">
      </div>
      <div class="settings-row">
        <label><span id="lblSpacing"></span> <span id="valSpacing"></span></label>
        <input type="range" id="spacingRange" min="0" max="0.12" step="0.01" value="0.01">
      </div>
      <div class="settings-row">
        <label><span id="lblLineHeight"></span> <span id="valLineHeight"></span></label>
        <input type="range" id="lineHeightRange" min="1.3" max="2.2" step="0.05" value="1.65">
      </div>
    </div>

    <div class="path" id="pathContainer"></div>
  </div>

  <!-- ================= EXERCISE SCREEN ================= -->
  <div class="screen" id="screen-exercise">
    <div class="ex-header">
      <button class="icon-btn" id="exitExerciseBtn" aria-label="Close">✕</button>
      <div class="progress-track"><div class="progress-fill" id="exProgressFill" style="width:0%"></div></div>
    </div>
    <div class="ex-card" id="exCard"></div>
  </div>

  <!-- ================= RESULTS SCREEN ================= -->
  <div class="screen" id="screen-results">
    <div class="result-wrap">
      <div class="result-emoji">🎉</div>
      <h2 class="result-title" id="resultTitle"></h2>
      <p class="result-sub" id="resultSub"></p>
      <div class="result-stats">
        <div class="result-stat"><b id="resultXp">0</b><span id="lblXp">XP</span></div>
        <div class="result-stat"><b id="resultAcc">0%</b><span id="lblAcc">ACC</span></div>
      </div>
      <button class="primary-btn" id="continueBtn"></button>
    </div>
  </div>

</div>

<script>
/* ======================= SAFE STORAGE ======================= */
const safeStorage = {
  get(key, fallback){
    try{ const v = localStorage.getItem(key); return v===null ? fallback : JSON.parse(v); }
    catch(e){ return (safeStorage._mem && safeStorage._mem[key]!==undefined) ? safeStorage._mem[key] : fallback; }
  },
  set(key, value){
    try{ localStorage.setItem(key, JSON.stringify(value)); }
    catch(e){ safeStorage._mem = safeStorage._mem || {}; safeStorage._mem[key] = value; }
  }
};

/* ======================= I18N ======================= */
const I18N = {
  kk: {
    heroTitle: "Сәлем! Мен Лекси 🦉",
    heroSub: "Күн сайын аздап жаттығып, оқуды жеңілдетейік.",
    settings: "Оқу параметрлері",
    fontSize: "Әріп өлшемі",
    spacing: "Аралық қашықтық",
    lineHeight: "Жол аралығы",
    xp: "ұпай",
    listen: "Тыңдау",
    checkBtn: "Тексеру",
    continueBtn: "Жалғастыру",
    finishBtn: "Аяқтау",
    correct: "Дұрыс! Жарайсың 🎉",
    incorrect: "Ештеңе етпейді, қайталап көрейік:",
    kicker_choose: "Тыңда да, дұрыс жазылуын таңда",
    kicker_syll: "Буындарды дұрыс ретпен құрастыр",
    kicker_confuse: "Бос орынға дұрыс әріпті қой",
    kicker_read: "Мәтінді оқы да, сұраққа жауап бер",
    resultTitle: "Сабақ аяқталды!",
    resultSub: "Тамаша жұмыс, жалғастыра бер.",
    lblXp: "ҰПАЙ",
    lblAcc: "ДӘЛДІК",
    lockedHint: "Алдыңғы сабақты аяқта",
    nameTitle: "Алдымен танысайық",
    nameSub: "Жаттығуды бастамас бұрын атыңды жаз.",
    namePlaceholder: "Атыңды осында жаз",
    startBtn: "Бастау",
    nameErrorEmpty: "Атыңды жазуды ұмытпа 🙂",
    greeting: "Сәлем",
  },
  ru: {
    heroTitle: "Привет! Я Лекси 🦉",
    heroSub: "Занимаемся понемногу каждый день — так легче.",
    settings: "Настройки чтения",
    fontSize: "Размер букв",
    spacing: "Межбуквенный интервал",
    lineHeight: "Межстрочный интервал",
    xp: "очков",
    listen: "Слушать",
    checkBtn: "Проверить",
    continueBtn: "Продолжить",
    finishBtn: "Завершить",
    correct: "Верно! Отлично 🎉",
    incorrect: "Ничего страшного, попробуем ещё раз:",
    kicker_choose: "Послушай и выбери верное написание",
    kicker_syll: "Собери слово из слогов по порядку",
    kicker_confuse: "Вставь правильную букву в пропуск",
    kicker_read: "Прочитай текст и ответь на вопрос",
    resultTitle: "Урок завершён!",
    resultSub: "Отличная работа, продолжай в том же духе.",
    lblXp: "ОЧКИ",
    lblAcc: "ТОЧНОСТЬ",
    lockedHint: "Сначала пройди предыдущий урок",
    nameTitle: "Для начала познакомимся",
    nameSub: "Прежде чем начать, напиши своё имя.",
    namePlaceholder: "Напиши своё имя здесь",
    startBtn: "Начать",
    nameErrorEmpty: "Не забудь написать имя 🙂",
    greeting: "Привет",
  },
  en: {
    heroTitle: "Hi! I'm Lexi 🦉",
    heroSub: "A little practice every day makes reading easier.",
    settings: "Reading settings",
    fontSize: "Letter size",
    spacing: "Letter spacing",
    lineHeight: "Line spacing",
    xp: "points",
    listen: "Listen",
    checkBtn: "Check",
    continueBtn: "Continue",
    finishBtn: "Finish",
    correct: "Correct! Nice work 🎉",
    incorrect: "No worries, let's look again:",
    kicker_choose: "Listen, then choose the correct spelling",
    kicker_syll: "Build the word from syllables in order",
    kicker_confuse: "Fill the blank with the right letter",
    kicker_read: "Read the text and answer the question",
    resultTitle: "Lesson complete!",
    resultSub: "Great work — keep up the streak.",
    lblXp: "XP",
    lblAcc: "ACCURACY",
    lockedHint: "Finish the previous lesson first",
    nameTitle: "Let's get acquainted first",
    nameSub: "Write your name before you start practicing.",
    namePlaceholder: "Type your name here",
    startBtn: "Start",
    nameErrorEmpty: "Don't forget to write your name 🙂",
    greeting: "Hi",
  }
};
const SPEECH_LANG = { kk:'kk-KZ', ru:'ru-RU', en:'en-US' };

/* =====================================================================
   GOOGLE SHEET-ГЕ НӘТИЖЕ ЖІБЕРУ
   Төмендегі жолға өз Google Apps Script Web App URL-ыңды қой.
   Орнату нұсқаулығын чаттан қара (Apps Script коды бөлек берілді).
   ===================================================================== */
const GOOGLE_SHEET_WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbxCWKW6qT4py09_O-BFLSXEqXQSqHsrXeBkRgbCATo9xwH7d49VwoRKc9rtPQ-XyvYB/exec";

function sendResultToSheet(payload){
  if(!GOOGLE_SHEET_WEBHOOK_URL || GOOGLE_SHEET_WEBHOOK_URL.indexOf('PASTE_YOUR') === 0){
    console.warn('LexiAid: Google Sheet webhook URL орнатылмаған, нәтиже жіберілмеді.', payload);
    return;
  }
  try{
    fetch(GOOGLE_SHEET_WEBHOOK_URL, {
      method:'POST',
      mode:'no-cors',
      headers:{'Content-Type':'text/plain;charset=utf-8'},
      body: JSON.stringify(payload)
    }).catch(()=>{ /* желі қатесі болса да қосымша жұмысын жалғастыра береді */ });
  }catch(e){ /* fail silently — never break the lesson flow */ }
}

/* ======================= LESSON CONTENT ======================= */
const LESSONS = [
  {
    id:1, icon:'🔤',
    title:{kk:'Дыбыс пен әріп', ru:'Звук и буква', en:'Sound & letter'},
    exercises:[
      {type:'choose', emoji:'🐱',
        audio:{kk:'мысық', ru:'кошка', en:'cat'},
        options:{kk:['мысық','мысик','мысых','мысыт'], ru:['кошка','кошта','кожка','кошна'], en:['cat','tac','cad','cet']},
        correct:0},
      {type:'syllables', emoji:'📘',
        word:{kk:'кітап', ru:'школа', en:'pencil'},
        tiles:{kk:['кі','тап'], ru:['шко','ла'], en:['pen','cil']}},
      {type:'confuse',
        sentence:{kk:'Б_гін ауа райы жақсы.', ru:'П_ла лежит на столе.', en:'The _og barks loudly.'},
        full:{kk:'Бүгін ауа райы жақсы.', ru:'Пила лежит на столе.', en:'The dog barks loudly.'},
        pair:{kk:['ү','ұ'], ru:['и','у'], en:['d','b']},
        correct:0},
      {type:'read',
        sentence:{kk:'Ана бала ойыншықпен ойнайды.', ru:'Кот сидит на окне и смотрит во двор.', en:'The dog runs fast in the park.'},
        question:{kk:'Бала немен ойнайды?', ru:'Где сидит кот?', en:'Where does the dog run?'},
        options:{kk:['ойыншықпен','кітаппен','доппен'], ru:['на окне','на диване','в саду'], en:['in the park','in the house','in the car']},
        correct:0}
    ]
  },
  {
    id:2, icon:'🧩',
    title:{kk:'Буындар мен сөздер', ru:'Слоги и слова', en:'Syllables & words'},
    exercises:[
      {type:'choose', emoji:'🐟',
        audio:{kk:'балық', ru:'рыба', en:'fish'},
        options:{kk:['балық','балуқ','балиқ','балыг'], ru:['рыба','рыпа','рыда','рыза'], en:['fish','fihs','fsih','fisc']},
        correct:0},
      {type:'syllables', emoji:'🪟',
        word:{kk:'терезе', ru:'машина', en:'rabbit'},
        tiles:{kk:['те','ре','зе'], ru:['ма','ши','на'], en:['rab','bit']}},
      {type:'confuse',
        sentence:{kk:'Мен қазақ т_лін үйренемін.', ru:'За домом есть большая ро_а.', en:'In the ocean lives a giant _hale.'},
        full:{kk:'Мен қазақ тілін үйренемін.', ru:'За домом есть большая роща.', en:'In the ocean lives a giant whale.'},
        pair:{kk:['і','и'], ru:['щ','ш'], en:['w','m']},
        correct:0},
      {type:'read',
        sentence:{kk:'Мұғалім сыныпта кітап оқып берді.', ru:'Дети играют во дворе после школы.', en:'She read a book before going to sleep.'},
        question:{kk:'Мұғалім не істеді?', ru:'Когда дети играют во дворе?', en:'When did she read the book?'},
        options:{kk:['кітап оқып берді','ән айтты','сурет салды'], ru:['после школы','утром','ночью'], en:['before going to sleep','in the morning','during lunch']},
        correct:0}
    ]
  },
  {
    id:3, icon:'📖',
    title:{kk:'Мәтінді түсіну', ru:'Понимание текста', en:'Reading comprehension'},
    exercises:[
      {type:'choose', emoji:'🤝',
        audio:{kk:'достық', ru:'дружба', en:'friend'},
        options:{kk:['достық','дострық','досдық','достик'], ru:['дружба','друшба','дружда','дружьба'], en:['friend','freind','fiend','frend']},
        correct:0},
      {type:'syllables', emoji:'😊',
        word:{kk:'отбасы', ru:'радость', en:'happy'},
        tiles:{kk:['от','ба','сы'], ru:['ра','дость'], en:['hap','py']}},
      {type:'confuse',
        sentence:{kk:'Менің а_ам көмектесті.', ru:'У Ани есть верная с_бака.', en:'The elephant is very _ig.'},
        full:{kk:'Менің ағам көмектесті.', ru:'У Ани есть верная собака.', en:'The elephant is very big.'},
        pair:{kk:['ғ','г'], ru:['о','а'], en:['b','d']},
        correct:0},
      {type:'read',
        sentence:{kk:'Асан мектепке ерте барады. Ол достарымен ойнайды және сабақ оқиды.', ru:'Аня любит читать книги вечером. Её любимая книга про животных.', en:'Tom has a small dog named Max. Every morning, they go for a walk in the park.'},
        question:{kk:'Асан кіммен ойнайды?', ru:'Что любит делать Аня вечером?', en:"What is the dog's name?"},
        options:{kk:['достарымен','мұғаліммен','әжесімен'], ru:['читать книги','смотреть телевизор','гулять'], en:['Max','Rex','Buddy']},
        correct:0}
    ]
  }
];

/* ======================= STATE ======================= */
let state = {
  name: safeStorage.get('lexiaid_name',''),
  lang: safeStorage.get('lexiaid_lang','kk'),
  theme: safeStorage.get('lexiaid_theme','light'),
  xp: safeStorage.get('lexiaid_xp',0),
  streak: safeStorage.get('lexiaid_streak',0),
  completed: safeStorage.get('lexiaid_completed',[]),
  fontScale: safeStorage.get('lexiaid_fontScale',1),
  spacing: safeStorage.get('lexiaid_spacing',0.01),
  lineHeight: safeStorage.get('lexiaid_lineHeight',1.65),
};

let currentLesson = null;
let exIndex = 0;
let exResults = [];
let tileAnswer = [];

const $ = (id)=>document.getElementById(id);
function t(key){ return I18N[state.lang][key]; }

/* ======================= THEME ======================= */
function applyTheme(){
  document.documentElement.setAttribute('data-theme', state.theme);
  $('themeToggle').textContent = state.theme==='dark' ? '☀️' : '🌙';
}
$('themeToggle').addEventListener('click', ()=>{
  state.theme = state.theme==='dark' ? 'light' : 'dark';
  safeStorage.set('lexiaid_theme', state.theme);
  applyTheme();
});

/* ======================= LANGUAGE ======================= */
function applyLangButtons(){
  document.querySelectorAll('#langSwitch button').forEach(b=>{
    b.classList.toggle('active', b.dataset.lang===state.lang);
  });
  document.documentElement.lang = state.lang;
}
document.querySelectorAll('#langSwitch button').forEach(b=>{
  b.addEventListener('click', ()=>{
    state.lang = b.dataset.lang;
    safeStorage.set('lexiaid_lang', state.lang);
    applyLangButtons();
    renderNameTexts();
    renderHomeTexts();
    renderPath();
  });
});

/* ======================= READING SETTINGS ======================= */
function applyReadingVars(){
  document.documentElement.style.setProperty('--user-font-scale', state.fontScale);
  document.documentElement.style.setProperty('--user-letter-spacing', state.spacing+'em');
  document.documentElement.style.setProperty('--user-line-height', state.lineHeight);
  $('fontSizeRange').value = state.fontScale;
  $('spacingRange').value = state.spacing;
  $('lineHeightRange').value = state.lineHeight;
  $('valFontSize').textContent = Math.round(state.fontScale*100)+'%';
  $('valSpacing').textContent = state.spacing.toFixed(2)+'em';
  $('valLineHeight').textContent = state.lineHeight.toFixed(2);
}
$('fontSizeRange').addEventListener('input', e=>{ state.fontScale=parseFloat(e.target.value); safeStorage.set('lexiaid_fontScale',state.fontScale); applyReadingVars(); });
$('spacingRange').addEventListener('input', e=>{ state.spacing=parseFloat(e.target.value); safeStorage.set('lexiaid_spacing',state.spacing); applyReadingVars(); });
$('lineHeightRange').addEventListener('input', e=>{ state.lineHeight=parseFloat(e.target.value); safeStorage.set('lexiaid_lineHeight',state.lineHeight); applyReadingVars(); });
$('settingsToggleBtn').addEventListener('click', ()=>{
  $('settingsPanel').classList.toggle('open');
});

/* ======================= NAME SCREEN ======================= */
function renderNameTexts(){
  $('nameTitle').textContent = t('nameTitle');
  $('nameSub').textContent = t('nameSub');
  $('nameInput').placeholder = t('namePlaceholder');
  $('startBtn').textContent = t('startBtn');
  $('nameInput').value = state.name || '';
}
function submitName(){
  const val = $('nameInput').value.trim();
  if(!val){
    $('nameError').textContent = t('nameErrorEmpty');
    $('nameInput').focus();
    return;
  }
  state.name = val;
  safeStorage.set('lexiaid_name', state.name);
  $('nameError').textContent = '';
  showScreen('screen-home');
  renderHomeTexts();
  renderPath();
}
$('startBtn').addEventListener('click', submitName);
$('nameInput').addEventListener('keydown', (e)=>{ if(e.key==='Enter') submitName(); });

/* ======================= HOME RENDER ======================= */
function renderHomeTexts(){
  $('heroTitle').textContent = state.name ? `${t('greeting')}, ${state.name}! 👋` : t('heroTitle');
  $('heroSub').textContent = t('heroSub');
  $('settingsLabel').textContent = t('settings');
  $('lblFontSize').textContent = t('fontSize');
  $('lblSpacing').textContent = t('spacing');
  $('lblLineHeight').textContent = t('lineHeight');
  $('streakCount').textContent = state.streak;
  $('xpCount').textContent = state.xp;
}

function renderPath(){
  const container = $('pathContainer');
  container.innerHTML = '';
  LESSONS.forEach((lesson, idx)=>{
    const isDone = state.completed.includes(lesson.id);
    const isUnlocked = idx===0 || state.completed.includes(LESSONS[idx-1].id);
    const row = document.createElement('div');
    row.className = 'lesson-row l'+(idx%3);
    const node = document.createElement('div');
    node.className = 'lesson-node ' + (isDone?'done':(isUnlocked?'unlocked':'locked'));
    node.innerHTML = `
      <div class="lesson-circle">${isDone?'✅':lesson.icon}</div>
      <div class="lesson-label">${lesson.title[state.lang]}</div>
    `;
    node.addEventListener('click', ()=>{
      if(!isUnlocked){
        node.animate([{transform:'translateX(0)'},{transform:'translateX(-4px)'},{transform:'translateX(4px)'},{transform:'translateX(0)'}],{duration:250});
        return;
      }
      startLesson(lesson);
    });
    row.appendChild(node);
    container.appendChild(row);
  });
}

/* ======================= SPEECH ======================= */
function speak(text){
  try{
    if(!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = SPEECH_LANG[state.lang];
    u.rate = 0.9;
    window.speechSynthesis.speak(u);
  }catch(e){ /* speech not available, fail silently */ }
}

/* ======================= SCREEN SWITCH ======================= */
function showScreen(id){
  document.querySelectorAll('.screen').forEach(s=>s.classList.remove('active'));
  $(id).classList.add('active');
}

/* ======================= LESSON FLOW ======================= */
function startLesson(lesson){
  currentLesson = lesson;
  exIndex = 0;
  exResults = [];
  showScreen('screen-exercise');
  renderExercise();
}
$('exitExerciseBtn').addEventListener('click', ()=>{
  showScreen('screen-home');
  renderPath();
});

function renderExercise(){
  const total = currentLesson.exercises.length;
  $('exProgressFill').style.width = Math.round((exIndex/total)*100)+'%';
  const ex = currentLesson.exercises[exIndex];
  const card = $('exCard');
  card.innerHTML = '';

  if(ex.type==='choose'){
    card.innerHTML = `
      <div class="ex-kicker">${t('kicker_choose')}</div>
      <div class="emoji-display">${ex.emoji}</div>
      <button class="listen-btn" id="playAudio">🔊 ${t('listen')}</button>
      <div class="options-grid" id="optGrid"></div>
      <div class="feedback" id="fb"></div>
      <button class="primary-btn" id="checkBtn" disabled>${t('checkBtn')}</button>
    `;
    $('playAudio').addEventListener('click', ()=>speak(ex.audio[state.lang]));
    let selected = null;
    const grid = $('optGrid');
    ex.options[state.lang].forEach((opt, i)=>{
      const b = document.createElement('button');
      b.className='opt-btn'; b.textContent = opt;
      b.addEventListener('click', ()=>{
        if(grid.dataset.locked) return;
        grid.querySelectorAll('.opt-btn').forEach(x=>x.classList.remove('selected'));
        selected = i;
        b.style.borderColor='var(--primary)';
        grid.querySelectorAll('.opt-btn').forEach(x=>{ if(x!==b) x.style.borderColor='var(--border)'; });
        $('checkBtn').disabled = false;
      });
      grid.appendChild(b);
    });
    $('checkBtn').addEventListener('click', ()=>{
      if(selected===null) return;
      grid.dataset.locked='1';
      const correct = selected===ex.correct;
      Array.from(grid.children).forEach((b,i)=>{
        if(i===ex.correct) b.classList.add('correct');
        else if(i===selected) b.classList.add('incorrect');
        b.disabled = true;
      });
      speak(ex.audio[state.lang]);
      finishAnswer(correct);
    });
  }

  else if(ex.type==='syllables'){
    tileAnswer = [];
    const shuffled = [...ex.tiles[state.lang]].sort(()=>Math.random()-0.5);
    card.innerHTML = `
      <div class="ex-kicker">${t('kicker_syll')}</div>
      <div class="emoji-display">${ex.emoji}</div>
      <div class="tile-row" id="answerRow"></div>
      <div class="tile-bank" id="tileBank"></div>
      <div class="feedback" id="fb"></div>
      <button class="primary-btn" id="checkBtn" disabled>${t('checkBtn')}</button>
    `;
    const bank = $('tileBank');
    const answerRow = $('answerRow');
    function refreshCheck(){
      $('checkBtn').disabled = tileAnswer.length !== ex.tiles[state.lang].length;
    }
    shuffled.forEach((syll)=>{
      const tile = document.createElement('button');
      tile.className='tile'; tile.textContent = syll;
      tile.addEventListener('click', ()=>{
        if(tile.classList.contains('placed')) return;
        tile.classList.add('placed');
        tileAnswer.push(syll);
        const ansTile = document.createElement('span');
        ansTile.className='tile answer';
        ansTile.textContent = syll;
        answerRow.appendChild(ansTile);
        refreshCheck();
      });
      bank.appendChild(tile);
    });
    $('checkBtn').addEventListener('click', ()=>{
      const correct = JSON.stringify(tileAnswer)===JSON.stringify(ex.tiles[state.lang]);
      speak(ex.word[state.lang]);
      $('checkBtn').disabled = true;
      bank.querySelectorAll('.tile').forEach(t=>t.style.pointerEvents='none');
      finishAnswer(correct);
    });
  }

  else if(ex.type==='confuse'){
    let selected = null;
    const pair = [...ex.pair[state.lang]].sort(()=>Math.random()-0.5);
    card.innerHTML = `
      <div class="ex-kicker">${t('kicker_confuse')}</div>
      <div class="sentence-block">${ex.sentence[state.lang]}</div>
      <div class="blank-choice" id="pairChoice"></div>
      <div class="feedback" id="fb"></div>
      <button class="primary-btn" id="checkBtn" disabled>${t('checkBtn')}</button>
    `;
    const wrap = $('pairChoice');
    pair.forEach((letter)=>{
      const b = document.createElement('button');
      b.className='opt-btn'; b.textContent = letter;
      b.addEventListener('click', ()=>{
        if(wrap.dataset.locked) return;
        selected = letter;
        wrap.querySelectorAll('.opt-btn').forEach(x=>x.style.borderColor='var(--border)');
        b.style.borderColor='var(--primary)';
        $('checkBtn').disabled = false;
      });
      wrap.appendChild(b);
    });
    $('checkBtn').addEventListener('click', ()=>{
      wrap.dataset.locked='1';
      const correctLetter = ex.pair[state.lang][ex.correct];
      const correct = selected===correctLetter;
      Array.from(wrap.children).forEach(b=>{
        if(b.textContent===correctLetter) b.classList.add('correct');
        else if(b.textContent===selected) b.classList.add('incorrect');
        b.disabled=true;
      });
      $('checkBtn').disabled = true;
      speak(ex.full[state.lang]);
      finishAnswer(correct);
    });
  }

  else if(ex.type==='read'){
    let selected = null;
    card.innerHTML = `
      <div class="ex-kicker">${t('kicker_read')}</div>
      <div class="sentence-block">${ex.sentence[state.lang]}</div>
      <button class="listen-btn" id="playAudio">🔊 ${t('listen')}</button>
      <div class="ex-prompt">${ex.question[state.lang]}</div>
      <div class="options-grid" id="optGrid" style="grid-template-columns:1fr;"></div>
      <div class="feedback" id="fb"></div>
      <button class="primary-btn" id="checkBtn" disabled>${t('checkBtn')}</button>
    `;
    $('playAudio').addEventListener('click', ()=>speak(ex.sentence[state.lang]));
    const grid = $('optGrid');
    ex.options[state.lang].forEach((opt,i)=>{
      const b = document.createElement('button');
      b.className='opt-btn'; b.textContent=opt; b.style.textAlign='left';
      b.addEventListener('click', ()=>{
        if(grid.dataset.locked) return;
        selected = i;
        grid.querySelectorAll('.opt-btn').forEach(x=>x.style.borderColor='var(--border)');
        b.style.borderColor='var(--primary)';
        $('checkBtn').disabled = false;
      });
      grid.appendChild(b);
    });
    $('checkBtn').addEventListener('click', ()=>{
      grid.dataset.locked='1';
      const correct = selected===ex.correct;
      Array.from(grid.children).forEach((b,i)=>{
        if(i===ex.correct) b.classList.add('correct');
        else if(i===selected) b.classList.add('incorrect');
        b.disabled=true;
      });
      finishAnswer(correct);
    });
  }
}

function finishAnswer(correct){
  exResults.push(correct);
  const fb = $('fb');
  fb.classList.add('show', correct?'good':'bad');
  fb.textContent = correct ? t('correct') : t('incorrect');
  const isLast = exIndex === currentLesson.exercises.length-1;
  const btn = document.createElement('button');
  btn.className='primary-btn';
  btn.textContent = isLast ? t('finishBtn') : t('continueBtn');
  btn.style.marginTop='14px';
  $('exCard').appendChild(btn);
  btn.scrollIntoView({behavior:'smooth', block:'nearest'});
  btn.addEventListener('click', ()=>{
    if(isLast){ finishLesson(); }
    else { exIndex++; renderExercise(); }
  });
}

function finishLesson(){
  const correctCount = exResults.filter(Boolean).length;
  const total = exResults.length;
  const earnedXp = correctCount*10 + (total*2);
  state.xp += earnedXp;
  if(!state.completed.includes(currentLesson.id)){
    state.completed.push(currentLesson.id);
    state.streak += 1;
  }
  safeStorage.set('lexiaid_xp', state.xp);
  safeStorage.set('lexiaid_streak', state.streak);
  safeStorage.set('lexiaid_completed', state.completed);

  sendResultToSheet({
    name: state.name,
    lang: state.lang,
    lesson_id: currentLesson.id,
    lesson_title: currentLesson.title[state.lang],
    correct: correctCount,
    total: total,
    accuracy: Math.round((correctCount/total)*100),
    xp_earned: earnedXp,
    xp_total: state.xp,
    streak: state.streak,
    timestamp: new Date().toISOString()
  });

  $('resultTitle').textContent = t('resultTitle');
  $('resultSub').textContent = t('resultSub');
  $('resultXp').textContent = earnedXp;
  $('resultAcc').textContent = Math.round((correctCount/total)*100)+'%';
  $('lblXp').textContent = t('lblXp');
  $('lblAcc').textContent = t('lblAcc');
  $('continueBtn').textContent = t('continueBtn');
  $('continueBtn').onclick = ()=>{
    showScreen('screen-home');
    renderHomeTexts();
    renderPath();
  };
  showScreen('screen-results');
}

/* ======================= INIT ======================= */
function init(){
  applyTheme();
  applyLangButtons();
  applyReadingVars();
  renderNameTexts();
  renderHomeTexts();
  renderPath();
  if(state.name){
    showScreen('screen-home');
  } else {
    showScreen('screen-name');
  }
}
init();
</script>
</body>
</html>

'''

components.html(HTML_CONTENT, height=1500, scrolling=True)
