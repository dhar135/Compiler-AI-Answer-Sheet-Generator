import os
import sys  # Moved sys import to the top
import time
import pathlib
import mimetypes
from dotenv import load_dotenv
from google.genai import types

# Add project root to the Python path
# os.path.dirname(__file__) gives the directory of the current script (app)
# os.path.join(os.path.dirname(__file__), '..') goes one level up to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.client.compiler_client import CompilerClient  # This is now correctly placed after sys.path modification  # noqa: E402

# Configuration
SCREENSHOTS_DIR = pathlib.Path(project_root) / "project_files/screenshots/"
PROCESSED_DIR = SCREENSHOTS_DIR / "processed"
ANSWER_FILE = pathlib.Path(project_root) / "project_files/answers/individual_question_answers.txt"
POLL_INTERVAL_SECONDS = 5  # Check for new files every 5 seconds

def ensure_dirs_exist():
    """Ensure that the screenshots and processed directories exist."""
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def process_image(client: CompilerClient, image_path: pathlib.Path):
    """Processes a single image: sends to AI, appends answer, moves image."""
    print(f"Processing image: {image_path.name}...")
    try:
        image_bytes = image_path.read_bytes()
        mime_type, _ = mimetypes.guess_type(image_path)
        if not mime_type or not mime_type.startswith('image/'):
            print(f"Skipping non-image file: {image_path.name} (MIME type: {mime_type})")
            # Move to processed to avoid re-checking if it's not an image we can handle
            image_path.rename(PROCESSED_DIR / image_path.name)
            return

        image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
        
        response_text = client.ask_ai_for_answer(question=image_part)

        if response_text:
            with open(ANSWER_FILE, 'a') as f:
                f.write(f"Question (Image: {image_path.name}):\n")
                f.write(f"{response_text}\n\n")
            print(f"Answer for {image_path.name} appended to {ANSWER_FILE}")
            # Move processed image
            image_path.rename(PROCESSED_DIR / image_path.name)
            print(f"Moved {image_path.name} to {PROCESSED_DIR}")
        else:
            print(f"No response received for {image_path.name}")

    except Exception as e:
        print(f"Error processing image {image_path.name}: {e}")


def main():
    """
    Main function to initialize the client and monitor a folder for screenshots.
    """
    load_dotenv()
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        print("Error: GEMINI_API_KEY not found in environment variables.")
        sys.exit(1)

    ensure_dirs_exist()
    client = CompilerClient(api_key=gemini_api_key)

    print(f"AI Assistant initialized. Monitoring {SCREENSHOTS_DIR} for new screenshots...")
    print(f"Answers will be saved to: {ANSWER_FILE}")
    print(f"Processed images will be moved to: {PROCESSED_DIR}")

    try:
        while True:
            for item_path in SCREENSHOTS_DIR.iterdir():
                if item_path.is_file() and item_path.parent == SCREENSHOTS_DIR: # Ensure it's a file directly in SCREENSHOTS_DIR
                    # Check for common image extensions
                    if item_path.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']:
                        process_image(client, item_path)
                    else:
                        # Optionally handle or log non-image files if needed, or ignore
                        pass # print(f"Skipping non-image or already processed path: {item_path.name}")
            
            time.sleep(POLL_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    except Exception as e:
        print(f"An unexpected error occurred during monitoring: {e}")


if __name__ == "__main__":
    main()