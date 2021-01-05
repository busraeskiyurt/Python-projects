  
number1=int(input("please enter to number for learn your want number if your number is prime or not.")) #ı wanted you enter a number here  
counter=0  #  I create a variable ı wanted you enter a number here 

for i in range(2, number1+1):            # If the number is prime, the counter must be 1.
    if number1% i == 0 :
        
        counter = counter + 1

if counter == 1:                         
    print("this number is prime")   here if counter is one , print; this number is prime.and if not, print; this number isn't prime. 
else :
    print("this number isn't prime")
