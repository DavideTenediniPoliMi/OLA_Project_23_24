from config.config import load_config
from logger.logger import Logger


config = load_config()

Logger.clear_logs(config["log_path"])
