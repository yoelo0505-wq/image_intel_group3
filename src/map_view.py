"""
map_view.py - יצירת מפה אינטראקטיבית
צוות 1, זוג B

ראו docs/api_contract.md לפורמט הקלט והפלט.

=== תיקונים ===
1. חישוב מרכז המפה - היה עובר על images_data (כולל תמונות בלי GPS) במקום gps_image, נופל עם None
2. הסרת CustomIcon שלא עובד (filename זה לא נתיב שהדפדפן מכיר)
3. הסרת m.save() - לפי API contract צריך להחזיר HTML string, לא לשמור קובץ
4. הסרת fake_data מגוף הקובץ - הועבר ל-if __name__
5. תיקון color_index - היה מתקדם על כל תמונה במקום רק על מכשיר חדש
6. הוספת מקרא מכשירים
"""

import folium
from extractor import extract_all
from timeline import create_timeline

# def sort_by_time(arr):
#     pass


def create_map(images_data):
    """
    יוצר מפה אינטראקטיבית עם כל המיקומים.

    Args:
        images_data: רשימת מילונים מ-extract_all

    Returns:
        string של HTML (המפה)
    """
    gps_images = [img for img in images_data if img["has_gps"]]
    
    if not gps_images:
        return "<h2>No GPS data found</h2>"
    
    
    center_lat = sum(img["latitude"] for img in gps_images) / len(gps_images)
    center_lon = sum(img["longitude"] for img in gps_images) / len(gps_images)
    
    m = folium.Map(location=[center_lat, center_lon], zoom_start=8)
    available_colors = ['blue', 'red','green', 'purple', 'orange', 'darkred', 'pink', 'cadetblue', 'gray', 'black']
    devices_list = [img["camera_model"] for img in gps_images if img["camera_model"]]
    c_d_dict = {}
    index = 0
    for device in devices_list:
        if device not in c_d_dict:
            c_d_dict[device] = available_colors[index]
            index+=1
    
    for img in gps_images:
        if img["camera_model"]:
            device_color = c_d_dict.get(img["camera_model"])
            costum_icon = folium.Icon(color=device_color,icon='camera', prefix='fa')
        else:
            costum_icon = folium.Icon(color="gray",icon='camera', prefix='fa')
        folium.Marker(
            location=[img["latitude"], img["longitude"]],
            popup=f"{img['filename']}<br>{img['datetime']}<br>{img['camera_model']}",
            icon= costum_icon
        ).add_to(m)
    create_timeline(images_data=images_data,m=m)
    
    return m._repr_html_()


