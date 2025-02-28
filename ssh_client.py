import paramiko
import time


class SSHClient:
    def __init__(self, host, username, password=None, key_path=None, key_pass=None, port=22):
        self.ssh = None
        self.shell = None
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.key_path = key_path
        self.key_pass = key_pass
        self.connect()

    def connect(self):
        """Establish an SSH connection using password or key."""
        self.ssh = paramiko.SSHClient()
        self.ssh.load_system_host_keys()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            print(f"Connecting to SSH server {self.host}:{self.port}")

            # Attempt password or key-based login
            if self.key_path:  # If a private key is provided
                try:
                    private_key = paramiko.RSAKey.from_private_key_file(self.key_path, password=self.key_pass)
                    self.ssh.connect(self.host, port=self.port, username=self.username, pkey=private_key)
                except paramiko.PasswordRequiredException:
                    print("The private key requires a passphrase.")
                    raise
                except paramiko.SSHException as e:
                    print(f"SSH error: {e}")
                    raise
            else:  # Use password authentication
                self.ssh.connect(self.host, port=self.port, username=self.username, password=self.password)

            print("Successfully connected to the SSH server!")

            # Open an interactive shell session
            self.shell = self.ssh.invoke_shell()
            if not self.shell:
                raise Exception("Failed to open the shell session.")

            self.shell.settimeout(1.0)

            # Allow time for the shell to be ready
            time.sleep(1)
            output = self.read_output()
            print(output)

        except paramiko.AuthenticationException:
            print("Authentication failed. Please check the username/password or SSH key.")
        except Exception as e:
            print(f"An error occurred with SSH connection: {e}")

    def send(self, command):
        """Send a command to the shell and return the output."""
        if self.shell:
            self.shell.send(command + '\n')
            time.sleep(1)  # Adjust the sleep time based on command execution time
            return self.read_output()
        else:
            print("No shell session available.")
            return None

    def read_output(self, timeout=1):
        """Read output from the shell."""
        output = ''
        if not self.shell:
            print("Shell session is not available.")
            return output

        end_time = time.time() + timeout
        while True:
            if self.shell.recv_ready():
                output += self.shell.recv(1024).decode('utf-8')
                end_time = time.time() + timeout  # Reset end time if data is received
            elif time.time() > end_time:
                break
            time.sleep(1)  # Small sleep to prevent busy-waiting

        return output

    def close(self):
        if self.ssh:
            self.ssh.close()

