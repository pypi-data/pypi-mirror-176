import time
import team13hackertype.hackertype as hackertype
import team13hackertype.penetrate as penetrate
import sys

def display_help():
    print('''
    hackertype - Starts listening for keyboard presses. On key press, print out 'speed' amount of characters from a sample document written in the 'language' coding language.

    Parameters
    ----------
    language : str
        The coding language of the hacker type to be printed.
        Supported values are python and java
    speed : int, optional
        The number of characters to print out on a single key
        press. (Default is 5.)



    penetrate - simulate a system penetration in your command line.

    Parameters 
    ----------
    language : str
        The coding language of the hacker type to be printed.
        Supported values include python and java. See hackertype.py.

    text: str, optional 
        The text shown in the banner (default "DARKWEB"), suggested maximum length is 7 characters.

    
    -h - display this message
    ''')

def main(argv):
    functionMap = {
        "hackertype": hackertype.hackertype,
        "penetrate": penetrate.penetrate,
        "-h": display_help
    }
    if (len(argv) == 0):
        display_help()
        sys.exit(1)
    command = argv[0]
    if (command in functionMap.keys()):
        try:
            functionMap[command](*argv[1:])
            # TODO: add string to int casting for parameters
            time.sleep(1)  # gives time for threads to resolve
        except Exception as e:
            print(f"Incorrect use of command: {command}")
            print(str(e))
            sys.exit(1)
    else:
        print("Command not found in package")
        sys.exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])
