# Betting Details Extraction from Images

This Python script extracts betting details from images using Optical Character Recognition (OCR) and the OpenAI API. It processes images in a specified folder, extracts text from them, calls the OpenAI API to extract structured betting details, and saves the results in a JSON file.

## Requirements

- Python 3.x
- `openai` library
- `Pillow` library
- `pytesseract` library
- `Tesseract-OCR` executable

You can install the necessary Python libraries using pip:

```bash
pip install openai pillow pytesseract
```

You also need to install Tesseract-OCR. Follow the installation instructions for your operating system.

## Confirguration

1.	Set your OpenAI API key: Replace 'your_openai_api_key' in the script with your actual OpenAI API key.
2.	Image Folder: Place the images you want to process in a folder named images (you can change this in the script if desired).
3.	Output JSON Path: The results will be saved to a file named cumulative_output.json in the output_json folder. The folder will be created if it does not exist.

## Usage

Run the script from the command line:

```bash
python extract.py
```

## Script Details

•	extract_text_from_image(image_path): Extracts text from an image using pytesseract.
•	call_openai_api(text): Sends the extracted text to the OpenAI API to extract structured betting details.
•	parse_extracted_details(extracted_details): Parses the JSON response from the OpenAI API. Attempts to correct JSON formatting issues if they occur.
•	save_to_json(all_details, json_path): Saves the extracted betting details to a JSON file.
•	process_images_in_folder(images_folder, output_json_path): Processes all images in the specified folder, extracts details, and saves them to the output JSON file.

## Troubleshooting
•	Ensure Tesseract-OCR is correctly installed and accessible in your system PATH.
•	Verify your OpenAI API key is valid and has the necessary permissions.
•	Check for any errors in the console output for debugging purposes.
