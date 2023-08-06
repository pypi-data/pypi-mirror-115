import os
import subprocess
import re
from google.colab import drive, files


class ColabGitlabSetup:

    def __init__(self,auto=False, mount_folder="/content/drive", git_folder="gitlabs",ssh_host="gitlab.com",
		 ssh_tar_file="ssh.tar.gz",ssh_tar_folder="ssh-colab",ssh_install_folder="/root/.ssh",
		 repo_account="dtime-ai",repo_group="admin",repo_name="google-colab-integration"):
        self.mount_folder = mount_folder
        self.git_folder = f"{self.mount_folder}/MyDrive/{git_folder}"
        self.repo_folder = f"{self.git_folder}/{repo_name}"
        self.ssh_host = ssh_host
        self.ssh_tar_file = ssh_tar_file
        self.ssh_tar_folder = ssh_tar_folder
        self.ssh_install_folder = ssh_install_folder
        self.repo_account = repo_account
        self.repo_group = repo_group
        self.repo_name = repo_name
        if auto:
            self.install_ssh_keys()
            self.load_private_key()
            self.mount_gdrive()

    def install_ssh_keys(self):
        if os.path.isdir(self.ssh_install_folder):
            os.system(f"rm -rf {self.ssh_install_folder}")
        os.system(f"mkdir {self.ssh_install_folder}")
        os.chdir(self.ssh_install_folder)
        print(f"Please select the SSH key tarball file to upload...")
        from google.colab import files # cough, cough!
        uploaded = files.upload()

        print("Installing ssh keys...")
        os.system(f"tar xvzf {self.ssh_tar_file}")
        os.system(f"cp {self.ssh_tar_folder}/* . && rm -rf {self.ssh_tar_folder} && rm -rf {self.ssh_tar_file}")
        os.system("chmod 700 .")
        print("...Installed")

    def load_private_key(self):
        print("Identifying the name of the private ssh key file...")
        os.chdir(self.ssh_install_folder)
        files = [i for i in os.listdir(".") if i.endswith('.pub')]
        self.private_key_file = f"{self.ssh_install_folder}/{os.path.splitext(files[0])[0]}"
        print(f"...Identified as {self.private_key_file}")

        print(f"Loading {self.private_key_file} into an ssh-agent...")
        self.ssh_agent_setup()
        self.ssh_agent_addkey( self.private_key_file )
        self.ssh_agent_kill()
        print("...Loaded")

    def mount_gdrive(self):
        print(f"Mounting google drive to {self.mount_folder}...") 
        if not os.path.isdir(self.mount_folder):
            drive.mount(self.mount_folder)
        print("...Mounted")
        print(f"Creating {self.git_folder} to clone repositories into...")
        if not os.path.isdir(self.git_folder):
            os.system(f"mkdir {self.git_folder}")
        print("... Git folder created")

    def clone(self):
        os.chdir(self.git_folder)
        if not os.path.isdir(self.repo_folder):
            os.system(f"git clone git@gitlab.com:{self.repo_account}/{self.repo_group}/{self.repo_name}.git")

    def ssh_agent_setup(self):
        if os.environ.get( 'SSH_AUTH_SOCK' ) is None:
            process = subprocess.run( [ 'ssh-agent', '-s' ], stdout = subprocess.PIPE, universal_newlines = True )
            OUTPUT_PATTERN = re.compile(  'SSH_AUTH_SOCK=(?P<socket>[^;]+).*SSH_AGENT_PID=(?P<pid>\d+)', re.MULTILINE | re.DOTALL )
            match = OUTPUT_PATTERN.search( process.stdout )
            agentData = match.groupdict()
            os.environ[ 'SSH_AUTH_SOCK' ] = agentData[ 'socket' ]
            os.environ[ 'SSH_AGENT_PID' ] = agentData[ 'pid' ]

    def ssh_agent_addkey(self,keyFile):
        process = subprocess.run( [ 'ssh-add', keyFile ] )
        print(process)

    def ssh_agent_kill(self):
        process = subprocess.run( [ 'ssh-agent', '-k' ] )
        print(process)
        del os.environ[ 'SSH_AUTH_SOCK' ]
        del os.environ[ 'SSH_AGENT_PID' ]

    def git_config_globals(self,user_name="",user_email=""):
        os.system(f"git config --global user.name '{user_name}'")
        os.system(f"git config --global user.email '{user_email}'")
