from colorama import Fore, Back, Style, init
init()

class ConsoleLog():
    def info(text : str):
        print(f"{Fore.BLUE}[INFO] {text}{Style.RESET_ALL}")
        
    def warning(text : str):
        print(f"{Fore.YELLOW}[WARNING] {text}{Style.RESET_ALL}")
        
    def error(text : str):
        print(f"{Fore.RED}[ERROR] {text}{Style.RESET_ALL}")