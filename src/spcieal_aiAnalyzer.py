import os
from ultralytics import YOLO

# Load the AI model
model = YOLO('yolov8n.pt')

def count_objects(image_path):
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

def process_image_folder(folder_path):
    all_images_data = []
    
    # os.walk goes through the main folder AND all sub-folders!
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            # Added .webp just in case you have modern image formats
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                full_path = os.path.join(root, filename)
                
                # Scan the image
                image_data = count_objects(full_path)
                
                # We only add it to the report if the AI actually found something
                if image_data: 
                    image_result = {filename: image_data}
                    all_images_data.append(image_result)
                
    return all_images_data