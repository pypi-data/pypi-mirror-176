import os

def message(message):
    return print(message)
def add(num1, num2):
    return num1 + num2
def subtract(num1, num2):
    return num1 - num2
def multiply(num1, num2):
    return num1 * num2
def divide(num1, num2):
    return num1 / num2
def createfolder(foldername):
    return os.system("mkdir " + foldername)
def removefolder(foldername):
    return os.system("rmdir "+ foldername)
def runpython(file):
    os.system("python3 " + file)
def runconsole(command):
    os.system(command)
def forinrange(variable, number, p):
    for variable in range(number):
        print(p)
def echo(message):
    return print(message)
def execute(command, value):
    if command == "p":
        return print(value)
    if command == "exit":
        os.system("exit")
        