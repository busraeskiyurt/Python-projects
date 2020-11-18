import random
 
rastgeleSayi = random.randint(1, 100)

tahminSayi = 0
 
while True:
        
    sayi = int(input("1 ile 100 arasında bir sayı giriniz. (Oyundan Çıkmak için 0):"))
    
    tahminSayi += 1
    
    if(sayi == 0):
        print("Oyundan Çıkış Yaptınız.")
        break
    
    elif sayi < rastgeleSayi:
        print("Daha Büyük Bir Sayı Giriniz.")
        continue
    
    elif sayi > rastgeleSayi:
        print("Daha Küçük Bir Sayı Giriniz.")
        continue
    
    else:
        print("Tebrikler Sayıyı Tahmin Ettiniz! Rastgele sayı = {0}".format(rastgeleSayi))
        
        print("{0} Kerede Sayıyı Tahmin Ettiniz.".format(tahminSayi))
