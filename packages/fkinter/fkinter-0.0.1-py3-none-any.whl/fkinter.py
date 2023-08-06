import os
from colorama import Fore, Back
import platform

reset = lambda: print(Fore.RESET)

def figma_to_tkinter(url, token):
    if url != "" and "www.figma.com" in url:
        print("[>>>] URL is valid!\n\n")
        if token != "" and "figd_" in token:
            print(Fore.BLUE + "[***] Generating project...")
            os.system(f'tkdesigner "{url}" "{token}"')
            os.system("cls")
            print("[###] Project successfully generated!")
            reset()
        else:
            print(Fore.RED + "TOKEN ERROR!!!")
            reset()
            exit(0)
    else:
        print(Fore.RED + "URL ERROR!!!")
        reset()
        exit(0)