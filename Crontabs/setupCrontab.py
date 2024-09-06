import os
from Modules import Utils

if __name__ == "__main__":

    directory = os.path.dirname(os.path.abspath(__file__))
    every5Min = "*/5 * * * *"
    everyMin = "*/1 * * * *"
    dailyPrograms = os.path.join(directory, "Crontab.py")

    otherInstructionsList = [
        "export DISPLAY=:1",
        "export XAUTHORITY=/run/user/1001/gdm/Xauthority",
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

    Utils.addNewCronTasks(
        [
            f"{every5Min} {otherInstructions} python3 {dailyPrograms} >> {output} 2>&1",
            f"{everyMin} {otherInstructions} python3 {backgroundChanger} >> {output} 2>&1",
        ]
    )

"""
*/5 * * * * export DISPLAY=:1 && export XAUTHORITY=/run/user/1001/gdm/Xauthority && export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/snap/bin && python3 /absolutePath/Crontabs/Crontab.py >> /absolutePath/Crontabs/output.log 2>&1
*/1 * * * * export DISPLAY=:1 && export XAUTHORITY=/run/user/1001/gdm/Xauthority && export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/snap/bin && python3 /absolutePath/Crontabs/BackgroundChanger.py >> /absolutePath/Crontabs/output.log 2>&1
"""
