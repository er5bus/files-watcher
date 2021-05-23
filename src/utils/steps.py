import time
import pysftp
import sys
import os
import requests
from datetime import datetime
import shutil
from retry import retry
import logging


handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(message)s at [%(asctime)s] %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d]s", datefmt="%a, %d %b %Y %H:%M:%S")
handler.setFormatter(formatter)

log = logging.getLogger()
log.setLevel(logging.INFO)
log.addHandler(handler)


@retry(delay=1, tries=3, backoff=2, logger=log)
def upload_file_to_server(file_path: str) -> datetime:
    """
    Parameters
    ----------
    file_path : str
        Local file path that will be uploaded
    Returns
    -------
    timestamp :
        the timestamp of the uploaded file
    """
    log.info("Step 1/3 : Start connection to the server")
    # auto close => with key word => context manager
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None 
    with pysftp.Connection(os.getenv("SERVER_HOSTNAME" ,"hostname"), cnopts=cnopts,
                           username=os.getenv("SERVER_USERNAME" ,"me"), 
                           password=os.getenv("SERVER_PASSWORD" ,"secret")) as sftp:
        log.info("Step 1/3 : Connection successful")
        with sftp.cd(os.getenv("SERVER_UPLOAD_PATH" ,"/home/app/uploads")):
            log.info("Step 1/3 : Start Upload")
            sftp.put(file_path)
            log.info("Step 1/3 : Finish Upload")
            log.info("Step 1/3 : close connection to the server")
            return datetime.now().timestamp()


@retry(delay=1, tries=3, backoff=2, logger=log)
def web_hook(filename: str, timestamp: datetime) -> None:
    """
    Parameters
    ----------
    filename : str
        The uploaded filename
    timestamp :
        the timestamp of the uploaded file
    """
    formatted_timesamp = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    data = {"filename": filename, "timestamp": timestamp, 
            "message": f"{filename} has been received at {formatted_timesamp}"}
    log.info(f"Step 2/3 : invoke web server start {data}")
    requests.post(os.getenv("WEB_HOOK_URL" ,"https://hostname/webhook"), data=data)
    log.info("Step 2/3 : invoke web server end")


@retry(delay=1, tries=3, backoff=2, logger=log)
def move_files_to_archive(file_path: str, filename: str) -> None:
    """
    Parameters
    ----------
    filename : str
        The uploaded filename
    file_path :
        Local file path
    """
    log.info("Step 3/3 : Move file to archive directory")
    shutil.move(file_path, os.path.join(os.getenv("ARCHIVE_DIRECTORY" ,"/var/tmp/files/archive"), filename))
