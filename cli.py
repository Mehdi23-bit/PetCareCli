# cli.py
import os
from pathlib import Path
from models import Pet

def clear():
    os.system('clear')


def header():
    print("╔══════════════════════════╗")
    print("║   PetCare Manager 🐾     ║")
    print("╚══════════════════════════╝\n")


def display_pets(pets):
    if not pets:
        print("  no pets found.")
        return
    print(f"\n  {'NAME':<15} {'SPECIES':<10} {'AGE':<5} {'WEIGHT':<8}")
    print(f"  {'─'*15} {'─'*10} {'─'*5} {'─'*8}")
    for pet in pets:
        print(f"  {pets[pet].name:<15} {pets[pet].species:<10} {pets[pet].age:<5} {pets[pet].weight:<8}")

    print()


def add_pet(manager):
    print("\n── Add Pet ──")
    try:
        name    = input("  name:    ").strip()
        print("  species: dog / cat / rabbit / bird / hamster")
        species = input("  species: ").strip().lower()
        age     = int(input("  age:     ").strip())
        weight  = int(input("  weight:  ").strip())
        pet = Pet(name=name, species=species, age=age, weight=weight)
        pet = manager.add(pet)
        print(f"\n  ✅ '{pet.name}' added successfully!")

    except ValueError as e:
        print(f"\n  ❌ {e}")


def list_pets(manager):
    print("\n── All Pets ──")
    display_pets(manager.all())


def search_pet(manager):
    print("\n── Search ──")
    query   = input("  search (name= ,species= etc ): ").strip()
    search_keys=query.strip().split(",")
    dict_={ search_key.strip().split("=")[0]:search_key.strip().split("=")[1] for search_key in search_keys}
    results = manager.find(**dict_)
    display_pets(results)


def update_pet(manager):
    print("\n── Update Pet ──")
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
        print(f"{name} is updated successfuly")
    except ValueError as e:
        print(f"Error : {e}")


def delete_pet(manager):
    print("\n── Delete Pet ──")
    try:
        name = input("  pet name: ").strip()
        pet  = manager.delete(name)
        print(f"\n  ✅ '{pet.name}' deleted.")
    except ValueError as e:
        print(f"\n  ❌ {e}")

def export_csv(manager):
    print("\n export")
    try:
        file=input("\n Enter the name of file or skip for default name (pets.csv)  : ")
        if not file:
            file='pets.csv'
        path=Path(file)
        manager.export_csv(path)
        print(f"data exported successfuly to {path}")
    except Exception as e:
        print(f"Error : {e}")

def show_stats(manager):
    print("\n── Stats ──")
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
