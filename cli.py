# cli.py
import os
from pathlib import Path
from colorama import  Fore,Style,init
from models import Pet

init()

def clear():
    os.system('clear')


def header():
    print("╔══════════════════════════╗")
    print("║      PetCare Manager     ║")
    print("╚══════════════════════════╝\n")


def display_pets(pets):
    if not pets:
        print("{Fore.RED}  no pets found.{Style.RESET_ALL}")
        return
    print(f"\n  {'NAME':<15} {'SPECIES':<10} {'AGE':<5} {'WEIGHT':<8}")
    print(f"  {'─'*15} {'─'*10} {'─'*5} {'─'*8}")
    if isinstance(pets,dict):
        for pet in pets:
            print(f"  {pets[pet].name:<15} {pets[pet].species:<10} {pets[pet].age:<5} {pets[pet].weight:<8}")
    elif isinstance(pets,list):
        for pet in pets:
            print(f"  {pet.name:<15} {pet.species:<10} {pet.age:<5} {pet.weight:<8}")

    print()


def add_pet(manager):
    print(f"\n{Fore.CYAN}── Add Pet ──{Style.RESET_ALL}")
    try:
        name    = input("  name:    ").strip()
        print("  species: dog / cat / rabbit / bird / hamster")
        species = input("  species: ").strip().lower()
        age     = int(input("  age:     ").strip())
        weight  = int(input("  weight:  ").strip())
        pet = Pet(name=name, species=species, age=age, weight=weight)
        pet = manager.add(pet)
        print(f"\n {Fore.GREEN}  '{pet.name}' added successfully!{Style.RESET_ALL}")

    except ValueError as e:
        print(f"\n {Fore.RED}  {e}{Style.RESET_ALL} ")


def list_pets(manager):
    print(f"\n{Fore.CYAN}── All Pets ──{Style.RESET_ALL}")
    display_pets(manager.all())


def search_pet(manager):
    print(f"\n{Fore.CYAN}── Search ──{Style.RESET_ALL}")
    query   = input("  search (name= ,species= etc ): ").strip()
    search_keys=query.strip().split(",")
    dict_={ search_key.strip().split("=")[0]:search_key.strip().split("=")[1] for search_key in search_keys}
    results = manager.find(**dict_)
    display_pets(results)


def update_pet(manager):
    print(f"\n{Fore.CYAN}── Update Pet ──{Style.RESET_ALL}")
    try:
        name = input("  pet name: ").strip()
        result=manager.find(name=name) 
        if not result:
            raise ValueError(f"{name} pet is not found")
        pet=result[0]
        print(f"Pet is found : {pet}")
        print(f"change the attributes you want ,others just skip them : ")
        dict_={}
        dict_["name"]  = input("  name:    ").strip()
        print("  species: dog / cat / rabbit / bird / hamster")
        dict_["species"] = input("  species: ").strip().lower()
        age     = input("  age:     ").strip()
        weight  = input("  weight:  ").strip()
        dict_["age"]= int(age) if age else None
        dict_["weight"]= int(weight) if weight else None
        kwargs={}
        for attr in dict_:
           if dict_[attr]:
               kwargs[attr]=dict_[attr]		
        manager.update(name,**kwargs)
        print(f"{Fore.GREEN}{name} is updated successfuly{Style.RESET_ALL}")
    except ValueError as e:
        print(f"{Fore.RED}Error : {e}{Style.RESET_ALL}")


def delete_pet(manager):
    print(f"\n{Fore.CYAN}── Delete Pet ──{Style.RESET_ALL}")
    try:
        name = input("  pet name: ").strip()
        pet  = manager.delete(name)
        print(f"\n {Fore.GREEN}  '{pet.name}' deleted.{Style.RESET_ALL}")
    except ValueError as e:
        print(f"\n  {Fore.RED} {e}{Style.RESET_ALL}")

def export_csv(manager):
    print(f"\n {Fore.CYAN} export csv{Style.RESET_ALL}")
    try:
        file=input("\n Enter the name of file or skip for default name (pets.csv)  : ")
        if not file:
            file='pets.csv'
        path=Path(file)
        manager.export_csv(path)
        print(f"{Fore.GREEN}data exported successfuly to {path}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Error : {e}{Style.RESET_ALL}")

def show_stats(manager):
    print(f"\n{Fore.CYAN}── Stats ──{Style.RESET_ALL}")
    stats = manager.stats()
    if not stats:
        print("  no pets yet.")
        return
    print(f"  total pets:    { stats['total']}")
    print(f"  average age:   {stats['avg_age'] +' years' if stats['avg_age'] else '-'}")
    print(f"  youngest:      {stats['youngest'].name if stats['youngest'] else '-'} ({stats['youngest'].age if stats['youngest'] else '-' })")
    print(f"  oldest:        {stats['oldest'].name if stats['oldest'] else '-'} ({stats['oldest'].age if stats['oldest'] else '-'  })")
    print(f"\n  species breakdown:")
    if stats['total']>0:
        for species, count in stats['species'].items():
            print(f"    {species:<12} → {count}")

    else:

        print("  (-)")


def menu():
    print("\n  1. Add pet")
    print("  2. List all pets")
    print("  3. Search")
    print("  4. Delete pet")
    print("  5. Stats")
    print("  6. Update")
    print("  7. Export ")
    print("  0. Exit\n")
    return input("  → ").strip()
