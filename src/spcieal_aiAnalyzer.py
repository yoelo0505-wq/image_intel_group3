import os
import json
from PIL import Image

# We hold the models here so they only load once!
yolo_model = None
gemini_client = None

def get_yolo_model():
    global yolo_model
    if yolo_model is None:
        from ultralytics import YOLO
        yolo_model = YOLO('yolov8n.pt') 
    return yolo_model

def get_gemini_client():
    global gemini_client
    if gemini_client is None:
        from google import genai
       
        gemini_client = genai.Client(api_key="AIzaSyArpBRJC7tOQ649_GJPv_FUcL5GYbDUSJs")
    return gemini_client

def count_objects_yolo(image_path):
    model = get_yolo_model()
    results = model(image_path)
    item_counts = {}
    category_names = results[0].names
    
    for item in results[0].boxes:
        class_id = int(item.cls[0])
        item_name = category_names[class_id]
        
        if item_name in item_counts:
            item_counts[item_name] += 1
        else:
            item_counts[item_name] = 1
            
    return item_counts

def count_objects_gemini(image_path):
    try:
        client = get_gemini_client()
        img = Image.open(image_path)
        
        prompt = """
        Look carefully at this image. Find and count the main objects you see. 
        Return ONLY a valid JSON dictionary where the keys are the object names in lowercase 
        and the values are the numbers. Do not write any other text.
        Example format: {"pool": 1, "cookie": 3, "car": 2}
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt, img]
        )
        
        clean_text = response.text.replace('```json', '').replace('```', '').strip()
        item_counts = json.loads(clean_text)
        return item_counts
        
    except Exception as e:
        print(f"Error checking {image_path}: {e}")
        return {}

def process_image_folder(folder_path, smart_mode=False):
    all_images_data = []
    
    print(f"\n--- Starting Analysis! Smart Mode is: {smart_mode} ---")
    
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                full_path = os.path.join(root, filename)
                
                if smart_mode:
                    print(f"Sending {filename} to Gemini (Web AI)...")
                    image_data = count_objects_gemini(full_path)
                else:
                    print(f"Scanning {filename} with YOLO (Local AI)...")
                    image_data = count_objects_yolo(full_path)
                
                if image_data: 
                    image_result = {filename: image_data}
                    all_images_data.append(image_result)
                    print(f"Success! Found: {image_data}")
                    
    return all_images_data