

def topla():
    
    sayi1 = int(input(" Sayı1: "))
    sayi2 = int(input(" Sayı2: ")) 
    print( sayi1 + sayi2 )

def cikar():
     sayi1 = int(input(" Sayı1: "))
     sayi2 = int(input(" Sayı2: "))
     print( sayi1 - sayi2) 

def carp():
     sayi1 = int(input(" Sayı1: "))
     sayi2 = int(input(" Sayı2: ")) 
     print (sayi1 * sayi2 )

def bol():
     sayi1 = int(input(" Sayı1: "))
     sayi2 = int(input(" Sayı2: "))
 
     print (sayi1 / sayi2)

def us():
     sayi1 = int(input(" Sayı1: "))
     sayi2 = int(input(" Sayı2: "))
 
     print (sayi1 ** sayi2) 


def kok():
     sayi1 = int(input(" Sayı1: "))
 
     print( sayi1 ** 0.5) 

    



print("1.Toplama,  2.Çıkarma, 3.çarpma,  4.Bölme, 5.üsalma,  6.kökal ")


secim = input("Seçiminiz:):")


   
if secim == '1':
   topla()
 
elif secim == '2':
   cikar()
 
elif secim == '3':
   carp()
   
elif secim == '4':    
    bol()

elif secim == '5':
   us()
 
elif secim == '6':
   kok()
   











   
