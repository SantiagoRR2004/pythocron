import os
import subprocess


directory = os.path.dirname(os.path.abspath(__file__))
every5Min = "*/5 * * * *"
everyMin = "*/1 * * * *"
dailyPrograms = os.path.join(directory, "Crontab.py")

# We check that the file exists and give an error message if it does not
if not os.path.exists(dailyPrograms):
    raise NameError(f"File {dailyPrograms} not found")

backgroundChanger = os.path.join(directory, "BackgroundChanger.py")

if not os.path.exists(backgroundChanger):
    raise NameError(f"File {backgroundChanger} not found")

output = os.path.join(directory, "output.log" )


cronTask = f"""{every5Min} python3 {dailyPrograms} >> {output} 2>&1
{everyMin} python3 {backgroundChanger} >> {output} 2>&1"""


command = f"echo '{cronTask}' | crontab -"
subprocess.call(command, shell=True)


"""
*/5 * * * * python3 /absolutePath/Crontabs/Crontab.py >> /absolutePath/Crontabs/output.log 2>&1
*/1 * * * * python3 /absolutePath/Crontabs/BackgroundChanger.py >> /absolutePath/Crontabs/output.log 2>&1
"""
