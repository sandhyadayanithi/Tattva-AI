import pytesseract
from PIL import Image
import os
import sys
import re
from dotenv import load_dotenv
from google import genai

class OCRService:
    def __init__(self, tesseract_path=None):
        """
        Initializes the OCR service.
        :param tesseract_path: Path to the tesseract executable. 
                               If None, it tries to find it in default Windows paths.
        """
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.genai_client = None
        if self.api_key:
            self.genai_client = genai.Client(api_key=self.api_key)
            
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        else:
            # Common Windows installation paths
            user_home = os.path.expanduser("~")
            possible_paths = [
                r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
                os.path.join(user_home, r'AppData\Local\Tesseract-OCR\tesseract.exe'),
            ]
            
            found = False
            for path in possible_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    found = True
                    break
            
            if not found:
                # If not found in common paths, assume it might be in the system PATH
                pytesseract.pytesseract.tesseract_cmd = 'tesseract'
        
        print(f"Using Tesseract at: {pytesseract.pytesseract.tesseract_cmd}")

    def clean_text(self, text):
        """
        Heuristic cleaning to remove noisy lines and garbage characters.
        """
        if not text:
            return ""
            
        # Remove common OCR garbage characters
        garbage_chars = ['é', '©', '®', '™', '§', '°', '·', '—', '—', '—', '|', '_']
        for char in garbage_chars:
            text = text.replace(char, ' ')
            
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            trimmed = line.strip()
            # Remove very short lines or lines that are just single words with symbols
            if len(trimmed) < 3:
                continue
            
            # Remove lines that are mostly special characters (more than 40% non-alphanumeric)
            # Include common Indian script ranges
            # \u0900-\u097F: Devanagari (Hindi, Marathi, etc.)
            # \u0B80-\u0BFF: Tamil
            # \u0C00-\u0C7F: Telugu
            # \u0980-\u09FF: Bengali
            alnum_regex = re.compile(r'[a-zA-Z0-9\u0900-\u097F\u0B80-\u0BFF\u0C00-\u0C7F\u0980-\u09FF]')
            alnum_count = len(alnum_regex.findall(trimmed))
            
            if len(trimmed) > 0 and alnum_count / len(trimmed) < 0.5:
                continue
                
            cleaned_lines.append(trimmed)
            
        # Join lines and remove multiple spaces
        result = '\n'.join(cleaned_lines)
        result = re.sub(r' +', ' ', result)
        return result.strip()

    def refine_text_with_llm(self, text):
        """
        Uses Gemini to denoise and refine OCR output.
        """
        if not self.genai_client or not text:
            return text
            
        prompt = (
            "Clean up and reconstruct this OCR text while PRESERVING ALL languages. "
            "Fix broken words and remove noise. "
            "Return ONLY the cleaned content:\n\n"
            f"{text}"
        )
        
        import time
        max_retries = 3
        retry_delay = 2 # Initial delay in seconds

        for attempt in range(max_retries):
            try:
                response = self.genai_client.models.generate_content(
                    model="gemini-1.5-flash-002",
                    contents=prompt
                )
                return response.text.strip()
            except Exception as e:
                if "429" in str(e) and attempt < max_retries - 1:
                    print(f"Quota exceeded (429) in OCR refinement. Retrying in {retry_delay}s... (Attempt {attempt + 1}/{max_retries})")
                    time.sleep(retry_delay)
                    retry_delay *= 2 # Exponential backoff
                else:
                    print(f"Error refining text with Gemini: {e}")
                    return text

    def extract_text(self, image_path, languages=['eng', 'hin', 'tam', 'tel', 'ben'], use_refinement=False):
        """
        Extracts and cleans text from an image.
        :param image_path: Path to the image file.
        :param languages: List of tesseract language codes.
        :param use_refinement: Whether to use LLM for refinement.
        :return: Extracted text as a string.
        """
        try:
            # Combine languages for tesseract (e.g., 'eng+hin+tam')
            lang_str = '+'.join(languages)
            
            # Open the image
            with Image.open(image_path) as img:
                # Perform OCR
                raw_text = pytesseract.image_to_string(img, lang=lang_str)
                
                # Step 1: Heuristic cleaning
                cleaned_text = self.clean_text(raw_text)
                
                # Step 2: LLM refinement
                if use_refinement and cleaned_text:
                    refined_text = self.refine_text_with_llm(cleaned_text)
                    return refined_text
                    
                return cleaned_text
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
