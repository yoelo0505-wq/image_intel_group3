import folium

def create_report(images_data: list[dict], map_html: str, timeline_html: str, analysis: dict) -> str:
    insight_items = ""
    for insight in analysis["insights"]:
        insight_items += f"<li>{insight}</li>"

    report_html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>Intelligence Report</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background-color: #f0f2f5; }}
            .report-container {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); max-width: 1200px; margin: auto; }}
            h1 {{ color: #1a73e8; border-bottom: 2px solid #1a73e8; padding-bottom: 10px; }}
            h2 {{ color: #3c4043; margin-top: 30px; }}
            .stats-box {{ display: flex; gap: 20px; margin-bottom: 20px; }}
            .stat-card {{ background: #e8f0fe; padding: 15px; border-radius: 8px; flex: 1; text-align: center; }}
            .map-section {{ margin-top: 30px; border: 1px solid #ddd; border-radius: 8px; overflow: hidden; height: 500px; }}
            ul {{ line-height: 1.6; }}
        </style>
    </head>
    <body>
        <div class="report-container">
            <h1>Digital Forensic Intelligence Report</h1>
            
            <div class="stats-box">
                <div class="stat-card"><strong>Total Images:</strong><br>{analysis['total_images']}</div>
                <div class="stat-card"><strong>GPS Located:</strong><br>{analysis['images_with_gps']}</div>
                <div class="stat-card"><strong>Start:</strong><br>{analysis['date_range']['start']}</div>
                <div class="stat-card"><strong>End:</strong><br>{analysis['date_range']['end']}</div>
            </div>

            <h2>Investigation Insights</h2>
            <ul>
                {insight_items}
            </ul>

            <h2>Interactive Location Map</h2>
            <div class="map-section">
                {map_html}
            </div>

            <h2>Movement Timeline</h2>
            <div class="map-section">
                {timeline_html}
            </div>
        </div>
    </body>
    </html>
    """
    return report_html

if __name__ == "__main__":
    
    from extractor import extract_all
    from map_view import create_map
    from timeline import create_timeline
    from analyzer import analyze

    path = r"C:\Users\yoelo\OneDrive\שולחן העבודה\end-project\image_intel_group3\images"

    
    data = extract_all(path)

   
    analysis_results = analyze(data)

    map_str = create_map(data)

    temp_map = folium.Map(location=[32.0, 34.8], zoom_start=8)
    timeline_str = create_timeline(data, m=temp_map)

    final_html = create_report(
        images_data=data,
        map_html=map_str,
        timeline_html=timeline_str,
        analysis=analysis_results
    )

    with open("test_report.html", "w", encoding="utf-8") as f:
        f.write(final_html)

    print("Process finished! Open 'test_report.html' to see the full result.")