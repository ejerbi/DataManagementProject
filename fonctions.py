import streamlit as st

def afficher_dataframe(data):
    st.subheader("Aperçu du DataFrame")
    
    # Option pour choisir entre tableau interactif et statique
    
    st.dataframe(data, use_container_width=True)  # Largeur s'adapte à la page
    
    # Nombre de lignes et colonnes
    st.write(f"Le DataFrame contient **{data.shape[0]} lignes** et **{data.shape[1]} colonnes**.")
