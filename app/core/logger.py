import logging
import sys

def setup_logger() -> logging.Logger:
  logger = logging.getLogger("portfolio_ai")

  if logger.handlers:
    return logger

  logger.setLevel(logging.INFO)

  formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
  )

  console_handler = logging.StreamHandler(sys.stdout)
  console_handler.setFormatter(formatter)

  logger.addHandler(console_handler)

  return logger


logger = setup_logger()