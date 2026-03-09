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

    
if __name__ == "__main__":
    images_data = extract_all(r"C:\Users\yoelo\OneDrive\שולחן העבודה\end-project\image_intel_group3\images")
    create_timeline(images_data=images_data)