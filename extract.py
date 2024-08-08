import openai
from PIL import Image
import pytesseract
import json
import os
import re

# Set your OpenAI API key
openai.api_key = 'openai-api-key'

def extract_text_from_image(image_path):
    # Open an image file
    with Image.open(image_path) as img:
        # Use pytesseract to do OCR on the image
        text = pytesseract.image_to_string(img)
    return text

def call_openai_api(text):
    prompt = f"""You will be provided with text extracted from an image. 
    Your task is to extract specific betting details and return them in valid JSON format. 
    Do not include any additional text, and ensure the JSON is correctly formatted.

    The output should have the following structure:

    {{
        "Bet Status": "<status>",
        "Amount wagered": <amount_wagered>,
        "Amount won": <amount_won>,
        "Players": {
            {"player1": "<player_name>", "metric": "<metric>", "over_under": "<over/under>", "line": "<line>"},
            {"player2": "<player_name>", "metric": "<metric>", "over_under": "<over/under>", "line": "<line>"},
            ...
        }
    }}

    Here is the text:
    {text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that extracts betting details from text."},
            {"role": "user", "content": prompt}
        ]
    )

    # Print raw response for debugging
    raw_response = response['choices'][0]['message']['content'].strip()
    print(f"Raw Response: {raw_response}")

    return raw_response

def parse_extracted_details(extracted_details):
    try:
        # Attempt to load JSON directly
        details = json.loads(extracted_details)
    except json.JSONDecodeError as e:
        print(f"JSON decoding error: {e}")
        # Attempt to correct common issues, e.g., missing commas, etc.
        corrected_details = re.sub(r'(?<=\w)\s*\n\s*(?=\w)', ',\n', extracted_details)
        try:
            details = json.loads(corrected_details)
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON after correction. Error: {e}")
            # Log the error for debugging
            with open('failed_response_log.txt', 'a') as log_file:
                log_file.write(f"Failed JSON:\n{extracted_details}\n\n")
            raise ValueError("Failed to decode JSON response from OpenAI.")
    return details

def save_to_json(all_details, json_path):
    with open(json_path, 'w') as json_file:
        json.dump(all_details, json_file, indent=4)

def process_images_in_folder(images_folder, output_json_path):
    all_details = []
    for filename in os.listdir(images_folder):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".PNG"):
            image_path = os.path.join(images_folder, filename)
            text = extract_text_from_image(image_path)
            extracted_details = call_openai_api(text)
            try:
                details = parse_extracted_details(extracted_details)
                all_details.append(details)
            except ValueError:
                print(f"Skipping file due to JSON decoding error: {filename}")
    save_to_json(all_details, output_json_path)
    print(f"Extracted Bet Details saved to {output_json_path}.")


if __name__ == "__main__":
    images_folder = 'input_screenshots'
    output_json_path = 'output_json/cumulative_output.json'
    
    # Create output_json folder if it doesn't exist
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)

    process_images_in_folder(images_folder, output_json_path)
