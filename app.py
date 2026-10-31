import streamlit as st
import os
from datetime import datetime

# 1. Page Configuration & Professional Styling
st.set_page_config(
    page_title="Ignite Youth Talent Championship 2027",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom Styling that automatically adapts to Light and Dark modes
st.markdown("""
    <style>
    .main-title { font-size: 42px; font-weight: 700; text-align: center; margin-bottom: 10px; }
    .subtitle { font-size: 18px; opacity: 0.8; text-align: center; margin-bottom: 30px; }
    .section-box { padding: 20px; border-radius: 10px; background-color: rgba(255, 75, 75, 0.1); border-left: 5px solid #FF4B4B; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)


# 2. Header Section
st.markdown("<div class='main-title'>Ignite National Talent Championship 2027</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>India's Premier Digital Stage for Writers, Creators, and Innovators</div>", unsafe_allow_html=True)

# 3. Informational Banner
st.markdown("""
<div class='section-box'>
    <h4>🚀 Phase 1: Launch Details</h4>
    <p><b>Eligibility:</b> Students from Classes 9 to 12 across India.<br>
    <b>Registration Fee:</b> ₹0 (Completely Free)<br>
    <b>Rewards:</b> National Publication, Performance Mentorships & Certificates of Excellence.</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# 4. Interactive Registration & Submission Form
st.header("📝 Registration & Submission Portal")

with st.form("submission_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        full_name = st.text_input("Full Name*", placeholder="Enter your full name")
        email = st.text_input("Email Address*", placeholder="name@example.com")
        city = st.text_input("City/Town*", placeholder="e.g., Delhi, Mumbai")
    with col2:
        phone = st.text_input("Phone Number (WhatsApp)*", placeholder="10-digit mobile number")
        school_name = st.text_input("School Name*", placeholder="Enter your school name")
        grade = st.selectbox("Current Class/Grade*", ["Class 9", "Class 10", "Class 11", "Class 12"])
    
    st.write("")
    category = st.selectbox(
        "Choose Your Competition Track*", 
        ["Creative & Sci-Fi Writing", "Performing Arts (Music/Acting/Dance)", "Athletic Skills (Gymnastics/Calisthenics)"]
    )
    
    project_title = st.text_input("Project / Entry Title*", placeholder="Give your submission a catchy title")
    description = st.text_area("Brief Abstract/Description", placeholder="Tell us the core idea behind your submission (Max 150 words)")
    
    # Dynamic Submission File Handling
    st.write("")
    st.subheader("📤 Upload Your Work")
    
    uploaded_pdf = None
    uploaded_video = None
    
    if category == "Creative & Sci-Fi Writing":
        uploaded_pdf = st.file_uploader("Upload your manuscript / essay (PDF format, Max 10MB)*", type=["pdf"])
    else:
        uploaded_video = st.file_uploader("Upload your performance showcase video (MP4/MOV format, Max 90 seconds, Max 50MB)*", type=["mp4", "mov"])
        
    st.write("")
    terms = st.checkbox("I confirm that this is my original work and all details provided are accurate.*")
    
    submit_button = st.form_submit_button("Submit Entry To National Panel")

# 5. Form Processing Architecture
if submit_button:
    if not (full_name and email and city and phone and school_name and project_title and terms):
        st.error("❌ Please fill out all required fields (*) and accept the terms.")
    elif category == "Creative & Sci-Fi Writing" and not uploaded_pdf:
        st.error("❌ Please upload your writing manuscript PDF to complete submission.")
    elif category != "Creative & Sci-Fi Writing" and not uploaded_video:
        st.error("❌ Please upload your 90-second performance video to complete submission.")
    else:
        # Create a secure local directory to store entries dynamically
        data_dir = "national_submissions"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_name = "".join(x for x in full_name if x.isalnum())
        folder_path = os.path.join(data_dir, f"{sanitized_name}_{timestamp}")
        os.makedirs(folder_path)
        
        # Save Metadata Summary Document
        with open(os.path.join(folder_path, "metadata.txt"), "w", encoding="utf-8") as f:
            f.write(f"Name: {full_name}\nEmail: {email}\nPhone: {phone}\nCity: {city}\nSchool: {school_name}\nGrade: {grade}\nCategory: {category}\nTitle: {project_title}\nDescription: {description}\n")
            
        # Save Uploaded Files safely
        if uploaded_pdf:
            with open(os.path.join(folder_path, "manuscript.pdf"), "wb") as f:
                f.write(uploaded_pdf.getbuffer())
        if uploaded_video:
            file_extension = "mp4" if uploaded_video.name.endswith("mp4") else "mov"
            with open(os.path.join(folder_path, f"performance.{file_extension}"), "wb") as f:
                f.write(uploaded_video.getbuffer())
                
        st.success(f"🎉 Success! Thank you {full_name}. Your entry for '{project_title}' has been securely logged on the national panel database.")
        st.balloons()
