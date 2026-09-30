# Urdu Voice Agent: PROGRESS.md

Goal: Urdu news-caster style voice-over. Input Roman Urdu ya Urdu script, output MP3.
English terms (AI, Google, iPhone, etc.) Latin letters mein rehte hain aur poora text ek hi flow mein parha jata hai.
Stack: OpenAI SDK (Groq base_url) + Edge TTS (Urdu voice ya Multilingual voice) + Streamlit.
Cost: free (Groq free tier, Edge TTS, Streamlit local).

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
- [x] Feature: English terms English voice mein (Urdu aur English hisse alag alag synthesize hote hain)
- [x] Fix 3: Awaaz tor tor ke aa rahi thi. Ab split band hai, poora text ek hi voice se ek hi bar mein synthesize hota hai
- [x] Feature: Multilingual voices (Andrew, Brian, Ava, Emma) test ke liye add
- [ ] Step 8: Voice tuning (sliders, test scripts)
- [ ] Step 9: (Optional) Web deploy

Jo step complete ho, `[ ]` ko `[x]` kar dein. Kal yahin se shuru karein.

## Aaj ka update (app.py)

1. `split_segments()` aur English voice dropdown hata diye. Ab poora text ek hi bar mein ek hi voice se synthesize hota hai (tor tor ka masla khatam).
2. Groq prompt mein pauses kam kar diye: `،` aur `۔` sirf natural jagah par, English lafz ke aas paas extra punctuation nahi.
3. Voice dropdown mein Urdu voices (Asad, Uzma) ke sath Multilingual test voices. Urdu ka talaffuz sun kar decide karein.

## Purana update (ab hata diya gaya)

1. Groq prompt: English words Latin letters mein hi rehte hain, sirf Urdu/Roman Urdu Urdu script banti hai.
2. `split_segments()`: text ko Urdu aur English hisson mein todta hai (iPhone 15, GPT-4, Machine Learning ek English hissa).
3. Har hissa apni voice se synthesize hota hai, phir audio jod di jati hai.
4. Sidebar: "English terms English voice mein parho" checkbox aur English voice dropdown (Guy, Ryan, Christopher, Aria, Sonia).

Zaroori: English split tab hi sahi chalta hai jab "Groq cleanup" on ho, warna Roman Urdu bhi English samjha jayega.

## App run

```
venv\Scripts\activate
streamlit run app.py
```
Update ke baad `app.py` replace karein aur browser refresh karein.

## Step 8: Voice tuning (news-caster feel)

| Setting | Value | Wajah |
|---|---|---|
| Urdu voice | Asad | mature, authoritative |
| English voice | Guy ya Ryan | Asad ke sath mel khata hai |
| Speed | -5% se -10% | steady pace |
| Pitch | -3Hz se -6Hz | thodi gehri awaaz |
| Volume | 0% | consistent |

Test script:
```
Google ne naya AI feature launch kiya hai jo Machine Learning par chalta hai aur iPhone 15 par bhi kaam karega.
```
Check karein:
- English lafz English accent mein aa rahe hain?
- Urdu aur English ke darmiyan awaaz ka farq zyada to nahi? Pitch/speed adjust karein ya English voice badlein.
- "Converted text" mein English terms Latin letters mein hain?
- Awaaz jorne par kahin click ya jhatka to nahi?

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
- Edge TTS ko internet chahiye.
- Urdu aur English awaaz alag voices hain, is liye tone thora farq ho sakta hai.

## Troubleshooting

| Masla | Hal |
|---|---|
| `GROQ_API_KEY missing` | `.env` check karein, app restart karein |
| `ModuleNotFoundError` | venv activate hai? `pip install -r requirements.txt` |
| Awaaz nahi aa rahi | Edge TTS test (`edge-tts --voice ur-PK-AsadNeural --text "ٹیسٹ" --write-media test.mp3`), internet check |
| Model 404 | Sidebar mein "Groq model" dropdown se dusra model chunein |
| English lafz Urdu accent mein | "English terms English voice mein parho" on hai? Groq cleanup on hai? |
| Awaaz jorne par jhatka | Speed/pitch same rakhein, English voice badal kar dekhein |

## Next ideas (baad mein)

- [ ] Pronunciation dictionary (names ke liye)
- [ ] Lambi script ko chunks mein todna
- [ ] Engine swap: Azure Neural TTS ya ElevenLabs (sirf `synthesize()` badalna hoga)
- [ ] Batch mode: multiple scripts ek sath

## Notes / Log

- (yahan apni progress aur errors likhte jayen)