import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
from fonctions import afficher_dataframe
def analysis(data):
    
    data['date_du_releve'] = pd.to_datetime(data['date_du_releve'])
    
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown("""
                    
    ### Defintion des colonnes de la base de donnée
                    
                    1 nouvel_identifiant        : Identifiant de la pénalisation

            2 regime_prioritaire        : le type d'infraction en regime prioritaire

            3 regime_particulier        : le type d'infraction en regime particulier

            4 type_de_voie              : le type la voie sur laquelle l'infraction est commise

            5 signalisation_horizontale : type de l'infraction en horizontal

            6 signalisation_verticale   : type de l'infraction en vertical

            7 date_du_releve            : la date d'infraction

            8 geo_point_2d              : contient la latitude et la longitude de l'infraction

            9 arrondissement            : le numero de l'arrondissement

            10 tarrification            : tarification de la l'interdiction""")
    
    with c2:
        buffer = io.StringIO()
        data.info(buf=buffer)
        info_string = buffer.getvalue()
        markdown_output = f"```plaintext\n{info_string}\n```"
        st.markdown(markdown_output)
            
    afficher_dataframe(data)

    st.subheader("Statistiques Descriptives")
    
    annee = sorted(data['annee'].unique())
    default_year = 2022 if 2022 in annee else annee[0]

    selected_year = st.selectbox("Sélectionnez une année", annee, index=annee.index(default_year))

    p1, p2 = st.columns([1, 1])

    with p1:
        filtered_data = data[data['annee'] == selected_year]

        grouped = filtered_data.groupby(["arrondissement"])["nouvel_identifiant"]
        stats_df = grouped.agg(
            Nombre_moyen_infraction="mean",
            Médiane_infraction="median",
            Écart_type_infraction="std"
        ).reset_index()
        st.dataframe(stats_df)
        
        st.subheader("Corrélation des variables sélectionnées")
        data["tarification"] = pd.to_numeric(data["tarification"], errors="coerce").astype("Int64")
        data_corr = data[["nouvel_identifiant","arrondissement","tarification","annee"]].corr()
        fig, ax = plt.subplots(figsize=(20, 6))
        sns.heatmap(data_corr, annot=True, cmap="coolwarm", fmt="0.2f", ax=ax)
        st.pyplot(fig)

    with p2:
        
        st.subheader(f"Répartition des infractions par vacance en {selected_year}")

        filtered_data = data[data["annee"] == selected_year]

        plt.figure(figsize=(6, 6))
        vacance_counts = filtered_data["vacances"].value_counts(normalize=True)
        labels = ["En vacances" if val == 1 else "Hors vacances" for val in vacance_counts.index]
        values = vacance_counts.values
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=["#ff9999", "#66b3ff"])
        plt.title(f"Répartition des infractions par période de vacances ({selected_year})")

        st.pyplot(plt.gcf())

    nombre_dinfraction_par_arrondissement= data.groupby("arrondissement")["nouvel_identifiant"].count()
    nombre_dinfraction_par_arrondissement

    nombre_dinfraction_par_arrondissement.plot(kind='bar', figsize=(10, 6))

    plt.title("Nombre d'infraction de stationnement par arrondissement à Paris")
    plt.xlabel("arrondissement")
    plt.ylabel("nombre_dinfraction_par_arrondissement")
    plt.show()
    plt.figure(figsize=(10,4),dpi=200)
    sns.countplot(x="conformite_signalisation",data=data)