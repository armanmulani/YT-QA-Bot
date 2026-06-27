# AIScribe QA BOT — Premium Video Intelligence Dashboard 🛡️✨

A production-grade, highly responsive **SaaS Semantic Ingestion Platform** built to analyze, audit, and query **any YouTube video** on **any device** (Mobile, Tablet, Laptop, and Desktop). 

Pasting any public YouTube link parses its structure, crawls its transcript dynamically, indexes it in-memory, and allows users to perform context-audited searches. The system generates source-cited AI reports and provides **clickable timestamp citation cards that redirect users to the exact second of the discussion on YouTube.**

---

## 🚀 Deployed Link & Product Demo


---

## 🎨 Design System: Premium Obsidian & Liquid Gold
This system's visual identity has been completely customized to match the **ELITE QA BOT Golden Shield Logo**:
* **Obsidian Slate Backgrounds:** Matte dark canvas reducing visual strain and presenting a professional corporate software aesthetic.
* **Liquid Gold Accents:** Controls, indicators, and left-borders use a premium metallic gold accent (`#D4AF37`) mapping to our brand identity.
* **Cross-Device Grid:** On desktop screens, the interface renders in a 2-column layout (Left-pane video monitor, Right-pane query monitor). Small screens automatically reflow into a linear vertical scroll with touch-friendly cards.

---

## 🔒 Enterprise-Grade Key Security
Exposing private API keys in client-side code or web interfaces is a major compliance violation. ELITE QA BOT integrates a **Zero-Frontend Credentials Architecture**:
* **Backend Ingestion:** The script securely reads credentials in-memory using **`os.environ.get("GEMINI_API_KEY")`** (perfect for local environment variables) or **`st.secrets["GEMINI_API_KEY"]`** (for Streamlit Cloud or Heroku config variables).
* **Safe Repository:** You can push this entire codebase to a public GitHub repository without the risk of exposing your private Google Gemini keys to crawlers.

---

## 🛠️ First-Principles Architecture (Zero-Framework)

Most beginner developers rely on heavy, opaque wrappers like LangChain or complex, expensive vector databases. ELITE QA BOT is built on a custom, lightweight, **zero-framework approach**:

1. **Regex URL Extraction:** A robust Python regular expression parses desktop, mobile, shorts, or embedded YouTube URLs dynamically to isolate the 11-character `video_id`.
2. **Dynamic Scraper:** Crawls transcripts live from YouTube servers using `youtube_transcript_api`.
3. **Resilient Error Boundaries:** Gracefully traps captions disabled, video private, or cloud rate-limiting exceptions rather than letting the application crash.
4. **Custom Pure-Python TF-IDF Search Engine:** Instead of introducing a database overhead (Chroma, Pinecone), we built a custom **TF-IDF (Term Frequency-Inverse Document Frequency) algorithm in 40 lines of pure Python using the `math` library.** It implements stopwatch-filtering to find semantically relevant segments instantly.
5. **Audited Generation:** Feeds contexts directly into the official **`gemini-1.5-flash`** or **`gemini-1.5-pro`** models, strictly constraining responses to transcript facts and forcing source timestamp citations (e.g., `[At 01:24:12]`).

---

## 📈 ADAPT Framework Implementation (Densight Labs Alignment)

This platform was architected following the **Densight Labs Applied AI Methodology**:

* **A - Assess:** Assessed client requirements—non-technical users need to quickly audit and find specific statements inside hours of video content across multiple device widths.
* **D - Diagnose:** Diagnosed critical production risks—rate-limits on public cloud IPs, disabled subtitles, and LLM hallucinations. Integrated robust try-except error boundaries and built-in stop-word filters.
* **A - Align:** Aligned technology with budget and latency constraints—using Google's official production-grade **Gemini 1.5 models** for high token capacity and Streamlit for instant, responsive browser-level UI deployment.
* **P - Pilot:** Created and launched this lightweight, high-performance prototype within a day to demonstrate instant operational value.
* **T - Track:** Tracked user verification habits by outputting custom, styled timestamp redirect cards. Users can instantly verify the AI's claims with a single click.

---

## ⚙️ Installation & Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/wtf-podcast-qa-bot.git
cd wtf-podcast-qa-bot
```

### 2. Set your Secure API Key
* **Windows (PowerShell):** `$env:GEMINI_API_KEY="your_actual_key"`
* **Windows (Cmd):** `set GEMINI_API_KEY=your_actual_key`
* **Mac/Linux:** `export GEMINI_API_KEY="your_actual_key"`

### 3. Run the application
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 📂 File Structure
* `app.py`: Core dashboard interface, TF-IDF engine, responsive UI, and prompt configurations.
* `logo.png`: Golden shield vector brand identity.
* `README.md`: System documentation and ADAPT framework alignment.
* `requirements.txt`: Project dependencies.
