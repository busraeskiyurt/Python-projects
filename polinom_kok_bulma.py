# Polinom Kök Bulma Programı
# Newton-Raphson yöntemi + Horner şeması + İndirgeme (Deflasyon) şeması
# Kaynak: Bölüm 1.9 - The Newton Method for Polynomials

# Herhangi bir dereceden polinomu girdi olarak alır ve tüm kökleri bulur.
# Karmaşık kökler de dahil olmak üzere n. dereceden bir polinomun n kökü vardır.


def horner_hesapla(katsayilar, nokta):
    """
    Horner şeması ile P(nokta) ve P'(nokta) hesaplar.
    Aynı zamanda indirgeme için b katsayılarını da döndürür.

    katsayilar[i] = x^i teriminin katsayısı  (a0 sabit terim, an en yüksek derece)
    Algoritma 1.25 (ders notundan)
    """
    derece = len(katsayilar) - 1

    b = [0] * (derece + 1)
    c = [0] * (derece + 1)

    # bn = an ile başla
    b[derece] = katsayilar[derece]
    c[derece] = b[derece]

    # j = n-1'den 1'e kadar: bj = aj + bj+1 * z,  cj = bj + cj+1 * z
    for j in range(derece - 1, 0, -1):
        b[j] = katsayilar[j] + nokta * b[j + 1]
        c[j] = b[j] + nokta * c[j + 1]

    # b0 = a0 + b1 * z  -> bu P(z) değeridir
    b[0] = katsayilar[0] + nokta * b[1]

    # P(z) = b0,  P'(z) = c1,  indirgeme katsayıları = b1..bn
    return b[0], c[1], b[1:]


def newton_raphson_kok_bul(katsayilar, baslangic, tolerans=1e-12, maks_iter=300):
    """
    Newton-Raphson iterasyonu: x_yeni = x - P(x) / P'(x)
    Horner şeması kullanılarak P(x) ve P'(x) hesaplanır.
    """
    x = complex(baslangic)

    for _ in range(maks_iter):
        polinom_degeri, turev_degeri, _ = horner_hesapla(katsayilar, x)

        # Türev sıfırsa iterasyon durur
        if abs(turev_degeri) == 0:
            break

        # Newton adımı
        x_yeni = x - polinom_degeri / turev_degeri

        # Yakınsama kontrolü
        if abs(x_yeni - x) < tolerans:
            return x_yeni

        x = x_yeni

    return x


def tum_kokleri_bul(katsayilar):
    """
    İndirgeme şeması ile polinomun tüm köklerini bulur.
    Her kök bulunduktan sonra polinom bir derece düşürülür (deflasyon).
    Bölüm 1.12 - Deflation Technique
    """
    kokler = []
    guncel_katsayilar = list(katsayilar)

    # Farklı başlangıç noktaları - gerçel ve karmaşık kökleri yakalamak için
    baslangic_noktalari = [
        1.0, -1.0, complex(0, 1), complex(0, -1),
        2.0, -2.0, complex(1, 1), complex(-1, 1),
        3.0, -3.0, complex(0.5, 1.5), complex(-0.5, -1.5)
    ]

    while len(guncel_katsayilar) > 1:
        derece = len(guncel_katsayilar) - 1

        if derece == 0:
            break

        # Derece 1 ise doğrudan çöz: a1*x + a0 = 0  ->  x = -a0/a1
        if derece == 1:
            kok = -guncel_katsayilar[0] / guncel_katsayilar[1]
            kokler.append(kok)
            break

        # Farklı başlangıç noktaları ile kök aramaya çalış
        bulunan_kok = None
        for baslangic in baslangic_noktalari:
            aday_kok = newton_raphson_kok_bul(guncel_katsayilar, baslangic)
            polinom_degeri, _, _ = horner_hesapla(guncel_katsayilar, aday_kok)

            # Kök yeterince küçük bir P(z) değeri veriyorsa kabul et
            if abs(polinom_degeri) < 1e-6:
                bulunan_kok = aday_kok
                break

        if bulunan_kok is None:
            print("  Uyarı: Bu adimda kök bulunamadı.")
            break

        # Çok küçük sanal kısım varsa gerçel kök olarak işle
        if abs(bulunan_kok.imag) < 1e-8:
            bulunan_kok = bulunan_kok.real

        kokler.append(bulunan_kok)

        # İndirgeme: bulunan kökü böl ve polinom derecesini azalt
        # P_n(x) = (x - kok) * Q_{n-1}(x)
        _, _, yeni_katsayilar = horner_hesapla(guncel_katsayilar, bulunan_kok)
        guncel_katsayilar = list(yeni_katsayilar)

    return kokler


def koku_yazdir(indeks, kok):
    """Kök değerini düzgün biçimde ekrana yazdırır."""
    if isinstance(kok, complex):
        gercek = kok.real
        sanal = kok.imag
        if sanal >= 0:
            print(f"  x{indeks} = {gercek:.8f} + {sanal:.8f}i")
        else:
            print(f"  x{indeks} = {gercek:.8f} - {abs(sanal):.8f}i")
    else:
        print(f"  x{indeks} = {kok:.8f}")


def main():
    print("=" * 55)
    print("  Polinom Kök Bulma - Newton-Raphson + Horner")
    print("  Indirgeme (Deflasyon) Seması")
    print("=" * 55)

    while True:
        print("\nYeni polinom girin  (çıkmak için derece olarak 0 yazın)")

        try:
            derece = int(input("\nPolinomun derecesi (n): "))
        except ValueError:
            print("Gecersiz giris, tekrar deneyin.")
            continue

        if derece == 0:
            print("\nProgram sonlandırıldı.")
            break

        if derece < 0:
            print("Derece negatif olamaz.")
            continue

        print(f"\n{derece}. derece polinom:")
        print(f"  P(x) = a{derece}*x^{derece} + ... + a1*x + a0")
        print("Katsayıları yüksek dereceden başlayarak girin:\n")

        # Kullanıcıdan katsayıları al (yüksekten düşüğe)
        katsayilar_ters = []
        for i in range(derece, -1, -1):
            while True:
                try:
                    deger = float(input(f"  a{i} (x^{i} katsayısı): "))
                    katsayilar_ters.append(deger)
                    break
                except ValueError:
                    print("  Hatalı giriş, lütfen sayısal bir değer girin.")

        # katsayilar[i] = x^i katsayısı olacak şekilde ters çevir
        katsayilar = list(reversed(katsayilar_ters))

        # En yüksek derecenin katsayısı sıfır olamaz
        if katsayilar[derece] == 0:
            print("\nHata: En yüksek derecenin katsayısı (an) sıfır olamaz!")
            continue

        print("\nKökler hesaplanıyor...\n")
        kokler = tum_kokleri_bul(katsayilar)

        print(f"Bulunan {len(kokler)} kök:")
        for i, kok in enumerate(kokler, 1):
            koku_yazdir(i, kok)

        # Kök doğrulama: orijinal polinoma P(kok) hesapla
        print("\nDogrulama - P(kok) degerlerı:")
        for i, kok in enumerate(kokler, 1):
            karmasik_kok = complex(kok) if not isinstance(kok, complex) else kok
            polinom_degeri, _, _ = horner_hesapla(katsayilar, karmasik_kok)
            print(f"  P(x{i}) = {polinom_degeri:.3e}")

        print("\n" + "-" * 55)


if __name__ == "__main__":
    main()
