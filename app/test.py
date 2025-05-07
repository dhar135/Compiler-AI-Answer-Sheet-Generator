import os
import sys
from dotenv import load_dotenv

# Add project root to the Python path
# os.path.dirname(__file__) gives the directory of the current script (app)
# os.path.join(os.path.dirname(__file__), '..') goes one level up to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.client.compiler_client import CompilerClient

def main():
    """
    Main function to initialize the client and process user input continuously.
    """
    load_dotenv()
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        print("Error: GEMINI_API_KEY not found in environment variables.")
        sys.exit(1)

    client = CompilerClient(api_key=gemini_api_key)

    print("AI Assistant initialized. Enter your source file below")

    user_input = input("Source File > ")

    if user_input:
        try:
            print("Source File Received. Processing answer sheet now...")
            response = client.ask_ai_for_answer_sheet(user_input)
            print(response)
            print("Answer Sheet Successfully Created!")
        except Exception as e:
            print(f" Error while processing answer sheet: + {e}")


if __name__ == "__main__":
    main()