from loguru import logger


logger.add(
    "logs/app.log",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="2 MB",
    compression="zip",
    serialize=False
)
