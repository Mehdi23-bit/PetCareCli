# cli.py
import os
from manager import PetManager
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
        print(f"  {pet.name:<15} {pet.species:<10} {pet.age:<5} {pet.weight:<8}")
    print()


def add_pet(manager):
    print("\n── Add Pet ──")
    try:
        name    = input("  name:    ").strip()
        print("  species: dog / cat / rabbit / bird / hamster")
        species = input("  species: ").strip().lower()
        age     = int(input("  age:     ").strip())
        weight  = int(input("  weight:  ").strip())
        pet = Pet(name, species, age, weight)
        pet = manager.add(Pet)
        print(f"\n  ✅ '{pet.name}' added successfully!")

    except ValueError as e:
        print(f"\n  ❌ {e}")


def list_pets(manager):
    print("\n── All Pets ──")
    display_pets(manager.all())


def search_pet(manager):
    print("\n── Search ──")
    query   = input("  search (name= ,species= etc ): ").strip()
    search_keys=query.trim().split(",")
    dict_={ search_key.trim().split(":")[0]:search_key.trim().split(":")[1] for search_key in search_keys}
    results = manager.find(dict_)
    display_pets(results)


def delete_pet(manager):
    print("\n── Delete Pet ──")
    try:
        name = input("  pet name: ").strip()
        pet  = manager.delete(name)
        print(f"\n  ✅ '{pet.name}' deleted.")
    except ValueError as e:
        print(f"\n  ❌ {e}")


def show_stats(manager):
    print("\n── Stats ──")
    stats = manager.stats()
    if not stats:
        print("  no pets yet.")
        return
    print(f"  total pets:    {stats['total']}")
    print(f"  average age:   {stats['avg_age']} years")
    print(f"  youngest:      {stats['youngest'].name} ({stats['youngest'].age})")
    print(f"  oldest:        {stats['oldest'].name} ({stats['oldest'].age})")
    print(f"\n  species breakdown:")
    for species, count in stats['species'].items():
        print(f"    {species:<12} → {count}")




def menu():
    print("\n  1. Add pet")
    print("  2. List all pets")
    print("  3. Search")
    print("  4. Delete pet")
    print("  5. Stats")
    print("  0. Exit\n")
    return input("  → ").strip()
