from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='ColabGitlabSetup',
    url='https://github.com/LaurenceMolloy/colab_gitlab_setup',
    author='Laurence Molloy',
    author_email='laurence.molloy@gmail.com',
    packages=['colab_gitlab_setup'],
    install_requires=['google.colab'],
    version = "0.0.1",
    license='MIT',
    keywords='colaboratory colab gitlab ssh',
    description='A simple API for linking Google Colab Notebooks to Gitlab using SSH',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
