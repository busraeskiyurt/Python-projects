import random
 print(--------------------------------------------)
 print(          SAYI TAHMİN OYUNU       )
 print(--------------------------------------------)
rastgeleSayi = random.randint(1, 100)

tahminSayi = 0
 
while True:
        
    sayi = int(input("1 ile 100 arasında bir sayı giriniz. (Oyundan Çıkmak için 0):"))    # input ile kullanıcıdan 1 ile 100 arasında bir sayı istenecek.
    
    tahminSayi += 1
    
    if(sayi == 0):
        print("Oyundan Çıkış Yaptınız.")
        break                                       # 0 tuşuna basıldığında oyundan çıkış yapıp programı bitiriyor
    
    elif sayi < rastgeleSayi:
        print("Daha Büyük Bir Sayı Giriniz.")
        continue                                 # tahmin ettiğimiz sayı bilgisayarın tahmin ettiği sayıdan küçükse  daha büyük bir sayı giriniz deyip devam ediyor
    
    elif sayi > rastgeleSayi:
        print("Daha Küçük Bir Sayı Giriniz.")
        continue                              # tahmin ettiğimiz sayı bilgisayarın tahmin ettiği sayıdan büyükse  daha küçük bir sayı giriniz deyip devam ediyor
     
    else:
        print("Tebrikler Sayıyı Tahmin Ettiniz! Rastgele sayı = {0}".format(rastgeleSayi))
        
        print("{0} Kerede Sayıyı Tahmin Ettiniz.".format(tahminSayi))
