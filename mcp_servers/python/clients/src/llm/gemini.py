import requests
import json
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

def gemini_processor(data: Dict[str, Any]) -> LlmResponseStruct:
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
        if not abstract_api_key:
            return LlmResponseStruct(Data=None, Error="Missing Abstract API Key", Status=False)
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
            },
            "tools": [{
                "functionDeclarations": [
                    {
                        "name": "verify_email",
                        "description": "Verifies if an email address is valid using Abstract API",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "email": {"type": "string", "description": "Email address to validate"}
                            },
                            "required": ["email"]
                        }
                    },
                    {
                        "name": "verify_phone",
                        "description": "Validates phone numbers using Abstract API",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "phone": {"type": "string", "description": "Phone number to validate"}
                            },
                            "required": ["phone"]
                        }
                    },
                    {
                        "name": "check_email_reputation",
                        "description": "Checks email reputation using Abstract API",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "email": {"type": "string", "description": "Email to assess for risk and quality"}
                            },
                            "required": ["email"]
                        }
                    }
                ]
            }]
        }

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{chat_model}:generateContent?key={gemini_api_key}"
        headers = {'Content-Type': 'application/json'}

        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        response_data = response.json()

        candidates = response_data.get("candidates", [])
        parts = candidates[0].get("content", {}).get("parts", []) if candidates else []
        tool_call = next((part.get("functionCall") for part in parts if "functionCall" in part), None)

        if tool_call:
            tool_name = tool_call.get("name")
            args = tool_call.get("args", {})

            if tool_name == "verify_email" and "email" in args:
                email = args["email"]
                verify_url = f"https://emailvalidation.abstractapi.com/v1/?api_key={abstract_api_key}&email={email}"
                verify_response = requests.get(verify_url)
                verify_data = verify_response.json()

                return LlmResponseStruct(Data={
                    "tool_name": tool_name,
                    "tool_args": args,
                    "tool_result": verify_data,
                    "message": f"Tool '{tool_name}' executed successfully"
                }, Error=None, Status=True)

            if tool_name == "verify_phone" and "phone" in args:
                phone = args["phone"]
                verify_url = f"https://phonevalidation.abstractapi.com/v1/?api_key={abstract_api_key}&phone={phone}"
                verify_response = requests.get(verify_url)
                verify_data = verify_response.json()

                return LlmResponseStruct(Data={
                    "tool_name": tool_name,
                    "tool_args": args,
                    "tool_result": verify_data,
                    "message": f"Tool '{tool_name}' executed successfully"
                }, Error=None, Status=True)

            if tool_name == "check_email_reputation" and "email" in args:
                email = args["email"]
                verify_url = f"https://emailvalidation.abstractapi.com/v1/?api_key={abstract_api_key}&email={email}"
                verify_response = requests.get(verify_url)
                verify_data = verify_response.json()

                return LlmResponseStruct(Data={
                    "tool_name": tool_name,
                    "tool_args": args,
                    "tool_result": verify_data,
                    "message": f"Tool '{tool_name}' executed successfully"
                }, Error=None, Status=True)

        message_text = parts[0].get("text", "") if parts else "No response"
        usage = response_data.get("usageMetadata", {})

        return LlmResponseStruct(Data=asdict(SuccessResponseDataFormat(
            total_llm_calls=1,
            total_tokens=usage.get("totalTokenCount", 0),
            total_input_tokens=usage.get("promptTokenCount", 0),
            total_output_tokens=usage.get("candidatesTokenCount", 0),
            final_llm_response=response_data,
            llm_responses_arr=[response_data],
            messages=[message_text],
            output_type="tool_call" if tool_call else "text"
        )), Error=None, Status=True)

    except requests.exceptions.RequestException as req_err:
        return LlmResponseStruct(Data=None, Error=f"HTTP error: {str(req_err)}", Status=False)

    except Exception as err:
        return LlmResponseStruct(Data=None, Error=f"Unhandled error: {str(err)}", Status=False)
