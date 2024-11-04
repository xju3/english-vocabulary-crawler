import cv2
import pytesseract
from pytesseract import Output
import subprocess


from common.logger import logger

# Path to the Tesseract executable (modify this path if necessary)
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'

def extract_single_frame(video_file, output_image_name, time="00:00:01"):
    command = [
        "ffmpeg",
        "-ss", time,
        "-i", video_file,
        "-frames:v", "1",
        '-y',
        output_image_name
    ]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def extract_largest_font_words(image_path):
    logger.debug(image_path)
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to RGB
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Perform OCR on the image
    data = pytesseract.image_to_data(rgb_image, output_type=Output.DICT)

    # Initialize variables to find the largest font size
    max_font_size = 0
    largest_words = []

    # Iterate through the OCR results
    for i in range(len(data['text'])):
        if int(data['conf'][i]) > 0:  # Check if confidence is greater than 0
            font_size = int(data['height'][i])  # Use height as an indicator of font size
            if font_size > max_font_size:
                max_font_size = font_size
                largest_words = [data['text'][i]]  # Start a new list for largest font
            elif font_size == max_font_size:
                largest_words.append(data['text'][i])  # Append if same font size

    return largest_words