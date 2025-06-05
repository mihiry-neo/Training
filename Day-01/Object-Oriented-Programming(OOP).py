# Define and use classes

class NeoSOFT():
    def __init__(self, desc):
        self.desc = desc
    def __str__(self):
        return f"NeoSOFT, {self.desc}"
    
neo = NeoSOFT("A CMMI-5 Company")
print(neo)


# Understand __init__, instance and class variables

class NeoEmp():
    dept = "Data-Science"  # Class/Static Variables

    def __init__(self, name, age, empid):
        self.name = name     # Instance Var 1
        self.age = age       # Instance Var 2
        self.empid = empid   # Instance Var 3

    def info(self):
        return f"Name:{self.name}, Age:{self.age}, EmpID:{self.empid}"
    
emp1 = NeoEmp("Mihir", 22, 1001)
emp2 = NeoEmp("Sahil", 23, 1002)

print(NeoEmp.dept)  # Recommended in case of Class-Variable
print(id(NeoEmp.dept))
print(id(emp1.dept))  # Calling a Class Variable using Object is not recommended
print(id(emp2.dept)) 

print("---------------------")
# As all the ID's are same, so Class Variables are common for all instances of the class. 

print(emp1.info())
print(emp2.info())

print("---------------------")
print(id(emp1.name))
print(id(emp2.name))

# As the ID's for the instance variable Name are different for both instances, so Instance Variables are valid for their own instances.


# Create methods inside classes and Use self and object instantiation

class NeoMeet():
    def __init__(self, name, day):
        self.name = name
        self.day = day
    
    def greet(self):
        return f"Hello {self.name}"
    
    def agenda(self):
        return f"On {self.day} we will be discussing about OOPs in Python"
    
    def reschedule(self, new_day):
        self.day = new_day
        return f"The meeting has been rescheduled to {self.day}"
    
meet = NeoMeet("Mihir", "Monday")
print(meet.greet())
print(meet.agenda())
print(meet.reschedule("Wednesday"))


# Learn inheritance and method overriding

# Single Inheritance

class Parent():
    def __init__(self):
        print("In Parent Constructor")
    def disp1(self):
        print("In disp1")

class Child(Parent):
    def disp2(self):
        print("In disp2")

chd = Child()  # Even though the Child has not defined it's own init, it's inheriting it's Parent init method(Constructor)
chd.disp1() #Child can also inherit Parent's other methods
chd.disp2()

print("------------------------")

# Multiple Inheritance

class Father():
    def __init__(self):
        print("In Father Constructor")

    def disp1(self):
        print("In disp1")

class Mother():
    def __init__(self):
        print("In Mother Constructor")

    def disp2(self):
        print("In disp2")

class Child(Father, Mother):
    def __init__(self):
        super().__init__() # Super can be called on Any line
        Mother.__init__(self) # We need to explicitly call second Parent constructor if needed
    def disp3(self):
        print("In disp3")
    

chd2 = Child()
chd2.disp1()
chd2.disp2
chd2.disp3()

print("--------------------------")

# Multilevel Inheritance

class GP():
    def __init__(self):
        print("In Grand Parent Constructor")

    def disp1(self):
        print("In disp1")

class Parent(GP):
    def __init__(self):
        print("In Parent Constructor")

    def disp2(self):
        print("In disp2")

class Child(Parent):
    def __init__(self):
        GP.__init__(self) # In this case, we need to explicitly call second GP constructor if needed
        super().__init__() # Super can be called on Any line
    def disp3(self):
        print("In disp3")
    

chd3 = Child()
chd3.disp1()
chd3.disp2
chd3.disp3()

# Hybrid and Heirarchical Inheritance works the same

print("---------------------")

# Method Overriding

class Weapon():
    def attack(self):
        pass

class Gun(Weapon):
    def attack(self):
        print("Shoot the Gun")

    def fillBullets(self):
        print("Fill back the Bullets")

class Sword(Weapon):
    def attack(self):
        print("Slash with the sword")
    
    def polish(self):
        print("Polish the sword")
    
def perform(obj):
    if isinstance(obj,Gun):  #isinstance is used to check whether the reference object is whether refering to that class or not
        obj.fillBullets()
    if isinstance(obj,Sword):
        obj.polish()
    obj.attack()

gun = Gun()
perform(gun)

sword = Sword()
perform(sword)

