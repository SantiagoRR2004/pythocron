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

def addNewCronTasks(newTasks:list) -> None:
    """
    This function will add new tasks to the crontab
    without deleting the old ones.

    Args:
        newTasks (list): A list of strings with the new tasks.

    Returns:
        None
    """
    result = subprocess.run(['crontab', '-l'], capture_output=True, text=True, check=True)

    if not result.stderr:
        oldTasks = result.stdout.split("\n")
        for task in newTasks:
            if task not in oldTasks:
                runTerminal(f"(crontab -l; echo '{task}') | crontab -")
