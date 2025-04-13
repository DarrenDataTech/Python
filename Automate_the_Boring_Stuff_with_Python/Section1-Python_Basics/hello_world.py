# This Program says hello to the world and asks for your name and age
# This is a comment. It is ignored by the Python interpreter.

print ("Hello World!")
print ("What is your name?") # ask for their name

myName = input() # input() is a function that takes user input

print ("It's good to meet you, " + myName + ".")
print ("The length of your name is:")
print (len(myName)) # length() is a function that returns the length of a string)

print ("What is your age?") # ask for their age
myAge = input()
print ("You will be " + str(int(myAge) + 1) + " in a year.")