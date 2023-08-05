class EnvException(Exception):
    from pydantic import ValidationError
    def __init__(self, error: ValidationError) -> None:
        msg = ''
        for item in error.errors():
            if item['type'] == 'value_error.missing':
                msg += f'Not found environment variable {item["loc"][0]}.\r\n'
            elif item['type'].split('.')[0] == 'type_error':
                msg += f'Invalid type specified environment variable {item["loc"][0]}. Required {item["type"].split(".")[1]}.\r\n'
        self.message = msg
        super().__init__(self.message)
