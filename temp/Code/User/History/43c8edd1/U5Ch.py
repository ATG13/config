class Dog:
    species = "Canine"  # Class attribute (shared by all dogs)
    number_of_dogs = 0 # Class attribute to count dogs

    def __init__(self, name, breed):
        self.name = name     # Instance attribute
        self.breed = breed    # Instance attribute
        Dog.number_of_dogs += 1 # Increment the dog count

    def bark(self):
        print("Woof!")

my_dog = Dog("Buddy", "Golden Retriever")
another_dog = Dog("Max", "German Shepherd")

print(my_dog.name)        # Accessing instance attribute
print(Dog.species)       # Accessing class attribute (can also be accessed via my_dog.species)
print(Dog.number_of_dogs) # Accessing class attribute to count dogs

Dog.bark(my_dog)