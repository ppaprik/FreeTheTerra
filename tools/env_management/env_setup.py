import traceback
import os
import subprocess
import sys


#------------------------------------------------------------------------------------------------------------------------------------------------------
# VARIABLES

REQUIREMENTS_FILE: str = "requirements.txt"

INSTALLED_FILE: str = "installed.txt"
default_installed_file_text: str = "Requirements installed (0 - False, 1 - True)\nUsage: for example when you want to start som app, you don't need to reinstall requirements every time, you can check state in this file\n"

ENV_NAME: str = ".env"
DEFUALT_PATH_TO_ROOT: str = "../../"


#------------------------------------------------------------------------------------------------------------------------------------------------------
# FUNCTIONS

#----------------------------------------------------------------------------------------------------
# VERIFY

def verifyInstalledFile(installed_file: str) -> None:
    """
        Check if "installed.txt" exists, if not it will be created with default "0" state
    """
    try:
        if not os.path.exists(installed_file):
            print("<< Installed file doesn't exist, creating it...")
        else:
            print("<< Verifying installed file...")
            
        with open(installed_file, "w") as file:
            array: list = [default_installed_file_text, "0"]
            file.writelines(array)
    except Exception as error:
        print(f"<< Failed: to verify: {installed_file}. Error: {error}")
        traceback.print_exc()


def verifyRequirementsFile(requirements_file: str) -> None:
    """
        Check if "requirements.txt" exists, if not it will be created
    """
    try:
        if not os.path.exists(requirements_file):
            print("<< Requirements file doesn't exist, creating it...")
            with open(requirements_file, "w") as file:
                pass
        else:
            print("<< Requirements file exists.")
    except Exception as error:
        print(f"<< Failed: to verify: {requirements_file}. Error: {error}")
        traceback.print_exc()


#----------------------------------------------------------------------------------------------------
# STATE MACHINE

def changeStateOfInstalledFile(installed_file: str) -> None:
    """
        Change state of "installed.txt" to "1"
    """
    try:
        print("<< Changing state of installed file to \"1\"...")
        with open(installed_file, "w") as file:
            array: list = [default_installed_file_text, "1"]
            file.writelines(array)
    except Exception as error:
        print(f"<< Failed: to change state of {installed_file}. Error: {error}")
        traceback.print_exc()


#----------------------------------------------------------------------------------------------------
# ENV

def getEnvFilePath(default_root_to_path: str, env_name: str) -> str:
    """
        Returns the path to the environment folder.
    """
    current_dir: str = os.getcwd().split(os.sep)
    env_file_path: str = None
    if current_dir[-1] == "env_management" and current_dir[-2] == "tools":
        env_file_path = os.path.join(default_root_to_path, env_name)
        return env_file_path
    else:
        return env_name


def getEnvPythonPath(env_file_path: str) -> str:
    """
        Returns the path to the environment's Python interpreter.
    """
    if os.name == "nt":
        return os.path.join(env_file_path, "Scripts", "python.exe")
    else:
        return os.path.join(env_file_path, "bin", "python")


def verifyEnv(env_file_path: str) -> None:
    """
       Create a environment if it doesn't exist.
       Environment is created with executed python
    """
    if not os.path.exists(env_file_path):
        print("<< Creating virtual environment...")
        try:
            # Create a environment with executed python and check=True ensures that the command succeeds
            subprocess.run([sys.executable, "-m", "venv", env_file_path], check=True)
        except subprocess.CalledProcessError as error:
            print(f"<< Failed: to create virtual environment. Error: {error}")
            traceback.print_exc()
    else:
        print("<< Virtual environment already exists.")


#----------------------------------------------------------------------------------------------------
# INSTALL & UPDATE

def installRequitments(env_python_path: str, requirements_file: str, installed_file: str) -> None:
    """
        Install requirements from a "requirements.txt" and change state of "installed.txt" to "1"
    """
    # Install requirements
    try:
        if os.path.exists(requirements_file) and os.path.exists(env_python_path):
            print("<< Installing requirements...")
            # Install requirements with pip into the environment and check=True ensures that the command succeeds
            subprocess.run([env_python_path, "-m", "pip", "install", "-r", requirements_file], check=True)

            # Change state of installed.txt
            changeStateOfInstalledFile(installed_file)
            print("<< Requirements installed.")
        else:
            print("<< Failed: Requirements file or Python environment not found.")
    except subprocess.CalledProcessError as error:
        print(f"<< Failed: to install requirements. Error: {error}")
        traceback.print_exc()
        return


def upgradePip(env_python_path: str) -> None:
    """
    Update pip to the latest version
    """
    try:
        if os.path.exists(env_python_path):
            print("<< Upgrading pip...")
            subprocess.run([env_python_path, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        else:
            print("<< Failed: Python environment not found.")
    except subprocess.CalledProcessError as error:
        print(f"<< Failed: to update pip. Error: {error}")
        traceback.print_exc()


#----------------------------------------------------------------------------------------------------
# MAIN

def main():

    verifyInstalledFile(INSTALLED_FILE)
    verifyRequirementsFile(REQUIREMENTS_FILE)

    env_file_path: str = getEnvFilePath(DEFUALT_PATH_TO_ROOT, ENV_NAME)
    verifyEnv(env_file_path)

    env_python_path: str = getEnvPythonPath(env_file_path)
    upgradePip(env_python_path)
    installRequitments(env_python_path, REQUIREMENTS_FILE, INSTALLED_FILE)


#------------------------------------------------------------------------------------------------------------------------------------------------------
# RUN

if __name__ == '__main__':
    main()