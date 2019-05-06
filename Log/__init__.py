import logging

logging.basicConfig(level=logging.ERROR,
                    filename='logging.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

__all__ = ["logger"]
