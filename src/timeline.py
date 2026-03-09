from folium.plugins import AntPath
from extractor import extract_all

def create_timeline(images_data: list[dict] ,m ):

     with_date = [img for img in images_data if img["datetime"]]

     srt_with_date = sorted(with_date , key= lambda x: x["datetime"])
     
     route_coordinates = [
          [img["latitude"],img["longitude"]]
           for img in srt_with_date
           if img["latitude"] is not None and img["longitude"] is not None
     ]
     if len(route_coordinates) > 1:
        AntPath(
            locations=route_coordinates,
            color="red",       
            weight=5,           
            dash_array=[10, 20]
        ).add_to(m)
    
     return m._repr_html_()

    
if __name__ == "__main__":
    import folium
    images_data = extract_all(r"C:\Users\yoelo\OneDrive\שולחן העבודה\end-project\image_intel_group3\images")
    # create_timeline(images_data=images_data,test_map)
    test_map = folium.Map(location=[32.0, 34.8], zoom_start=10)
    html_str = create_timeline(images_data=images_data, m=test_map)
   