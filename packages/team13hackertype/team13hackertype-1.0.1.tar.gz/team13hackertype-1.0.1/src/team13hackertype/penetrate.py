import random
import math
from time import sleep

import pyfiglet
import rich
from rich.console import Console

import src.team13hackertype.hackertype as hackertype
#import hackertype as hackertype


def show_header(con, text="DARKWEB", style="bold green"):
    '''

    Parameters 
    ----------
    con: rich.console
        supplied in penetrate()
    text: str, optional 
        The text shown in the banner (default "DARKWEB"), suggested maximum length is 7 characters.
    style: str, optional
        The style for Console print of emphasized text (default "bold red")
    '''
    banner = pyfiglet.figlet_format(text, font="banner3-D")
    con.print(banner, "Penetrating server firewall in...", style=style)
    for i in range(0, 4):
        sleep(1)
        if (i == 3):
            print("                          ", end="\r")
        else:
            print(str(3-i) + "...", end='\r')


def show_loading_bar(con, loading_bar_speed):
    bar = "|"+" "*10 + "|"
    progress = 0
    loading_bar_char = "█"

    while True:
        if (progress > 10):
            print("                          ", end="\r")
            con.print("SUCCESSFUL", style="bold green")
            break
        else:
            sleep(0.3)
            increment = random.random() * loading_bar_speed
            if math.floor(progress) < math.floor(progress + increment):
                bar = "[" + math.floor(progress+increment) * loading_bar_char + \
                    (10-math.floor(progress+increment)) * "_" + "]"
            progress += increment
            print("{:.2f}".format(min((progress*10), 100)
                                  ) + "%" + bar + str("{:.2f}".format(increment)) + "/s", end='\r', flush=True)


def penetrate(language, text="DARKWEB", loading_bar_speed=1.0, emphasis_style="bold red", notification_style="bold green"):
    '''

    Parameters 
    ----------
    language : str
        The coding language of the hacker type to be printed.
        Supported values include python and java. See hackertype.py.

    text: str, optional 
        The text shown in the banner (default "DARKWEB"), suggested maximum length is 7 characters.

    loading_bar_speed : float, optional 
        The speed of loading bar progress. (default is 1)

    emphasis_style: str, optional
        The style for Console print of emphasized text (default "bold red")
        See: https://rich.readthedocs.io/en/stable/style.html

    notification_style: str, optional
        The style for Console print of emphasized text, used in show_header (default "bold green")
    '''
    con = Console()
    if (len(text) > 7):
        raise UserWarning(
            "Incorrect Display: Text length should be less than 8.")
    try:

        show_header(con, text=text, style=notification_style)

        # loading_bar_speed should be larger than 0
        if (loading_bar_speed <= 0):
            loading_bar_speed = 1.0
        show_loading_bar(con, loading_bar_speed)

        con.print(
            "Admin privileges acquired... Ready to implant virus code... ", style=emphasis_style)

        hackertype.hackertype(language)

        print("\n")
        con.print("\nLogged Out... Successfully implanted",
                  style=notification_style)
        sleep(1)

    except NotImplementedError as e:
        raise e
    except rich.errors.MissingStyle:
        raise ValueError(
            f"style of {notification_style} and/or {emphasis_style} is not supported"
        )

    except Exception as e:
        raise Exception("Unexpected exception", e)


if __name__ == '__main__':
    penetrate('python')
