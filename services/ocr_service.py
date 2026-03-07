import pytesseract
from PIL import Image
import os
import sys

class OCRService:
    def __init__(self, tesseract_path=None):
        """
        Initializes the OCR service.
        :param tesseract_path: Path to the tesseract executable. 
                               If None, it tries to find it in default Windows paths.
        """
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        else:
            # Common Windows installation paths
            possible_paths = [
                r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                r'C:\Users\\' + os.getlogin() + r'\AppData\Local\Tesseract-OCR\tesseract.exe'
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    break
        
        print(f"Using Tesseract at: {pytesseract.pytesseract.tesseract_cmd}")

    def extract_text(self, image_path, languages=['eng', 'hin', 'tam', 'tel', 'ben']):
        """
        Extracts text from an image.
        :param image_path: Path to the image file.
        :param languages: List of tesseract language codes.
        :return: Extracted text as a string.
        """
        try:
            # Combine languages for tesseract (e.g., 'eng+hin+tam')
            lang_str = '+'.join(languages)
            
            # Open the image
            with Image.open(image_path) as img:
                # Perform OCR
                text = pytesseract.image_to_string(img, lang=lang_str)
                return text.strip()
        except Exception as e:
            print(f"Error extracting text: {e}")
            return None

if __name__ == "__main__":
    # For standalone testing
    if len(sys.argv) < 2:
        print("Usage: python ocr_service.py <image_path> [tesseract_exe_path]")
        sys.exit(1)
        
    img_path = sys.argv[1]
    
    # Handle paths with spaces if not quoted by joining remaining args
    tess_path = None
    if len(sys.argv) > 2:
        tess_path = " ".join(sys.argv[2:])
        # If it's a directory, point to the executable inside
        if os.path.isdir(tess_path):
            tess_path = os.path.join(tess_path, "tesseract.exe")
        # Ensure it has .exe extension on Windows if provided manually
        if os.name == 'nt' and not tess_path.lower().endswith('.exe'):
            if os.path.exists(tess_path + ".exe"):
                tess_path += ".exe"
    
    if not os.path.exists(img_path):
        print(f"Error: Image file not found at {img_path}")
        sys.exit(1)
        
    ocr = OCRService(tess_path)
    print(f"Extracting text from: {img_path}...")
    
    extracted = ocr.extract_text(img_path)
    
    if extracted:
        print("\n--- Extracted Text ---")
        print(extracted)
        print("----------------------")
    else:
        print("No text extracted or an error occurred.")
        print("Tip: Make sure Tesseract is installed and the path is correct.")
        print("If you haven't, download it from: https://github.com/UB-Mannheim/tesseract/wiki")
