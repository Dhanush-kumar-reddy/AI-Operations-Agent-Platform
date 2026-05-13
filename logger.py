import logging

logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_step(step, data):
    logging.info(f"{step}: {data}")

def log_error(step, error):
    logging.error(f"{step} ERROR: {error}")