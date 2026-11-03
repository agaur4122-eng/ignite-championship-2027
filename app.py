import streamlit as st
import streamlit.components.v1 as components

# Configure Streamlit page settings
st.set_page_config(
    page_title="AstraScribe Championship", page_icon="🚀", layout="wide"
)

# Load and render the HTML file
try:
  with open(
      "astrascribe_writing_championship.html", "r", encoding="utf-8"
  ) as f:
    html_content = f.read()
  components.html(html_content, height=1250, scrolling=True)
except FileNotFoundError:
  st.error(
      "Error: 'astrascribe_writing_championship.html' was not found in the"
      " folder. Please make sure both files are saved in the same directory."
  )