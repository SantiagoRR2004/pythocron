import os
from modules import Utils

if __name__ == "__main__":

    directory = os.path.dirname(os.path.abspath(__file__))
    every5Min = "*/5 * * * *"
    everyMin = "*/1 * * * *"
    dailyPrograms = os.path.join(directory, "Crontab.py")

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

    # We check that the file exists and give an error message if it does not
    if not os.path.exists(dailyPrograms):
        raise NameError(f"File {dailyPrograms} not found")

    backgroundChanger = os.path.join(directory, "BackgroundChanger.py")

    if not os.path.exists(backgroundChanger):
        raise NameError(f"File {backgroundChanger} not found")

    output = os.path.join(directory, "output.log")

    cronLocation = os.path.join(directory, "runCron.sh")

    Utils.addNewCronTasks(
        [
            f"{every5Min} {otherInstructions} {cronLocation} {dailyPrograms}",
            f"{everyMin} {otherInstructions} {cronLocation} {backgroundChanger}",
        ]
    )

"""
*/5 * * * * export DISPLAY=?? && export XAUTHORITY=?? && export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/snap/bin && python3 /absolutePath/Crontabs/Crontab.py >> /absolutePath/Crontabs/output.log 2>&1
*/1 * * * * export DISPLAY=?? && export XAUTHORITY=?? && export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/snap/bin && python3 /absolutePath/Crontabs/BackgroundChanger.py >> /absolutePath/Crontabs/output.log 2>&1
"""
