from typing import List, Optional
from pydantic import BaseModel
from ml.llm.prompt_format import Message


class GenerateRequest(BaseModel):
    """Generate Completion Request

    Attributes
    ----------
        prompt -> str: Prompt to use for this generation
        messages -> List[Message]: List of messages to use for this generation
        stream -> Bool: flag whether to stream the output or not
        max_tokens -> int: Maximum number of tokens to generate per output sequence
        temperature -> float: Controls the randomness of the sampling.
            Lower temperature results in less random completions. As the
            temperature approaches zero, the model will become deterministic and
            repetitive. Higher temperature results in more random completions.
        ignore_eos -> bool: Whether to ignore EOS token when generating
            output. Default to True as we always want to generate the full
            sequence.

        Sampling parameters
        -------------------
            See -> vllm/sampling_params.py
    """

    prompt: Optional[str]
    messages: Optional[List[Message]]
    stream: Optional[bool] = False
    max_tokens: Optional[int] = 128
    temperature: Optional[float] = 0.7
    ignore_eos: Optional[bool] = False


class GenerateResponse(BaseModel):
    """Generate completion response.

    Attributes
    ----------
        output -> str: Model output
        prompt_tokens -> int: Number of tokens in the prompt
        output_tokens -> int: Number of generated tokens
        finish_reason -> str: Reason the genertion has finished
    """

    output: str
    prompt_tokens: int
    output_tokens: int
    finish_reason: Optional[str]
