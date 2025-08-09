import os
from dotenv import load_dotenv
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig


load_dotenv()
# gemini_api_key set
gemini_api_key = os.getenv("GEMINI_API_KEY")

#Check the gemini API key If not then raise error
if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")

external_client = AsyncOpenAI(
        api_key = gemini_api_key,
        base_url = "https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
        model="gemini-2.5-flash",
        openai_client=external_client,
       

)

google_gemini_config = RunConfig(
        model =model,
        model_provider = external_client,
)