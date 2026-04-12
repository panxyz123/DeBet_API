import json
import re
from openai import OpenAI
from anthropic import Anthropic
# import google.generativeai as genai
from .prompt import SYSTEM_PROMPT

class LLMManager:
    def __init__(self, keys: dict):
        self.openai_client = OpenAI(api_key=keys.get("openai"))
        self.anthropic_client = Anthropic(api_key=keys.get("anthropic"))
        # genai.configure(api_key=keys.get("google"))
        # self.gemini_model = genai.GenerativeModel('gemini-1.5-pro')

    def call_openai(self, text: str):
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

    def call_anthropic(self, text: str):
        response = self.anthropic_client.messages.create(
            model="claude-opus-4-6", 
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": text}]
        )
        
        raw_text = response.content[0].text

        try:
            json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                print(f"Raw response: {raw_text}")
                raise ValueError("No JSON object found in response")
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e} | Raw Text: {raw_text}")
            raise

    # def call_gemini(self, text: str):
    #     prompt = f"{SYSTEM_PROMPT}\n\nArgument to analyze:\n{text}"
    #     response = self.gemini_model.generate_content(
    #         prompt,
    #         generation_config={"response_mime_type": "application/json"}
    #     )
    #     return json.loads(response.text)