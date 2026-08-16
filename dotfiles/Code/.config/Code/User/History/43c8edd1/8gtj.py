class Dog:
    species = "Canine"

    def __init__(self, name):  # Instance method
        self.name = name

    def bark(self):            # Instance method
        print("Woof!")

    @classmethod
    def get_species(cls):      # Class method
        return cls.species

    @staticmethod
    def is_mammal():          # Static method
        return True

my_dog = Dog("Buddy")

my_dog.bark()              # Calling an instance method
print(Dog.get_species())    # Calling a class method
print(Dog.is_mammal())      # Calling a static method
print(my_dog.get_species()) # Calling a class method using instance, but cls is passed as class Dog.