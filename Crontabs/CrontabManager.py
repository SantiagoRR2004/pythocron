import subprocess
import datetime
import json
import os


class CrontabManager:
    currentDirectory = os.path.dirname(os.path.abspath(__file__))
    counterFile = os.path.join(currentDirectory, "counter.txt")
    crontabsFile = os.path.join(currentDirectory, "Crontabs.json")

    env = os.environ.copy()

    def setup(self, pythonFiles: list[dict]) -> None:
        """
        Prepare the files for automatic execution

        Args:
            - pythonFiles (list[dict]): List of python files to add to the crontab
                The keys of the dict are:
                    - "file": The file to add

        Returns:
            - None
        """
        # Open old contrabs
        data = {}
        if os.path.exists(self.crontabsFile):
            with open(self.crontabsFile, "r") as file:
                data = json.load(file)

        # Add the files
        for file in pythonFiles:
            data[file["file"]] = "2023-01-01"

        # Save the crontab files
        with open(self.crontabsFile, "w") as file:
            # TODO: Create function to dump like Prettier
            json.dump(data, file, indent=2, ensure_ascii=False)
            file.write("\n")

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

        for script, date in data.items():

            if datetime.datetime.strptime(date, "%Y-%m-%d").date() != currentDate:
                print(script)

                process = subprocess.Popen(
                    ["python3", script],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env=self.env,
                )

                return_code = process.wait()
                output, error = process.communicate()

                print("Return Code:", return_code)
                print("Error Message:", error.decode())

                if error.decode() == "":  # We have executed today if it works
                    data[script] = currentDate.strftime("%Y-%m-%d")

                print(output.decode())

        # Save the most recent dates
        with open(self.crontabsFile, "w") as file:
            # TODO: Create function to dump like Prettier
            json.dump(data, file, indent=2, ensure_ascii=False)
            file.write("\n")

        # Update counter
        with open(self.counterFile, "w") as file:
            file.write(str(counter + 1))

    def createCronCommand(self) -> str:
        """
        Create the cron command to add to the crontab the
        current file with the necessary environment variables.

        Args:
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
        */5 * * * * export DISPLAY=?? && export XAUTHORITY=?? && export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/snap/bin && /absolutePath/runCron.sh /absolutePath/CrontabManager.py
        """

        return f"{every5Min} {otherInstructions} {cronLocation} {currentFile}"

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
