"""
               /$$           /$$                       /$$
              |__/          |__/                      | $$
 /$$$$$$/$$$$  /$$ /$$$$$$$  /$$  /$$$$$$   /$$$$$$  /$$$$$$
| $$_  $$_  $$| $$| $$__  $$| $$ /$$__  $$ /$$__  $$|_  $$_/
| $$ \ $$ \ $$| $$| $$  \ $$| $$| $$  \ $$| $$  \ $$  | $$
| $$ | $$ | $$| $$| $$  | $$| $$| $$  | $$| $$  | $$  | $$ /$$
| $$ | $$ | $$| $$| $$  | $$| $$| $$$$$$$/|  $$$$$$/  |  $$$$/
|__/ |__/ |__/|__/|__/  |__/|__/| $$____/  \______/    \___/
                                | $$
                                | $$
                                |__/

TO-DO:
    MAKE CUSTOM FILE

    DELETE/READ/WRITE PROTECTION

    OPTIONAL:
    --------
    ANALYZER -- NLP
    OTHER STREAMS
"""
import os
import sys
import configparser
from minipot import HoneyPot

DEFAULT_CONFIG_FILEPATH = './minipot.example.ini'

print("\n\n"
      "               /$$           /$$                       /$$\n"
      "              |__/          |__/                      | $$\n"
      " /$$$$$$/$$$$  /$$ /$$$$$$$  /$$  /$$$$$$   /$$$$$$  /$$$$$$\n"
      "| $$_  $$_  $$| $$| $$__  $$| $$ /$$__  $$ /$$__  $$|_  $$_/\n"
      "| $$ \ $$ \ $$| $$| $$  \ $$| $$| $$  \ $$| $$  \ $$  | $$\n"
      "| $$ | $$ | $$| $$| $$  | $$| $$| $$  | $$| $$  | $$  | $$ /$$\n"
      "| $$ | $$ | $$| $$| $$  | $$| $$| $$$$$$$/|  $$$$$$/  |  $$$$/\n"
      "|__/ |__/ |__/|__/|__/  |__/|__/| $$____/  \______/    \___/\n"
      "                                | $$\n"
      "                                | $$\n"
      "                                |__/\n"
      "\nA simple honey pot for reverse tcp shells, netcat reverse shell attacks ...\n"
      "DEFAULTS:\n"
      "\tconfig file:   \t/etc/minipot.example.ini\n"
      "\tlogfile path:  \t./minipot.log\n"
      "\tports watched: \t8080,8888,9999,3306 "
      )

# Options
while True:
    print("\nSetup config file:\n"
          "\t1. Use Existing config file\n"
          "\t2. Make your own config file\n"
          "\t3. View example\n"
          "\t4. Use default\n"
          "\nEnter choice: ", end="")
    ch = input()
    if ch == '1':
        config_filepath = input()
        if not os.path.isfile(config_filepath):
            print("Config file does not exist\n")
            continue
        break

    elif ch == '2':
        print("Enter the file name (extension is self generated): ", end="")
        file_name = input()

        f = open(file_name + '.ini', "w+")
        f.write('[default]\n')
        print("Enter the ports (comma-separated without spaces): ", end="")
        ports_input = input()
        f.write('ports=' + ports_input + '\n')
        print("Enter the host (if hostname doesnt exist 0.0.0.0 will be taken by de facto): ", end="")
        host_input = input()
        f.write('host=' + host_input + '\n')
        print("Enter the logfile_path (if logfile cannot be created here, ./minipot.log will be taken by de facto): ", end="")
        logfile_input = input()
        f.write('logfile=' + logfile_input + '\n')
        f.close()

        print(file_name + ".ini has been created successfully")

    elif ch == '3':
        print("File name: minipot.example.ini [ format *.ini ] \n ")
        os.system('cat ./minipot.example.ini')

    else:
        config_filepath = DEFAULT_CONFIG_FILEPATH
        break

config = configparser.ConfigParser()
config.read(config_filepath)

ports = config.get('default', 'ports', raw=True, fallback='8080,8888,9999,3306')
host = config.get('default', 'host', raw=True, fallback='0.0.0.0')
logfile = config.get('default', 'logfile', raw=True, fallback='minipot.log')

ports_list = []
try:
    ports_list = ports.split(',')
except Exception:
    print("Error parsing ports: %s Exiting ... ", ports)
    sys.exit(1)

print("\nEnable verbosity: [Y/n]? ", end='')
if input() in ['y', 'Y', 'yes', 'Yes']:
    verbose = True
else:
    verbose = False

print("\nSHELL SIMULATION:"
      "\n-----------------"
      "\n\tOpens a shell simulator and sends a part of the output (if generated)\n"
      "\tBEWARE: this shell simulation can be a potential threat\n"
      "\tDeveloper is not responsible for the loss data\n"
      "\tChoose the option at your own risk\n"
      "\n\tEnable shell simulation [Y/n]? ", end='')
if input() in ['y', 'Y', 'yes', 'Yes']:
    rev_shell_enable = True
else:
    rev_shell_enable = False

print("\n\nPorts: ", ports_list)
HoneyPot(ports_list, logfile, host, verbose, rev_shell_enable).run()
