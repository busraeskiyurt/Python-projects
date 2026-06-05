# Polinom Denkleminin Tüm Köklerini Bulan Program
# Yöntem: Newton-Raphson + Horner Şeması + İndirgeme (Deflation)
# Bölüm 1.9 - Polinomlar için Newton Yöntemi

# ---------------------------------------------------------------
# HORNER YÖNTEMI
# Polinomu P(x) = a_n * x^n + ... + a_1 * x + a_0 şeklinde
# katsayilar = [a_n, a_{n-1}, ..., a_1, a_0] formatında tutuyoruz
# ---------------------------------------------------------------

def horner(katsayilar, nokta):
    """
    Horner şemasıyla P(nokta) ve P'(nokta) hesaplar.
    Aynı zamanda bölüm polinomun katsayılarını döndürür (deflasyon için).
    """
    derece = len(katsayilar) - 1

    if derece == 0:
        return katsayilar[0], 0, []

    # b dizisini hesapla: b_n = a_n, b_k = a_k + b_{k+1} * nokta
    bolum = [katsayilar[0]]
    for k in range(1, derece + 1):
        sonraki = bolum[-1] * nokta + katsayilar[k]
        bolum.append(sonraki)

    polinom_degeri = bolum[derece]          # P(nokta) = b_0
    bolum_katsayilari = bolum[:derece]      # bölüm polinomu katsayıları

    # Türev için ikinci Horner uygulaması (c dizisi)
    turev = bolum_katsayilari[0]
    for k in range(1, derece):
        turev = turev * nokta + bolum_katsayilari[k]

    return polinom_degeri, turev, bolum_katsayilari


# ---------------------------------------------------------------
# NEWTON-RAPHSON ITERASYOnu
# x_{k+1} = x_k - P(x_k) / P'(x_k)
# ---------------------------------------------------------------

def newton_raphson(katsayilar, baslangic, tolerans=1e-10, maks_iter=300):
    """Verilen başlangıç noktasından Newton-Raphson ile bir kök bulur."""
    x = complex(baslangic)  # karmaşık sayı desteği

    for _ in range(maks_iter):
        p_degeri, p_turev, _ = horner(katsayilar, x)

        if p_turev == 0:  # türev sıfırsa iterasyonu durdur
            break

        yeni_x = x - p_degeri / p_turev

        # Yakınsama kontrolü
        if abs(yeni_x - x) < tolerans * (1 + abs(x)):
            return yeni_x

        x = yeni_x

    return x


# ---------------------------------------------------------------
# TÜM KÖKLERİ BULMA (Newton-Raphson + İndirgeme)
# Bir kök bulunca polinomun derecesini 1 azaltıyoruz
# ---------------------------------------------------------------

def tum_kokleri_bul(katsayilar):
    """
    Newton-Raphson + Horner deflasyon yöntemiyle
    polinomun tüm köklerini bulur.
    """
    kokler = []
    mevcut = list(katsayilar)

    # Farklı başlangıç noktaları - gerçel ve karmaşık
    baslangiclar = [
        1.0, -1.0, 2.0, -2.0, 0.5, -0.5,
        complex(1, 1), complex(-1, 1),
        complex(1, -1), complex(-1, -1),
        3.0, -3.0, complex(0, 2), complex(0, -2)
    ]

    # Her adımda bir kök bul, polinomu indirge
    while len(mevcut) > 2:
        kok_bulundu = False

        for baslangic in baslangiclar:
            aday_kok = newton_raphson(mevcut, baslangic)
            p_kontrol, _, bolum = horner(mevcut, aday_kok)

            # Kök geçerli mi? (Polinom değeri yeterince küçük mü?)
            if abs(p_kontrol) < 1e-6:
                kokler.append(aday_kok)
                mevcut = bolum      # polinomu bir derece küçült
                kok_bulundu = True
                break

        if not kok_bulundu:
            print("Uyari: Bir kok bulunamadi, farkli baslangic noktasi gerekebilir.")
            break

    # Derece 1 kaldıysa: a_1 * x + a_0 = 0 => x = -a_0 / a_1
    if len(mevcut) == 2:
        son_kok = -mevcut[1] / mevcut[0]
        kokler.append(son_kok)

    return kokler


# ---------------------------------------------------------------
# ANA PROGRAM
# ---------------------------------------------------------------

def main():
    print("=" * 55)
    print("  Newton-Raphson Yontemi ile Polinom Kok Bulucu")
    print("  (Horner Semasi + Indirgeme Teknigi)")
    print("=" * 55)
    print()

    while True:
        # Derece girişi
        while True:
            try:
                derece = int(input("Polinomun derecesini girin: "))
                if derece >= 1:
                    break
                print("Derece en az 1 olmalidir.")
            except ValueError:
                print("Lutfen tam sayi girin.")

        # Katsayı girişi (en yüksek kattan sabite doğru)
        print(f"\nKatsayilari buyuk kattan kucuge dogru girin:")
        katsayilar = []
        for i in range(derece, -1, -1):
            while True:
                try:
                    deger = float(input(f"  x^{i} katsayisi: "))
                    katsayilar.append(deger)
                    break
                except ValueError:
                    print("Gecerli bir sayi girin.")

        # En yüksek katsayı kontrolü
        if katsayilar[0] == 0:
            print("En yuksek katsayi sifir olamaz!\n")
            continue

        # Kökleri hesapla
        print("\nKokler hesaplaniyor...\n")
        kokler = tum_kokleri_bul(katsayilar)

        # Sonuçları yazdır
        print(f"Bulunan {len(kokler)} kok:")
        for i, kok in enumerate(kokler):
            gercek_kisim = kok.real
            sanal_kisim = kok.imag

            if abs(sanal_kisim) < 1e-8:
                print(f"  Kok {i+1}: {gercek_kisim:.8f}  (gercek)".replace(".", ","))
            else:
                isaret = "+" if sanal_kisim >= 0 else "-"
                print(f"  Kok {i+1}: {gercek_kisim:.6f} {isaret} {abs(sanal_kisim):.6f}i  (karmasik)".replace(".", ","))

        # Doğrulama: her kökü polinoma koy
        print("\nDogrulama - P(kok) degerleri:")
        for i, kok in enumerate(kokler):
            p_val, _, _ = horner(katsayilar, kok)
            print(f"  P(Kok {i+1}) = {p_val:.3e}")

        print()
        devam = input("Baska bir polinom cözmek ister misiniz? (e/h): ").strip().lower()
        if devam != "e":
            print("\nProgram sonlandirildi.")
            break
        print()


if __name__ == "__main__":
    main()
