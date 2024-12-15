# Notebook Data management

## Importation des librairies nécessaires


```python
!pip install unidecode
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from unidecode import unidecode
import string
import nltk
from nltk.corpus import stopwords
import re

```

    Requirement already satisfied: unidecode in /usr/local/lib/python3.10/dist-packages (1.3.8)


## Importation de la base de donnée


```python
#importation de la base de données
data = pd.read_csv("/content/stationnement-sur-voie-publique-stationnement-interdit.csv", sep=';' ,on_bad_lines='skip',quoting=3)

```

    <ipython-input-221-24e9c399df9c>:2: DtypeWarning: Columns (6,19,20) have mixed types. Specify dtype option on import or set low_memory=False.
      data = pd.read_csv("/content/stationnement-sur-voie-publique-stationnement-interdit.csv", sep=';' ,on_bad_lines='skip',quoting=3)


## 1 Nettoyage de la base de données


```python
#Standardisation des noms de colonnes

data.columns = [unidecode(col) for col in data.columns]
data.columns = data.columns.str.strip().str.replace(' ', '_')
data.columns = data.columns.str.lower()

print("Après nettoyage:", data.columns)

```

    Après nettoyage: Index(['nouvel_identifiant', 'ancien_identifiant', 'regime_prioritaire',
           'regime_particulier', 'arrondissement', 'zone_residentielle',
           'tarification', 'type_de_voie', 'nom_de_la_voie', 'parite', 'longueur',
           'longueur_calculee', 'signalisation_horizontale',
           'signalisation_verticale', 'conformite_signalisation',
           'plage_horaire_1-debut', 'plage_horaire_1-fin', 'plage_horaire_2-debut',
           'plage_horaire_2-fin', 'plage_horaire_3-debut', 'plage_horaire_3-fin',
           'date_du_releve', 'derniere_date_edition', 'code_voie_ville_de_paris',
           'numero_sequentiel_troncon_voie', 'numero_ilot', 'numero_iris',
           'zone_asp', 'numero_section_territoriale_de_voirie', 'zone_prefecture',
           '1er_numero_troncon_voie', 'dernier_numero_troncon_voie', 'geo_shape',
           'geo_point_2d'],
          dtype='object')



```python
#Affichage de la taille de notre base de données
print(f"la base de données est composée de {data.shape[0]} lignes et {data.shape[1]} colonnes.")
```

    la base de données est composée de 1091114 lignes et 34 colonnes.


## Suppression des colonnes totalement vides



```python
data.dropna(axis=1,how = "all", inplace =True,)
```


```python
data.shape
```




    (1091114, 31)




```python
#Vérification des valeurs manquantes
print(data.isnull().sum())
```

    nouvel_identifiant                         11816
    ancien_identifiant                       1079298
    regime_prioritaire                             0
    regime_particulier                             0
    arrondissement                              1484
    zone_residentielle                          1484
    tarification                                1484
    type_de_voie                                   0
    nom_de_la_voie                                 0
    parite                                       640
    longueur                                       0
    longueur_calculee                              0
    signalisation_horizontale                      0
    signalisation_verticale                        0
    conformite_signalisation                       0
    plage_horaire_1-debut                    1070061
    plage_horaire_1-fin                      1070061
    plage_horaire_2-debut                    1071009
    plage_horaire_2-fin                      1071009
    plage_horaire_3-debut                    1091112
    plage_horaire_3-fin                      1091009
    date_du_releve                                 0
    derniere_date_edition                          0
    code_voie_ville_de_paris                       0
    numero_sequentiel_troncon_voie                 0
    zone_asp                                   11754
    numero_section_territoriale_de_voirie       1484
    1er_numero_troncon_voie                        0
    dernier_numero_troncon_voie                    0
    geo_shape                                      0
    geo_point_2d                                   0
    dtype: int64


## Suppression des colonnes avec les valeurs manquantes à plus  de 90%



```python
liste = ["ancien_identifiant","plage_horaire_1-debut","plage_horaire_1-fin","plage_horaire_2-debut",
         "plage_horaire_2-fin","plage_horaire_3-debut","plage_horaire_3-fin"]
data.drop(columns = liste, inplace =True)
```

## On supprime les lignes qui contiennent des valeurs manquantes et on réinitialise les index


```python
data = data.dropna().reset_index(drop=True)
```

## Suppresion des colonnes qu'on a jugé non intéressantes



```python
liste = ["zone_residentielle","nom_de_la_voie","parite","longueur","longueur_calculee","signalisation_horizontale",
         "1er_numero_troncon_voie","dernier_numero_troncon_voie","geo_shape", "zone_asp","numero_section_territoriale_de_voirie",
         "numero_sequentiel_troncon_voie", "signalisation_verticale", "code_voie_ville_de_paris", "derniere_date_edition"]
data.drop(columns = liste, inplace =True)
```

# Analyse appronfondie de la base de donnée

## Detection des valeurs aberrates dans les colonnes



```python
data["regime_particulier"].unique()
```




    array(['Stationnement gênant', 'Stationnement simple', 'Arrêt Pompiers',
           'Arrêt gênant divers', 'Arrêt simple',
           'Arrêt vigipirate pérennisé', 'Arrêt vigipirate non pérennisé',
           'Livraison BUS', 'rien'], dtype=object)




```python
data["regime_prioritaire"].unique()
```




    array(['INTERDIT', 'LIVRAISON BUS'], dtype=object)




```python
#détection des fausses information dans la colonne arrondissement
data["arrondissement"].unique()
```




    array([15., 19., 10., 14., 13., 17.,  4.,  9., 18., 20.,  7., 11.,  5.,
           12.,  6.,  2., 16.,  8.,  3., 21.,  1., 22., -1.])




```python
data["tarification"].unique()
```




    array(['01', '02', '2', '1', 'Bois', 'NR', 2.0, 1.0], dtype=object)




```python
#caster les colonnes arrondissement et tarification en entier
data["arrondissement"] = data["arrondissement"].astype("Int64")
data["tarification"] = pd.to_numeric(data["tarification"], errors="coerce").astype("Int64")
```


```python
data["tarification"].unique()
```




    <IntegerArray>
    [1, 2, <NA>]
    Length: 3, dtype: Int64




```python
#Vérification de la colonne conformite_signalisation
data["conformite_signalisation"].unique()
```




    array(['SV Non-conforme', 'Conforme', 'Non conforme', 'SH Non-conforme'],
          dtype=object)




```python
data["type_de_voie"].unique()
```




    array(['BD DES', 'AV DE', "RUE D'", 'RUE DES', 'AV DE LA', 'RUE DU',
           'RUE', 'SQ', 'IMP DE', 'AV', 'PL DE', 'BD DE', 'RUE DE',
           "RUE DE L'", 'AV DES', "IMP D'", 'AV DU', 'RTE DES', 'QU',
           'PL DE LA', 'RPT DES', 'QU DE', 'RUE DE LA', 'BD', 'PL', 'PAS',
           "PL DE L'", 'VLA', 'ALL DU', 'RTE DU', 'PORT DE', 'RTE DE',
           'CAR DE', 'RTE DE LA', 'PL DU', 'PL DES', 'IMP', 'PAS DU',
           'PAS DE LA', "PL D'", "AV DE L'", 'ALL DE LA', 'QU DE LA', "QU D'",
           'VOIE', 'ALL DE', 'CAR DE LA', 'RTE', "CAR DE L'", 'CRS LA',
           "AV D'", "QU DE L'", 'CITE', 'CRS DES', 'QU AUX', 'ALL DES',
           'BD DE LA', 'CITE DU', 'CHEM DE', 'CHEM DE LA', 'CITE DE LA',
           'BD DU', 'COUR', 'RUE AU', 'SEN DES', "PAS DE L'", 'CITE DES',
           'IMP DES', 'CITE DE', 'ALL', "PONT D'", 'SOUT', 'PAS DE', 'PONT',
           'QU DES', "CITE D'", "BD D'", 'SQ DE', "BD DE L'", 'CRS DE', 'CRS',
           "IMP DE L'", 'CHEM DU', 'SENT', 'CAR DES', 'VLA DE', "RTE D'",
           'IMP DU', 'ECH', 'IMP DE LA', 'CAR DU', 'PONT DE LA', 'PAS DES',
           'VLA DU', 'COUR DU', 'PONT DE', 'PARV DU', 'PORT DU', "VLA D'",
           'HAM DE', "RTE DE L'", 'VLA DES', 'CHAU DE LA', 'COUR DE LA',
           'PONT DU', 'SENT DE', "PONT DE L'", "CHEM DE L'", 'GRIL DE', 'PRT',
           'ESPL'], dtype=object)




```python
data["nouvel_identifiant"] = data["nouvel_identifiant"].astype("Int64")
```


```python
#Conversion date du releve en datetime
data["date_du_releve"] = pd.to_datetime(data["date_du_releve"], format="%Y-%m-%d", errors="coerce")
```

## Suppression des valeurs aberrantes


```python
#suppression de l'arrondissement -1, 21 et 22 car le arrondissement n'existe pas
data = data[data["arrondissement"] != 21]
data = data[data["arrondissement"] != 22]
data = data[data["arrondissement"] != -1]
```


```python
#verification des années dans le dataframe
data["date_du_releve"].dt.year.unique()
```




    array([2021, 2022, 2020, 2023, 2018, 2024, 2017, 2016, 2004, 1970, 2019,
           2015], dtype=int32)




```python
#Affichage des infraction pour l'année 1970
data.loc[data["date_du_releve"].dt.year==1970,:].shape
```




    (825, 9)




```python
data.loc[data["date_du_releve"].dt.year==2004,:].shape
```




    (104, 9)




```python
data.loc[data["date_du_releve"].dt.year==1995,:].shape
```




    (0, 9)



## On remarque qu'on n'a pas trop de donnée pour l'année 1995, 1970 et 2004, ce qui nous motive à travailler sur les année restantes comme elles se suivent


```python
#Liste des années sur les quelles on va faire nos analyses
liste_annee = [2016,2017,2018,2019,2020,2021,2022,2023,2024] #on préfére travailler sur les données les plus récentes
```


```python
#Création de la dataframe avec les années sélectionnée
data = data.loc[data["date_du_releve"].dt.year.isin (liste_annee),:]
```

## Vérification des doublons



```python
print(data.duplicated().value_counts())
```

    True     863339
    False    203036
    Name: count, dtype: int64


## Localisation des doublons



```python
print(data.loc[data.duplicated(),:].sort_values(by=["nouvel_identifiant"]))
```

            nouvel_identifiant regime_prioritaire    regime_particulier  \
    265068                  11           INTERDIT  Stationnement gênant   
    358326                  11           INTERDIT  Stationnement gênant   
    362259                  11           INTERDIT  Stationnement gênant   
    364092                  11           INTERDIT  Stationnement gênant   
    358319                  11           INTERDIT  Stationnement gênant   
    ...                    ...                ...                   ...   
    384829               13955           INTERDIT  Stationnement gênant   
    384823               13955           INTERDIT  Stationnement gênant   
    443415               13955           INTERDIT  Stationnement gênant   
    567561               13955           INTERDIT  Stationnement gênant   
    347571               13955           INTERDIT  Stationnement gênant   
    
            arrondissement  tarification type_de_voie conformite_signalisation  \
    265068              14             2      SENT DE                 Conforme   
    358326              20             2      SENT DE                 Conforme   
    362259              16             1      SENT DE                 Conforme   
    364092              13             1      SENT DE                 Conforme   
    358319              20             2      SENT DE                 Conforme   
    ...                ...           ...          ...                      ...   
    384829               3             2       RUE DE                 Conforme   
    384823              11             2       RUE DE                 Conforme   
    443415              11             2       RUE DE                 Conforme   
    567561              18             1       RUE DE                 Conforme   
    347571              15             1       RUE DE                 Conforme   
    
           date_du_releve                           geo_point_2d  
    265068     2020-08-31   48.84029517538814, 2.401590676758553  
    358326     2020-08-31   48.84029517538814, 2.401590676758553  
    362259     2020-08-31   48.84029517538814, 2.401590676758553  
    364092     2020-08-31   48.84029517538814, 2.401590676758553  
    358319     2020-08-31   48.84029517538814, 2.401590676758553  
    ...               ...                                    ...  
    384829     2022-08-11  48.84880314978486, 2.3511666210094253  
    384823     2022-08-11  48.84880314978486, 2.3511666210094253  
    443415     2022-08-11  48.84880314978486, 2.3511666210094253  
    567561     2022-08-11  48.84880314978486, 2.3511666210094253  
    347571     2022-08-11  48.84880314978486, 2.3511666210094253  
    
    [863339 rows x 9 columns]


Les doublons correspondent aux infractions effectuées par la même personne le même jour, mais à des localisations différentes. Par conséquent, ce sont des infractions distinctes que nous ne supprimerons pas.

## Creation de nouvelles colonnes à partirs des existantes


```python
#Création de la colonne année qui affiche l'annee de chaque infraction
data["annee"] = data["date_du_releve"].dt.year
```


```python
#Création de la colonne "saison" qui affiche la saison pour chaque infraction
data["saison"] = data["date_du_releve"].apply(
    lambda x: (
        "été" if x.month in [6, 7, 8] else
        "automne" if x.month in [9, 10, 11] else
        "hiver" if x.month in [12, 1, 2] else
        "printemps"
    )
    if pd.notnull(x) else None
)

```


```python
#Creation de la colonne "vacances" qui est égales à 1 en periode de vacances et 0 sinon
data['vacances'] = data['date_du_releve'].apply(lambda x: 1 if x.month in [7, 8, 12] else 0)
```

## Distribution temporelle : Analyser les infractions par  mois et année pour identifier des tendances temporelles.


```python
data = data.set_index("date_du_releve")
```


```python
#Creation de data_mois qui  affiche les infractions par mois
data_mois = data.resample("ME")["nouvel_identifiant"].count().reset_index()

```


```python
#Création de data_anneé qui affiche les infractions par année
data_annee = data.resample("YE")["nouvel_identifiant"].count().reset_index()

```


```python
print(data.columns)
```

    Index(['nouvel_identifiant', 'regime_prioritaire', 'regime_particulier',
           'arrondissement', 'tarification', 'type_de_voie',
           'conformite_signalisation', 'geo_point_2d', 'annee', 'saison',
           'vacances'],
          dtype='object')


## Exportation de la base de donnée en fichier CSV


```python
data.to_csv("data_manag_final_v.csv")
```

# Analyse descriptive de la base


```python
#Calcule du nombre total d'infractions
nombre_total_dinfraction = data.shape[0]
print(f"Le nombre_total_dinfraction est {nombre_total_dinfraction}")
```

    Le nombre_total_dinfraction est 1066375



```python
#calcule du nombre d'infraction moyen par ans dans la ville de Paris
nombre_annee = 9
nombre_dinfraction_moyen = nombre_total_dinfraction/nombre_annee
print(f"le nombre moyen dinfraction par an est {nombre_dinfraction_moyen}")
```

    le nombre moyen dinfraction par an est 118486.11111111111



```python
#Calcule du nombre d'infraction par arrondissement
nombre_dinfraction_par_arrondissement= data.groupby("arrondissement")["nouvel_identifiant"].count()
print(nombre_dinfraction_par_arrondissement)

```

    arrondissement
    1        178
    2      20678
    3      20706
    4      20764
    5      20862
    6      41356
    7      51662
    8      31370
    9      41525
    10     72180
    11     82522
    12     62253
    13     62170
    14    103108
    15     93110
    16     62530
    17     72351
    18     82527
    19     51909
    20     72614
    Name: nouvel_identifiant, dtype: Int64



```python
moyenne_infractions = data.groupby("arrondissement")["nouvel_identifiant"].mean()
print(moyenne_infractions)
```

    arrondissement
    1     7861.252809
    2      7347.91179
    3     7387.752197
    4     7388.191389
    5      7373.43759
    6     7374.740328
    7     7370.953931
    8     7410.893369
    9     7387.663937
    10    7360.578207
    11    7362.248564
    12    7370.485455
    13    7362.126411
    14    7368.480176
    15    7370.355569
    16    7393.941596
    17    7370.417686
    18    7361.675609
    19    7374.291433
    20    7366.452282
    Name: nouvel_identifiant, dtype: Float64

