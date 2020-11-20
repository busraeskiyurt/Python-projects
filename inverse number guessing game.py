# bilgisayar bir sayı seçiyor ve aklımıza tuttuğumuz sayıyı bulmaya çalışıyor biz de  biglisayar sayıyı bulana kadar ona bulması için yardımcı oluyoruz.

import random           # andom kütüphanesini yüklüyor.
üstlimit=50       
altlimit=1
print(------------------------------)
print(      SAYI TAHMiN OYUNU       )
print(------------------------------)
print("-eger dogru bildiysem d tusuna sayiyi azaltmam gerekiyorsa a tusuna arttirmam gerekiyorsa t tusuna bas-")
tahminsayi= random.randrange(altlimit,üstlimit)               #üstlimit ve altlimit sayıları arasında bir sayı seçiyor.
print("benim tahminim:  ", tahminsayi)                  # benim tahminim deyip tahminini ekrana yazdırıyor
y =input("dogrumu")                          #tahmini doğru mu diye souyor. ve bunu y değişkenine atıyor
d = ("d")
a = ("a")
t = ("t")


while True:

    if y=="q" or y=="Q":                    #cevaba eğer q veya Q girildiye oyundan çıkıyor.
        print("çikis yaptiniz.")
        break


    elif y == "d"  :                         # vevap d ise tebrikler deyip oyunu bitiiyor.
        print("tebrikler sayiyi dogru bildin..")
        break
        
    elif y == "a" :                         # cevap eğer a ise stlimitin değernn tahmin sayıdan bir azaltıyor çünk verdii cevaptan daha az bir ayı vermei gerek
                    
        üstlimit= (tahminsayi - 1)
        tahminsayi= random.randrange(altlimit,üstlimit)    # tkrardan tahmin yapıyor ve ekrana yazdırıp doru mu diye sooruyor.
        print(tahminsayi)
        y =input("dogru mu?")
                                
               
    elif y == "t" :                                     # ceva eğer t ise altlimitin değernn tahmin saıdan bie arttırıyor. çünk verdii cevaptan daha büyük bir sayı vermei gerek  
        altlimit= (tahminsayi + 1)
        tahminsayi= random.randrange(altlimit,üstlimit)
        print(tahminsayi)                                        # tkrardan tahmin yapıyor ve ekrana yazdırıp doru mu diye sooruyor.
        y =input("dogru mu?")
    else :
        print("lütfen a, d, q veya t tusuna basin")             # eğer başka bir tua basarsa uyarı veriyor.
                   
