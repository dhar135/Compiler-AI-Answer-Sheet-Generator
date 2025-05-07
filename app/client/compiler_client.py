from google import genai
from google.genai import types
import pathlib

class CompilerClient:

    system_instructions = """
    You are an world class expert in Compiler Construction and Design. You answer can answer any question about compilers thoughtfully.
    Please reference the given context of an compiler construction university course. 
    """

    prompt = """
    Answer all of the given questions. Be short and concise. Structure your output as Question Number, Question, Answer, short explanation (1-2 sentences). DO NOT OVER EXPLAIN YOUR ANSWER. It must be short and quick to look through"
    """
    textbook_path = pathlib.Path(
        "project_files/textbook.pdf")

    midterm_questions = pathlib.Path("project_files/midterm.pdf")
    syntax_analysis_path = pathlib.Path("project_files/Syntax Analysis.pdf")
    intermediate_code_path = pathlib.Path("project_files/IntermediateCode.pdf")
    activation_records_path = pathlib.Path("project_files/ActivationRecords.pdf")
    lexical_analysis_path = pathlib.Path("project_files/02_lexical_analysis.pdf")
    compiler_construction_path = pathlib.Path("project_files/01_compiler_construction.pdf")
    semantic_analysis_path = pathlib.Path("project_files/Module 4 - Semantic Analysis.pdf")

    context_list = [
        "Here is the course textbook:",
        types.Part.from_bytes(
            data=textbook_path.read_bytes(),
            mime_type='application/pdf'
        ),
        types.Part.from_bytes(
            data=midterm_questions.read_bytes(),
            mime_type='application/pdf'
        ),
        types.Part.from_bytes(
            data=syntax_analysis_path.read_bytes(),
            mime_type='application/pdf'
        ),
        types.Part.from_bytes(
            data=intermediate_code_path.read_bytes(),
            mime_type='application/pdf'
        ),
        types.Part.from_bytes(
            data=activation_records_path.read_bytes(),
            mime_type='application/pdf'
        ),
        types.Part.from_bytes(
            data=lexical_analysis_path.read_bytes(),
            mime_type='application/pdf'
        ),
        types.Part.from_bytes(
            data=compiler_construction_path.read_bytes(),
            mime_type='application/pdf'
        ),
        types.Part.from_bytes(
            data=semantic_analysis_path.read_bytes(),
            mime_type='application/pdf'
        ),
    ]

    def __init__(self, api_key):
        self.client = genai.Client(
            api_key=api_key
        )

    def ask_ai_for_answer(self, question: (str | types.Part)):  # Changed types.Image to types.Part
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash-preview-04-17",
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instructions
                ),
                contents=[  # This should now be fine as question can be str or Part
                    self.prompt,
                    question],
            )
        except Exception as e:
            raise Exception(f"Failed to generate content: {str(e)}")
        if response:
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
                    self.context_list,
                    self.prompt,
                    types.Part.from_bytes(
                        data=filepath.read_bytes(),
                        mime_type='application/pdf'
                    )
                ],
            )
        except Exception as e:
            raise Exception(f"Failed to generate content: {str(e)}")
        if response:
            # Corrected f-string to normal string
            with open("/Users/donovanharrison/Projects/answers/final_exam_ai_answer_sheet",
                      'w') as answer_file:
                print(response.text, file=answer_file)
            return answer_file.name
        return None