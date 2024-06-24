import json
import subprocess
import datetime
import os

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env = os.environ.copy()
env['PYTHONPATH'] = path
env['PATH'] = os.pathsep.join([path, os.environ.get('PATH', '')])

directory = os.path.dirname(os.path.abspath(__file__))
counterFile = os.path.join(directory, "counter.txt")
crontabsFile = os.path.join(directory, "Crontabs.json")


try:
    with open(counterFile, "r") as file:
        counter = int(file.read())
except FileNotFoundError:
    counter = 0


currentDate = datetime.date.today()

scripts = {"setupCrontab.py":"2023-01-01",}

# Now we read the file if it exists
data = {}
if os.path.exists(crontabsFile):
    with open(crontabsFile, "r") as file:
        data = json.load(file)

scripts.update(data)
data = scripts

for script, date in data.items():

    if datetime.datetime.strptime(date, "%Y-%m-%d").date() != currentDate:
        print(script)
        scriptFile = os.path.join(directory, script)

        process = subprocess.Popen(['python3', scriptFile], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)

        return_code = process.wait()
        output, error = process.communicate()

        print("Return Code:", return_code)
        print("Error Message:", error.decode())
        if error.decode() == "": # We have executed today if it works
            data[script] = currentDate.strftime("%Y-%m-%d")
        print(output.decode())


with open(crontabsFile, "w") as file:
    file.write(json.dumps(data))

counter += 1

with open(counterFile, "w") as file:
    file.write(str(counter))











