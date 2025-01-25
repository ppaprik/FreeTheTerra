import os
import subprocess
import sys


#----------------------------------------------------------------------------------------------------
# VARIABLES

ENV_NAME = ".env"
APP_NAME = "./game/run.py"
PATH_TO_REQUIRMENTS = "./tools/env_management/installed.txt"


#----------------------------------------------------------------------------------------------------
# FUNCTIONS

def checkIfRequitmentsInstalled():
    with open(PATH_TO_REQUIRMENTS, "r") as file:
        lines = file.readlines()
        if lines[2] == "0":
            print("False")
        elif lines[2] == "1":
            print("True")


def getEnvPythonPath(env_name: str) -> str:
    """
        Returns the path to the virtual environment's Python interpreter.
    """
    if os.name == "nt":
        return os.path.join(env_name, "Scripts", "python.exe")
    else:
        return os.path.join(env_name, "bin", "python")


def run(app_script: str, env_path: str) -> None:
    """
        Run the app script and terminate this script once app.py has been launched.
    """
    try:
        print("Running app...")
        subprocess.run([env_path, app_script], check=True)
    except subprocess.CalledProcessError as error:
        print(f"Error running app: {error}")

    print("Exiting...")
    sys.exit()


def main():
    checkIfRequitmentsInstalled()
    # run(APP_NAME, getEnvPythonPath(ENV_NAME))


#----------------------------------------------------------------------------------------------------
# MAIN

if __name__ == '__main__':
    main()