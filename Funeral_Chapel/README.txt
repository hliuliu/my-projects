
Welcome. This is the help file for the Legacy software.


The following will get you started:
Instructions are specific to Windows, I apologize for any inconvience.
.................................................................

Make sure you have Python 2.7 installed. If not, You can install it through this link: https://www.python.org/downloads/
Click on "Download Python 2.7.10" and follow the instructions.

After downloading Python, open up the command prompt (Windows) or Terminal (Linux/UNIX).
Type "python". You should see the Python interprter display.

If instead, you see the following message: "'python' is not recognized as an internal or external command, operable program or batch file." on Windows,
this means that there are 2 possibilities:
1. The installation was unsuccessful.
2. The python directory was not added to the path variable.

Suppose Option 2 is the issue. Then do the following:
1. Click on the start menu.
2. Right click on Computer.
3. Select Properties.
4. Goto Advanced System Settings -> Environment Variables
5. Under Systems Variables, double click on Path.
6. In the Variable Value field, add the path to python to the end. Be sure that paths are separated with a semicolon.
7. Click OK -> OK.
8. now restart the Command Prompt. type python again. The issue should be resolved.

Type 'exit()' to leave the python interpreter.

cd to the directory that contain the included file, legacyexe.py . Syntax is cd path/to/directory/containing/the_file

Now type "python legacyexe.py" and press enter.

Following the instructions carefully.

To select the default option, simply type nothing and press enter.
when the program prompts for a .csv filename, If the input corresponds to an existing file, It will ask whether or not you want to overwrite it.

Thank You for using this software. I will provide more documentation if needed.
