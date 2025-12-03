import logging
from pathlib import Path

Path("logs").mkdir(exist_ok=True)
logger = logging.getLogger("auditLogger")
logger.setLevel(logging.INFO)

handler = logging.FileHandler("logs/audit.log")
formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

def logEvent(type, username, ip, description=""):
    logger.info(f"{type} - User: {username} - IP: {ip} - {description}")