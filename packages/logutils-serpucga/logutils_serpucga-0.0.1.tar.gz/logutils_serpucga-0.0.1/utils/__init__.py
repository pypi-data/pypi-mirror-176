__version__ = "0.0.1"

import logging


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;1m"
    yellow = "\x1b[33;1m"
    blue = "\x1b[34;1m"
    red = "\x1b[38;2;255;0;0;1m"
    bold_red = "\x1b[38;2;128;0;0;1m"
    reset = "\x1b[0m"
    fmt = "[%(asctime)s] %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    def get_fmt_string(self, level):
        level_name = '%(levelname)s'
        start, end = self.fmt.split(level_name)
        match level:
            case logging.DEBUG:
                log_fmt = f"{start}{self.grey}{level_name}{self.reset}{end}"
            case logging.INFO:
                log_fmt = f"{start}{self.blue}{level_name}{self.reset}{end}"
            case logging.WARNING:
                log_fmt = f"{start}{self.yellow}{level_name}{self.reset}{end}"
            case logging.ERROR:
                log_fmt = f"{start}{self.red}{level_name}{self.reset}{end}"
            case logging.CRITICAL:
                log_fmt = f"{start}{self.bold_red}{level_name}{self.reset}{end}"
            case _:
                raise Exception("Wrong log level")
        return log_fmt

    def format(self, record):
        log_fmt = self.get_fmt_string(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(name, level=logging.INFO, handler_type="stream"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    match handler_type:
        case "stream":
            handler = logging.StreamHandler()
        case _:
            raise Exception(f"Handler {handler_type} not supported")
    if level not in (
        logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL
    ):
        raise Exception(f"Level {level} not supported")
    handler.setLevel(level)
    handler.setFormatter(CustomFormatter())
    logger.addHandler(handler)
    return logger
