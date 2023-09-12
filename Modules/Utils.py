import subprocess

def runTerminal(command):
    try:
        completed_process = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
