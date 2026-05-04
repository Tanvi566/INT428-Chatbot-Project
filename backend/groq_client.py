import asyncio
import httpx
import os

# Groq uses an OpenAI-compatible chat completions endpoint
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

async def call_groq_api(messages, model="llama-3.3-70b-versatile", api_key=""):
    """
    Calls the Groq API with provided messages and model.
    Implements exponential backoff for reliability.
    """
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 4096
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Exponential backoff retry logic (1s, 2s, 4s, 8s, 16s)
    for delay in [1, 2, 4, 8, 16]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    GROQ_URL, 
                    json=payload, 
                    headers=headers, 
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result['choices'][0]['message']['content']
                
                # If rate limited (429), trigger retry logic
                if response.status_code == 429:
                    await asyncio.sleep(delay)
                    continue
                    
                response.raise_for_status()
        except Exception:
            await asyncio.sleep(delay)
            
    return "Error: The academic server (Groq) is currently unavailable or the rate limit was exceeded."