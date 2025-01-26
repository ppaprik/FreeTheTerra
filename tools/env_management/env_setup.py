import traceback
import os
import subprocess
import sys


#------------------------------------------------------------------------------------------------------------------------------------------------------
# ENVIRONMENT SETUP CLASS

class EnvSetup:
    #----------------------------------------------------------------------------------------------------
    # VARIABLES

    requirements_file: str = "requirements.txt"
    installed_file: str = "installed.txt"
    default_installed_file_text: list = [
        "Requirements installed (0 - False, 1 - True)\n",
        "Usage: for example when you want to start som app, you don't need to reinstall requirements every time, you can check state in this file\n",
        "0"
    ]
    ENV_NAME: str = ".env"


    #----------------------------------------------------------------------------------------------------
    # INIT

    def __init__(self):
        pass


    #----------------------------------------------------------------------------------------------------
    # RUN

    def run(self, local_file_path: bool = True, local_env_path: bool = False) -> None:
        """
            If "local_file_path = True" requitments and installed files will be created in the directory where env_setup is located.
            If "local_file_path = False", the requirements and installed files will be created in the directory where this script is executed.
            Same for python environment.
            if "local_env_path = True" environment will be created in the directory where env_setup is located.
            If "local_env_path = False", the environment will be created in the directory where this script is executed.
        """
        self.local_file_path = local_file_path
        self.requirements_file = self.setLocalPath(self.requirements_file, self.local_file_path)
        self.installed_file = self.setLocalPath(self.installed_file, self.local_file_path)

        self.verifyFile(self.installed_file, self.default_installed_file_text)
        self.verifyFile(self.requirements_file)

        self.local_env_path = local_env_path
        env_file_path: str = self.getEnvFilePath(self.ENV_NAME, self.local_env_path)
        self.verifyEnv(env_file_path)

        env_python_path: str = self.getEnvPythonPath(env_file_path)
        self.upgradePip(env_python_path)
        self.installRequitments(env_python_path, self.requirements_file, self.installed_file)


    #----------------------------------------------------------------------------------------------------
    # VERIFY

    def setLocalPath(self, file_path: str, local_file_path: bool) -> str:
        """
            If "local_file_path = True" means that path will be modified to the directory where env_setup is located.
            If "local_file_path = False", the path will be modified to the directory where this script is executed.
        """
        if local_file_path:
            this_script_file_path: str = os.path.abspath(__file__)
            this_script_file_directory: str = os.path.dirname(this_script_file_path)
            return os.path.join(this_script_file_directory, file_path)
        else:
            return file_path


    def verifyFile(self, file: str, array: list = None) -> None:
        """
            Verify if file exists. If not file will be created with inputed string.
            If array is not None, it will be written to the file.
        """
        try:
            if not os.path.exists(file):
                print(f"<< {file} doesn't exist, creating it...")
                with open(file, "w") as file:
                    if array == None:
                        pass
                    else:
                        file.writelines(array)
            else:
                if array != None:
                    print(f"<< Writing to file... {file}")
                    with open(file, "w") as file:
                        file.writelines(array)

                print(f"<< {file} exists.")
        except Exception as error:
            print(f"<< Failed: to verify: {file}. Error: {error}")
            traceback.print_exc()


    #----------------------------------------------------------------------------------------------------
    # STATE MACHINE

    def changeStateOfInstalledFile(self, installed_file: str) -> None:
        """
            Change state of "installed.txt" to "1".
        """
        try:
            print("<< Changing state of installed file to \"1\"...")
            with open(installed_file, "w") as file:
                array: list = self.default_installed_file_text
                array.pop()
                array.append("1")
                file.writelines(array)
        except Exception as error:
            print(f"<< Failed: to change state of {installed_file}. Error: {error}")
            traceback.print_exc()


    #----------------------------------------------------------------------------------------------------
    # ENV

    def getEnvFilePath(self, env_name: str, local_env_path: bool) -> str:
        """
            Returns the path to the environment folder.
        """
        if local_env_path:
            this_script_file_path: str = os.path.abspath(__file__)
            this_script_file_directory: str = os.path.dirname(this_script_file_path)
            return os.path.join(this_script_file_directory, env_name)
        else:
            return env_name


    def getEnvPythonPath(self, env_file_path: str) -> str:
        """
            Returns the path to the environment's Python interpreter.
        """
        if os.name == "nt":
            return os.path.join(env_file_path, "Scripts", "python.exe")
        else:
            return os.path.join(env_file_path, "bin", "python")


    def verifyEnv(self, env_file_path: str) -> None:
        """
        Create a environment if it doesn't exist.
        Environment is created with executed python.
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

    def installRequitments(self, env_python_path: str, requirements_file: str, installed_file: str) -> None:
        """
            Install requirements from a "requirements.txt" and change state of "installed.txt" to "1".
        """
        # Install requirements
        try:
            if os.path.exists(requirements_file) and os.path.exists(env_python_path):
                print("<< Installing requirements...")
                # Install requirements with pip into the environment and check=True ensures that the command succeeds
                subprocess.run([env_python_path, "-m", "pip", "install", "-r", requirements_file], check=True)

                # Change state of installed.txt
                self.changeStateOfInstalledFile(installed_file)
                print("<< Requirements installed.")
            else:
                print("<< Failed: Requirements file or Python environment not found.")
        except subprocess.CalledProcessError as error:
            print(f"<< Failed: to install requirements. Error: {error}")
            traceback.print_exc()
            return


    def upgradePip(self, env_python_path: str) -> None:
        """
        Update pip to the latest version.
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



#------------------------------------------------------------------------------------------------------------------------------------------------------
# EXECUTE

if __name__ == '__main__':
    env_maker = EnvSetup()
    env_maker.run()