import streamlit as st


def intro():
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
    st.markdown('<div class="title">SDA_2024</div>', unsafe_allow_html=True)
    context = """
    <div class="full-width">
        <h3>Inroduction</h3>
        <p>
            Les infractions de stationnement à Paris sont un enjeu majeur pour la gestion de l’espace urbain.
        </p>
        <p>
        Ce projet exploite une base de données regroupant des informations détaillées sur les infractions de 
        stationnement interdit, telles que la date et le lieu.
        </p>
        <p>
            Grâce à des outils d’analyse de données et de visualisation géographique, l’objectif est d’identifier les 
            tendances, les zones critiques et les périodes les plus propices aux infractions. Cette étude offre une 
            nouvelle perspective sur un problème quotidien, en alliant exploration technique et réflexion pratique sur
            la mobilité urbaine.
        </p>
    </div>
    """
    st.markdown(context, unsafe_allow_html=True)

    st.markdown("""
Ce projet est réalisé dans le cadre de la formation en Data Analytics de la Sorbonne, avec un focus sur la gestion des données, la visualisation des données.

---

### **(1) Phase de Gestion des Données**
*Réalisée avec Jupyter Notebook et Pandas*

#### **1. Chargement et Nettoyage des Données**
- Chargement et inspection du jeu de données sur les infractions de stationnement à Paris.
- Gestion des valeurs manquantes et uniformisation des données (formats de date, standardisation des adresses).

#### **2. Analyse Préliminaire**
- Compréhension de la structure des données : colonnes clés comme la date, le lieu et le type d’infraction.
---

### **(2) Phase d’Analyse Statistique et Création de Nouvelles Colonnes**

#### **Statistiques Descriptives**
- Moyenne, médiane, écart-type des infractions par jour/arrondissement.
- Distribution temporelle et géographique des infractions.
- Identification des valeurs aberrantes.

#### **Création de Nouvelles Colonnes**
- Saison : Printemps, été, automne, hiver, en fonction de la date.
- Année : Extraction de l’année à partir des données temporelles.
- Vacances : Indicateur binaire pour différencier les périodes scolaires et les vacances.

---

### **(3) Phase de Visualisation des Données**

#### **Visualisations Statistiques**
- Histogrammes : Distribution des infractions par arrondissement ou période.
- Barplots : Comparaison des infractions entre saisons ou types de journées.
- Heatmaps temporelles : Visualisation des infractions par heure ou jour de la semaine.

#### **Visualisation Géographique**
- Cartographie des infractions sur un plan de Paris :
  - Points de données indiquant les lieux précis des infractions.
  - Cartes de chaleur pour repérer les zones les plus touchées.
  - Segmentation des cartes par arrondissement ou type de violation.

#### **Visualisations Dynamiques**
- Mise en place d’interactions avec Streamlit pour :
  - Filtrer les données en fonction de l’année, de la saison ou de l’arrondissement.
  - Générer des graphiques ou cartes personnalisées selon les choix de l’utilisateur.
""")