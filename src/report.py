from datetime import datetime

def create_report(images_data, map_html, timeline_html, analysis, yolo_data=None):
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    insights_html = ""
    for insight in analysis.get("insights", []):
        insights_html += f"<li>{insight}</li>"
    
    cameras_html = ""
    for cam in analysis.get("unique_cameras", []):
        cameras_html += f"<span class='badge'>{cam}</span> "
        
    # --- NEW: Build the YOLO AI Table ---
    yolo_table_html = ""
    if yolo_data:
        yolo_table_html = """
        <div class="section">
            <h2>AI Object Detection Intelligence</h2>
            <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
                <thead>
                    <tr style="background-color: #1B4F72; color: white; text-align: left;">
                        <th style="padding: 12px; border-bottom: 2px solid #ddd;">Image File</th>
                        <th style="padding: 12px; border-bottom: 2px solid #ddd;">Detected Objects (אובייקטים שזוהו)</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        # Iterate through the list of dictionaries
        for image_dict in yolo_data:
            for img_name, objects in image_dict.items():
                
                # Format the objects as nice green badges
                objects_list = []
                for obj_name, count in objects.items():
                    badge = f"<span class='badge' style='background-color:#28B463;'>{obj_name}: {count}</span>"
                    objects_list.append(badge)
                    
                objects_str = " ".join(objects_list)
                
                # If the AI found nothing, show a message
                if not objects_str:
                    objects_str = "<span style='color: #888; font-style: italic;'>No objects found</span>"
                    
                # Add the row to our HTML table
                yolo_table_html += f"""
                <tr style="border-bottom: 1px solid #ddd; background-color: #fafafa;">
                    <td style="padding: 12px; font-weight: bold; color: #1B4F72;">{img_name}</td>
                    <td style="padding: 12px;">{objects_str}</td>
                </tr>
                """
                
        # Close the table and section tags
        yolo_table_html += """
                </tbody>
            </table>
        </div>
        """
    
    # --- Main HTML Assembly ---
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
            <h2>Map with timeline and devices</h2>
            {map_html}
        </div>
        
        
        <div class="section">
            <h2>Devices</h2>
            {cameras_html}
        </div>
        
        {yolo_table_html}
        
        <div style="text-align:center; color:#888; margin-top:30px;">
            Image Intel | Hackathon 2025
        </div>
    </body>
    </html>
    """
    return html