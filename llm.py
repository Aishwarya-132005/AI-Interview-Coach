import json
import os  # just to  access GEMINI API key we use it 
from dotenv import load_dotenv
from google import genai  #to access tools to communicate with gemini

#to load the api key
load_dotenv()

#to connect gemini api key
client= genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

#to choose a model
MODEL = "gemini-3.5-flash-lite"

#define a funtion to send a prompt
def ask_ai(prompt):
    response=client.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    return response.text

#To create json response function
def ask_ai_json(prompt):
    response=client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config={
            "response_mime_type":"application/json"
        }
    )
    return json.loads(response.text)