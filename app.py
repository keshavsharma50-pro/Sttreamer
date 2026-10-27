from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Keshav's Cloud Streamer</title>
        <style>
            body { background-color: #2b2b2b; color: white; font-family: sans-serif; text-align: center; padding-top: 50px; }
            input, button { margin: 10px; padding: 10px; border-radius: 5px; width: 80%; max-width: 400px; }
            button { background-color: #ff0000; color: white; border: none; font-weight: bold; cursor: pointer; }
        </style>
    </head>
    <body>
        <h2>Keshav's Cloud Streamer</h2>
        <form action="/stream" method="POST">
            <input type="text" name="video_url" placeholder="Paste Direct Video Link Here" required><br>
            <input type="password" name="stream_key" placeholder="Paste YouTube Stream Key Here" required><br>
            <button type="submit">Start Stream</button>
        </form>
    </body>
    </html>
    '''

@app.route('/stream', methods=['POST'])
def stream():
    video_url = request.form['video_url']
    stream_key = request.form['stream_key']
    
    rtmp_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"
    
    # FFmpeg command to pull from URL and push to YouTube
    command = [
        'ffmpeg', '-re', '-i', video_url,
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k',
        '-f', 'flv', rtmp_url
    ]
    
    subprocess.Popen(command)
    return "Stream started! Check your YouTube Live Dashboard."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
