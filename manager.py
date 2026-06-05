"""Pet Manager"""
import json
import statistics
import csv
from pathlib import Path
from models import Pet
class PetManager:
    """PetManager class for  managing pets"""

    def __init__(self, file="pets.json"):
        self.file = Path(file)
        self._pets = {}
        self._load()

    def _load(self):
        """loading pets from file"""
        if self.file is None:
            raise ValueError("File is None")
        try:
            with open(self.file, "r",encoding="utf-8") as f:
                data = json.load(f)
                for pet in data:
                    self._pets[pet]=Pet.from_dict(data[pet])
        except (FileNotFoundError, json.JSONDecodeError, PermissionError) as e:
            print(f"Error : {e} ")
            self._pets = {}

    def _save(self):
        """saving pets in file"""
        if self.file is None:
            raise ValueError("file is None")
        try:
            with open(self.file, "r",encoding="utf-8") as f:

               data = json.load(f)
        except (FileNotFoundError,json.JSONDecodeError, PermissionError):
            data={}
        try:
            with open(self.file,"w",encoding="utf-8") as f:
     
                dict_={self._pets[pet].name:self._pets[pet].as_dict() for pet in self._pets}
                json.dump(dict_, f, indent=4)
        except (FileNotFoundError, PermissionError) as e:
            print(f"Error : {e} ")

    # CRUD OPERATIONS
    def add(self, pet):
        """adding pet into list and also into file"""
        if not isinstance(pet, Pet):
            raise ValueError("pet is not instance of Pet class")

        if pet.name  not in self._pets:
            self._pets[pet.name]=pet
            self._save()
            return pet
        raise ValueError(f"{pet.name} already existed")    

    def update(self,Updatedname,**kwargs):
        """ update the pet by name  """
        pet=self.find(name=Updatedname)[0]
        for key,value in kwargs.items():
            pet.__dict__[key]=value
        self.delete(Updatedname)
        self.add(pet)
        self._save()            
    def all(self):
        """returning all pets"""
        return self._pets

    def find(self, **kwargs):
        """finding pets with kwargs"""
        match = True
        result = []
        for pet in self._pets:
            for key, value in kwargs.items():
                if not self._pets[pet].__dict__.get(key) ==type(self._pets[pet].__dict__.get(key)) (value):
                    match = False
            if match:
                result.append(self._pets[pet])
            match = True
        return result if result else None

    def delete(self, name):
        """deleting pets with their names"""
        iter_=self._pets
        for pet in iter_:
            if iter_[pet].name.casefold() == name.casefold():
                poped_pet = self._pets.pop(pet)
                self._save()
                return poped_pet
        raise ValueError(f"No pet found with the name {name}")
    def stats(self):
        """returning stats from _pets"""
        ages = [self._pets[pet].age for pet in self._pets]
        species = {pet.species : len([p for p in self._pets if p.species==self._pets[pet].species ])  for pet in self._pets}
        return {
            "total":    len(self._pets),
            "species":  species if species else None,
            "avg_age":  statistics.mean(ages) if len(self._pets)> 0 else None,
            "youngest": min(self._pets, key=lambda pet: self._pets[pet].age) if len(self._pets)>0 else None,
            "oldest":   max(self._pets, key=lambda pet: self._pets[pet].age) if len(self._pets)>0 else None ,
        }

    def export_csv(self,file=None):
        
        with open(file,"w",encoding="utf-8") as f:
            writer= csv.writer(f)
            writer.writerow(["name","species","age","weight","created_at"])
            for pet in self._pets:
                writer.writerow([
                       self._pets[pet].name,
                       self._pets[pet].species,
                       self._pets[pet].age,
                       self._pets[pet].weight,
                       self._pets[pet].created_at
                   ])
            



    def __iter__(self):
        return iter(self._pets)

    def __len__(self):
        return len(self._pets)
