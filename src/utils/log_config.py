import logging
def log_config():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger(__name__)
    logger.info("Starting application...")
    return logger