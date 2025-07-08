import json
import aiohttp
import asyncio
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field, asdict

# --------------------- Data Models ---------------------

@dataclass
class ChatMessage:
    role: str
    content: str

@dataclass
class SuccessResponseDataFormat:
    total_llm_calls: int
    total_tokens: int
    total_input_tokens: int
    total_output_tokens: int
    final_llm_response: Dict[str, Any]
    llm_responses_arr: List[Dict[str, Any]]
    messages: List[str]
    output_type: str

@dataclass
class LlmResponseStruct:
    Data: Optional[Dict[str, Any]]
    Error: Optional[Union[Exception, str, Dict[str, Any]]]
    Status: bool

# --------------------- Gemini Processor ---------------------

async def gemini_processor(data: Dict[str, Any]) -> LlmResponseStruct:
    print("DEBUG: Starting gemini_processor")
    try:
        server_creds = data.get("selected_server_credentials", {}).get("MCP-ABSTRACT", {})
        abstract_api_key = server_creds.get("ABSTRACT_API_KEY")

        client_details = data.get("client_details", {})
        gemini_api_key = client_details.get("api_key", "")
        temperature = client_details.get("temperature", 0.1)
        max_tokens = client_details.get("max_token", 1000)
        input_text = client_details.get("input", "")
        prompt = client_details.get("prompt", "")
        input_type = client_details.get("input_type", "text")
        chat_model = client_details.get("chat_model", "gemini-1.5-pro-latest")
        chat_history_raw = client_details.get("chat_history", [])

        if not gemini_api_key:
            return LlmResponseStruct(Data=None, Error="Missing Gemini API Key", Status=False)
        if not input_text and not prompt:
            return LlmResponseStruct(Data=None, Error="Missing input text or prompt", Status=False)

        chat_history = [ChatMessage(**msg) for msg in chat_history_raw]
        chat_contents = [{"role": msg.role, "parts": [{"text": msg.content}]} for msg in chat_history]
        chat_contents.append({"role": "user", "parts": [{"text": input_text}]})

        payload = {
            "contents": chat_contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens
            },
            "system_instruction": {
                "parts": [{"text": prompt}]
            }
        }

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{chat_model}:generateContent?key={gemini_api_key}"
        headers = {'Content-Type': 'application/json'}

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload, timeout=60) as response:
                response.raise_for_status()
                response_data = await response.json()

        candidates = response_data.get("candidates", [])
        parts = candidates[0].get("content", {}).get("parts", []) if candidates else []
        message_text = parts[0].get("text", "") if parts else "No response"
        usage = response_data.get("usageMetadata", {})

        success_data = SuccessResponseDataFormat(
            total_llm_calls=1,
            total_tokens=usage.get("totalTokenCount", 0),
            total_input_tokens=usage.get("promptTokenCount", 0),
            total_output_tokens=usage.get("candidatesTokenCount", 0),
            final_llm_response=response_data,
            llm_responses_arr=[response_data],
            messages=[message_text],
            output_type="text"
        )

        response = LlmResponseStruct(Data=asdict(success_data), Error=None, Status=True)
        print("DEBUG: Returning LlmResponseStruct:", response)
        print("DEBUG: Response type:", type(response))
        return response

    except aiohttp.ClientError as req_err:
        error_response = LlmResponseStruct(Data=None, Error=f"HTTP error: {str(req_err)}", Status=False)
        print("DEBUG: Returning error LlmResponseStruct:", error_response)
        return error_response

    except Exception as err:
        return LlmResponseStruct(Data=None, Error=f"Unhandled error: {str(err)}", Status=False)

# --------------------- Entry Point ---------------------

if __name__ == "__main__":
    # Sample data to run
    input_data = {
        "selected_server_credentials": {
            "MCP-ABSTRACT": {
                "ABSTRACT_API_KEY": "d54448a5244b4ef6b025f5616da3a116"
            }
        },
        "client_details": {
            "api_key": "AIzaSyAMYj9cse5pwNNurSZj_L0UdPYJFRG68u9",
            "temperature": 0.1,
            "max_token": 1000,
            "input": "search for documents related to 'machine learning' in the pinecone index",
            "input_type": "text",
            "prompt": "you are a helpful assistant",
            "chat_model": "gemini-1.5-pro-latest",
            "chat_history": [
                {
                    "role": "user",
                    "content": "Hi"
                }
            ]
        },
        "selected_client": "MCP_CLIENT_GEMINI",
        "selected_servers": [
            "MCP-PINECONE-DEV"
        ]
    }

    result = asyncio.run(gemini_processor(input_data))
    print(json.dumps(result, indent=2))
