import random
'''
1 for snake     snake vs water = snake win
-1 for water     water vs gun = water win
0 for gun       gun vs snake = gun win
'''
computer = random.choice([-1, 0, 1])
youstr = input("Enter your choice: ")
youDict ={"s":1,"w": -1,"g":0}
reverseDict ={1: "Snake", -1: "Water", 0: "Gun"}

you = youDict[youstr]
#By now we have 2 numbers (variables), you and computer

print(f"You chose {reverseDict[you]}\nComputer chose {reverseDict[computer]}")
if (computer == you):
    print("It a draw")
else:
    if(computer == -1 and you == 1):
        print("You win!")
        
    elif(computer == -1 and you == 0):
        print("You lose!")
        
    elif(computer == 1 and you == -1):
        print("You lose!")
        
    elif(computer == 1 and you == 0):
        print("You win!")
        
    elif(computer == 0 and you == -1):
        print("You win!")
        
    elif(computer == 0 and you == 1):
        print("You lose!")
        
    else:
        print("something went wrong")
    

