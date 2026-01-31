from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import subprocess
import os
import json
from datetime import datetime
import re

app = Flask(__name__)

# Configuración
UPLOAD_FOLDER = 'downloads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    """Descarga video de YouTube"""
    try:
        data = request.json
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL no proporcionada'}), 400
        
        # Opciones de yt-dlp
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(UPLOAD_FOLDER, '%(id)s.%(ext)s'),
            'quiet': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_id = info['id']
            title = info['title']
            duration = info['duration']
            
            # Buscar el archivo descargado
            video_file = None
            for ext in ['mp4', 'webm', 'mkv']:
                potential_file = os.path.join(UPLOAD_FOLDER, f"{video_id}.{ext}")
                if os.path.exists(potential_file):
                    video_file = potential_file
                    break
            
            if not video_file:
                return jsonify({'error': 'Video descargado pero archivo no encontrado'}), 500
            
            return jsonify({
                'success': True,
                'video_id': video_id,
                'title': title,
                'duration': duration,
                'file': video_file
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/create_clip', methods=['POST'])
def create_clip():
    """Crea un clip vertical del video"""
    try:
        data = request.json
        video_file = data.get('video_file')
        start_time = float(data.get('start_time', 0))
        duration = float(data.get('duration', 30))
        
        if not video_file or not os.path.exists(video_file):
            return jsonify({'error': 'Archivo de video no encontrado'}), 400
        
        # Nombre del archivo de salida
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(OUTPUT_FOLDER, f'clip_{timestamp}.mp4')
        
        # Comando FFmpeg para crear clip vertical (9:16)
        # 1. Cortar el video
        # 2. Escalar y recortar al formato vertical
        # 3. Añadir filtros para mejorar calidad
        cmd = [
            'ffmpeg',
            '-ss', str(start_time),
            '-i', video_file,
            '-t', str(duration),
            '-vf', 'scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920',
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-y',
            output_file
        ]
        
        # Ejecutar FFmpeg
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            return jsonify({'error': f'Error en FFmpeg: {result.stderr}'}), 500
        
        # Obtener tamaño del archivo
        file_size = os.path.getsize(output_file)
        
        return jsonify({
            'success': True,
            'output_file': output_file,
            'file_size': file_size,
            'download_url': f'/download_clip/{os.path.basename(output_file)}'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download_clip/<filename>')
def download_clip(filename):
    """Descarga el clip generado"""
    try:
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'Archivo no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_video_info/<video_id>')
def get_video_info(video_id):
    """Obtiene información del video sin descargarlo"""
    try:
        url = f'https://www.youtube.com/watch?v={video_id}'
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            return jsonify({
                'title': info['title'],
                'duration': info['duration'],
                'thumbnail': info['thumbnail'],
                'view_count': info.get('view_count', 0),
                'channel': info.get('channel', 'Unknown')
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
