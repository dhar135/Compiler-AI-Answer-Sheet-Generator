from google import genai
from google.genai import types
import pathlib

class CompilerClient:

    system_instructions = """
    You are an world class expert in Compiler Construction and Design. You answer can answer any question about compilers thoughtfully.
    """

    prompt = """
    Answer all of the given questions. Be short and concise. Structure your output as Question Number, Question, Answer, short explanation (1-2 sentences)."
    """

    def __init__(self, api_key):
        self.client = genai.Client(
            api_key=api_key
        )

    def ask_ai_for_answer(self, question: (str | types.Image)):
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-preview-04-17",
                config=types.GenerateContentConfig(
                    system_instruction = self.system_instructions
                ),
                contents=[
                    self.prompt,
                    question],
            )
        except Exception as e:
            raise Exception(f"Failed to generate content: {str(e)}")
        if response:
            with open(f"/Users/donovanharrison/Projects/answers/answer_{question[0:5]}" , 'w') as answer_file:
                print(response.text, file=answer_file)

            return response.text
        return None

    def ask_ai_for_answer_sheet(self, question_sheet_path: str) -> str | None:
        if not question_sheet_path:
            print("please print a valid string url.")
        try:
            filepath = pathlib.Path(question_sheet_path)
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-preview-04-17",
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instructions
                ),
                contents=[
                    self.prompt,
                    types.Part.from_bytes(
                        data=filepath.read_bytes(),
                        mime_type='application/pdf'
                    )],
            )
        except Exception as e:
            raise Exception(f"Failed to generate content: {str(e)}")
        if response:
            with open(f"/Users/donovanharrison/Projects/answers/final_exam_ai_answer_sheet",
                      'w') as answer_file:
                print(response.text, file=answer_file)
            return answer_file.name
        return None
