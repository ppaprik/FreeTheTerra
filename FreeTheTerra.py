import os
import subprocess
import sys
import traceback
from tools.env_management.env_setup import EnvSetup


#------------------------------------------------------------------------------------------------------------------------------------------------------
# VARIABLES

ENV_NAME: str = ".env"
APP_NAME: str = "./game/run.py"
PATH_TO_REQUIRMENTS: str = "./tools/env_management/installed.txt"


#------------------------------------------------------------------------------------------------------------------------------------------------------
# FUNCTIONS

def checkRequitments(path_to_requirements: str) -> bool:
    """
        Check if requirements are installed.
    """
    try:
        with open(path_to_requirements, "r") as file:
            lines: list = file.readlines()
            if lines[2] == "0":
                return False
            elif lines[2] == "1":
                return True
    except Exception as error:
        print(f"<< Failed: to check if requirements are installed. Error: {error}")
        traceback.print_exc()


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
        Run the app with custom environment.
    """
    try:
        print("<< Running app...")
        subprocess.run([env_path, app_script], check=True)
    except subprocess.CalledProcessError as error:
        print(f"<< Failed: running app: {error}")
        traceback.print_exc()

    print("<< Exiting...")
    sys.exit(0)


def main():
    if not checkRequitments(PATH_TO_REQUIRMENTS):
        print("<< Requitments not installed. Please make sure to run \"env_setup.py\" in \"/tool/env_management\" first.")
        EnvSetup().run()

    if checkRequitments(PATH_TO_REQUIRMENTS):
        run(APP_NAME, getEnvPythonPath(ENV_NAME))


#------------------------------------------------------------------------------------------------------------------------------------------------------
# MAIN

if __name__ == '__main__':
    main()