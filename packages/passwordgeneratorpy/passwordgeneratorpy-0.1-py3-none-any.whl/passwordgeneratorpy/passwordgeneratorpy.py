#!/usr/bin/python
def main():

    import random

    passlength = input("How much character do you want in your password ?")
    passlength = int(passlength)

    answerCharsNb = input("Do you want numbers in your password ? (y/n)")
    answerCharsSpecial = input("Do you want special characters in your password ? (y/n)")
    answerCharsCapital = input("Do you want Capital letters in your password ? (y/n)")
    chars=""
    if answerCharsNb == "y":
        if answerCharsSpecial =="y":
            if answerCharsCapital == "y":
                chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890!@#$%^&*()?"
            if answerCharsCapital == "n":
                chars = "abcdefghijklmnopqrstuvwxyz01234567890!@#$%^&*()?"

        if answerCharsSpecial == "n": 
            if answerCharsCapital == "y":
                chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890"
            if answerCharsCapital == "n": 
                chars = "abcdefghijklmnopqrstuvwxyz01234567890"  

    if answerCharsNb == "n":
        if answerCharsSpecial =="y":
            if answerCharsCapital == "y":
                chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
            if answerCharsCapital == "n":
                chars = "abcdefghijklmnopqrstuvwxyz!@#$%^&*()?"

        if answerCharsSpecial == "n":  
            if answerCharsCapital == "y":
                chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
            if answerCharsCapital == "n": 
                chars = "abcdefghijklmnopqrstuvwxyz"
 

    password =  "".join(random.sample(chars,passlength ))
    print (password)
