from nbconvert import MarkdownExporter
import nbformat

# Charger le notebook
with open('Projet_data_visualisation.ipynb') as f:
    notebook = nbformat.read(f, as_version=4)

# Créer un exporteur Markdown
md_exporter = MarkdownExporter()

# Convertir en Markdown
body, resources = md_exporter.from_notebook_node(notebook)

# Sauvegarder dans un fichier
with open('final.md', 'w') as f:
    f.write(body)