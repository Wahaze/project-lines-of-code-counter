import os
import argparse
import chardet
import html as html_utils
from datetime import datetime

def est_fichier_texte(chemin):
    try:
        with open(chemin, 'rb') as file:
            contenu = file.read(1024)  # Lire les premiers 1024 octets
        result = chardet.detect(contenu)
        if result['encoding'] is None:
            return False
        confidence = result['confidence']
        return confidence > 0.7 and not contenu.startswith(b'\x00')  # Éviter les fichiers commençant par un octet nul
    except Exception:
        return False

def lire_fichier(chemin):
    try:
        with open(chemin, 'rb') as file:
            raw_data = file.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        if encoding is None:
            return None
        return raw_data.decode(encoding)
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {chemin}: {str(e)}")
        return None

def analyser_contenu(contenu):
    """Analyse le contenu pour extraire les statistiques"""
    if contenu is None:
        return 0, 0, 0
    
    nb_caracteres = len(contenu)
    nb_mots = len(contenu.split())
    nb_lignes = len(contenu.splitlines())
    
    return nb_caracteres, nb_mots, nb_lignes

def obtenir_extension(nom_fichier):
    """Obtient l'extension du fichier"""
    return os.path.splitext(nom_fichier)[1].lower()

def ecrire_contenu_txt(fichier_sortie, nom_fichier, chemin, contenu):
    """Écrit le contenu dans le fichier texte"""
    fichier_sortie.write(f"\n{'='*80}\n")
    fichier_sortie.write(f"Fichier : {nom_fichier}\n")
    fichier_sortie.write(f"Chemin : {chemin}\n")
    fichier_sortie.write(f"{'='*80}\n\n")
    fichier_sortie.write(contenu)
    fichier_sortie.write("\n\n")

def generer_html_header(nom_projet):
    """Génère l'en-tête HTML avec le CSS"""
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analyse du projet {nom_projet}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header .date {{
            opacity: 0.9;
            font-size: 1.1em;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            color: #666;
            text-transform: uppercase;
            font-size: 0.9em;
            letter-spacing: 1px;
        }}
        
        .section {{
            background: white;
            border-radius: 10px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 2px 15px rgba(0,0,0,0.1);
        }}
        
        .section h2 {{
            color: #333;
            margin-bottom: 20px;
            font-size: 1.8em;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        
        .files-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        
        .files-table th,
        .files-table td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        
        .files-table th {{
            background-color: #f8f9fa;
            font-weight: 600;
            color: #555;
            text-transform: uppercase;
            font-size: 0.9em;
            letter-spacing: 0.5px;
        }}
        
        .files-table tr:hover {{
            background-color: #f8f9fa;
        }}
        
        .file-extension {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
            color: white;
        }}
        
        .ext-py {{ background-color: #3776ab; }}
        .ext-js {{ background-color: #f7df1e; color: #333; }}
        .ext-html {{ background-color: #e34c26; }}
        .ext-css {{ background-color: #1572b6; }}
        .ext-json {{ background-color: #000; }}
        .ext-md {{ background-color: #083fa1; }}
        .ext-txt {{ background-color: #666; }}
        .ext-default {{ background-color: #999; }}
        
        .file-content {{
            background-color: #f8f9fa;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 20px;
            margin: 20px 0;
        }}
        
        .file-header {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 15px;
            border-radius: 5px 5px 0 0;
            border-bottom: 2px solid #667eea;
            margin-bottom: 15px;
        }}
        
        .file-title {{
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }}
        
        .file-path {{
            color: #666;
            font-size: 0.9em;
            font-family: 'Courier New', monospace;
        }}
        
        .code-content {{
            background-color: #282c34;
            color: #abb2bf;
            padding: 20px;
            border-radius: 5px;
            overflow-x: auto;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            line-height: 1.4;
            white-space: pre-wrap;
        }}
        
        .nav-top {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #667eea;
            color: white;
            padding: 15px;
            border-radius: 50%;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: all 0.3s ease;
            text-decoration: none;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 60px;
            height: 60px;
        }}
        
        .nav-top:hover {{
            background: #5a67d8;
            transform: translateY(-3px);
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 10px;
            }}
            
            .header h1 {{
                font-size: 2em;
            }}
            
            .files-table {{
                font-size: 0.9em;
            }}
            
            .files-table th,
            .files-table td {{
                padding: 8px 4px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📁 Analyse du projet {nom_projet}</h1>
            <div class="date">Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}</div>
        </div>
"""

def generer_statistiques_html(fichiers_info, nom_projet):
    """Génère les statistiques générales"""
    total_fichiers = len(fichiers_info)
    total_caracteres = sum(info['nb_caracteres'] for info in fichiers_info)
    total_mots = sum(info['nb_mots'] for info in fichiers_info)
    total_lignes = sum(info['nb_lignes'] for info in fichiers_info)
    
    # Statistiques par extension
    extensions = {}
    for info in fichiers_info:
        ext = info['extension']
        if ext not in extensions:
            extensions[ext] = 0
        extensions[ext] += 1
    
    html = f"""
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{total_fichiers:,}</div>
                <div class="stat-label">Fichiers</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_caracteres:,}</div>
                <div class="stat-label">Caractères</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_mots:,}</div>
                <div class="stat-label">Mots</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_lignes:,}</div>
                <div class="stat-label">Lignes</div>
            </div>
        </div>
    """
    
    return html

def obtenir_classe_extension(extension):
    """Retourne la classe CSS pour l'extension"""
    ext_classes = {
        '.py': 'ext-py',
        '.js': 'ext-js',
        '.html': 'ext-html',
        '.css': 'ext-css',
        '.json': 'ext-json',
        '.md': 'ext-md',
        '.txt': 'ext-txt'
    }
    return ext_classes.get(extension, 'ext-default')

def generer_tableau_fichiers_html(fichiers_info):
    """Génère le tableau des fichiers triés par taille"""
    # Trier les fichiers par nombre de caractères (décroissant)
    fichiers_tries = sorted(fichiers_info, key=lambda x: x['nb_caracteres'], reverse=True)
    
    html = """
        <div class="section">
            <h2 id="classement">📊 Classement des fichiers par taille</h2>
            <table class="files-table">
                <thead>
                    <tr>
                        <th>Rang</th>
                        <th>Fichier</th>
                        <th>Extension</th>
                        <th>Caractères</th>
                        <th>Mots</th>
                        <th>Lignes</th>
                        <th>Chemin</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    for i, info in enumerate(fichiers_tries, 1):
        classe_ext = obtenir_classe_extension(info['extension'])
        html += f"""
                    <tr>
                        <td><strong>#{i}</strong></td>
                        <td><strong>{html_utils.escape(info['nom_fichier'])}</strong></td>
                        <td><span class="file-extension {classe_ext}">{info['extension'] or 'N/A'}</span></td>
                        <td>{info['nb_caracteres']:,}</td>
                        <td>{info['nb_mots']:,}</td>
                        <td>{info['nb_lignes']:,}</td>
                        <td><code>{html_utils.escape(info['chemin'])}</code></td>
                    </tr>
        """
    
    html += """
                </tbody>
            </table>
        </div>
    """
    
    return html

def generer_contenu_fichiers_html(fichiers_info):
    """Génère le contenu détaillé de chaque fichier"""
    # Trier les fichiers par nombre de caractères (décroissant)
    fichiers_tries = sorted(fichiers_info, key=lambda x: x['nb_caracteres'], reverse=True)
    
    html = """
        <div class="section">
            <h2 id="contenu">📄 Contenu des fichiers</h2>
    """
    
    for i, info in enumerate(fichiers_tries, 1):
        if info['contenu'] is not None:
            html += f"""
            <div class="file-content">
                <div class="file-header">
                    <div class="file-title">#{i} - {html_utils.escape(info['nom_fichier'])}</div>
                    <div class="file-path">{html_utils.escape(info['chemin'])}</div>
                    <div style="margin-top: 10px;">
                        <strong>Stats:</strong> {info['nb_caracteres']:,} caractères | {info['nb_mots']:,} mots | {info['nb_lignes']:,} lignes
                    </div>
                </div>
                <div class="code-content">{html_utils.escape(info['contenu'])}</div>
            </div>
            """
    
    html += """
        </div>
    """
    
    return html

def generer_html_footer():
    """Génère le pied de page HTML"""
    return """
        <a href="#" class="nav-top" onclick="window.scrollTo(0,0); return false;">↑</a>
    </div>
</body>
</html>
"""

def doit_ignorer_chemin(chemin):
    # Liste des dossiers à exclure
    dossiers_exclus = ['node_modules', 'dist', 'dist-electron']
    
    # Vérifier si le chemin contient un des dossiers à exclure
    for dossier in dossiers_exclus:
        if f'/{dossier}/' in chemin.replace('\\', '/') or chemin.replace('\\', '/').endswith(f'/{dossier}'):
            return True
    
    # Vérifier si c'est le fichier package-lock.json
    if os.path.basename(chemin) == 'package-lock.json':
        return True
        
    return False

def parcourir_repertoire(repertoire):
    fichiers = []
    for racine, dossiers, noms_fichiers in os.walk(repertoire):
        # Filtrer les dossiers à exclure pour éviter de les traverser
        dossiers[:] = [d for d in dossiers if d not in ['node_modules', 'dist', 'dist-electron']]
        
        for nom_fichier in noms_fichiers:
            if nom_fichier == 'package-lock.json':
                continue
                
            chemin_complet = os.path.join(racine, nom_fichier)
            if not doit_ignorer_chemin(chemin_complet) and est_fichier_texte(chemin_complet):
                fichiers.append((nom_fichier, chemin_complet))
    return fichiers

def main(repertoire):
    fichiers = parcourir_repertoire(repertoire)
    nom_projet = os.path.basename(repertoire)
    
    # Collecter les informations sur tous les fichiers
    fichiers_info = []
    
    print(f"Analyse de {len(fichiers)} fichiers...")
    
    for nom_fichier, chemin in fichiers:
        contenu = lire_fichier(chemin)
        nb_caracteres, nb_mots, nb_lignes = analyser_contenu(contenu)
        extension = obtenir_extension(nom_fichier)
        
        fichiers_info.append({
            'nom_fichier': nom_fichier,
            'chemin': chemin,
            'contenu': contenu,
            'nb_caracteres': nb_caracteres,
            'nb_mots': nb_mots,
            'nb_lignes': nb_lignes,
            'extension': extension
        })
        
        print(f"  ✓ {nom_fichier} ({nb_caracteres:,} caractères)")
    
    # Générer le fichier texte (format original)
    fichier_txt_path = f"contenu_{nom_projet}.txt"
    with open(fichier_txt_path, 'w', encoding='utf-8') as fichier_sortie:
        for info in fichiers_info:
            if info['contenu'] is not None:
                ecrire_contenu_txt(fichier_sortie, info['nom_fichier'], info['chemin'], info['contenu'])
    
    # Générer le fichier HTML
    fichier_html_path = f"analyse_{nom_projet}.html"
    with open(fichier_html_path, 'w', encoding='utf-8') as fichier_html:
        # En-tête HTML avec CSS
        fichier_html.write(generer_html_header(nom_projet))
        
        # Statistiques générales
        fichier_html.write(generer_statistiques_html(fichiers_info, nom_projet))
        
        # Tableau des fichiers triés
        fichier_html.write(generer_tableau_fichiers_html(fichiers_info))
        
        # Contenu détaillé des fichiers
        fichier_html.write(generer_contenu_fichiers_html(fichiers_info))
        
        # Pied de page
        fichier_html.write(generer_html_footer())
    
    print(f"\n✅ Analyse terminée !")
    print(f"📄 Fichier texte : {fichier_txt_path}")
    print(f"🌐 Fichier HTML : {fichier_html_path}")
    print(f"📊 {len(fichiers_info)} fichiers analysés")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Consolide le contenu des fichiers texte d'un répertoire et génère une analyse HTML.")
    parser.add_argument("repertoire", help="Chemin du répertoire à analyser")
    args = parser.parse_args()

    main(args.repertoire)