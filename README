# WTF Ep.16 — Elon Musk × Nikhil Kamath Podcast Q&A Bot 🎙️

A production-ready, ultra-fast Applied AI Q&A bot built for **WTF Podcast Ep. 16**. It lets users search the 2-hour discussion and instantly jump to the exact clickable timestamp on YouTube to verify the answers.

Built with a **zero-framework, first-principles** architecture using **Streamlit**, raw **Python**, and the **Google Gemini API**.

---

## 🚀 Deployed Link
👉 **Live Prototype:** [Streamlit Cloud Deployment Link (Insert Your Streamlit URL Here)]  
👉 **Video Walkthrough:** [Loom Video Link (Insert Your Loom URL Here)]

---

## 🛠️ The Architecture (Zero-Framework Applied AI)

Most junior developers copy-paste LangChain code without understanding what is happening under the hood. For this enterprise proof-of-concept, I chose a **first-principles architecture**:

1. **Local Transcript Cache:** The transcript is stored locally in `transcript.json`. This completely bypasses YouTube's scraper blocks at runtime, saving network roundtrips and ensuring 100% uptime in production.
2. **Deterministic Chunking:** The 2-hour video is chunked into logical topics of fixed-duration time frames (default: 45 seconds).
3. **Custom Pure-Python TF-IDF Engine:** Instead of pulling in massive vector database infrastructure (Chroma, Pinecone, or pgvector) for a single document, I implemented a custom **TF-IDF (Term Frequency-Inverse Document Frequency)** ranking algorithm in pure Python using just the `math` library.
4. **Constrained Generation (Guardrails):** The top 3 most relevant context chunks are fed into **Gemini-1.5-Flash** inside a strict prompt structure. The system prompt commands Gemini to answer ONLY using the provided text blocks and cite precise source timestamps (e.g., `[At 1403s]`).

---

## 📈 ADAPT Framework Implementation (Densight Labs Alignment)

This project was engineered following the **Densight Labs ADAPT Framework**:

* **A - Assess:** Assessed the business requirement—clients need to quickly audit or find moments in long-form media. Traditional keyword search fails to answer complex questions, while standard RAG frameworks introduce unnecessary database costs and YouTube scraper latency.
* **D - Diagnose:** Diagnosed the high failure rate of AI scrapers on cloud servers (IP bans) and the business risk of LLM hallucinations on corporate documents.
* **A - Align:** Aligned the technical solution with client constraints—using Google Gemini 1.5-Flash for fast, cost-efficient, high-context-window generation, and a local pre-cached `transcript.json` to guarantee 100% reliability.
* **P - Pilot:** Built and deployed this lightweight Streamlit prototype within a day to demonstrate the speed-to-value of semantic discussion auditing.
* **T - Track:** Designed the UI to track verification by outputting **clickable YouTube timestamp links** (e.g., adding `&t=1403s` to the URL). If the AI makes a claim, the user can verify it in one click.

---

## ⚙️ Installation & Local Setup

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git
cd YOUR_REPOSITORY_NAME
```

### 2. Install dependencies
```bash
pip install streamlit google-generativeai pypdf
```

### 3. Run the application
```bash
streamlit run app.py
```

---

## 📂 File Structure
* `app.py`: The core Streamlit application containing the UI, TF-IDF search engine, and prompt engineering.
* `transcript.json`: Pre-fetched transcript snippets with precise start times in seconds.
* `README.md`: System documentation and ADAPT framework alignment.
* `requirements.txt`: List of dependencies for Streamlit Cloud deployment.
