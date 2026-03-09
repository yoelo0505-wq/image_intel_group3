from extractor import extract_all

def analyze(images_data : list[dict]) -> dict:
    total_images = len(images_data)
    image_with_gps = len([img for img in images_data if img["has_gps"]])
    uniq_camers_s = set([img["camera_model"] for img in images_data if img["camera_model"]])
    uniq_camera_models = list(uniq_camers_s)
    with_date = [img for img in images_data if img["datetime"]]
    if with_date:
        start_date = min(map(lambda x: x["datetime"],with_date))
        end_date = max(map(lambda x: x["datetime"],with_date))
    else:
        start_date = end_date = "N/A"
    insights = []
    
    insights.append(f"Found {len(uniq_camera_models)} different camera model(s)")

    if len(with_date) > 1:
        
        srt = sorted(with_date, key=lambda x: x["datetime"])
        for i in range(len(srt) - 1):
            if srt[i]["camera_model"] != srt[i+1]["camera_model"]:
                switch_date = srt[i+1]["datetime"][:10] 
                insights.append(f"The agent swiched device on :{switch_date}")
        
    if image_with_gps > 0:
        locations = []
        for img in images_data:
            if img["has_gps"]:
                loc_key = (round(img["latitude"], 1), round(img["longitude"], 1))
                locations.append(loc_key)
            
        if locations:
            most_common_loc = max(set(locations), key=locations.count)
            insights.append(f"Image concentration in coordinates {most_common_loc}")
        
    analyze_dict ={

        "total_images": total_images,
        "images_with_gps": image_with_gps,
        "unique_cameras": uniq_camera_models,
        "date_range": {"start": start_date, "end": end_date},
        "insights": insights
    }

    return analyze_dict
          

if __name__ == "__main__":
    images_data = extract_all(r"C:\Users\yoelo\OneDrive\שולחן העבודה\end-project\image_intel_group3\images")
    print(analyze(images_data))