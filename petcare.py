# petcare.py
from colorama  import Fore,Style,init
from cli import *
from manager import PetManager

init()
def main():
    manager = PetManager('pets.json')

    while True:
        clear()
        header()
        choice = menu()

        if choice == '1':
            add_pet(manager)
        elif choice == '2':
            list_pets(manager)
        elif choice == '3':
            search_pet(manager)
        elif choice == '4':
            delete_pet(manager)
        elif choice == '5':
            show_stats(manager)
        elif choice == '6':
            update_pet(manager)
        elif choice == '7':
            export_csv(manager)
        elif choice == '0':
            clear()
            print(f"\n {Fore.CYAN}  goodbye! \n{Style.RESET_ALL}")
            break
        else:
            print(f"\n{Fore.RED}   invalid choice{Style.RESET_ALL}")

        input("\n  {Fore.GREEN}press enter to continue...{Style.RESET_ALL}")


if __name__ == '__main__':
    main()
