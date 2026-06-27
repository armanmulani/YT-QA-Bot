import streamlit as st
import google.generativeai as genai
import json
import math
import os
import re
from youtube_transcript_api import YouTubeTranscriptApi

# 1. Page Configuration
st.set_page_config(
    page_title="ScribeAI — Premium YouTube Intelligence",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Modern SaaS Design System (Custom HTML/CSS injection)
st.markdown("""
    <style>
    /* Global Font & Background Alignment */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Remove default Streamlit header bar decoration */
    header {visibility: hidden;}
    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        max-width: 95% !important;
    }

    /* Core SaaS Containers */
    .brand-container {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #E5E7EB;
    }
    .dark .brand-container {
        border-bottom: 1px solid #2D3748;
    }
    
    /* SaaS Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #07070b 0%, #0F172A 100%);
        color: #FFFFFF;
        padding: 2.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        border: 1px solid rgba(212,175,55,0.12);
        box-shadow: 0 6px 30px rgba(11,12,13,0.6);
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.05em;
        line-height: 1.1;
        margin-bottom: 0.5rem;
        background: linear-gradient(to right, #F8F6EB, #D4AF37);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 1rem;
        color: #94A3B8;
        max-width: 650px;
        line-height: 1.5;
    }
    
    /* Premium Bordered Cards */
    .saas-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .dark .saas-card {
        background-color: #0F172A;
        border: 1px solid #1E293B;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .saas-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
        border-color: #CBD5E1;
    }
    .dark .saas-card:hover {
        border-color: #334155;
    }
    
    /* Reference Timestamp Cards (Crimson YouTube Identity) */
    .timestamp-card {
        background-color: #F8F6EB;
        border: 1px solid rgba(212,175,55,0.12);
        border-radius: 8px;
        padding: 14px;
        margin-bottom: 12px;
        border-left: 4px solid #D4AF37; /* Gold left accent */
        transition: all 0.2s ease;
    }
    .dark .timestamp-card {
        background-color: #0F172A;
        border: 1px solid rgba(255,255,255,0.04);
        border-left: 4px solid #D4AF37;
    }
    .timestamp-card:hover {
        transform: scale(1.01);
        border-color: #CBD5E1;
    }
    .dark .timestamp-card:hover {
        border-color: #475569;
    }

    /* Elegant Custom Buttons */
    .jump-btn {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: #B8860B;
        color: #0F0F0F !important;
        padding: 6px 14px;
        border-radius: 6px;
        text-decoration: none;
        font-size: 0.8rem;
        font-weight: 600;
        transition: background-color 0.15s ease;
    }
    .jump-btn:hover {
        background-color: #D4AF37;
    }
    
    /* Indicators / Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
    }
    .badge-success {
        background-color: #FFF6E1;
        color: #B8860B;
        border: 1px solid rgba(184,134,11,0.12);
    }
    .dark .badge-success {
        background-color: #2B1F10;
        color: #FFD37A;
    }
    
    /* Active Stats Board */
    .stats-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin-top: 1rem;
    }
    .stat-item {
        background: #F1F5F9;
        padding: 10px;
        border-radius: 6px;
        text-align: center;
    }
    .dark .stat-item {
        background: #1E293B;
    }
    .stat-val {
        font-size: 1.1rem;
        font-weight: 700;
        color: #0F172A;
    }
    .dark .stat-val {
        color: #F8FAFC;
    }
    .stat-lbl {
        font-size: 0.7rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Configuration Pane
logo_path = os.path.join("assets", "logo.png")
try:
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, width=280)
        st.sidebar.markdown("<div style='text-align:center; font-weight:800; color:#D4AF37; margin-top:8px;'>ELITE QA BOT</div>", unsafe_allow_html=True)
    else:
        raise FileNotFoundError
except Exception:
    st.sidebar.markdown("""
        <div class='brand-container'>
            <span style='font-size: 1.6rem;'>🎬</span>
            <span style='font-size: 1.25rem; font-weight: 800; letter-spacing: -0.05em; color: #0F172A;' class='dark-txt'>ScribeAI Premium</span>
        </div>
    """, unsafe_allow_html=True)

# ============================================================================
# SECURE API KEY CONFIGURATION (ENVIRONMENT ONLY)
# ============================================================================
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.sidebar.warning("GEMINI_API_KEY is not set. Load it from your environment or local .env file.")
else:
    genai.configure(api_key=api_key)

st.sidebar.subheader("⚙️ System Status")
if api_key:
    st.sidebar.markdown("<span class='badge badge-success'>● API Connected</span>", unsafe_allow_html=True)
else:
    st.sidebar.markdown("<span class='badge badge-success'>● API Not Configured</span>", unsafe_allow_html=True)

st.sidebar.subheader("🎯 Search Calibration")
model_choice = st.sidebar.selectbox("Select Core Model Engine", ["gemini-3.5-flash"])
chunk_size = st.sidebar.slider("Semantic Chunk Window (Seconds)", min_value=15, max_value=90, value=40)
top_n = st.sidebar.slider("Reference Citations (K)", min_value=1, max_value=5, value=3)

# 4. Global Hero Header
st.markdown("""
    <div class='hero-banner'>
        <div class='hero-title'>ScribeAI — Premium YouTube Intelligence</div>
        <div class='hero-subtitle'>
            Enterprise-grade semantic ingestion dashboard. Paste any YouTube video URL to fetch transcripts live, index them in-memory, and perform source-audited, clickable timestamp-anchored Q&A.
        </div>
    </div>
""", unsafe_allow_html=True)

# Stop words list to filter out noise in search
STOP_WORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
    'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
    'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
    'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
    'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
    'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
    'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
    'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
    'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should',
    "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",
    'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",
    'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't",
    'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't", 'yeah', 'like', 'know', 'think',
    'just', 'get', 'got', 'right', 'going', 'would', 'actually', 'sort', 'kind', 'well', 'people', 'say'
}

# Helper Functions
def extract_video_id(url):
    pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/|youtube\.com\/shorts\/)([a-zA-Z0-9_-]{11})'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    if len(url.strip()) == 11:
        return url.strip()
    return None

@st.cache_data(show_spinner=False)
def fetch_transcript_live(video_id):
    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)
        formatted_data = []
        for entry in transcript:
            formatted_data.append({
                "start": int(entry.start),
                "text": entry.text
            })
        return formatted_data, None
    except Exception as e:
        error_msg = str(e)
        if "Subtitles are disabled" in error_msg or "NoTranscriptFound" in error_msg:
            return None, "subtitles_disabled"
        elif "Cookies" in error_msg or "IpBlocked" in error_msg:
            return None, "rate_limited"
        return None, "unknown_error"

def chunk_transcript(data, size_in_sec):
    chunks = []
    if not data:
        return chunks
    current_chunk = []
    current_start = data[0]["start"]
    for entry in data:
        current_chunk.append(entry["text"])
        if entry["start"] - current_start >= size_in_sec:
            chunks.append({
                "start": current_start,
                "text": " ".join(current_chunk)
            })
            current_chunk = []
            current_start = entry["start"]
    if current_chunk:
        chunks.append({
            "start": current_start,
            "text": " ".join(current_chunk)
        })
    return chunks

def search_tfidf(query, chunks, top_k=3):
    query_cleaned = [w.strip("?,.:!\"()").lower() for w in query.split()]
    query_words = set([w for w in query_cleaned if w and w not in STOP_WORDS])
    
    if not query_words:
        query_words = set([w for w in query_cleaned if w])
        
    total_docs = len(chunks)
    df = {}
    for word in query_words:
        count = sum(1 for chunk in chunks if word in chunk["text"].lower())
        df[word] = count
        
    scored_chunks = []
    for chunk in chunks:
        score = 0.0
        text_lower = chunk["text"].lower()
        words_in_chunk = text_lower.split()
        doc_len = len(words_in_chunk) if len(words_in_chunk) > 0 else 1
        
        for word in query_words:
            term_frequency = text_lower.count(word)
            if term_frequency > 0 and df.get(word, 0) > 0:
                tf = term_frequency / doc_len
                idf = math.log((total_docs / (df[word] + 1)) + 1)
                score += tf * idf
        scored_chunks.append((score, chunk))
        
    scored_chunks.sort(reverse=True, key=lambda x: x[0])
    return [chunk for score, chunk in scored_chunks[:top_k] if score > 0]

def format_time(seconds):
    mins = seconds // 60
    secs = seconds % 60
    if mins >= 60:
        hrs = mins // 60
        mins = mins % 60
        return f"{hrs:02d}:{mins:02d}:{secs:02d}"
    return f"{mins:02d}:{secs:02d}"

# 5. Dashboard Grid (1/3 Width left pane, 2/3 Width right pane)
col_left, col_right = st.columns([1, 2])

with col_left:
    st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
    st.subheader("📼 Video Ingestion Port")
    video_url = st.text_input("YouTube Link:", value="https://www.youtube.com/watch?v=Rni7Fz7208c", placeholder="Paste desktop, mobile, or shorts URL...")
    st.markdown("</div>", unsafe_allow_html=True)
    
    if video_url:
        video_id = extract_video_id(video_url)
        
        if video_id:
            # Embed Video
            st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
            st.subheader("📺 Video Monitor")
            st.video(f"https://www.youtube.com/watch?v={video_id}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Fetch and process
            transcript, error_type = fetch_transcript_live(video_id)
            
            if transcript:
                # Analytics Board
                total_words = sum(len(entry["text"].split()) for entry in transcript)
                est_duration = transcript[-1]["start"] - transcript[0]["start"]
                read_time = max(1, total_words // 150)
                
                st.markdown(f"""
                    <div class='saas-card'>
                        <h4 style='margin-top:0;'>📊 Semantic Analytics Board</h4>
                        <div class='stats-container'>
                            <div class='stat-item'>
                                <div class='stat-val'>{total_words:,}</div>
                                <div class='stat-lbl'>Words</div>
                            </div>
                            <div class='stat-item'>
                                <div class='stat-val'>{format_time(est_duration)}</div>
                                <div class='stat-lbl'>Duration</div>
                            </div>
                            <div class='stat-item'>
                                <div class='stat-val'>{read_time}m</div>
                                <div class='stat-lbl'>Read Time</div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Slicing
                chunks = chunk_transcript(transcript, chunk_size)
            else:
                if error_type == "subtitles_disabled":
                    st.error("❌ Caption files disabled for this video.")
                elif error_type == "rate_limited":
                    st.error("❌ Cloud rate-limit activated. Open locally to run without sharing IP.")
                else:
                    st.error("❌ API retrieval failed.")
        else:
            st.error("❌ Unrecognized URL structure.")

with col_right:
    if video_url and video_id and 'transcript' in locals() and transcript:
        st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
        st.subheader("🔍 AI Semantic Query Portal")
        
        # Interactive Presets
        st.markdown("<p style='font-size:0.8rem; color:#888; margin-bottom:5px;'>💡 Premium Search Presets (Click to pre-fill):</p>", unsafe_allow_html=True)
        preset_cols = st.columns(3)
        
        # We track selected query in session state
        if 'query_val' not in st.session_state:
            st.session_state.query_val = ""
            
        with preset_cols[0]:
            if st.button("🚀 Summary", key="btn_summary", use_container_width=True):
                st.session_state.query_val = "Provide a high-level concise summary of the main topics discussed."
        with preset_cols[1]:
            if st.button("📈 Main Takeaways", key="btn_takeaways", use_container_width=True):
                st.session_state.query_val = "What are the core technical takeaways and breakthroughs discussed?"
        with preset_cols[2]:
            if st.button("🛠️ Tech Stack", key="btn_tech", use_container_width=True):
                st.session_state.query_val = "Which software, algorithms, or technological tools are mentioned?"
                
        # Query input
        query = st.text_input("Type your question here:", value=st.session_state.query_val, placeholder="e.g. What does Elon think about the future of humanoid robots?")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if query:
            results = search_tfidf(query, chunks, top_k=top_n)
            
            if results:
                # Answer and References Splitting inside saas-card
                st.markdown("<div class='saas-card'>", unsafe_allow_html=True)
                
                col_ans, col_ref = st.columns([1.6, 1])
                
                with col_ans:
                    st.subheader("💡 Verified Answer Matrix")
                    
                    # Formulate system prompt
                    context_blocks = []
                    for i, c in enumerate(results):
                        context_blocks.append(f"--- CONTEXT PIECE {i+1} (Starts at {c['start']} seconds) ---\n{c['text']}\n")
                    context_str = "\n".join(context_blocks)
                    
                    system_prompt = f"""You are a precise, corporate-level AI research director.
                    Answer the user's question using ONLY the provided YouTube transcript context segments.
                    
                    RULES:
                    1. If the answer cannot be found in the provided context, state "Answer not present in this segment."
                    2. Maintain a highly professional, objective tone.
                    3. Cite precise timestamps (e.g., "[At 01:24:12]") corresponding to the sources. Convert the seconds to standard clock format.
                    
                    CONTEXT:
                    {context_str}
                    
                    USER QUESTION:
                    {query}
                    """
                    
                    with st.spinner("Processing deep semantic answers..."):
                        try:
                            model = genai.GenerativeModel(model_choice)
                            response = model.generate_content(system_prompt)
                            st.write(response.text)
                            
                            # Add direct text download button
                            st.download_button(
                                label="📥 Export Report as Text",
                                data=response.text,
                                file_name="scribe_ai_report.txt",
                                mime="text/plain"
                            )
                        except Exception as e:
                            st.error(f"API Error: {e}")
                        
                with col_ref:
                    st.subheader("🎯 Context Reference Cards")
                    st.markdown("Click to review the raw video segment at that exact second:")
                    
                    for i, chunk in enumerate(results):
                        start_sec = chunk["start"]
                        time_str = format_time(start_sec)
                        yt_link = f"https://www.youtube.com/watch?v={video_id}&t={start_sec}s"
                        
                        st.markdown(f"""
                            <div class="timestamp-card">
                                <span style="font-weight: 700; font-size:0.9rem; color: #EF4444;">SOURCE CONTEXT #{i+1} ({time_str})</span>
                                <p style="font-size: 0.8rem; line-height: 1.4; margin-top: 5px; margin-bottom: 8px; color:#555;" class='dark-txt'>
                                    "{chunk['text'][:110]}..."
                                </p>
                                <a href="{yt_link}" target="_blank" class="jump-btn">▶️ Verify Segment ({time_str})</a>
                            </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("🔍 No relevant audio context matches found. Adjust parameters in the sidebar.")
    else:
        st.info("💡 Paste a valid YouTube link to activate the Q&A matrix.")
