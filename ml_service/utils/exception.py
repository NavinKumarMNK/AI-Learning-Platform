class ConfigFileMissingError(Exception):
    """This Exception is raised when any config files
    need to run services were missing"""

    def __init__(self, msg):
        super().__init__(msg)


class MaximumContextLengthError(Exception):
    """This Exception is raised when maximum tokens
    requested is greater than model's maximum context length"""

    def __init__(self, max_model_len, prompt_len, request_max_len):
        super().__init__(
            f"This model's maximum context length is {max_model_len} tokens. "
            f"However, you requested {request_max_len + prompt_len} tokens "
            f"(len of the message is {prompt_len}, completion len {request_max_len}) "
            f"Please reduce the length of the messages or completion."
        )
