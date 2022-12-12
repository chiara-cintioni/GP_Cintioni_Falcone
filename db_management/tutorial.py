# this command prints Hello World!
print("Hello World!")

# these commands print:
# Hello,
# World!
# print("Hello,")
# print("World!")

# returns the sum of x and y
def somma(x,y):
    return x+y
# it's out of the scope of the function, so it works
# print(somma(1,2))

# def somma(x, y):
# return x+y
# doesn't work because it's not separated with spaces

# these are different variables declarations, Python is case sensitivd
pippo = "Pippo"
Pippo = "Pippo"

#prints the type of a variable
# print(type(Pippo))

# 3 types of numbers: int, float & complex
# + can be used to concatenate strings
print(pippo+Pippo)

# can't concatenate a string to an int
nome = "Denise"
eta = 21
#print(nome+" "+eta)
eta = "21"
# now it works because eta is a string
# print(nome+" "+eta)

# True and False need to have the firs letter capitalized or it's not recognized as a boolean
# boolean_false = False
# boolean_true = True

# takes an input and saves it in a variable
# the input is considered a string: "1982" is different from 1982
# word = input("Insert a word ")
# print("The word you gave as an input is: " + word)

# convert string to int
# num = input("Insert a number: ")
# double = int(num) * 2
# print("The double of the number you gave is: "+str(double))
# to convert we have: float(), str(), bool() & int()

# simple calculator
# first_number = float(input("Insert the first number to sum "))
# second_number = float(input("Insert the second number to sum "))
# sum = first_number + second_number
# print("The sum of the numbers is: "+str(sum))

# strings:
str1 = "Hi I'm a string!"
str2 = str1.upper()
print(str1+" "+str2)

# returns the index of the first occurrence of the value we pass
# these methods create a new string, because strings are immutable
str1.find("I")
str3 = str1.replace("I'm","You're")
print(str3)

# in operator: returns a bool value
string_to_check = "Ricky and Gina love each other, change my mind!"
print('Gina' in string_to_check)

# math operators
# 2 kind of divisions: / & //
division1 = 7/5 #gives all numbers
division2 = 7//5 #returns only int
module = 7%5 # resto divisione
print("First division: "+str(division1)+", Second division: "+str(division2)+", module: "+str(module))
# exponent operator: **
print(2**4) # 16
x = 4
x = x + 3
x += 3 # equal to the one above
print(x)

x = 10 + 3 * 2
print(x)
# operator precedence: can change it with ()
x = (10 + 3) * 2
print(x)

# comparison operators
x = 3 > 2
print(x)
# other operators: >=, <, <=, ==, !=

#logical operators
price = 25
print(price > 10 and price < 30)
# others: or, not (before trhe expression
# 3 logical operators: and, or & not

#if statements
tempearature = 35
#the indentation represents a block of code
if tempearature > 30:
    print("Today is a hot day")
else:
    print("Today is a good day")
# after if statement and else we have to use :
# to represent a block we use indentation
# to have another if after the else we use elif
if tempearature > 30 and tempearature < 35:
    print("Today is a hot day")
elif tempearature == 35:
    print("The temperature is: 35")

#exercise
#weight = input("Weight: ")
#type = input("(K)g or (L)bs: ")
#type = type.upper()
#if(type == "K"):
#   print("Weight in Lbs is: "+ str(int(weight)/0.4536))
#elif type == "L":
#    print("Weight in Kg is: "+ str(int(weight)*0.4536))
# better than the tutorial guy :)

#while
i = 1
while i <= 5:
    print(i)
    i += 1
i = 1
#1_000 used to separate the number. Doesn't affect anything at all
#while i <= 1_000:
#    print(i)
#    i += 1

# print an expression
i = 1
#prints i-numbers of *
while i <= 10:
    print(i * '*')
    i += 1

# lists

names = ["Nate","Bob","Luke","Michael","Marius","Artem","Vyn"]
print(names) #prints the names (with [])
print(names[0]) # prints the first element
print(names[-1]) # prints the LAST element
names[0] = "Nathan"
print(names[0])
# list_name[start_index:end_index] gets part of the list
partial_list = names[4:7]
print(partial_list)

numbers = [1,2,3,4,5]
numbers.append(6) #adds an element at the END of the list
print(numbers)
# you can insert strings in an int/float list
numbers.insert(0, "ciao")
print(numbers)
numbers.remove("ciao") #removes the VALUE
print(numbers)
print(1 in numbers)
numbers.clear() #clears the list (it's an empty list now)
print(numbers)
len(numbers) # returns the numbers of elements in the list

# for
numbers = [1,2,3,4,5]
#item is a variable, like i, that goes through all the element of the list numbers
for item in numbers:
    print(item)

#generate a sequence of numbers
numbers = range(5)
print(numbers) # prints the range
#to print the single numbers we need a for
#prints the element from 0 to 4 (like arrays it starts from 0)
for item in numbers:
    print(item)

numbers = range(5,10)
#prints numbers from 5 to 9
for item in numbers:
    print(item)

numbers = range(5,10,2) #2 is the number of "jumps"
#it skips every 2 numbers
for item in numbers:
    print(item)
# we can call the range in the for, without a variable

#tuples: lists but immutable
# uses () instead of []
numbers = (1,2,3)
#numbers[0] doesn't work for tuples
numbers.count(3) #returns the number of times the value inside are present
numbers.index(3) #returns the first occurrence of the value
numbers.__len__() #magic methods?

#classes and objects
#creates a class with a constructor that takes a name and age and inserts them in the object it's creating
class my_first_class():
    def __init__(self,name,age):
        self.name = name
        self.age = age

    #function of my_first_class
    def myfunc(self):
        print("Hello my name is " + self.name)

p1 = my_first_class("John",23)
print(p1) #prints the memory address of the object
print(p1.name)
print(p1.age)
p1.myfunc()
#the self parameter is a reference to the current instance of the class