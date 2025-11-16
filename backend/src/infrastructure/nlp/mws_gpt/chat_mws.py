import requests
from typing import Any, Dict, List, Optional
from pydantic import Field
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult


class ChatMWS(BaseChatModel):
    model_name: str = Field(alias="model")
    api_key: str = Field(alias="api_key")
    temperature: Optional[float] = Field(alias="t")
    max_tokens: Optional[int] = Field(alias="max_tokens")
    base_url: str = "https://api.gpt.mws.ru/v1/chat/completions"

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> ChatResult:
        # Собираем текст запроса
        # prompt = "\n".join([m.content for m in messages if hasattr(m, "content")])
        # print(messages)
        prompt = self.convert_to_api_format(messages)
        # print(prompt)
        # print("====")

        # Готовим API-запрос
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        # payload = {
        #     "model": self.model_name,
        #     "prompt": prompt,
        #     "temperature": self.temperature,
        #     "max_tokens": self.max_tokens
        # }
        payload = {
            "model": self.model_name,
            "temperature": self.temperature,
            "messages": prompt
        }
        if stop:
            payload["stop"] = stop

        # Отправляем POST-запрос к MWS API
        response = requests.post(self.base_url, headers=headers, json=payload)

        # print(response.json())
        # print("===")

        if response.status_code != 200:
            raise Exception(f"Error from MWS API: {response.status_code} - {response.text}")

        data = response.json()
    
        # Извлекаем сообщение от ИИ
        output_message = data["choices"][0]["message"]

        # Создаём AIMessage
        ai_message = AIMessage(
            content=output_message["content"],
            additional_kwargs={
                "function_call": output_message.get("function_call"),
                "role": output_message.get("role", "assistant")
            },
            response_metadata={
                "model_name": self.model_name,
                "finish_reason": data["choices"][0].get("finish_reason"),
                "response_id": data.get("id")
            },
            usage_metadata={
                "input_tokens": data.get("usage", {}).get("prompt_tokens", len(prompt)),
                "output_tokens": data.get("usage", {}).get("completion_tokens", len(output_message["content"])),
                "total_tokens": data.get("usage", {}).get("total_tokens", 0)
            }
        )

        return ChatResult(generations=[ChatGeneration(message=ai_message)])

    @property
    def _llm_type(self) -> str:
        return "mws-chat-model"

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        return {
            "model_name": self.model_name,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }

    def convert_to_api_format(self, messages):
        return [{"role": msg.type, "content": msg.content} for msg in messages]
