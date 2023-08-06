# colab_gitlab_setup

A simple pythion package-based API that supports a workflow for integrating Google Colab notebooks with
Gitlab repositories, using SSH token authentication.

# synopsis

This package simplifies the process of linking a Google Colaboratory Notebook to Gitlab using SSH key authentication.
The use of SSH keys removes the need to enter passwords or insert keys in the notebook, both of which would represent 
security risks.  

The setup process can be broken down into the following steps:  

1. Generate an SSH key pair and SSH config file and create a tarball file on your local machine.
2. Upload a copy of the public key to your chosen Gitlab repository as a Deploy Key.
3. Upload the SSH key tarball to the Colab environment.
4. Install the SSH keys and set up the necessary SSH config files in the Colab file system.
5. Start an SSH Agent and Provide it with your Private SSH key.
6. Mount your GDrive and create a folder for cloning to.
7. Clone your gitlab repository to a chosen Google Drive folder.


You will still need to do steps 1 & 2 yourself (instructions to follow shortly).
This python package automates the process for steps 3-6.
It also provides a simple API to perform step 7 as proof that the integration has worked.

