# ============================================================
# Polinom Denklemlerinin Köklerini Bulan Program
# Yöntem: Newton-Raphson + Horner Şeması + Deflasyon
# Kaynak: Ders notları, Bölüm 1.9
# ============================================================

# Polinom gösterimi: katsayilar listesi KÜÇÜKTEN BÜYÜĞE derece sırasıyla
# Örnek: x^3 - 6x^2 + 11x - 6  -->  [-6, 11, -6, 1]


def horner_hesapla(katsayilar, nokta):
    """
    Horner şeması ile P(nokta) ve P'(nokta) değerlerini hesaplar.

    Algoritma (Bölüm 1.9.1):
      b[n] = a[n]
      b[k] = a[k] + b[k+1] * nokta,  k = n-1, ..., 0
      --> P(nokta) = b[0]

      c[n] = b[n]
      c[k] = b[k] + c[k+1] * nokta,  k = n-1, ..., 1
      --> P'(nokta) = c[1]

    Döndürür: (polinom degeri, turev degeri, b dizisi)
    b dizisi deflasyon için de kullanılır.
    """
    derece = len(katsayilar) - 1

    # --- b dizisini hesapla ---
    b = [0] * (derece + 1)
    b[derece] = katsayilar[derece]
    for k in range(derece - 1, -1, -1):
        b[k] = katsayilar[k] + b[k + 1] * nokta

    polinom_degeri = b[0]

    # Sabit polinom için türev sıfır
    if derece == 0:
        return polinom_degeri, 0, b

    # --- c dizisini hesapla ---
    c = [0] * (derece + 1)
    c[derece] = b[derece]
    for k in range(derece - 1, 0, -1):
        c[k] = b[k] + c[k + 1] * nokta

    turev_degeri = c[1]

    return polinom_degeri, turev_degeri, b


def newton_raphson_tek_kok(katsayilar, baslangic, tolerans=1e-12, maks_iter=200):
    """
    Newton-Raphson iterasyonu ile tek bir kök bulur.

    Formül: x_yeni = x - P(x) / P'(x)

    Horner şeması her adımda hem P(x) hem de P'(x) değerini verir.
    """
    x = baslangic

    for _ in range(maks_iter):
        polinom_degeri, turev_degeri, _ = horner_hesapla(katsayilar, x)

        # Yeterince küçük fonksiyon değeri --> yakınsadı
        if abs(polinom_degeri) < tolerans:
            return x

        # Türev sıfırsa iterasyona devam edilemez
        if abs(turev_degeri) == 0:
            break

        x_yeni = x - polinom_degeri / turev_degeri

        # Değişim çok küçük --> yakınsadı
        if abs(x_yeni - x) < tolerans:
            return x_yeni

        x = x_yeni

    return x


def deflasyon_uygula(katsayilar, bulunan_kok):
    """
    Polinomu (x - bulunan_kok) ile böler.

    Horner şemasının b dizisi bölüm polinomunun katsayılarını verir:
      P(x) = (x - kok) * Q(x)
    Yeni katsayılar: b[1], b[2], ..., b[n]
    """
    _, _, b = horner_hesapla(katsayilar, bulunan_kok)
    return b[1:]  # bölüm polinomunun katsayıları


def tum_kokleri_bul(katsayilar, tolerans=1e-10):
    """
    Verilen polinomun tüm köklerini Newton-Raphson ve deflasyon ile bulur.

    Adımlar:
      1) Birkaç farklı başlangıç noktasıyla Newton-Raphson çalıştır.
      2) Kök bulununca deflasyonla polinomu küçült.
      3) Kalan kökler için aynı işlemi tekrarla.
    """
    mevcut_katsayilar = list(katsayilar)
    bulunan_kokler = []

    # Farklı başlangıç noktaları (gerçel ve karmaşık)
    baslangic_noktalari = [1.0, -1.0, complex(1, 1), complex(-1, -1)]

    while len(mevcut_katsayilar) > 1:
        derece = len(mevcut_katsayilar) - 1

        if derece == 0:
            break

        kok_bulundu = False

        for baslangic in baslangic_noktalari:
            aday = newton_raphson_tek_kok(mevcut_katsayilar, baslangic, tolerans)
            p_val, _, _ = horner_hesapla(mevcut_katsayilar, aday)

            # Aday gerçekten kök mü?
            if abs(p_val) < 1e-6:
                # Sanal kısım çok küçükse gerçel sayı olarak kabul et
                if abs(aday.imag) < 1e-8 if isinstance(aday, complex) else True:
                    if isinstance(aday, complex):
                        aday = aday.real

                bulunan_kokler.append(aday)
                mevcut_katsayilar = deflasyon_uygula(mevcut_katsayilar, aday)
                kok_bulundu = True
                break

        if not kok_bulundu:
            print("Uyari: Bu derecede kok bulunamadi.")
            break

    return bulunan_kokler


def polinomu_yazdir(katsayilar):
    """Polinomu okunaklı şekilde ekrana yazar."""
    derece = len(katsayilar) - 1
    parcalar = []
    for i in range(derece, -1, -1):
        kat = katsayilar[i]
        if kat == 0:
            continue
        if i == 0:
            parcalar.append(str(kat))
        elif i == 1:
            parcalar.append("{}x".format(kat))
        else:
            parcalar.append("{}x^{}".format(kat, i))
    return " + ".join(parcalar).replace("+ -", "- ")


def kokleri_dogrula(katsayilar, kokler):
    """Her kökü polinoma koyup P(kok) değerini hesaplar (doğrulama için)."""
    print("\nDogrulama - P(kok) degerleri:")
    for kok in kokler:
        p_val, _, _ = horner_hesapla(katsayilar, kok)
        if isinstance(kok, complex):
            print("  P({:.4f} + {:.4f}i) = {:.2e}".format(kok.real, kok.imag, abs(p_val)))
        else:
            print("  P({:.6f}) = {:.2e}".format(kok, abs(p_val)))


# ============================================================
# TEST / DOGRULAMA BÖLÜMLERİ
# ============================================================

def test_calistir(baslik, katsayilar, beklenen_aciklama=""):
    """Tek bir test polinomunu çalıştırır ve sonuçları gösterir."""
    print("=" * 55)
    print(baslik)
    if beklenen_aciklama:
        print("Beklenen kökler:", beklenen_aciklama)
    print("Polinom: P(x) =", polinomu_yazdir(katsayilar))

    kokler = tum_kokleri_bul(katsayilar)

    print("\nBulunan kokler:")
    for kok in kokler:
        if isinstance(kok, complex):
            print("  {:.6f} + {:.6f}i".format(kok.real, kok.imag))
        else:
            print("  {:.6f}".format(kok))

    kokleri_dogrula(katsayilar, kokler)
    print()


# --- Test 1: Derece 3, gerçel kökler (x-1)(x-2)(x-3) ---
# P(x) = x^3 - 6x^2 + 11x - 6
test_calistir(
    "TEST 1: Derece 3 polinom - gercek kokler",
    [-6, 11, -6, 1],
    "x = 1, 2, 3"
)

# --- Test 2: Derece 2, karmaşık kökler x^2 + 1 = 0 ---
# P(x) = x^2 + 1
test_calistir(
    "TEST 2: Derece 2 polinom - karmasik kokler",
    [1, 0, 1],
    "x = +i, -i"
)

# --- Test 3: Derece 4, karışık (x-1)(x-2)(x^2+1) ---
# P(x) = x^4 - 3x^3 + 3x^2 - 3x + 2
test_calistir(
    "TEST 3: Derece 4 polinom - gercek ve karmasik kokler",
    [2, -3, 3, -3, 1],
    "x = 1, 2, +i, -i"
)

# --- Test 4: Derece 5 polinom ---
# (x-1)(x+1)(x-2)(x+2)(x-3) = x^5 - 3x^4 - 5x^3 + 15x^2 + 4x - 12
test_calistir(
    "TEST 4: Derece 5 polinom - gercek kokler",
    [-12, 4, 15, -5, -3, 1],
    "x = -2, -1, 1, 2, 3"
)

# --- Test 5: Derece 3, karmaşık kökler x^3 - 2x^2 - 5 = 0 ---
# Kökler: 2.6906, -0.3453 ± 1.3187i  (ders notundaki örnek)
test_calistir(
    "TEST 5: Derece 3 - karmasik cift kok (ders notu ornegi)",
    [-5, 0, -2, 1],
    "x = 2.6906, -0.3453+1.3187i, -0.3453-1.3187i"
)

# --- Test 6: Derece 7 ---
# (x-1)(x-2)(x-3)(x-4)(x-5)(x-6)(x-7)
# katsayilar elle hesaplamak zor, bilinen degerleri kullaniyoruz
test_calistir(
    "TEST 6: Derece 7 polinom - gercek kokler",
    [-5040, 13068, -13132, 6769, -1960, 322, -28, 1],
    "x = 1, 2, 3, 4, 5, 6, 7"
)
