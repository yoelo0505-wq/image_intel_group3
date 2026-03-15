from flask import Flask, request
import folium
import os
import tempfile
from werkzeug.utils import secure_filename

from extractor import extract_all
from map_view import create_map
from timeline import create_timeline
from analyzer import analyze
from report import create_report  

from spcieal_aiAnalyzer import process_image_folder 

app = Flask(__name__)

# DEVELOPER CONTROLS 
DEV_SMART_MODE = False  

def smart_mode(is_active):
    global DEV_SMART_MODE
    DEV_SMART_MODE = is_active
    print(f"[*] Developer switched Smart Mode to: {DEV_SMART_MODE}")

# DEVELOPER: Change this to True to use Gemini, or False to use YOLO!
smart_mode(True) 


@app.route('/') 
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Image Intel</title>
        <style>
            body { 
                background-color: #0B1120; 
                color: white; 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                display: flex; 
                justify-content: center; 
                align-items: center; 
                height: 100vh; 
                margin: 0; 
            }
            .card { 
                background-color: #1E293B; 
                padding: 40px; 
                border-radius: 12px; 
                box-shadow: 0 10px 25px rgba(0,0,0,0.5); 
                width: 100%; 
                max-width: 450px; 
                text-align: center; 
            }
            h1 { 
                color: #38BDF8; 
                margin-top: 0;
                margin-bottom: 5px; 
                font-size: 36px; 
                letter-spacing: 1px;
            }
            .subtitle { 
                color: #94A3B8; 
                margin-bottom: 30px; 
                font-size: 15px; 
            }
            .skinny-input {
                width: 100%;
                background-color: #0F172A;
                border: 1px solid #475569;
                border-radius: 6px;
                color: white;
                padding: 12px 15px;
                font-size: 14px;
                box-sizing: border-box;
                outline: none;
                transition: border-color 0.2s;
            }
            .skinny-input:focus { border-color: #38BDF8; }
            .divider { margin: 20px 0; color: #64748B; font-weight: bold; font-size: 14px; }
            .drop-zone {
                border: 2px dashed #475569;
                border-radius: 12px;
                padding: 40px 20px;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            .drop-zone:hover, .drop-zone.dragover { border-color: #38BDF8; background-color: rgba(56, 189, 248, 0.05); }
            .plus-sign { font-size: 60px; color: #38BDF8; line-height: 1; margin-bottom: 10px; }
            button { 
                background-color: #38BDF8; 
                color: #0F172A; 
                font-weight: bold; 
                font-size: 18px; 
                padding: 15px; 
                width: 100%; 
                border: none; 
                border-radius: 8px; 
                cursor: pointer; 
                margin-top: 25px;
            }
            button:hover { background-color: #0EA5E9; }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Image Intel</h1>
            <p class="subtitle">EXIF Data Scanning and Analysis System</p>
            
            <form action="/analyze" method="POST" enctype="multipart/form-data">
                <input type="text" name="folder_path" class="skinny-input" placeholder="Paste full folder path here...">

                <div class="divider">--- OR ---</div>

                <div class="drop-zone" id="drop-zone">
                    <div class="plus-sign">+</div>
                    <div id="drop-text" style="color: #94A3B8; font-size: 14px;">Drag & drop photos or click to browse</div>
                    <input type="file" name="uploaded_images" id="file-input" multiple accept="image/*" style="display: none;">
                </div>

                <button type="submit">Start Intelligence Analysis</button>
            </form>
        </div>

        <script>
            const dropZone = document.getElementById('drop-zone');
            const fileInput = document.getElementById('file-input');
            const dropText = document.getElementById('drop-text');
            
            const dataTransfer = new DataTransfer();

            function handleFiles(newFiles) {
                for (let i = 0; i < newFiles.length; i++) {
                    dataTransfer.items.add(newFiles[i]);
                }
                fileInput.files = dataTransfer.files;
                
                if (fileInput.files.length > 0) {
                    dropText.innerHTML = `<span style="color: #38BDF8; font-weight: bold;">${fileInput.files.length} photos selected so far</span>`;
                }
            }

            dropZone.addEventListener('click', () => fileInput.click());
            
            fileInput.addEventListener('change', (e) => {
                handleFiles(e.target.files);
            });

            dropZone.addEventListener('dragover', (e) => {
                e.preventDefault();
                dropZone.classList.add('dragover');
            });

            dropZone.addEventListener('dragleave', () => {
                dropZone.classList.remove('dragover');
            });

            dropZone.addEventListener('drop', (e) => {
                e.preventDefault();
                dropZone.classList.remove('dragover');
                if (e.dataTransfer.files.length > 0) {
                    handleFiles(e.dataTransfer.files);
                }
            });
        </script>
    </body>
    </html>
    '''

@app.route('/analyze', methods=['POST'])
def run_analysis():
    path = request.form.get('folder_path')
    uploaded_files = request.files.getlist('uploaded_images')
    
    target_directory = None
    
    if uploaded_files and uploaded_files[0].filename != '':
        temp_dir = tempfile.mkdtemp()
        for file in uploaded_files:
            if file and file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(temp_dir, filename))
        target_directory = temp_dir

    elif path and os.path.isdir(path):
        target_directory = path
        
    else:
        return "<h2 style='color: red; text-align: center;'>Error: Provide a folder path or upload images!</h2>"

    try:
        data = extract_all(target_directory)
        analysis_results = analyze(data)
        map_html = create_map(data)

        temp_map = folium.Map(location=[32.0, 34.8], zoom_start=8)
        timeline_html = create_timeline(data, m=temp_map)

        # Uses the global developer switch right here!
        yolo_data_results = process_image_folder(target_directory, smart_mode=DEV_SMART_MODE)

        final_report = create_report(
            images_data=data,
            map_html=map_html,
            timeline_html=timeline_html,
            analysis=analysis_results,
            yolo_data=yolo_data_results
        )
        return final_report

    except Exception as e:
        return f"<h2 style='color: red;'>An error occurred: {str(e)}</h2>"

if __name__ == '__main__':
    app.run(debug=True, port=5000)