from src.config.config import load_config
from src.logger.logger import Logger


config = load_config()

Logger.clear_logs(config["log_path"])
