from flask import Flask, send_file, jsonify, request, render_template_string
from flask_cors import CORS
import os
import json
from datetime import datetime
from typing import List, Dict, Any
import logging
from .exporter import DataExporter

logger = logging.getLogger(__name__)

class DownloadServer:
    """Serveur web pour télécharger les fichiers exportés"""
    
    def __init__(self, host: str = "0.0.0.0", port: int = 5000, exports_dir: str = "exports"):
        self.host = host
        self.port = port
        self.exports_dir = exports_dir
        self.app = Flask(__name__)
        CORS(self.app)
        self.exporter = DataExporter(exports_dir)
        
        # Configuration des routes
        self._setup_routes()
        
    def _setup_routes(self):
        """Configure les routes de l'application Flask"""
        
        @self.app.route('/')
        def index():
            """Page d'accueil avec interface de téléchargement"""
            return self._get_index_html()
        
        @self.app.route('/api/files')
        def list_files():
            """API pour lister les fichiers disponibles"""
            try:
                files = self._get_available_files()
                return jsonify({
                    'success': True,
                    'files': files
                })
            except Exception as e:
                logger.error(f"Erreur lors de la liste des fichiers: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/export', methods=['POST'])
        def export_data():
            """API pour exporter des données"""
            try:
                data = request.get_json()
                if not data or 'data' not in data:
                    return jsonify({
                        'success': False,
                        'error': 'Données manquantes'
                    }), 400
                
                export_data = data['data']
                format_type = data.get('format', 'all')
                filename = data.get('filename')
                
                if format_type == 'json':
                    filepath = self.exporter.export_to_json(export_data, filename)
                    return jsonify({
                        'success': True,
                        'filepath': filepath,
                        'filename': os.path.basename(filepath)
                    })
                elif format_type == 'csv':
                    filepath = self.exporter.export_to_csv(export_data, filename)
                    return jsonify({
                        'success': True,
                        'filepath': filepath,
                        'filename': os.path.basename(filepath)
                    })
                elif format_type == 'excel':
                    filepath = self.exporter.export_to_excel(export_data, filename)
                    return jsonify({
                        'success': True,
                        'filepath': filepath,
                        'filename': os.path.basename(filepath)
                    })
                elif format_type == 'all':
                    results = self.exporter.export_all_formats(export_data, filename)
                    return jsonify({
                        'success': True,
                        'results': results
                    })
                else:
                    return jsonify({
                        'success': False,
                        'error': f'Format non supporté: {format_type}'
                    }), 400
                    
            except Exception as e:
                logger.error(f"Erreur lors de l'export: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/download/<filename>')
        def download_file(filename):
            """Télécharge un fichier spécifique"""
            try:
                filepath = os.path.join(self.exports_dir, filename)
                if not os.path.exists(filepath):
                    return jsonify({
                        'success': False,
                        'error': 'Fichier non trouvé'
                    }), 404
                
                return send_file(
                    filepath,
                    as_attachment=True,
                    download_name=filename
                )
            except Exception as e:
                logger.error(f"Erreur lors du téléchargement: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
        
        @self.app.route('/api/load-json', methods=['POST'])
        def load_json_file():
            """Charge un fichier JSON existant"""
            try:
                if 'file' not in request.files:
                    return jsonify({
                        'success': False,
                        'error': 'Aucun fichier fourni'
                    }), 400
                
                file = request.files['file']
                if file.filename == '':
                    return jsonify({
                        'success': False,
                        'error': 'Aucun fichier sélectionné'
                    }), 400
                
                if not file.filename.endswith('.json'):
                    return jsonify({
                        'success': False,
                        'error': 'Le fichier doit être au format JSON'
                    }), 400
                
                # Lire le contenu JSON
                content = file.read()
                data = json.loads(content.decode('utf-8'))
                
                return jsonify({
                    'success': True,
                    'data': data,
                    'count': len(data) if isinstance(data, list) else 1
                })
                
            except json.JSONDecodeError as e:
                return jsonify({
                    'success': False,
                    'error': f'Erreur de décodage JSON: {e}'
                }), 400
            except Exception as e:
                logger.error(f"Erreur lors du chargement du fichier: {e}")
                return jsonify({
                    'success': False,
                    'error': str(e)
                }), 500
    
    def _get_available_files(self) -> List[Dict[str, Any]]:
        """Retourne la liste des fichiers disponibles"""
        files = []
        
        if not os.path.exists(self.exports_dir):
            return files
        
        for filename in os.listdir(self.exports_dir):
            filepath = os.path.join(self.exports_dir, filename)
            if os.path.isfile(filepath):
                stat = os.stat(filepath)
                files.append({
                    'filename': filename,
                    'size': stat.st_size,
                    'size_mb': round(stat.st_size / (1024 * 1024), 2),
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'download_url': f'/download/{filename}'
                })
        
        # Trier par date de modification (plus récent en premier)
        files.sort(key=lambda x: x['modified'], reverse=True)
        return files
    
    def _get_index_html(self) -> str:
        """Retourne le HTML de la page d'accueil"""
        return """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Système d'Export et Téléchargement</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .content {
            padding: 30px;
        }
        
        .section {
            margin-bottom: 40px;
            padding: 25px;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            background: #fafafa;
        }
        
        .section h2 {
            color: #333;
            margin-bottom: 20px;
            font-size: 1.5em;
            border-bottom: 2px solid #4facfe;
            padding-bottom: 10px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #555;
        }
        
        .form-group input, .form-group select, .form-group textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        .form-group input:focus, .form-group select:focus, .form-group textarea:focus {
            outline: none;
            border-color: #4facfe;
        }
        
        .btn {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 12px 25px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: transform 0.2s;
            margin-right: 10px;
            margin-bottom: 10px;
        }
        
        .btn:hover {
            transform: translateY(-2px);
        }
        
        .btn-secondary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .btn-success {
            background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        }
        
        .files-list {
            max-height: 400px;
            overflow-y: auto;
            border: 1px solid #ddd;
            border-radius: 8px;
            background: white;
        }
        
        .file-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px;
            border-bottom: 1px solid #eee;
            transition: background-color 0.2s;
        }
        
        .file-item:hover {
            background-color: #f5f5f5;
        }
        
        .file-item:last-child {
            border-bottom: none;
        }
        
        .file-info {
            flex: 1;
        }
        
        .file-name {
            font-weight: 600;
            color: #333;
            margin-bottom: 5px;
        }
        
        .file-meta {
            font-size: 0.9em;
            color: #666;
        }
        
        .status {
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            font-weight: 600;
        }
        
        .status.success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .status.error {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .status.info {
            background-color: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #4facfe;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Système d'Export et Téléchargement</h1>
            <p>Exportez vos données vers JSON, CSV, Excel et téléchargez-les facilement</p>
        </div>
        
        <div class="content">
            <!-- Section Export -->
            <div class="section">
                <h2>🚀 Exporter des Données</h2>
                
                <div class="form-group">
                    <label for="dataInput">Données JSON (optionnel):</label>
                    <textarea id="dataInput" rows="5" placeholder='[{"nom": "exemple", "valeur": 123}]'></textarea>
                </div>
                
                <div class="form-group">
                    <label for="fileInput">Ou charger un fichier JSON:</label>
                    <input type="file" id="fileInput" accept=".json">
                </div>
                
                <div class="form-group">
                    <label for="formatSelect">Format d'export:</label>
                    <select id="formatSelect">
                        <option value="all">Tous les formats</option>
                        <option value="json">JSON</option>
                        <option value="csv">CSV</option>
                        <option value="excel">Excel</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="filenameInput">Nom de fichier (optionnel):</label>
                    <input type="text" id="filenameInput" placeholder="mon_export">
                </div>
                
                <button class="btn" onclick="exportData()">📤 Exporter</button>
                <button class="btn btn-secondary" onclick="loadExistingData()">📁 Charger ads_1.json</button>
            </div>
            
            <!-- Section Fichiers -->
            <div class="section">
                <h2>📁 Fichiers Disponibles</h2>
                <button class="btn btn-secondary" onclick="refreshFiles()">🔄 Actualiser</button>
                <div id="filesList" class="files-list">
                    <div class="loading">
                        <div class="spinner"></div>
                        <p>Chargement des fichiers...</p>
                    </div>
                </div>
            </div>
            
            <!-- Section Statut -->
            <div id="status"></div>
        </div>
    </div>
    
    <script>
        // Charger les fichiers au démarrage
        document.addEventListener('DOMContentLoaded', function() {
            refreshFiles();
        });
        
        function showStatus(message, type = 'info') {
            const statusDiv = document.getElementById('status');
            statusDiv.innerHTML = `<div class="status ${type}">${message}</div>`;
            setTimeout(() => {
                statusDiv.innerHTML = '';
            }, 5000);
        }
        
        function showLoading(show = true) {
            const loading = document.querySelector('.loading');
            loading.style.display = show ? 'block' : 'none';
        }
        
        async function exportData() {
            const dataInput = document.getElementById('dataInput').value;
            const formatSelect = document.getElementById('formatSelect').value;
            const filenameInput = document.getElementById('filenameInput').value;
            
            let data;
            
            try {
                if (dataInput.trim()) {
                    data = JSON.parse(dataInput);
                } else {
                    showStatus('Veuillez fournir des données JSON ou charger un fichier', 'error');
                    return;
                }
                
                showLoading(true);
                
                const response = await fetch('/api/export', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        data: data,
                        format: formatSelect,
                        filename: filenameInput || undefined
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    showStatus('Export réussi!', 'success');
                    refreshFiles();
                } else {
                    showStatus('Erreur lors de l\'export: ' + result.error, 'error');
                }
                
            } catch (error) {
                showStatus('Erreur: ' + error.message, 'error');
            } finally {
                showLoading(false);
            }
        }
        
        async function loadExistingData() {
            try {
                showLoading(true);
                
                const response = await fetch('/download/ads_1.json');
                if (response.ok) {
                    const data = await response.json();
                    document.getElementById('dataInput').value = JSON.stringify(data.slice(0, 5), null, 2);
                    showStatus(`Données chargées (${data.length} éléments, affichage des 5 premiers)`, 'success');
                } else {
                    showStatus('Fichier ads_1.json non trouvé', 'error');
                }
                
            } catch (error) {
                showStatus('Erreur lors du chargement: ' + error.message, 'error');
            } finally {
                showLoading(false);
            }
        }
        
        async function refreshFiles() {
            try {
                showLoading(true);
                
                const response = await fetch('/api/files');
                const result = await response.json();
                
                const filesList = document.getElementById('filesList');
                
                if (result.success) {
                    if (result.files.length === 0) {
                        filesList.innerHTML = '<div style="padding: 20px; text-align: center; color: #666;">Aucun fichier disponible</div>';
                    } else {
                        filesList.innerHTML = result.files.map(file => `
                            <div class="file-item">
                                <div class="file-info">
                                    <div class="file-name">${file.filename}</div>
                                    <div class="file-meta">
                                        Taille: ${file.size_mb} MB | Modifié: ${new Date(file.modified).toLocaleString()}
                                    </div>
                                </div>
                                <a href="${file.download_url}" class="btn btn-success">📥 Télécharger</a>
                            </div>
                        `).join('');
                    }
                } else {
                    filesList.innerHTML = '<div style="padding: 20px; text-align: center; color: #f00;">Erreur lors du chargement des fichiers</div>';
                }
                
            } catch (error) {
                document.getElementById('filesList').innerHTML = 
                    '<div style="padding: 20px; text-align: center; color: #f00;">Erreur de connexion</div>';
            } finally {
                showLoading(false);
            }
        }
        
        // Gestion du chargement de fichier
        document.getElementById('fileInput').addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    try {
                        const data = JSON.parse(e.target.result);
                        document.getElementById('dataInput').value = JSON.stringify(data, null, 2);
                        showStatus(`Fichier chargé: ${file.name} (${data.length} éléments)`, 'success');
                    } catch (error) {
                        showStatus('Erreur lors du parsing du fichier JSON', 'error');
                    }
                };
                reader.readAsText(file);
            }
        });
    </script>
</body>
</html>
        """
    
    def start(self):
        """Démarre le serveur"""
        logger.info(f"Démarrage du serveur de téléchargement sur http://{self.host}:{self.port}")
        self.app.run(host=self.host, port=self.port, debug=False)
    
    def stop(self):
        """Arrête le serveur"""
        logger.info("Arrêt du serveur de téléchargement") 