#
#
#


import random
üstlimit=50
print(------------------------------)
print(      SAYI TAHMiN OYUNU       )
print(------------------------------)

altlimit=1
print("-eger dogru bildiysem d tusuna sayiyi azaltmam gerekiyorsa a tusuna arttirmam gerekiyorsa t tusuna bas-")
tahminsayi= random.randrange(altlimit,üstlimit)
print("benim tahminim:  ", tahminsayi)
y =input("dogrumu")
d = ("d")
a = ("a")
t = ("t")


while True:

    if y=="q" or y=="Q":
        print("çikis yaptiniz.")
        break


    elif y == "d"  :
        print("tebrikler sayiyi dogru bildin..")
        break
        
    elif y == "a" :
                    
        üstlimit= (tahminsayi - 1)
        tahminsayi= random.randrange(altlimit,üstlimit)
        print(tahminsayi)
        y =input("dogru mu?")
                                
                    
    elif y == "t" :
        altlimit= (tahminsayi + 1)
        tahminsayi= random.randrange(altlimit,üstlimit)
        print(tahminsayi)
        y =input("dogru mu?")
    else :
        print("lütfen a, d veya t tusuna basin")
                   
