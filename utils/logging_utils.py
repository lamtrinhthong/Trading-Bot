import logging

def setup_logging(log_file='bot.log', log_level=logging.DEBUG):
    """Set up logging configuration."""
    logging.basicConfig(filename=log_file, level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

def get_logger(name):
    """Get a logger instance with the specified name."""
    return logging.getLogger(name)
