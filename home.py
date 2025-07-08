# my_website/home.py# This file is part of my-website.
import streamlit as st
import base64

def home():
    st.set_page_config(
        page_title="Bio-Grad: Data-Based Strategy for Cell-Derived Products",
        page_icon=":house:",
        layout="wide",
    )
    # CSS styles
    with open("styles/main.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
    # Home Page Icon
    with open("assets/logo.png", "rb") as icon_file:
        icon = base64.b64encode(icon_file.read()).decode()
        st.markdown(f'<img src="data:image/png;base64,{icon}" class="logo">', unsafe_allow_html=True)
    
    # CV Download Link
    with open("assets/CV_Rodrigo_Grandy_Principal_Scientist_Group_Leader_June_2025.pdf", "rb") as pdf_file:
        pdf_bytes = pdf_file.read()
    st.download_button(
        label="Download CV",
        data=pdf_bytes,
        file_name="CV_Rodrigo_Grandy_Principal_Scientist_Group_Leader_June_2025.pdf",
        mime="application/pdf"
    )

    # Home Page Title
    st.markdown("""
    <h1 class="title"> About Me</h1>
   
    """, unsafe_allow_html=True)
    # Home Page Content
    st.markdown("""
    <div class="content">
        <p>Innovative  scientific  leader  with  over  19  years  of  combined  experience  in  academia  and  biotech.  Skilled  in establishing  and  managing  R&D  projects,  driving  innovation,  and  fostering  collaboration.  Experienced  in supporting  process  development  and  manufacturing  efforts  to  facilitate  seamless  translation  of  scientific ideas  into  healthcare  solutions.  Passionate  about  leading  teams  and  transforming  scientific  research  into impactful healthcare advancements.</p>
        <p>Explore our resources, tools, and community to stay updated with the latest advancements in cell-derived product development.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    home()

