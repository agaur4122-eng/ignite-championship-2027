import streamlit as st
import os
import shutil
from datetime import datetime
import pandas as pd

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
data_dir = "national_submissions"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

if submit_button:
    if not (full_name and email and city and phone and school_name and project_title and terms):
        st.error("❌ Please fill out all required fields (*) and accept the terms.")
    elif category == "Creative & Sci-Fi Writing" and not uploaded_pdf:
        st.error("❌ Please upload your writing manuscript PDF to complete submission.")
    elif category != "Creative & Sci-Fi Writing" and not uploaded_video:
        st.error("❌ Please upload your 90-second performance video to complete submission.")
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_name = "".join(x for x in full_name if x.isalnum())
        folder_name = f"{sanitized_name}_{timestamp}"
        folder_path = os.path.join(data_dir, folder_name)
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
                
        st.success(f"🎉 Success! Thank you {full_name}. Your entry has been logged.")
        st.balloons()

# ====================================================================
# 6. SECRET ADMIN OVERLAY (Only visible when checked)
# ====================================================================
st.write("")
st.write("")
st.divider()
show_admin = st.checkbox("🛠️ Open Organizer Control Panel")

if show_admin:
    st.header("🔒 Central Submissions Database")
    
    # Read all metadata.txt files to show a live table
    sub_folders = os.listdir(data_dir) if os.path.exists(data_dir) else []
    
    if len(sub_folders) == 0:
        st.info("No entries recorded in the cloud data bank yet.")
    else:
        records = []
        for folder in sub_folders:
            meta_path = os.path.join(data_dir, folder, "metadata.txt")
            if os.path.exists(meta_path):
                with open(meta_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    data_dict = {}
                    for line in lines:
                        if ":" in line:
                            k, v = line.split(":", 1)
                            data_dict[k.strip()] = v.strip()
                    records.append(data_dict)
        
        if records:
            df = pd.DataFrame(records)
            st.dataframe(df, use_container_width=True)
            
            # Zip all submissions for easy local extraction
            zip_name = "all_national_entries"
            shutil.make_archive(zip_name, 'zip', data_dir)
            
            with open(f"{zip_name}.zip", "rb") as f:
                st.download_button(
                    label="📥 Download All Submissions & Media Files (.ZIP)",
                    data=f,
                    file_name=f"ignite_submissions_{datetime.now().strftime('%Y%m%d')}.zip",
                    mime="application/zip",
                    use_container_width=True
                )
