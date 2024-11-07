from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

# Folder, do którego będą zapisywane pliki
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def download_video(url, format='mp4'):
    # Ustawienia dla yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best' if format == 'mp3' else 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if format == 'mp3' else [],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        return os.path.join(DOWNLOAD_FOLDER, f"{info_dict['title']}.{format}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    video_url = request.form['url']
    format_choice = request.form['format']

    if format_choice not in ['mp3', 'mp4']:
        return "Błędny format! Proszę wybrać mp3 lub mp4.", 400

    try:
        file_path = download_video(video_url, format_choice)
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return f"Coś poszło nie tak: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
