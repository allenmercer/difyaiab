from openai import AsyncAzureOpenAI
from app.core.config import settings

# Define model parameters from environment variables
API_KEY = settings.LLM_API_KEY
MODEL_NAME = settings.LLM_MODEL
ENDPOINT = settings.LLM_URL
LLM_API_VERSION = settings.LLM_API_VERSION


async def call_llm_ws(
    system_message: str, user_prompt: str, websocket, temperature=0.7
):
    try:
        client = AsyncAzureOpenAI(
            api_key=API_KEY, azure_endpoint=ENDPOINT, api_version=LLM_API_VERSION
        )

        response = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt},
            ],
            stream=True,
            model=MODEL_NAME,
            temperature=temperature,
        )

        # Stream tokens immediately.
        async for chunk in response:
            if chunk.choices and len(chunk.choices) > 0:
                token = chunk.choices[0].delta.content if chunk.choices[0].delta else ""
                if token:
                    await websocket.send_text(token)

    except Exception as e:
        await websocket.send_text(f"Error generating response from llm: {str(e)}")


async def generic_llm_call(
    system_message: str, user_prompt: str, temperature=0.7
) -> bool:
    try:
        client = AsyncAzureOpenAI(
            api_key=API_KEY, azure_endpoint=ENDPOINT, api_version=LLM_API_VERSION
        )
        response = await client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt},
            ],
            model=MODEL_NAME,
            temperature=temperature,
        )
        return response.choices[0].message.content.strip().lower()
    except Exception:
        pass
