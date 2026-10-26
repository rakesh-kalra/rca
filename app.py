import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(page_title="Kalra Coaching Center", layout="centered")

st.title("📝 KALRA COACHING CENTER")
st.subheader("Foundation Learning Assessment")

# -------------------------------------------------------------
# गूगल शीट से कनेक्ट करना (अपनी शीट का लिंक यहाँ डालें)
# -------------------------------------------------------------
sheet_url = "https://docs.google.com/spreadsheets/d/1VfAl2L32tCElvFeJ4E6DbQx9pKJpcHpv6lWuImjuz7c/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# पुरानी रिपोर्ट्स लोड करना
try:
    existing_data = conn.read(spreadsheet=sheet_url, ttl="0d")
except Exception:
    existing_data = pd.DataFrame()

# नेविगेशन मेन्यू (टैब्स)
tab1, tab2 = st.tabs(["🆕 New Assessment Form", "🔍 View & Search Reports"])

# ==========================================
# TAB 1: नया असेसमेंट फॉर्म भरना
# ==========================================
with tab1:
    st.header("Teacher Assessment Sheet")
    
    with st.form("assessment_form", clear_on_submit=True):
        # Student Details
        col1, col2, col3 = st.columns(3)
        with col1:
            student_name = st.text_input("Student Name*")
        with col2:
            student_class = st.text_input("Class")
        with col3:
            age = st.text_input("Age")
            
        col4, col5 = st.columns(2)
        with col4:
            assess_type = st.radio("Assessment Mode", ["Initial", "Progress"], horizontal=True)
        with col5:
            teacher_name = st.text_input("Teacher Name", value="Rakesh Kalra")

        st.markdown("---")
        
        # 1. Basic Observation
        st.subheader("1. Basic Observation")
        attention = st.selectbox("Attention", ["Good", "Moderate", "Easily distracted"])
        instructions = st.selectbox("Understands instructions", ["Easily", "Repetition needed", "Demonstration needed"])
        independent = st.selectbox("Works independently", ["Yes", "Sometimes", "Mostly needs help"])
        difficulty = st.selectbox("Response to difficulty", ["Tries", "Asks help", "Gives up", "Avoids"])
        gen_obs = st.text_area("General observation notes")

        st.markdown("---")

        # 2. English / Reading
        st.subheader("2. English / Reading")
        c1, c2, c3 = st.columns(3)
        rec_letters = c1.number_input("Recognises letters (/10)", 0, 10, 0)
        let_sound = c2.number_input("Connects letter -> sound (/10)", 0, 10, 0)
        read_words = c3.number_input("Reads simple words (/10)", 0, 10, 0)
        
        c4, c5 = st.columns(2)
        read_sent = c4.number_input("Reads simple sentence (/5)", 0, 5, 0)
        understand = c5.number_input("Understands what was read (/5)", 0, 5, 0)
        
        read_style = st.select_slider("Reading style", ["Letter-by-letter", "Skipping", "Guessing", "Slow", "Smooth"])
        read_well = st.text_input("One thing the child reads well")
        main_diff = st.text_input("Main difficulty")

        st.markdown("---")

        # 3. Writing
        st.subheader("3. Writing")
        write_name = st.selectbox("Writes own name", ["Yes", "With help", "No"])
        copy_words = st.selectbox("Copies words", ["Good", "Moderate", "Difficult"])
        write_ind = st.selectbox("Writes independently", ["Good", "Developing", "Difficult"])
        handwriting = st.selectbox("Handwriting", ["Clear", "Uneven", "Very difficult to read"])
        write_obs = st.text_input("Writing observation")

        st.markdown("---")

        # 4. Number & Math Foundation
        st.subheader("4. Number & Math Foundation")
        m1, m2, m3, m4 = st.columns(4)
        counting = m1.text_input("Counting (e.g. 1-50)")
        num_rec = m2.number_input("Number recognition (/10)", 0, 10, 0)
        num_write = m3.number_input("Number writing (/10)", 0, 10, 0)
        num_names = m4.number_input("Number names (/20)", 0, 20, 0)
        
        tables = st.text_input("Tables known")
        
        st.write("**Math Skills Status**")
        ms1, ms2, ms3 = st.columns(3)
        add = ms1.selectbox("Addition", ["Independent", "With Help", "Not Yet"])
        add_carry = ms2.selectbox("Addition with carry", ["Independent", "With Help", "Not Yet"])
        sub = ms3.selectbox("Subtraction", ["Independent", "With Help", "Not Yet"])
        
        ms4, ms5, ms6 = st.columns(3)
        mult = ms4.selectbox("Multiplication", ["Independent", "With Help", "Not Yet"])
        div = ms5.selectbox("Division", ["Independent", "With Help", "Not Yet"])
        word_prob = ms6.selectbox("Simple word problem", ["Independent", "With Help", "Not Yet"])
        
        math_reason = st.selectbox("Mathematical reasoning", ["Tries independently", "Uses a logical method", "Needs hint", "Mostly guesses", "Gives up quickly"])

        # Submit Button
        submit_button = st.form_submit_button(label="💾 Save Assessment Online")
        
        if submit_button:
            if not student_name:
                st.error("Please enter the Student's Name.")
            else:
                # सारा डेटा एक रो (row) में तैयार करना
                new_entry = {
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Student Name": student_name,
                    "Class": student_class,
                    "Age": age,
                    "Type": assess_type,
                    "Teacher": teacher_name,
                    "Attention": attention,
                    "English Score": f"{rec_letters + let_sound + read_words + read_sent + understand}/40",
                    "Math Rec Score": f"{num_rec}/10",
                    "Main Difficulty": main_diff,
                    "General Notes": gen_obs
                }
                
                # डेटा को पुराना डेटा के साथ जोड़कर Google Sheet में भेजना
                new_df = pd.DataFrame([new_entry])
                updated_df = pd.concat([existing_data, new_df], ignore_index=True)
                conn.update(spreadsheet=sheet_url, data=updated_df)
                st.success(f"🎉 Success! {student_name}'s report has been saved to Google Sheets.")
                st.balloons()

# ==========================================
# TAB 2: डेटा खोजना और देखना
# ==========================================
with tab2:
    st.header("Search Student Records")
    if not existing_data.empty:
        search_query = st.text_input("Enter Student Name to Filter:")
        
        if search_query:
            filtered_df = existing_data[existing_data["Student Name"].str.contains(search_query, case=False, na=False)]
            st.dataframe(filtered_df)
        else:
            st.write("Showing all recorded assessments:")
            st.dataframe(existing_data)
    else:
        st.info("No records found yet. Go to the first tab to add one!")
