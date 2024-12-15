import streamlit as st
import pandas as pd
def data_man():

    
    st.markdown(
        """
        <style>
        .title {
            font-size: 75px;
            margin-top: 10px
            margin: 15px;
            font-weight: bold;
        }
        .full-width {
            width: 150%; /* Largeur maximale */
            padding: 20px 20px;
            background-color: #000000;
            border-radius: 8px;
            margin-left: -230px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Titre principal
    st.markdown('<div class="title">SDA_2024</div>', unsafe_allow_html=True)

    st.markdown("# Data Management_")

    st.text("Voici le Jupyter Notebook de la partie Data Management")

    notebook_path = 'final.md'
    with open(notebook_path, "r", encoding="utf-8") as f:
        markdown_text = f.read()

    st.markdown(markdown_text)