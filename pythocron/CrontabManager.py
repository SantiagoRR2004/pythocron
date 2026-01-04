import subprocess
import datetime
import logging
import json
import os


class CrontabManager:
    currentDirectory = os.path.dirname(os.path.abspath(__file__))
    counterFile = os.path.join(currentDirectory, "counter.txt")
    crontabsFile = os.path.join(currentDirectory, "Crontabs.json")
    logFile = os.path.join(currentDirectory, "output.log")

    env = os.environ.copy()

    def setup(
        self,
        environmentPath: str,
        pythonFiles: list[dict] = [],
        updateEnvironment: bool = True,
    ) -> None:
        """
        Prepare the files for automatic execution. Each python file will be run
        every 5 minutes until it succeeds. Once it succeeds, it will not be run again
        until the next day.

        Args:
            - environmentPath (str): The path to the environment. It needs to be the absolute with
                bin/activate at the end.
            - pythonFiles (list[dict]): List of python files to add to the crontab
                The keys of the dict are:
                    - "file" (str): The file to add
                    - "oncePerDay" (bool): If True, the file will be run once per day.
                        Default is True.
                    - "logFile" (str): The file to save the output. Default is output.log
            - updateEnvironment (bool): If True, the environment will be updated using a
                python script. Default is True.

        Returns:
            - None
        """
        # Update the environment task
        if updateEnvironment:
            pythonFiles.append(
                {
                    "file": os.path.join(self.currentDirectory, "updateEnvironment.py"),
                    "oncePerDay": True,
                    "logFile": os.path.join(self.currentDirectory, "updateEnv.log"),
                }
            )

        # Open old contrabs
        data = {}
        if os.path.exists(self.crontabsFile):
            with open(self.crontabsFile, "r") as file:
                data = json.load(file)

        # Add the files
        for file in pythonFiles:

            # Add empty if not exists
            data.setdefault(file["file"], {})

            # Do not override the date
            if "date" not in data[file["file"]]:
                data[file["file"]]["date"] = "2023-01-01"

            data[file["file"]]["oncePerDay"] = file.get("oncePerDay", True)

            data[file["file"]]["logFile"] = file.get("logFile", self.logFile)

        # Save the crontab files
        with open(self.crontabsFile, "w") as file:
            # TODO: Create function to dump like Prettier
            json.dump(data, file, indent=2, ensure_ascii=False)
            file.write("\n")

        # Add the cron command
        cronCommand = self.createCronCommand(environmentPath=environmentPath)
        CrontabManager.addNewCronTasks([cronCommand])

    def main(self) -> None:
        """
        Run all the files that are in the crontab file

        Args:
            - None

        Returns:
            - None
        """
        # Keep counter updated
        try:
            with open(self.counterFile, "r") as file:
                counter = int(file.read())
        except FileNotFoundError:
            counter = 0

        # Now we read the file if it exists
        data = {}
        if os.path.exists(self.crontabsFile):
            with open(self.crontabsFile, "r") as file:
                data = json.load(file)

        currentDate = datetime.date.today()

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        for script, config in data.items():

            if (
                datetime.datetime.strptime(config["date"], "%Y-%m-%d").date()
                != currentDate
            ):
                handler = logging.FileHandler(config["logFile"], mode="a")
                formatter = logging.Formatter(
                    "%(asctime)s - %(levelname)s - %(message)s"
                )
                handler.setFormatter(formatter)

                # Remove old handlers
                logger.handlers = []
                logger.addHandler(handler)

                logging.info(script)

                process = subprocess.Popen(
                    ["python3", script],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env=self.env,
                )

                return_code = process.wait()
                output, error = process.communicate()

                logging.info("Return Code: %s", return_code)
                if error.decode() != "":
                    logging.error(error.decode())

                if error.decode() == "":  # We have executed today if it works
                    config["date"] = currentDate.strftime("%Y-%m-%d")

                if output.decode() != "":
                    logging.info(output.decode())

        # Save the most recent dates
        with open(self.crontabsFile, "w") as file:
            # TODO: Create function to dump like Prettier
            json.dump(data, file, indent=2, ensure_ascii=False)
            file.write("\n")

        # Update counter
        with open(self.counterFile, "w") as file:
            file.write(str(counter + 1))

    def createCronCommand(self, environmentPath: str) -> str:
        """
        Create the cron command to add to the crontab the
        current file with the necessary environment variables.

        Args:
            - environmentPath (str): The path to the environment. It needs to be the absolute with
                bin/activate at the end.
            - None

        Returns:
            - str: The cron command
        """
        every5Min = "*/5 * * * *"
        currentFile = os.path.abspath(__file__)

        otherInstructionsList = [
            f"export DISPLAY={os.getenv('DISPLAY')}",
            f"export XAUTHORITY={os.getenv('XAUTHORITY')}",
            "export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/snap/bin",
        ]

        otherInstructions = ""

        for instruction in otherInstructionsList:
            otherInstructions += f"{instruction} && "
        else:
            otherInstructions = otherInstructions[:-1]  # Remove the last space

        cronLocation = os.path.join(self.currentDirectory, "runCron.sh")
        """
        */5 * * * * export DISPLAY=?? && export XAUTHORITY=?? && export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/snap/bin && /absolutePath/runCron.sh /absolutePath/environment/bin/activate /absolutePath/CrontabManager.py
        """

        return f"{every5Min} {otherInstructions} {cronLocation} {environmentPath} {currentFile}"

    @staticmethod
    def runTerminal(command: str) -> None:
        """
        Run a terminal command and print the output or error.

        TODO: Use this function from modules instead of duplicating code.

        Args:
            - command (str): The command to run.

        Returns:
            - None
        """
        try:
            completed_process = subprocess.run(
                command,
                shell=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if completed_process.returncode == 0:
                print("Command executed successfully!")
                print("Output:")
                print(completed_process.stdout)
            else:
                print("Command failed!")
                print("Error:")
                print(completed_process.stderr)
        except Exception as e:
            print("An error occurred:", e)

    @staticmethod
    def addNewCronTasks(newTasks: list) -> None:
        """
        This function will add new tasks to the crontab
        without deleting the old ones.

        Args:
            newTasks (list): A list of strings with the new tasks.

        Returns:
            None
        """
        result = subprocess.run(
            ["crontab", "-l"], capture_output=True, text=True, check=True
        )

        if not result.stderr:
            oldTasks = result.stdout.split("\n")
            for task in newTasks:
                if task not in oldTasks:
                    CrontabManager.runTerminal(
                        f"(crontab -l; echo '{task}') | crontab -"
                    )


if __name__ == "__main__":
    CrontabManager().main()
