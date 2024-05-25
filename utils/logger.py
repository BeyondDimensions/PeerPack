from loguru import logger

# Remove the default logger to avoid duplicate logs
logger.remove()

# Add a logger to stdout with a simple format
logger.add(sys.stdout, format="{time} {level} {message}", level="DEBUG")
