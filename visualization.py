import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import numpy as np
from streamlit_folium import st_folium
from folium.plugins import HeatMap
from wordcloud import WordCloud
from PIL import Image


def visualization(data):

    data['date_du_releve'] = pd.to_datetime(data['date_du_releve'])
    # Creation de nouvelles colonnes
    data["annee"] = data["date_du_releve"].dt.year

    data["saison"] = data["date_du_releve"].apply(
        lambda x: (
            "été" if x.month in [6, 7, 8] else
            "automne" if x.month in [9, 10, 11] else
            "hiver" if x.month in [12, 1, 2] else
            "printemps"
        )
        if pd.notnull(x) else None
    )
    data['vacances'] = data['date_du_releve'].apply(lambda x: 1 if x.month in [7, 8, 12] else 0)

    # Charger les données
    filtered_data = data

    st.title("Analyse des Infractions de Stationnement à Paris")



    st.subheader("Visualisation Géographique")

    coords = data['geo_point_2d'].dropna().str.split(',', expand=True).astype(float)
    data['latitude'] = coords[0]
    data['longitude'] = coords[1]

    # --- Filtres ---
    st.subheader("Filtres")
    col1, col2 = st.columns([1, 1])

    with col1:
        annee = sorted(data['annee'].unique())
        default_year = 2022 if 2022 in annee else annee[0]
        selected_year = st.selectbox("Sélectionnez une année", annee, index=annee.index(default_year))

    with col2:
        selected_season = st.selectbox("Sélectionnez une saison", sorted(data['saison'].unique()))

   

    # Application de flitres
    filtered_data = data[data['annee'] == selected_year]
    filtered_data = filtered_data[filtered_data['saison'] == selected_season]

    # --- MAPS ---
    st.subheader("Cartes des infractions")
    col_points, col_heatmap = st.columns([1, 1])

    # Points Map
    with col_points:
        st.subheader(f"Carte des infractions (Points) pour l'année: {selected_year} en {selected_season} ")
        if not filtered_data.empty:
            st.map(filtered_data[['latitude', 'longitude']], zoom=9)
        else:
            st.warning("Aucune donnée disponible pour cette sélection.")

    # Heatmap
    with col_heatmap:
        st.subheader(f"Carte des infractions (Chaleur) pour l'année {selected_year} en {selected_season}")
        m = folium.Map(location=[48.8566, 2.3522], zoom_start=9)  # Center on Paris

        # Add data to heatmap
        heat_data = filtered_data[['latitude', 'longitude']].dropna().values.tolist()
        if heat_data:  
            HeatMap(heat_data, radius=15).add_to(m)
            st_folium(m, width=900, height=500)  # Adjust size as needed
        else:
            st.warning("Aucune donnée disponible pour générer la carte de chaleur.")
        

    st.subheader("Visualisations Statistiques")

    c1, c2 = st.columns([1, 1])
    with c1:
        st.subheader(f"Distribution des infractions par arrondissement pour l'année {selected_year}")
        fig, ax = plt.subplots(figsize=(10, 10))
        filtered_data['arrondissement'].value_counts().plot(kind='bar', color='skyblue', ax=ax)
        ax.set_xlabel("Arrondissement")
        ax.set_ylabel("Nombre d'infractions")
        st.pyplot(fig)
        st.markdown("""
                    
                        le graphique montre une variation de nombre d'infractions entre les arrondissements.
                        Certains arrondissements se démarquent par un nombre plus élevé d'infractions, surtout 
                        le 14 et 15 éme arrondissement suggérant une concentration particulière de problèmes de stationnement,
                        tandis que d'autres affichent des chiffres plus faibles (1er,2 éme ,3 éme,4 éme, et 5 éme arrondissements),
                        reflétant potentiellement des contextes plus calmes ou des mesures de sécurité efficaces.
                    """)

    with c2:
        st.subheader(f"Distribution des infractions par saison")
        labels = data["saison"].value_counts(normalize=True).keys()
        values = data["saison"].value_counts(normalize=True).values

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.set_title("Répartition des infractions par saison")

        st.pyplot(fig)
        st.markdown("""on remarque bien que la majorité des infractions s'effectue l'éte pendant la
                     saison estivale L’été est une période de vacances où les déplacements augmentent
                    , notamment avec l’arrivée de nombreux touristes et vacanciers à Paris. Cette 
                    hausse du trafic conduit souvent à une saturation des places de stationnement,
                     forçant certains conducteurs à enfreindre les règles. Les visiteurs, moins
                     familiers avec les règles de stationnement locales, peuvent commettre des
                     infractions involontaires. Les résidents, avec moins de contrôle social en 
                    période de vacances, pourraient être plus enclins à enfreindre les règles.
                     Contrôles intensifiés : Pendant la saison touristique, les autorités 
                    peuvent intensifier les contrôles pour réguler le stationnement et la 
                    circulation, augmentant mécaniquement le nombre d’infractions recensées.
                     Impact des vacances estivales : Paris connaît une redistribution de 
                    la population en été, avec de nombreux départs de résidents et l’arrivée
                     massive de visiteurs, ce qui perturbe les dynamiques habituelles de 
                    stationnement. Les événements estivaux, comme les festivals ou activités 
                    en plein air, peuvent également contribuer à des comportements inhabituels 
                    en matière de stationnement.""")
        
    col3, col4 = st.columns([1, 1])

    with col3:
        # Compte des infractions par arrondissement et régime prioritaire
        st.subheader("Infractions par Arrondissement et Régime Prioritaire")
        plt.figure(figsize=(10, 10), dpi=200)
        sns.countplot(x="arrondissement", data=data, hue="regime_prioritaire", palette='Paired')
        st.pyplot(plt.gcf())  # Afficher le countplot
        st.markdown("""Dans tous les arrondissements, la majorité des infractions concerne 
                le stationnement interdit, tandis que la minorité est liée au 
                stationnement réservé aux livraisons ou aux bus""")

    with col4:
         # Répartition des types d'infractions (régime prioritaire)
        st.subheader("Répartition des types d'infraction (Régime Prioritaire)")
        plt.figure(figsize=(5, 5))
        labels = data["regime_prioritaire"].value_counts(normalize=True).keys()
        values = data["regime_prioritaire"].value_counts(normalize=True).values
        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title("Répartition des types d'infraction")
        st.pyplot(plt.gcf())  # Afficher la figure pie
        st.markdown("""==>La quasi-totalité des infractions relevées concerne des stationnements interdits.""")

    st.subheader("Distribution des infractions par mois ")
    if 'mois' not in data.columns:
        data['mois'] = pd.to_datetime(data['date_du_releve']).dt.month

    if 'nombre_infractions' not in data.columns:
        data['nombre_infractions'] = 1

    monthly_infractions = (
        data.groupby('mois')['nombre_infractions']
        .sum()
        .reset_index()
        .sort_values('mois')
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(
        x="mois",
        y="nombre_infractions",
        data=monthly_infractions,
        palette="coolwarm",
        legend= False,
        hue="mois",
        ax=ax
    )
    ax.set_title("Distribution des infractions par mois ")
    ax.set_xlabel("Mois")
    ax.set_ylabel("Nombre d'infractions")
    st.pyplot(fig)

    
    

    col5, col6 = st.columns([1,1])

    with col5:
        # Compte des infractions par arrondissement et régime particulier
        st.subheader("Infractions par Arrondissement et Régime Particulier")
        plt.figure(figsize=(5, 5), dpi=200)
        sns.countplot(x="arrondissement", data=data, hue="regime_particulier", palette='Paired')
        st.pyplot(plt.gcf())  # Afficher le countplot 
    
    with col6:
        # Répartition des types d'infractions (régime particulier)
        st.subheader("Répartition des types d'infraction (Régime Particulier)")
        plt.figure(figsize=(10, 10))
        labels = data["regime_particulier"].value_counts(normalize=True).keys()
        values = data["regime_particulier"].value_counts(normalize=True).values
        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title("Répartition des types d'infraction")
        st.pyplot(plt.gcf())   
        st.markdown("""==>La majorité des infractions sont des infractions liées aux stationnements gênants""")
        
    s, c = st.columns([1, 1])
    with s:

        st.subheader("Distribution des conformités de signalisation")
        fig, ax = plt.subplots(figsize=(10, 4), dpi=200)

        # Tracé du graphique
        sns.countplot(x="conformite_signalisation", data=data, ax=ax)
        ax.set_title("Distribution des conformités de signalisation")
        ax.set_xlabel("Conformité de la signalisation")
        ax.set_ylabel("Nombre d'occurrences")

        st.pyplot(fig)
        st.markdown(
        """
        <style>
        .title {
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
        }
        .full-width {
            width: 100%;
            padding: 20px 20px;
            background-color: #00000;
            border-radius: 8px;
            margin-left: -20px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True
        )
        context = """
        <div class="full-width">
             <p>
                la Signalisation Horizontale (SH) fait référence aux marquages au sol 
                utilisés pour réguler la circulation et indiquer les règles (lignes, 
                flèches, zébras, emplacements réservés..)
            </p>
            <p>
                -SV (Signalisation Verticale) concerne les panneaux, 
                feux et dispositifs installés en hauteur.
            </p>
            <p>
                -la majorité des infractions sont effectuées lorsque la signalisation 
                verticale est non conforme ce qui implique la ville de Paris
                a travailler sur l'amélioration des signalisation verticales 
            </p>
            <p>
                -La signalisation horizontale (marquages au sol) semble dans ce cas être
                conforme aux normes, mais cela n'empêche pas une 
                majorité d'infractions. Cette tendance peut être 
                attribuée à un autre problème de manque de places de 
                stationnement disponibles dans une ville densément 
                peuplée comme Paris.
            </p>
            <p>
                -Malgré une signalisation conforme, le stationnement 
                reste un défi majeur pour les usagers, ce qui entraîne
                des infractions fréquentes.
            </p>
        
        </div>
        """
        st.markdown(context, unsafe_allow_html=True)


    with c:
        st.subheader("Évolution des infractions au fil du temps")
        data = data.set_index("date_du_releve")
        data_mois = data.resample("ME")["nouvel_identifiant"].count().reset_index()
        
        # Création de la figure
        fig, ax = plt.subplots(figsize=(10, 5), dpi=200)

        # Tracé du graphique de ligne
        sns.lineplot(data=data_mois, x="date_du_releve", y="nouvel_identifiant", ax=ax, color="blue")

        ax.set_title("Évolution des infractions au fil du temps")
        ax.set_xlabel("Date du relevé")
        ax.set_ylabel("Nombre d'infractions")

        # Affichage du graphique dans Streamlit
        st.pyplot(fig)
        st.markdown("""la courbe montre une tendance globale stable durant 
                    toutes les annees de 2016 à 2025 sauf les mois de 2020
                     ou on voit un pic des infractions ,on remarque bien 
                    une explosion des infraction le mois de juillet et 
                    Aout 2024 et c'est attribuables à des événements s
                    ociaux majeurs (fin du confinement, hausse estivale).
                     Cela souligne l’importance de contextualiser les 
                    données pour mieux comprendre les facteurs qui 
                    influencent les infractions. Une meilleure gestion 
                    des flux de véhicules et une communication claire 
                    sur les règles pourraient réduire ces pics à l’avenir.
                    """)
        
#fonction pour le wordccloud
def page_4(contenu_path="contenu_clean.txt", image_path="image.png"):
    st.header("WorldCloud")
    st.subheader("Visualisation des mots clés")
    
    # Chargement de contenu
    try:
        contenu = pd.read_csv(contenu_path, header=None, names=["text"])
        if contenu.empty:  # Vérifie si le DataFrame est vide
            st.error("Le fichier de contenu est vide. Veuillez fournir un contenu valide.")
            return
        texte = ' '.join(contenu["text"])
    except FileNotFoundError:
        st.error(f"Le fichier '{contenu_path}' est introuvable. Veuillez vérifier le chemin.")
        return
    except Exception as e:
        st.error(f"Erreur lors du chargement du fichier : {e}")
        return

    # Chargement du masque (image)
    try:
        mask = np.array(Image.open(image_path))
    except FileNotFoundError:
        st.error(f"L'image '{image_path}' est introuvable. Assurez-vous qu'elle existe.")
        return
    except Exception as e:
        st.error(f"Erreur lors du chargement de l'image : {e}")
        return

    # Génération du Word Cloud
    wordcloud = WordCloud(
        width=20,
        height=20,
        background_color='white',
        mask=mask,
        contour_width=3,
        contour_color='steelblue'
    ).generate(texte)

    # Affichage du Word Cloud
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')  # Masquer les axes pour une meilleure lisibilité

    # Affichage du graphique dans Streamlit
    st.pyplot(fig)
