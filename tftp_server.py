import paramiko
import tftpy
import threading
import time
import logging


class TFTPServer:
    def __init__(self, server_ip, server_port, root):
        self.server_ip = server_ip
        self.server_port = server_port
        self.root = root
        self.server = None
        self.server_thread = None
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        return logger

    def start_server(self):
        """Function to start the TFTP server."""
        try:
            self.server = tftpy.TftpServer(self.root)
            self.server_thread = threading.Thread(target=self.server.listen,
                                                  args=(self.server_ip, self.server_port))
            self.server_thread.start()
            self.logger.info(
                f"TFTP server started on {self.server_ip}:{self.server_port}, serving files from {self.root}")
        except Exception as e:
            self.logger.error(f"An error occurred while starting TFTP server: {e}")

    def stop_server(self):
        """Function to stop the TFTP server."""
        if self.server:
            self.server.stop()
            self.server_thread.join()
            self.logger.info("TFTP server stopped.")
        else:
            self.logger.warning("TFTP server is not running.")


def stop_server():
    return None