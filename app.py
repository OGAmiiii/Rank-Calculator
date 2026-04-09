import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF
import datetime
import tempfile

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="SSC Pro Analyzer", page_icon="🏆", layout="centered")

# --- PREMIUM CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
    html, body, [class*="css"] {font-family: 'Poppins', sans-serif;}
    .main-title { font-size: 32px; font-weight: 800; color: #1E3A8A; text-align: center; text-transform: uppercase; letter-spacing: 1px;}
    .sub-title { text-align: center; color: #6B7280; margin-bottom: 20px; font-size: 14px;}
    .score-card { background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); padding: 20px; border-radius: 15px; text-align: center; color: white; box-shadow: 0 4px 15px rgba(0,0,0,0.2);}
    .score-text { font-size: 45px; font-weight: 900; margin: 0; line-height: 1.2; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);}
    .highlight-box { background-color: #F3F4F6; padding: 15px; border-radius: 10px; border-left: 5px solid #3B82F6; margin-top: 15px;}
    </style>
""", unsafe_allow_html=True)

# --- PDF GENERATOR (Advanced) ---
def create_pdf(name, exam_name, score, c, w, b, q_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 22)
    pdf.set_text_color(30, 58, 138)
    pdf.cell(200, 15, txt="SSC PRO ANALYZER SCORECARD", ln=True, align='C')
    
    pdf.set_font("Arial", '', 12)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(200, 10, txt=f"Date Generated: {datetime.date.today()} | Verified Result", ln=True, align='C')
    pdf.line(10, 35, 200, 35)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(100, 10, txt=f"Candidate Name: {name.upper()}", ln=True)
    pdf.cell(100, 10, txt=f"Exam: {exam_name}", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(0, 128, 0)
    pdf.cell(200, 15, txt=f"FINAL SCORE: {score} Marks", ln=True, align='C')
    
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(100, 10, txt=f"✅ Correct: {c}", ln=True)
    pdf.cell(100, 10, txt=f"❌ Wrong: {w}", ln=True)
    pdf.cell(100, 10, txt=f"⚠️ Unattempted: {b}", ln=True)
    
    pdf.line(10, 120, 200, 120)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(200, 10, txt="Tool by: [Your Website/Telegram Name]", ln=True, align='C')
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

# --- SSC SCRAPING & SECTIONAL LOGIC ---
def calculate_ssc_marks(url, pos_mark, neg_mark):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        blocks = soup.find_all('div', class_='question-pnl')
        if not blocks:
            blocks = soup.find_all('table', class_='menu-tbl')
            
        if not blocks:
            return None, "Error: HTML format changed or URL invalid."

        question_data = [] # For Sectional Analysis
        correct, wrong, blank = 0, 0, 0
        
        for block in blocks:
            right_ans_elem = block.find('td', class_='rightAns')
            if not right_ans_elem: continue
            right_ans = right_ans_elem.text.strip()[0]
            
            chosen_ans = "--"
            tds = block.find_all('td')
            for i, td in enumerate(tds):
                if "Chosen Option" in td.text:
                    if i + 1 < len(tds):
                        chosen_ans = tds[i+1].text.strip()
                    break
            
            if chosen_ans in ["--", ""]:
                blank += 1
                question_data.append("Blank")
            elif chosen_ans == right_ans:
                correct += 1
                question_data.append("Correct")
            else:
                wrong += 1
                question_data.append("Wrong")
                
        score = (correct * pos_mark) - (wrong * neg_mark)
        return (correct, wrong, blank, round(score, 2), question_data), "Success"
        
    except Exception as e:
        return None, str(e)


# --- UI START ---
st.markdown('<p class="main-title">🏆 SSC Pro Analyzer</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Advanced Sectional & Accuracy Analysis</p>', unsafe_allow_html=True)

url = st.text_input("🔗 Paste Answer Key URL Here:")
col1, col2 = st.columns(2)
name = col1.text_input("👤 Your Name:")
exam_mapping = {"SSC Pre (100 Qs)": (2.0, 0.5), "SSC Mains": (3.0, 1.0), "SSC GD": (1.0, 0.25)}
exam_type = col2.selectbox("🎯 Exam Type:", list(exam_mapping.keys()))

if st.button("Generate Super Analytics", use_container_width=True):
    if url and name:
        with st.spinner("Hacking into SSC Matrix... 🕵️‍♂️"):
            pos_m, neg_m = exam_mapping[exam_type]
            result, msg = calculate_ssc_marks(url, pos_m, neg_m)
            
            if result:
                c, w, b, total_score, q_data = result
                
                # --- 1. HERO SCORECARD ---
                st.markdown(f"""
                <div class="score-card">
                    <p style="margin:0; font-size:16px; font-weight:600; opacity:0.9;">{name.upper()}'S FINAL SCORE</p>
                    <p class="score-text">{total_score}</p>
                    <p style="margin:0; font-size:12px; margin-top:5px;">Marks calculated out of {len(q_data)*pos_m}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("")
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("✅ Correct", c, f"+{c*pos_m} Marks")
                col_b.metric("❌ Wrong", w, f"-{w*neg_m} Marks", delta_color="inverse")
                col_c.metric("⚠️ Blank", b)

                # --- 2. UNIQUE: SECTIONAL ANALYSIS (Only if 100 Qs) ---
                if len(q_data) == 100 and exam_type == "SSC Pre (100 Qs)":
                    st.markdown("### 📚 Subject-wise Breakdown")
                    sections = {
                        "🧠 Reasoning": q_data[0:25],
                        "🌍 General Awareness": q_data[25:50],
                        "📐 Maths (Quants)": q_data[50:75],
                        "🔤 English": q_data[75:100]
                    }
                    
                    sec_cols = st.columns(4)
                    for i, (sec_name, sec_data) in enumerate(sections.items()):
                        sec_c = sec_data.count("Correct")
                        sec_w = sec_data.count("Wrong")
                        sec_score = (sec_c * pos_m) - (sec_w * neg_m)
                        with sec_cols[i]:
                            st.markdown(f"<div style='text-align:center; background:#F9FAFB; padding:10px; border-radius:8px; border:1px solid #E5E7EB;'><p style='font-size:12px; margin:0;'>{sec_name}</p><p style='font-weight:bold; font-size:18px; color:#1E3A8A; margin:0;'>{sec_score}</p></div>", unsafe_allow_html=True)

                st.write("---")

                # --- 3. UNIQUE: NEGATIVE MARKING DAMAGE METER ---
                st.markdown("### 💥 Negative Marking Impact")
                damage = w * neg_m
                max_possible_damage = len(q_data) * neg_m
                
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = damage,
                    title = {'text': "Marks Lost in Negative"},
                    gauge = {
                        'axis': {'range': [0, 20]}, # Max 20 marks damage scaling
                        'bar': {'color': "red"},
                        'steps': [
                            {'range': [0, 5], 'color': "lightgreen"},
                            {'range': [5, 10], 'color': "yellow"},
                            {'range': [10, 20], 'color': "salmon"}],
                    }))
                fig_gauge.update_layout(height=250, margin=dict(t=30, b=10, l=10, r=10))
                st.plotly_chart(fig_gauge, use_container_width=True)

                # --- 4. VIRAL FEATURE: TELEGRAM FLEX GENERATOR ---
                st.markdown("### 📲 Share Your Result (Flex Mode)")
                flex_text = f"""🔥 *My SSC Exam Result* 🔥
👤 Name: {name}
🎯 Total Score: *{total_score} Marks*

✅ Correct: {c}
❌ Wrong: {w}
📊 Accuracy: {round((c/(c+w))*100, 1) if (c+w)>0 else 0}%

Check yours here: [Your Website Link]
"""
                st.code(flex_text, language="markdown")
                st.caption("👆 Copy this text and paste it in Telegram/WhatsApp groups!")

                # --- 5. PDF DOWNLOAD ---
                st.write("---")
                pdf_path = create_pdf(name, exam_type, total_score, c, w, b, q_data)
                with open(pdf_path, "rb") as file:
                    st.download_button(
                        label="📥 Download Pro Marksheet (PDF)",
                        data=file,
                        file_name=f"{name}_SSC_Analyzer.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
            else:
                st.error(f"Failed! Reason: {msg}")
    else:
        st.warning("Please enter both URL and Name!")
