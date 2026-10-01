# Urdu Voice Agent: PROGRESS.md

Goal: Do mode wali Streamlit app.
1. News voice-over: Roman Urdu ya Urdu script input, news-caster style MP3 output.
2. Quran tilawat: surah aur ayat range chunein, asli qari ki recording MP3 mein milti hai.

English terms (AI, Google, iPhone, etc.) news mode mein Latin letters mein rehte hain aur poora text ek hi flow mein parha jata hai.

Stack:
- News mode: OpenAI SDK (Groq base_url) + Edge TTS (Urdu voice ya Multilingual voice) + Streamlit
- Quran mode: alquran.cloud (Arabic text) + everyayah.com (qari ki ayat-by-ayat MP3) + requests + Streamlit

Cost: free (Groq free tier, Edge TTS, alquran.cloud, everyayah.com, Streamlit local).

## Folder structure

```
urdu-voice-agent/
  app.py
  requirements.txt
  .env.example
  .env            (aap banayenge, git mein mat dalna)
  .gitignore
  PROGRESS.md
```

`requirements.txt` mein ye packages hone chahiye: `streamlit`, `openai`, `edge-tts`, `python-dotenv`, `requests`.

## Status

- [x] Step 0: Files generate
- [x] Step 1: Python check
- [x] Step 2: Virtual environment
- [x] Step 3: Dependencies install
- [x] Step 4: Groq API key
- [x] Step 5: .env file
- [x] Step 6: Edge TTS quick test
- [x] Step 7: App run (localhost:8501)
- [x] Fix 1: Groq model 404 (ab model list Groq se automatic aati hai)
- [x] Fix 2: Download MP3 button (ab result session_state mein save hota hai)
- [x] Fix 3: Awaaz tor tor ke aa rahi thi. Ab split band hai, poora text ek hi voice se ek hi bar mein synthesize hota hai
- [x] Feature: Multilingual voices (Andrew, Brian, Ava, Emma) test ke liye add
- [x] Feature: Quran tilawat mode (8 qari, 114 surah, ayat range, Bismillah option, MP3 download)
- [ ] Step 8: Voice tuning (sliders, test scripts)
- [ ] Step 8b: Quran mode test (alag alag surah aur qari, lambi range, Fatiha aur Tawbah ka Bismillah check)
- [ ] Step 9: (Optional) Web deploy

Jo step complete ho, `[ ]` ko `[x]` kar dein. Kal yahin se shuru karein.

## Aaj ka update (app.py)

1. Sidebar mein Mode radio aaya: "News voice-over" aur "Quran tilawat".
2. Quran mode: surah list alquran.cloud se, ayat ki recording everyayah.com se, Arabic text Uthmani script mein RTL display.
3. 8 qari: Alafasy, Abdul Basit, Husary, Minshawi, Sudais, Shuraim, Maher Al-Muaiqly, Hudhaify.
4. Ek bar mein zyada se zyada 50 ayat (`MAX_AYAT`).
5. Bismillah checkbox (Fatiha aur Tawbah ke siwa). Bismillah audio 001001 se aati hai, aur display text se API wali Bismillah hata di jati hai (`strip_bismillah`).
6. Quran ka text aur audio kisi AI model ya TTS se nahi guzarte, taake tajweed aur text mein koi tabdeeli na ho.
7. Surah list, surah text aur ayat audio `st.cache_data` mein cache hote hain (list aur text 24 ghante, audio bhi 24 ghante).
8. Result `session_state` mein save hota hai (`q_audio`, `q_ayat`, `q_title`, `q_reciter`), is liye download dabane par gayab nahi hota.

## Pichla update (news mode)

1. `split_segments()` aur English voice dropdown hata diye. Poora text ek hi voice se ek hi bar mein synthesize hota hai.
2. Groq prompt mein pauses kam kiye: `،` aur `۔` sirf natural jagah par, English lafz ke aas paas extra punctuation nahi.
3. English words Latin letters mein hi rehte hain, sirf Urdu/Roman Urdu Urdu script banti hai.
4. Voice dropdown mein Urdu voices (Asad, Uzma) ke sath Multilingual test voices.

Zaroori: "Groq cleanup" on rakhein, warna Roman Urdu text Urdu script mein convert nahi hoga.

## App run

```
venv\Scripts\activate
streamlit run app.py
```
Update ke baad `app.py` replace karein aur browser refresh karein.

## Step 8: Voice tuning, news mode (news-caster feel)

| Setting | Value | Wajah |
|---|---|---|
| Voice | Asad (ur-PK-AsadNeural) | mature, authoritative |
| Speed | -5% (default), -5% se -10% try karein | steady pace |
| Pitch | -4Hz (default), -3Hz se -6Hz try karein | thodi gehri awaaz |
| Volume | 0% | consistent |
| Groq cleanup | on | Roman to Urdu, numbers words mein, pauses |

Test script:
```
Google ne naya AI feature launch kiya hai jo Machine Learning par chalta hai aur iPhone 15 par bhi kaam karega.
```
Check karein:
- English lafz theek parhe ja rahe hain? (Asad voice mein English ka talaffuz kamzor ho sakta hai)
- Multilingual voices (Andrew, Brian, Ava, Emma) mein Urdu ka talaffuz kaisa hai? Theek na lage to Asad par wapas jayein.
- "Converted text" mein English terms Latin letters mein hain?
- Awaaz mein kahin jhatka ya tor tor to nahi?

## Step 8b: Quran mode test

- Surah 1 (Fatiha): Bismillah checkbox nazar nahi aana chahiye, pehli ayat Bismillah hi hai.
- Surah 9 (Tawbah): Bismillah checkbox nazar nahi aana chahiye.
- Koi aur surah (jaise 112 ya 36): Bismillah on karke ayat 1 se shuru karein, display text mein Bismillah dobara nahi aani chahiye.
- Har qari ek bar try karein, kisi ki recording missing to nahi.
- Range 50 se zyada karein to warning aani chahiye.
- "Ayat tak" chhota karein "Ayat se" se to warning aani chahiye.

## Step 9: (Optional) Web deploy, Streamlit Community Cloud (free)

1. Project GitHub par push karein (`.env` mat dalna)
2. share.streamlit.io par repo connect karein, main file `app.py`
3. App Settings > Secrets mein:
   ```
   GROQ_API_KEY = "gsk_your_key_here"
   ```
4. Deploy

## Limits aur risks

- Groq free tier: rate limits hain. Error aaye to thora ruk kar dobara try karein.
- Groq models badalte rehte hain, is liye app list khud fetch karti hai. Default `openai/gpt-oss-120b`, na mile to sidebar se dusra chunein.
- Edge TTS unofficial hai. Personal aur testing ke liye theek. Client ke paid kaam ke liye Azure Neural TTS (paid) behtar.
- Edge TTS, alquran.cloud aur everyayah.com sab ko internet chahiye.
- Quran mode mein sirf Groq nahi, TTS bhi use nahi hota. Is mode ke liye `GROQ_API_KEY` ki zaroorat nahi.
- everyayah.com aur alquran.cloud third-party free services hain. Down hon to Quran mode kaam nahi karega.
- Client ya public use se pehle everyayah.com ke qari recordings ki licensing/terms check karein.
- Ayat ki MP3 seedhi jodi jati hai (concatenate), is liye ayat ke darmiyan thori khamoshi ya halka jhatka ho sakta hai.

## Troubleshooting

| Masla | Hal |
|---|---|
| `GROQ_API_KEY missing` | `.env` check karein, app restart karein |
| `ModuleNotFoundError` | venv activate hai? `pip install -r requirements.txt` (requests bhi chahiye) |
| Awaaz nahi aa rahi (news mode) | Edge TTS test: `edge-tts --voice ur-PK-AsadNeural --text "ٹیسٹ" --write-media test.mp3`, internet check |
| Model 404 | Sidebar mein "Groq model" dropdown se dusra model chunein |
| Multilingual voice mein Urdu galat | Asad ya Uzma par wapas jayein |
| "Surah list nahi mili" | Internet check karein, alquran.cloud open hota hai? |
| "Recording ya text nahi mila" | Internet check karein ya dusra qari chunein |
| Quran text mein Bismillah do bar | Bismillah checkbox aur `strip_bismillah()` check karein |

## Next ideas (baad mein)

- [ ] Pronunciation dictionary (names ke liye)
- [ ] Lambi script ko chunks mein todna
- [ ] Engine swap: Azure Neural TTS ya ElevenLabs (sirf `synthesize()` badalna hoga)
- [ ] Batch mode: multiple scripts ek sath
- [ ] Quran mode: Urdu tarjuma ya tafseer text option
- [ ] Quran mode: ayat ke darmiyan khamoshi ka control
- [ ] Quran mode: 50 ayat ki limit se zyada ke liye chunks mein download

## Notes / Log

- (yahan apni progress aur errors likhte jayen)
