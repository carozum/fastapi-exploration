from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

load_dotenv((find_dotenv()))
api_key = os.environ["OPENAI_API_KEY"]


# Initialize OpenAI client with your API key
client = OpenAI(
    api_key=api_key
)


# Initialize FastAPI client
app = FastAPI()


# Create class with pydantic BaseModel
class TranslationRequest(BaseModel):
    input_str: str


def translate_text(input_str):
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are an expert translator who translates text from english to french and only return translated text",
            },
            {"role": "user", "content": input_str},
        ],
    )

    return completion.choices[0].message.content


@app.post("/translate/")  # This line decorates 'translate' as a POST endpoint
async def translate(request: TranslationRequest):
    try:
        # Call your translation function
        translated_text = translate_text(request.input_str)
        return {"translated_text": translated_text}
    except Exception as e:
        # Handle exceptions or errors during translation
        raise HTTPException(status_code=500, detail=str(e))
