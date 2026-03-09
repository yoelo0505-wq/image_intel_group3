from flask import Flask, request, render_template_string
import folium

# Importing your project modules
from extractor import extract_all
from map_view import create_map
from timeline import create_timeline
from analyzer import analyze
from report import create_report

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
        <head><title>Image Intel Tool</title></head>
        <body style="font-family: Arial; margin: 50px; text-align: center;">
            <h1>Image Intelligence Analyzer</h1>
            <p>Enter the full path to your image folder:</p>
            <form action="/analyze" method="post">
                <input type="text" name="folder_path" style="width: 400px; padding: 10px;" 
                       placeholder="C:\\Users\\Name\\Desktop\\images">
                <br><br>
                <input type="submit" value="Run Full Analysis" style="padding: 10px 20px; cursor: pointer;">
            </form>
        </body>
    </html>
    '''


@app.route('/analyze', methods=['POST'])
def run_analysis():
    
    path = request.form.get('folder_path')
    
    if not path:
        return "<h2>Error: Please provide a folder path!</h2>"

    try:
       
        data = extract_all(path)
    
        analysis_results = analyze(data)

        map_html = create_map(data)

        temp_map = folium.Map(location=[32.0, 34.8], zoom_start=8)
        timeline_html = create_timeline(data, m=temp_map)

        final_report = create_report(
            images_data=data,
            map_html=map_html,
            timeline_html=timeline_html,
            analysis=analysis_results
        )
        return final_report

    except Exception as e:
        return f"<h2>An error occurred: {str(e)}</h2>"

if __name__ == '__main__':
    app.run(debug=True, port=5000)