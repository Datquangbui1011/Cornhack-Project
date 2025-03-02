import logging

# Create a logger for your application
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

# Create a console handler (you can add other handlers as needed)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Define a formatter and attach it to the handler
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

# Add the handler to the logger if not already added
if not logger.handlers:
    logger.addHandler(console_handler)
