# Polinom Denkleminin Tüm Köklerini Bulan Program
# Yöntem: Newton-Raphson + Horner Şeması + Deflasyon (Bölüm 1.9)
#
# Polinomun gösterimi: P(x) = a0 + a1*x + a2*x^2 + ... + an*x^n
# Katsayı listesi: [a0, a1, a2, ..., an]  (sabitten başlar, yüksek kuvvete gider)


def horner(katsayilar, z):
    """
    Horner şeması ile P(z) ve P'(z) değerlerini hesaplar.
    Kitaptaki Algoritma 1.25'e göre uygulanmıştır.
    """
    n = len(katsayilar) - 1  # polinom derecesi

    # b katsayılarını hesapla => b[0] = P(z)
    b = [0] * (n + 1)
    b[n] = katsayilar[n]
    for k in range(n - 1, -1, -1):
        b[k] = katsayilar[k] + b[k + 1] * z

    # c katsayılarını hesapla => c[1] = P'(z)
    c = [0] * (n + 1)
    c[n] = b[n]
    for k in range(n - 1, 0, -1):
        c[k] = b[k] + c[k + 1] * z

    polinom_degeri = b[0]
    turev_degeri = c[1]

    return polinom_degeri, turev_degeri, b


def deflasyon(katsayilar, bulunan_kok):
    """
    Polinomu (x - bulunan_kok) ile böler, derece 1 azaltır.
    Horner b katsayıları (b[1]...b[n]) yeni polinomun katsayılarıdır.
    """
    n = len(katsayilar) - 1
    b = [0] * (n + 1)
    b[n] = katsayilar[n]
    for k in range(n - 1, -1, -1):
        b[k] = katsayilar[k] + b[k + 1] * bulunan_kok
    return b[1:]  # derece n-1'lik yeni polinom katsayıları


def newton_raphson(katsayilar, baslangic, tolerans=1e-10, maks_iter=200):
    """
    Verilen başlangıç noktasından Newton-Raphson iterasyonu ile kök bulur.
    Formül: x_yeni = x - P(x) / P'(x)
    """
    x = baslangic
    for _ in range(maks_iter):
        polinom_val, turev_val, _ = horner(katsayilar, x)

        if turev_val == 0:
            break  # türev sıfırsa iterasyon durur

        x_yeni = x - polinom_val / turev_val

        # Yakınsama kontrolü
        if abs(x_yeni - x) < tolerans:
            return x_yeni

        x = x_yeni
    return x


def tum_kokleri_bul(katsayilar):
    """
    Newton-Raphson + deflasyon döngüsü ile tüm kökleri bulur.
    Her adımda bir kök bulunur, polinom bölünerek küçültülür.
    """
    suanki_katsayilar = list(katsayilar)
    bulunan_kokler = []

    # Farklı başlangıç noktaları: hem gerçel hem karmaşık
    baslangiclar = [1.0, -1.0, 2.0, complex(1, 1), complex(-1, -1)]

    while len(suanki_katsayilar) > 2:  # en az 1. dereceli polinomda devam et

        kok_bulundu = False

        for baslangic in baslangiclar:
            aday = newton_raphson(suanki_katsayilar, baslangic)

            # Adayın gerçekten kök olup olmadığını kontrol et
            deger, _, _ = horner(suanki_katsayilar, aday)
            if abs(deger) < 1e-6:
                bulunan_kokler.append(aday)
                suanki_katsayilar = deflasyon(suanki_katsayilar, aday)
                kok_bulundu = True
                break

        if not kok_bulundu:
            print("Uyari: Bu adimda kok bulunamadi.")
            break

    # Son kalan polinom doğrusal ise: a1*x + a0 = 0 => x = -a0/a1
    if len(suanki_katsayilar) == 2:
        son_kok = -suanki_katsayilar[0] / suanki_katsayilar[1]
        bulunan_kokler.append(son_kok)

    return bulunan_kokler


def kokleri_yazdir(baslik, katsayilar, beklenen=""):
    """Test sonuçlarını düzenli şekilde ekrana yazdırır."""
    print(f"\n{'='*55}")
    print(f"  {baslik}")
    if beklenen:
        print(f"  Beklenen: {beklenen}")
    print(f"{'='*55}")

    kokler = tum_kokleri_bul(katsayilar)

    print(f"  Bulunan {len(kokler)} kok:")
    for i, kok in enumerate(kokler):
        # Kökün polinomda verdiği değeri hesapla (doğrulama)
        kontrol, _, _ = horner(katsayilar, kok)
        print(f"  x{i+1} = {kok:.6f}    |P(x)| = {abs(kontrol):.2e}")


# ----------------------------------------------------------------
# ANA PROGRAM - Test polinomları ile doğrulama
# ----------------------------------------------------------------
def main():
    print("\n" + "="*55)
    print("  Newton-Raphson + Horner + Deflasyon Kok Bulucu")
    print("  (Hoca notlari Bolum 1.9 yontemine gore)")
    print("="*55)

    # Test 1: 2. derece - x^2 - 5x + 6 = 0 (kökler: 2, 3)
    # Katsayılar: a0=6, a1=-5, a2=1
    kokleri_yazdir(
        "Test 1: x^2 - 5x + 6 = 0",
        [6, -5, 1],
        "x=2 ve x=3"
    )

    # Test 2: 3. derece - x^3 - 6x^2 + 11x - 6 = 0 (kökler: 1, 2, 3)
    # a0=-6, a1=11, a2=-6, a3=1
    kokleri_yazdir(
        "Test 2: x^3 - 6x^2 + 11x - 6 = 0",
        [-6, 11, -6, 1],
        "x=1, x=2, x=3"
    )

    # Test 3: 3. derece - karmaşık kökler - x^3 - 2x^2 - 5 = 0
    # a0=-5, a1=0, a2=-2, a3=1
    kokleri_yazdir(
        "Test 3: x^3 - 2x^2 - 5 = 0",
        [-5, 0, -2, 1],
        "~2.6906, ~-0.3453+1.3187i, ~-0.3453-1.3187i"
    )

    # Test 4: 4. derece - x^4 - 1 = 0 (kökler: 1, -1, i, -i)
    # a0=-1, a1=0, a2=0, a3=0, a4=1
    kokleri_yazdir(
        "Test 4: x^4 - 1 = 0",
        [-1, 0, 0, 0, 1],
        "x=1, x=-1, x=i, x=-i"
    )

    # Test 5: 5. derece - (x-1)(x-2)(x-3)(x-4)(x-5) = 0
    # Açılımı: x^5 - 15x^4 + 85x^3 - 225x^2 + 274x - 120
    kokleri_yazdir(
        "Test 5: x^5 - 15x^4 + 85x^3 - 225x^2 + 274x - 120 = 0",
        [-120, 274, -225, 85, -15, 1],
        "x=1, 2, 3, 4, 5"
    )

    # Test 6: 7. derece - (x-1)(x-2)...(x-7)
    # Katsayılar için hızlı hesap - doğrulama amaçlı
    # x^7 - 28x^6 + 322x^5 - 1960x^4 + 6769x^3 - 13132x^2 + 13068x - 5040
    kokleri_yazdir(
        "Test 6: 7. dereceli polinom - kokleri 1'den 7'ye",
        [-5040, 13068, -13132, 6769, -1960, 322, -28, 1],
        "x=1, 2, 3, 4, 5, 6, 7"
    )

    print("\n" + "="*55)
    print("  Program tamamlandi.")
    print("="*55 + "\n")


if __name__ == "__main__":
    main()
