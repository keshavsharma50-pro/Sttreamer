from flask import Flask, request, render_template_string
import subprocess
import os
import threading

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# The mobile-friendly user interface
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloud Streamer</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; background-color: #121212; color: white; text-align: center; }
        .container { max-width: 400px; margin: auto; background: #1e1e1e; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
        input[type="text"], input[type="file"] { width: 90%; padding: 10px; margin: 10px 0; border-radius: 5px; border: none; }
        button { background-color: #ff0000; color: white; border: none; padding: 15px 20px; font-size: 16px; border-radius: 5px; width: 100%; cursor: pointer; font-weight: bold; }
        button:hover { background-color: #cc0000; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Keshav's Cloud Streamer</h2>
        <p>Upload a video to stream flawlessly to YouTube.</p>
        <form action="/start_stream" method="post" enctype="multipart/form-data">
            <input type="file" name="video" accept="video/mp4,video/x-m4v,video/*" required>
            <input type="text" name="stream_key" placeholder="Paste YouTube Stream Key Here" required>
            <button type="submit">Upload & Go Live</button>
        </form>
    </div>
</body>
</html>
"""

def stream_video(video_path, stream_key):
    # This runs the perfect FFmpeg command in the cloud for zero quality loss
    youtube_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"
    command = [
        "ffmpeg", "-re", "-i", video_path,
        "-c:v", "copy", "-c:a", "copy",
        "-f", "flv", youtube_url
    ]
    subprocess.run(command)
    # Clean up the file after streaming finishes to save cloud space
    os.remove(video_path)

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/start_stream', methods=['POST'])
def start_stream():
    if 'video' not in request.files or not request.form.get('stream_key'):
        return "Missing video or stream key!", 400
    
    file = request.files['video']
    stream_key = request.form['stream_key']
    
    if file.filename == '':
        return "No selected file", 400
        
    video_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(video_path)
    
    # Start the stream in the background so the webpage doesn't freeze
    thread = threading.Thread(target=stream_video, args=(video_path, stream_key))
    thread.start()
    
    return "<h2 style='color: white; text-align:center; font-family: Arial; margin-top: 50px;'>Success! Your video is now being streamed from the cloud to Keshav Sharma 2023. You can safely close this app.</h2>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
  
