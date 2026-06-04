from pathlib import Path
from models import Pet
import json 
import statistics 




class PetManager:

	def __init__(self,file='pets.json'):
		self.file=Path(file)
		self._pets=[]
		self._load()


	def _load(self):
		if self.file is None:
			raise ValueError("File is None")
		try:
			with open(self.file,'r') as f:
				data=json.load(f)
				for pet in data:
					self._pets.append(Pet.from_dict(pet))
		except (FileNotFoundError,json.JSONDecodeError,PermissionError) as e:
			print(f"Error : {e} ")
			self._pets=[]				

	def _save(self):
		if self.file is None:
			raise ValueError("file is None")
		try:
			with(self.file,'w') as f:
				data=json.load(f)
				for pet in self._pets:
					if pet.name not in data: 
						json.dump(pet.as_dict(),f,indent=4)
		except (FileNotFoundError,PermissionError) as e:
                        print(f"Error : {e} ")


	#CRUD OPERATIONS 
	def add(self,pet):
		if not isinstance(pet,Pet):
			raise ValueError("pet is not instance of Pet class")
		
		if pet not in self._pets:
			self._pets.append(pet)
		self._save()
		return pet

	def all(self):
		return self._pets

	def find(self,**kwargs):
		match=True
		result=[]
		for pet in self._pets:
			for  key,value in kwargs.items():
				if not pet.__dict__.get(key)==value:
					match=false
			if match:
				result.append(pet)
			match=True
		return  result if result else None

	
			
	def delete(self,name):
		for index,pet in enumerate(self._pets):
			if pet.name.casefole()==name.casefold():
				pet=self._pets.pop(index)
				self._save()
		return pet if pet else None

	def stats(self):
		ages=[pet.age for pet  in self._pets]
		species=[pet.species for pet  in self._pets]
		return {
		"total" : len(self.pets),
		"species":species,
		"avg_age":statistics.mean(ages),
		"youngest":min(self._pets,key=lambda pet:pet.age),
		"oldest":max(self._pets,key=lambda pet:pet.age)
}
		 




	def __iter__(self):
		return iter(self._pets) 
	def __len__(self):
		return len(self._pets)

