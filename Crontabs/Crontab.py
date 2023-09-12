import json
import subprocess
import datetime
import os

directory = os.path.dirname(os.path.abspath(__file__))
counterFile = os.path.join(directory, "counter.txt")
crontabsFile = os.path.join(directory, "Crontabs.json")


try:
    with open(counterFile, "r") as file:
        counter = int(file.read())
except FileNotFoundError:
    counter = 0


currentDate = datetime.date.today()

scripts = {}

with open(crontabsFile, "r") as file:
    data = json.load(file)

for script, date in data.items():

    if datetime.datetime.strptime(date, "%Y-%m-%d").date() != currentDate:
        print(script)
        scriptFile = os.path.join(directory, script)

        process = subprocess.Popen(['python3', scriptFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        data[script] = currentDate.strftime("%Y-%m-%d")

        return_code = process.wait()
        output, error = process.communicate()

        print("Return Code:", return_code)
        print("Error Message:", error.decode())
        print(output.decode())


with open(crontabsFile, "w") as file:
    file.write(json.dumps(data))

counter += 1

with open(counterFile, "w") as file:
    file.write(str(counter))
