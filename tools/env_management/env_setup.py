import traceback
import os
import subprocess
import sys


#------------------------------------------------------------------------------------------------------------------------------------------------------
# ENVIRONMENT SETUP CLASS

class EnvSetup:
    """
        Automatic environment setup.\n
    """
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
    # START OF PROGRAM

    def run(self, local_file_path: bool = True, local_env_path: bool = False, custom_directory_path: str = None) -> None:
        """
            This function will install requirements and create environment.\n

            If you use "custom_directory_path" you have to be sure that "custom_directory_path" is ABSOLUTE PATH TO DIRECTORY !!\n
            \n
            ### In Short:\n

            "local_file_path" defines if "requirements.txt" and "installed.txt" will be created in the directory where this script is executed or in custom_directory_path.\n
            Same for "local_env_path".\n
            "custom_directory_path" is: if you don't want directory where this script is executed or where env_setup is located. You can use your custom directory path.\n

            ### Complex Behavior:\n

            If "local_file_path" is "True" and "custom_directory_path" is not None, requitments and installed files will be created in custom_directory_path.
            And if "custom_directory_path" is None, requitments and installed files will be created in the directory where env_setup is located.\n

            If "local_file_path = False", requirements and installed files will be created in the directory where this script is executed.
            At this case "custom_directory_path" doesn't have influence.\n

            Same thing for "local_env_path".\n

            If "local_env_path = True" and "custom_directory_path" is not None, environment will be created in "custom_directory_path".
            And if "custom_directory_path" is None, environment will be created in the directory where env_setup is located.\n

            If "local_env_path = False", environment will be created in the directory where this script is executed.
            At this case "custom_directory_path" doesn't have influence.\n
        """
        
        if custom_directory_path == None:
            this_script_file_path: str = os.path.abspath(__file__)
            custom_directory_path: str = os.path.dirname(this_script_file_path)

        self.requirements_file = self.setLocalPath(self.requirements_file, local_file_path, custom_directory_path)
        self.installed_file = self.setLocalPath(self.installed_file, local_file_path, custom_directory_path)

        self.verifyFile(self.installed_file, self.default_installed_file_text)
        self.verifyFile(self.requirements_file)

        env_file_path: str = self.getEnvFilePath(self.ENV_NAME, local_env_path, custom_directory_path)
        self.verifyEnv(env_file_path)

        env_python_path: str = self.getEnvPythonPath(env_file_path)
        self.upgradePip(env_python_path)
        self.installRequitments(env_python_path, self.requirements_file, self.installed_file)


    #----------------------------------------------------------------------------------------------------
    # VERIFY

    def setLocalPath(self, file: str, local_file_path: bool, custom_directory_path: str) -> str:
        """
            If "local_file_path" is "True" and "custom_directory_path" is not None, "file" will be created in custom_directory_path.
            And if "custom_directory_path" is None, "file" will be created in the directory where env_setup is located.\n

            If "local_file_path = False", "file" will be created in the directory where this script is executed.
            At this case "custom_directory_path" doesn't have influence.\n
        """
        if local_file_path:
            return os.path.join(custom_directory_path, file)
        else:
            return file


    def verifyFile(self, file: str, array: list = None) -> None:
        """
            Verify if "file" exists. If not file will be created.\n
            If "array" is not None, it will be written to the file.
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
                print(f"<< {file} exists.")
                if array != None:
                    print(f"<< Writing to file... {file}")
                    with open(file, "w") as file:
                        file.writelines(array)
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

    def getEnvFilePath(self, env_name: str, local_env_path: bool, custom_directory_path: str) -> str:
        """
            If "local_env_path = True" and "custom_directory_path" is not None, environment will be created in custom_directory_path.
            And if "custom_directory_path" is None, environment will be created in the directory where env_setup is located.\n

            If "local_env_path = False", environment will be created in the directory where this script is executed.
            At this case "custom_directory_path" doesn't have influence.\n
        """
        if local_env_path:
            return os.path.join(custom_directory_path, env_name)
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
        Create a environment if it doesn't exist.\n
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
        try:
            if os.path.exists(requirements_file) and os.path.exists(env_python_path):
                print("<< Installing requirements...")
                # Install requirements with pip into the environment and check=True ensures that the command succeeds
                subprocess.run([env_python_path, "-m", "pip", "install", "-r", requirements_file], check=True)

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