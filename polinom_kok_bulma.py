# Polinom denkleminin tüm köklerini Newton-Raphson yöntemiyle bulan program
# Kullanılan yöntem: Bölüm 1.9 - Horner Şeması + İndirgeme (Deflation) Tekniği
#
# Temel fikir:
#   1. Horner şemasıyla P(x) ve P'(x) verimli hesaplanır
#   2. Newton-Raphson ile bir kök bulunur: x_yeni = x - P(x)/P'(x)
#   3. Bulunan kök kullanılarak polinom bir derece indirgenir
#   4. Bu işlem tüm kökler bulunana kadar tekrarlanır


def horner(katsayilar, nokta):
    # Horner şemasıyla P(nokta) ve P'(nokta) değerlerini hesaplar
    # Ayrıca indirgeme için bölünmüş polinomu da döndürür
    #
    # katsayilar listesi: [a0, a1, a2, ..., an]
    #   -> P(x) = a0 + a1*x + a2*x^2 + ... + an*x^n
    # Algoritma 1.25'ten (dokümandaki indislemeyle):
    #   b[n] = a[n]
    #   b[k] = a[k] + b[k+1]*nokta    (k = n-1, ..., 0)
    #   c[n] = b[n]
    #   c[k] = b[k] + c[k+1]*nokta    (k = n-1, ..., 1)
    #   P(nokta)  = b[0]
    #   P'(nokta) = c[1]

    n = len(katsayilar) - 1  # polinomun derecesi

    b = [complex(0)] * (n + 1)
    b[n] = complex(katsayilar[n])
    for k in range(n - 1, -1, -1):
        b[k] = complex(katsayilar[k]) + b[k + 1] * nokta

    if n == 0:
        return b[0], complex(0), []

    c = [complex(0)] * (n + 1)
    c[n] = b[n]
    for k in range(n - 1, 0, -1):
        c[k] = b[k] + c[k + 1] * nokta

    polinom_degeri = b[0]       # P(nokta)
    turev_degeri = c[1]         # P'(nokta)
    bolunmus_katsayilar = b[1:] # Q(x) katsayıları: P(x) = (x - nokta)*Q(x) + b[0]

    return polinom_degeri, turev_degeri, bolunmus_katsayilar


def newton_raphson(katsayilar, baslangic, tolerans=1e-10, max_iter=500):
    # Newton-Raphson yöntemiyle tek bir kök bulur
    # Formül: x_yeni = x - P(x) / P'(x)
    # Karmaşık sayılarla da çalışır

    x = complex(baslangic)

    for _ in range(max_iter):
        p_degeri, p_turev, _ = horner(katsayilar, x)

        if p_turev == 0:
            # Türev sıfır çıkarsa dur (yakınsama olmadı)
            break

        x_yeni = x - p_degeri / p_turev

        # Durma kriteri: art arda iki tahmin arasındaki fark toleransın altına düştüğünde
        if abs(x_yeni - x) < tolerans:
            return x_yeni

        x = x_yeni

    return x


def tum_kokleri_bul(katsayilar):
    # Tüm kökleri Newton-Raphson + indirgeme (deflation) yöntemiyle bulur
    #
    # İndirgeme tekniği (Bölüm 1.12):
    #   Bir kök (alfa) bulunduktan sonra:
    #   P(x) = (x - alfa) * Q(x)
    #   Q(x)'in katsayıları Horner şemasından doğrudan elde edilir (b[1..n])
    #   Ardından aynı yöntem Q(x)'e uygulanır

    kokler = []
    aktif_katsayilar = [complex(k) for k in katsayilar]

    # Başlangıç noktası: karmaşık kökler de bulunabilsin diye karmaşık seçildi
    # İndirgeme sayesinde her adımda farklı bir kök bulunur
    baslangic_noktalari = [
        complex(0.4, 0.9),
        complex(-0.4, 0.9),
        complex(1.0, 0.5),
        complex(-1.0, 0.5),
        complex(0.0, 1.0),
    ]

    while len(aktif_katsayilar) > 1:
        derece = len(aktif_katsayilar) - 1
        if derece == 0:
            break

        # En iyi başlangıç noktasını dene
        en_iyi_kok = None
        en_kucuk_hata = None

        for baslangic in baslangic_noktalari:
            aday_kok = newton_raphson(aktif_katsayilar, baslangic)
            p_val, _, _ = horner(aktif_katsayilar, aday_kok)
            hata = abs(p_val)

            if en_kucuk_hata is None or hata < en_kucuk_hata:
                en_kucuk_hata = hata
                en_iyi_kok = aday_kok

        kokler.append(en_iyi_kok)

        # Polinomu bu kökle indirge: aktif polinom bir derece azalır
        _, _, indirgenmiş = horner(aktif_katsayilar, en_iyi_kok)
        aktif_katsayilar = indirgenmiş

    return kokler


def katsayilari_al(derece):
    # Kullanıcıdan katsayıları yüksek dereceden düşüğe doğru alır
    # İç kullanımda [a0, a1, ..., an] sırasında saklanır

    print(f"\nP(x) = a{derece}*x^{derece} + ... + a1*x + a0")
    print("Katsayıları girin (yüksek dereceden düşüğe):\n")

    katsayilar_ters = []
    for i in range(derece, -1, -1):
        while True:
            try:
                girdi = input(f"  a{i} (x^{i} katsayisi): ")
                deger = float(girdi)
                katsayilar_ters.append(deger)
                break
            except ValueError:
                print("  Gecersiz giris, lutfen sayi girin.")

    # [an, a(n-1), ..., a0] -> [a0, a1, ..., an]
    return list(reversed(katsayilar_ters))


def kokleri_yazdir(kokler):
    # Bulunan kökleri gerçel / karmaşık olarak ayırt ederek yazdırır

    print(f"\nBulunan kokler ({len(kokler)} adet):")
    print("-" * 45)

    for numara, kok in enumerate(kokler, 1):
        gercek_kisim = kok.real
        sanal_kisim = kok.imag

        if abs(sanal_kisim) < 1e-6:
            # Gerçel kök
            print(f"  Kok {numara}: x = {gercek_kisim:.6f}   (gercel)")
        else:
            # Karmaşık kök
            if sanal_kisim >= 0:
                print(f"  Kok {numara}: x = {gercek_kisim:.6f} + {sanal_kisim:.6f}i   (karmasik)")
            else:
                print(f"  Kok {numara}: x = {gercek_kisim:.6f} - {abs(sanal_kisim):.6f}i   (karmasik)")

    print("-" * 45)


def main():
    print("=" * 50)
    print("  POLINOM KOK BULMA PROGRAMI")
    print("  Newton-Raphson + Horner Semasi + Indirgeme")
    print("=" * 50)

    while True:
        print()

        # Derece girişi
        while True:
            try:
                girdi = input("Polinomun derecesini girin (cikmak icin 'q'): ")
                if girdi.strip().lower() == 'q':
                    print("\nProgram sonlandirildi.")
                    return
                derece = int(girdi)
                if derece < 1:
                    print("  Hata: Derece en az 1 olmalidir.")
                    continue
                break
            except ValueError:
                print("  Hata: Lutfen tam sayi girin.")

        # Katsayı girişi
        katsayilar = katsayilari_al(derece)

        # En yüksek katsayı kontrolü
        if katsayilar[-1] == 0:
            print("  Hata: En yuksek derece katsayisi (a" + str(derece) + ") sifir olamaz!")
            continue

        # Kökleri hesapla ve yazdır
        print("\nKokler hesaplaniyor...")
        kokler = tum_kokleri_bul(katsayilar)
        kokleri_yazdir(kokler)

        print("\nYeni polinom girmek icin devam ediliyor...")
        print("=" * 50)


if __name__ == "__main__":
    main()
