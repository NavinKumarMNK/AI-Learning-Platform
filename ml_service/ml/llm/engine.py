from typing import AsyncGenerator, Dict, List, Optional, Tuple

from vllm.config import CacheConfig as VLLMCacheConfig
from vllm.config import ModelConfig as VLLMModelConfig
from vllm.config import ParallelConfig as VLLMParallelConfig
from vllm.config import SchedulerConfig as VLLMSchedulerConfig
from vllm.engine.arg_utils import AsyncEngineArgs
from vllm.engine.async_llm_engine import (
    AsyncLLMEngine,
    AsyncStream,
    _AsyncLLMEngine,
)

VLLMConfig = Tuple[
    VLLMCacheConfig, VLLMModelConfig, VLLMParallelConfig, VLLMSchedulerConfig
]


def get_vllm_engine_config(config: Dict) -> Tuple[AsyncEngineArgs, VLLMConfig]:
    async_engine_args = AsyncEngineArgs(**config)
    configs = async_engine_args.create_engine_configs()
    return async_engine_args, configs
