# petcare.py
from cli import *
from manager import PetManager


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
        elif choice == '0':
            print("\n  goodbye! 🐾\n")
            break
        else:
            print("\n  ❌ invalid choice")

        input("\n  press enter to continue...")


if __name__ == '__main__':
    main()
