from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
import os

"""
extractor.py - שליפת EXIF מתמונות
צוות 1, זוג A

ראו docs/api_contract.md לפורמט המדויק של הפלט.

"""


def has_gps(data: dict):
    lat = latitude(data)
    lon = longitude(data)

    if lat is not None and lon is not None:
        return True
    else:
        return False


def latitude(data: dict):
    gps = data.get("GPSInfo")

    if gps:
        my_tuple = gps.get(2)
        ref = gps.get(1)

        if my_tuple:
            decimal_value = convert_to_decimal(my_tuple)

            if ref == "S":
                return -decimal_value
            return decimal_value
    return None


def longitude(data: dict):
    gps = data.get("GPSInfo")

    if gps:
        my_tuple = gps.get(4)
        ref = gps.get(3)

        if my_tuple:
            decimal_value = convert_to_decimal(my_tuple)

            if ref == "W":
                return -decimal_value
            return decimal_value
    return None


def datatime(data: dict):
    return data.get("DateTimeOriginal")


def camera_make(data: dict):
    make = data.get("Make")
    if isinstance(make,str):
        return make.strip().replace("\x00","")
    return make

def convert_to_decimal(gps_tup):
    degrees = float(gps_tup[0])
    minutes = float(gps_tup[1])
    seconds = float(gps_tup[2])

    result = degrees + (minutes / 60) + (seconds / 3600)
    return round(result,6)


def camera_model(data: dict):
    model = data.get("Model")
    if isinstance(model,str):
        return model.strip().replace("\x00","")

    return model

def extract_metadata(image_path):
    """
    שולף EXIF מתמונה בודדת.

    Args:
        image_path: נתיב לקובץ תמונה

    Returns:
        dict עם: filename, datetime, latitude, longitude,
              camera_make, camera_model, has_gps
    """
    path = Path(image_path)

    # תיקון: טיפול בתמונה בלי EXIF - בלי זה, exif.items() נופל עם AttributeError
    try:
        img = Image.open(image_path)
        exif = img._getexif()
    except Exception:
        exif = None

    if exif is None:
        return {
            "filename": path.name,
            "datetime": None,
            "latitude": None,
            "longitude": None,
            "camera_make": None,
            "camera_model": None,
            "has_gps": False
        }

    data = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        data[tag] = value

    # תיקון: הוסר print(data) שהיה כאן - הדפיס את כל ה-EXIF הגולמי על כל תמונה

    exif_dict = {
        "filename": path.name,
        "datetime": datatime(data),
        "latitude": latitude(data),
        "longitude": longitude(data),
        "camera_make": camera_make(data),
        "camera_model": camera_model(data),
        "has_gps": has_gps(data)
    }
    return exif_dict


def extract_all(folder_path):
    """
    שולף EXIF מכל התמונות בתיקייה.

    Args:
        folder_path: נתיב לתיקייה

    Returns:
        list של dicts (כמו extract_metadata)
    """

    exif_list = []
    images_types = {".jpg",".jpeg",".png",".webp"}
    for img_path in Path(folder_path).rglob("*"):
        if img_path.suffix.lower() in images_types:
            result = extract_metadata(img_path)
            exif_list.append(result)

    return exif_list
    

