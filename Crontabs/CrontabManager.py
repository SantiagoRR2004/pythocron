import subprocess
import datetime
import json
import os


class CrontabManager:
    currentDirectory = os.path.dirname(os.path.abspath(__file__))
    counterFile = os.path.join(currentDirectory, "counter.txt")
    crontabsFile = os.path.join(currentDirectory, "Crontabs.json")

    env = os.environ.copy()

    def setup(self, pythonFiles: list[str]) -> None:
        pass

    def main(self) -> None:
        """ """

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


if __name__ == "__main__":
    CrontabManager().main()
