# Adapted from:
# https://github.com/ray-project/ray-llm/blob/master/rayllm/common/models.py

from typing import (
    Any,
    Dict,
    List,
    Literal,
    Optional,
    Type,
    TypeVar,
    Union,
)

import yaml
from pydantic import BaseModel, validator

T = TypeVar("T")
ModelT = TypeVar("ModelT", bound=BaseModel)


class BaseModelExtended(BaseModel):
    @classmethod
    def parse_yaml(cls: Type[ModelT], file, **kwargs) -> ModelT:
        kwargs.setdefault("Loader", yaml.SafeLoader)
        dict_args = yaml.load(file, **kwargs)
        return cls.parse_obj(dict_args)


class Message(BaseModel):
    role: Literal["system", "assistant", "user"]
    content: str

    def __str__(self):
        return self.content


class Prompt(BaseModel):
    prompt: Union[str, List[Message]]
    use_prompt_format: bool = True
    parameters: Optional[Union[Dict[str, Any], BaseModel]] = None


class PromptFormat(BaseModel):
    system: str
    user: str
    assistant: str
    system_in_user: bool = False
    strip_whitespace: bool = True
    trailing_assistant: str
    accept_sys_from_req: bool = False

    @validator("assistant")
    def check_assistant(cls, value):
        assert (
            value and "{instruction}" in value
        ), "assistant must be a string containing '{instruction}'"
        return value

    @validator("user")
    def check_user(cls, value):
        assert value and (
            "{instruction}" in value
        ), "user must be a string containing '{instruction}'"
        return value

    def generate_prompt(self, messages: List[Message]) -> str:
        """Generate prompt from system messages
        
        Parameters
        ----------
        messages: List[Message]
            list of messages with OpenAI format

        Returns
        -------
        prompt: str
            resulted prompt from applying prompt_template

        Raises
        ------
            ValueError: If the input messages only contain a system message.
        """
        
        # Extract system message (if present)
        system_message_index = -1
        for i, message in enumerate(messages):
            if message.role == "system":
                if not self.accept_sys_from_req:
                    KeyError("system prompt is not accepted from user")
                system_message_index = i
                break

        if system_message_index != -1:
            self.system = messages.pop(system_message_index).content
        
        messages.insert(0, Message(role='system', content=self.system))

        print(messages)

        if all(message.role == "system" for message in messages):
            raise ValueError("Only System messages are not allowed")
        
        prompt = []
        
        if self.system_in_user:
            prompt.append(
                self.user.format(
                    system=messages[0].content,
                    instruction=messages[1].content,
                )
            )
        else:
            prompt.append(messages[0].content)
            prompt.append(
                self.user.format(
                    instruction=messages[1].content
                )
            )
            
        print(prompt, messages)

        for message in messages[2:]:
            message_content = message.content
            if self.strip_whitespace:
                message_content = message_content.strip()
            
            if message.role == "user":
                if self.system_in_user:
                    user_prompt = self.user.format(instruction=message_content, system="")    
                else:
                    user_prompt = self.user.format(instruction=message_content)
                prompt.append(user_prompt)
            elif message.role == "assistant":
                prompt.append(self.assistant.format(instruction=message_content))
        
        prompt.append(self.trailing_assistant)
        print(prompt)
        return "".join(prompt)


class ModelConfig(BaseModelExtended):
    prompt_format: PromptFormat
