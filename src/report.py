from datetime import datetime

def create_report(images_data, map_html, timeline_html, analysis):
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    insights_html = ""
    for insight in analysis.get("insights", []):
        insights_html += f"<li>{insight}</li>"
    
    cameras_html = ""
    for cam in analysis.get("unique_cameras", []):
        cameras_html += f"<span class='badge'>{cam}</span> "
    
    html = f"""
    <!DOCTYPE html>
    <html lang="en" dir="ltr">
    <head>
        <meta charset="UTF-8">
        <title>Image Intel Report</title>
        <style>
            body {{ font-family: Arial; max-width: 1200px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
            .header {{ background: #1B4F72; color: white; padding: 30px; border-radius: 10px; text-align: center; }}
            .section {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .stats {{ display: flex; gap: 20px; justify-content: center; }}
            .stat-card {{ background: #E8F4FD; padding: 15px 25px; border-radius: 8px; text-align: center; }}
            .stat-number {{ font-size: 2em; font-weight: bold; color: #1B4F72; }}
            .badge {{ background: #2E86AB; color: white; padding: 5px 10px; border-radius: 15px; margin: 3px; display: inline-block; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Image Intel Report</h1>
            <p>Created on {now}</p>
        </div>
        
        <div class="section">
            <h2>Summary</h2>
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{analysis.get('total_images', 0)}</div>
                    <div>Images</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{analysis.get('images_with_gps', 0)}</div>
                    <div>With GPS</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{len(analysis.get('unique_cameras', []))}</div>
                    <div>Devices</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>Key Insights</h2>
            <ul>{insights_html}</ul>
        </div>
        
        <div class="section">
            <h2>Map</h2>
            {map_html}
        </div>
        
        <div class="section">
            <h2>Timeline</h2>
            {timeline_html}
        </div>
        
        <div class="section">
            <h2>Devices</h2>
            {cameras_html}
        </div>
        
        <div style="text-align:center; color:#888; margin-top:30px;">
            Image Intel | Hackathon 2025
        </div>
    </body>
    </html>
    """
    return html

# if __name__ == "__main__":
#     from extractor import extract_all
#     from map_view import create_map
#     from timeline import create_timeline
#     from analyzer import analyze

#     path = r"C:\Users\yoelo\OneDrive\שולחן העבודה\end-project\image_intel_group3\images"
    
    
#     data = extract_all(path)
#     analysis_results = analyze(data)
#     map_str = create_map(data)

#     temp_map = folium.Map(location=[32.0, 34.8], zoom_start=8)
#     timeline_str = create_timeline(data, m=temp_map)

#     final_html = create_report(
#         images_data=data,
#         map_html=map_str,
#         timeline_html=timeline_str,
#         analysis=analysis_results
#     )

#     with open("test_report.html", "w", encoding="utf-8") as f:
#         f.write(final_html)

#     print("Process finished! Open 'test_report.html' to see the full result.")