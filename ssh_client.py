import paramiko
import time

class SSHClient:
    def __init__(self, host, username, key_path, key_pass=None, port=22):
        self.ssh = None
        self.shell = None
        self.host = host
        self.port = port
        self.username = username
        self.key_path = key_path
        self.key_pass = key_pass
        self.connect()

    def send(self, command):
        """Send a command to the shell and return the output."""
        self.shell.send(command + '\n')
        time.sleep(1)  # Adjust the sleep time based on command execution time
        self.read_output()

    def read_output(self, timeout=1):
        """Continuously read output from the shell until there is no more data."""
        output = ''
        end_time = time.time() + timeout
        while True:
            if self.shell.recv_ready():
                print(self.shell.recv(1024).decode('utf-8'))
                end_time = time.time() + timeout  # Reset end time if data is received
            elif time.time() > end_time:
                break
            time.sleep(0.1)  # Small sleep to prevent busy-waiting

        # Check one last time if there's any remaining output
        while self.shell.recv_ready():
            print(self.shell.recv(1024).decode('utf-8'))

        return output

    def read_output_for_duration(self, duration=300):
        """Read output from the shell for a fixed duration of time."""
        output = ''
        start_time = time.time()
        while time.time() - start_time < duration:
            if self.shell.recv_ready():
                output += self.shell.recv(1024).decode('utf-8')
            time.sleep(0.1)  # Small sleep to prevent busy-waiting

        return output
    def connect(self):
        """Function to establish an SSH connection and run commands."""
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        private_key = paramiko.RSAKey(filename=self.key_path, password=self.key_pass)

        try:
            print(f"Connecting to SSH server {self.host}:{self.port}")
            self.ssh.connect(hostname=self.host, port=self.port, username=self.username, pkey=private_key)
            print("Successfully connected to the SSH server!")

            # Open an interactive shell session
            self.shell = self.ssh.invoke_shell()
            self.shell.settimeout(1.0)

            # Allow time for the shell to be ready
            time.sleep(1)

            # Read the initial output
            self.read_output()


        except Exception as e:
            print(f"An error occurred with SSH connection: {e}")

    def close(self):
        if self.ssh:
            self.ssh.close()
