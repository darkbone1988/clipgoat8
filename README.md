# 🎬 ClipGOAT - Generador de Clips Verticales

Herramienta web para convertir videos de YouTube en clips verticales (formato 9:16) perfectos para TikTok, Instagram Reels y YouTube Shorts.

## 🚀 Características

- ✅ Descarga videos de YouTube
- ✅ Corta clips personalizados (5-60 segundos)
- ✅ Convierte automáticamente a formato vertical (1080x1920)
- ✅ Interfaz web moderna y fácil de usar
- ✅ Procesamiento con FFmpeg de alta calidad

## 📦 Tecnologías

- **Backend**: Flask (Python)
- **Descarga**: yt-dlp
- **Procesamiento**: FFmpeg
- **Frontend**: HTML, CSS, JavaScript

## 🔧 Instalación Local (Opcional)

```bash
# Clonar el repositorio
git clone <tu-repo>
cd clipgoat

# Instalar dependencias
pip install -r requirements.txt

# Instalar FFmpeg (si no está instalado)
# Ubuntu/Debian:
sudo apt-get install ffmpeg

# macOS:
brew install ffmpeg

# Windows:
# Descargar desde https://ffmpeg.org/download.html

# Ejecutar la aplicación
python app.py
```

Visita `http://localhost:5000` en tu navegador.

## 🚂 Desplegar en Railway

### Paso 1: Preparar el Código

1. Sube tu código a GitHub (si aún no lo has hecho)
2. Asegúrate de que todos los archivos estén en el repositorio:
   - `app.py`
   - `requirements.txt`
   - `Procfile`
   - `nixpacks.toml`
   - `railway.json`
   - Carpeta `templates/`
   - Carpeta `static/`

### Paso 2: Crear Cuenta en Railway

1. Ve a [railway.app](https://railway.app)
2. Haz clic en "Start a New Project"
3. Conecta tu cuenta de GitHub

### Paso 3: Desplegar

1. Selecciona "Deploy from GitHub repo"
2. Elige tu repositorio `clipgoat`
3. Railway detectará automáticamente:
   - Python como lenguaje
   - Instalará FFmpeg usando nixpacks.toml
   - Configurará el puerto automáticamente
4. Espera 2-3 minutos mientras se despliega

### Paso 4: Obtener tu URL

1. Una vez desplegado, haz clic en "Settings"
2. Genera un dominio público
3. ¡Tu app estará disponible en `tu-app.railway.app`!

## 📝 Estructura del Proyecto

```
clipgoat/
├── app.py                 # Aplicación Flask principal
├── requirements.txt       # Dependencias Python
├── Procfile              # Comando de inicio para Railway
├── nixpacks.toml         # Configuración FFmpeg para Railway
├── railway.json          # Configuración Railway
├── .gitignore           # Archivos a ignorar
├── README.md            # Este archivo
├── templates/
│   └── index.html       # Interfaz web
└── static/
    ├── css/
    │   └── style.css    # Estilos
    └── js/
        └── main.js      # Lógica del frontend
```

## 💡 Uso

1. **Pega la URL de YouTube**: Copia cualquier URL de YouTube y pégala en el campo
2. **Descarga**: Haz clic en "Descargar" y espera unos segundos
3. **Configura el clip**: 
   - Establece el tiempo de inicio (en segundos)
   - Define la duración del clip (5-60 segundos)
4. **Genera**: Haz clic en "Generar Clip Vertical"
5. **Descarga**: Una vez procesado, descarga tu clip vertical

## ⚙️ Configuración FFmpeg

El comando FFmpeg usado para crear clips verticales:

```bash
ffmpeg -ss START -i INPUT.mp4 -t DURATION \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k \
  OUTPUT.mp4
```

Esto:
- Escala el video a 1080x1920 (9:16)
- Recorta el contenido para llenar el formato vertical
- Mantiene buena calidad (CRF 23)
- Optimiza para redes sociales

## 🎯 Mejoras Futuras

- [ ] Transcripción automática con Whisper
- [ ] Detección automática de momentos virales
- [ ] Generación automática de subtítulos
- [ ] Análisis de score viral
- [ ] Múltiples clips del mismo video
- [ ] Preview del clip antes de procesar
- [ ] Selector visual del punto de corte

## 📊 Límites de Railway (Plan Gratuito)

- **Tiempo**: ~500 horas/mes gratis
- **RAM**: 512 MB - 8 GB (configurable)
- **Almacenamiento**: Efímero (los archivos se borran al reiniciar)
- **Ancho de banda**: Ilimitado

💡 **Tip**: Los archivos se borran cuando el servicio se reinicia, así que descarga tus clips inmediatamente.

## 🐛 Solución de Problemas

### Error: "Video descargado pero archivo no encontrado"
- Verifica que FFmpeg esté instalado
- Revisa los logs de Railway

### Error: "FFmpeg no encontrado"
- Asegúrate de que `nixpacks.toml` esté en el repositorio
- Verifica que FFmpeg esté listado en nixPkgs

### El video tarda mucho en procesarse
- Es normal para videos largos
- Railway procesa en sus servidores, no en tu computadora

## 📧 Soporte

Si tienes problemas:
1. Revisa los logs en Railway Dashboard
2. Verifica que todos los archivos estén en GitHub
3. Asegúrate de que FFmpeg esté instalado correctamente

## 📄 Licencia

Proyecto personal - Uso libre

---

**¡Disfruta creando clips virales! 🎉**
