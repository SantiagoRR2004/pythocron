import os
import subprocess


directory = os.path.dirname(os.path.abspath(__file__))
time = "*/5 * * * *"
program = os.path.join(directory, "Crontab.py")

# We check that the file exists and give an error message if it does not
if not os.path.exists(program):
    raise NameError(f"File {program} not found")



output = os.path.join(directory, "output.log" )


cronTask = f"{time} python3 {program} >> {output} 2>&1"


command = f"echo '{cronTask}' | crontab -"
subprocess.call(command, shell=True)


"""
*/5 * * * * python3 /absolutePath/Crontabs/Crontab.py >> /absolutePath/Crontabs/output.log 2>&1
 
"""
