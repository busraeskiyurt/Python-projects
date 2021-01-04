a =(int(input("Enter the number to  taken the  factorial")))  
counter=a
resault=1
for i in range(a):
    resault*=a-(a-counter)
    counter-=1
print(resault)
  
