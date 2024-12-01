"""This script manages the execution of multiple bots in the background.
 It first checks if each bot is already running, terminates it if necessary using its PID,
  and then restarts the bot.If you only want to kill background process you have
  to comment line no 35"""

import os
import subprocess


def run_all_scripts_in_background(directory):
    # Get a list of all Python files in the specified directory
    python_files = [
        "sellbot.py",
        "telegrambot_function.py",
        "buy_sell_notification_bot.py",
        "pulse_tracker_notification_bot.py",
    ]

    for py_file in python_files:
        # Creating the full path to the script
        file_path = os.path.join(directory, py_file)

        # Check if the script is already running and terminate it
        try:
            # Find the process ID (PID) of the running script
            pid = subprocess.check_output(["pgrep", "-f", file_path]).decode().strip()
            # Terminate the process
            subprocess.run(["sudo", "pkill", "-f", file_path])
            print(file_path)
            print(f"Terminated existing process: {pid}")
        except subprocess.CalledProcessError:
            # No existing process found
            print("No active process found")

        # Run the Python file as a subprocess using nohup
        print(f"Running {file_path} in background...")
        subprocess.Popen(["nohup", "python", file_path, "&"], preexec_fn=os.setpgrp)


# Specify the directory containing the Python scripts
directory = os.getcwd()

# Run all scripts in the specified directory
run_all_scripts_in_background(directory)
