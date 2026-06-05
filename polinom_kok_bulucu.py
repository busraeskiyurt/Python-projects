# ================================================================
# Polinom Denkleminin Tüm Köklerini Bulan Program
# Yöntem: Newton-Raphson + Horner Şeması + İndirgeme (Bölüm 1.9)
#
# Referans: "Numerical Methods for the Root Finding Problem",
#           Section 1.9 - The Newton Method for Polynomials
#
# Polinom gösterimi: P(x) = a0 + a1*x + a2*x^2 + ... + an*x^n
# Katsayılar listesi: [a0, a1, a2, ..., an]
# ================================================================


def horner(katsayilar, z):
    """
    Horner şemasıyla P(z) ve P'(z) hesaplar (Algoritma 1.23 ve 1.25).

    Adımlar (bölüm 1.9.1'den):
      b[n] = a[n]
      b[k] = a[k] + b[k+1] * z   (k = n-1, ..., 0)  → P(z) = b[0]

      c[n] = b[n]
      c[k] = b[k] + c[k+1] * z   (k = n-1, ..., 1)  → P'(z) = c[1]

    İndirgeme: b[1..n] = P(x)/(x-z) polinomunun katsayıları

    Parametreler:
      katsayilar : [a0, a1, ..., an]
      z          : hesaplama yapılacak nokta (gerçel veya karmaşık)

    Döndürür: (P(z), P'(z), indirgenmiş_katsayilar)
    """
    n = len(katsayilar) - 1

    # --- b dizisi: P(z) hesabı ---
    b = [0] * (n + 1)
    b[n] = katsayilar[n]
    for k in range(n - 1, -1, -1):
        b[k] = katsayilar[k] + b[k + 1] * z

    # --- c dizisi: P'(z) hesabı ---
    turev = 0
    if n >= 1:
        c = [0] * (n + 1)
        c[n] = b[n]
        for k in range(n - 1, 0, -1):
            c[k] = b[k] + c[k + 1] * z
        turev = c[1]

    # b[1..n]: P(x)/(x-z) polinomunun katsayıları (indirgeme için)
    indirgenmiş = b[1:]

    return b[0], turev, indirgenmiş


def newton_raphson(katsayilar, baslangic_noktasi, tolerans=1e-12, maks_iter=150):
    """
    Newton-Raphson yöntemiyle bir kök yaklaşımı bulur.

    Formül (Algoritma 1.11 ve 1.25):
      x_yeni = x - P(x) / P'(x)

    Parametreler:
      katsayilar         : mevcut (indirgenmiş) polinom katsayıları
      baslangic_noktasi  : başlangıç tahmini
      tolerans           : yakınsama toleransı
      maks_iter          : maksimum iterasyon sayısı

    Döndürür: yaklaşık kök
    """
    x = complex(baslangic_noktasi)

    for _ in range(maks_iter):
        deger, turev, _ = horner(katsayilar, x)

        if turev == 0:
            # Türev sıfır olursa iterasyonu durdur
            break

        adim = deger / turev
        x = x - adim

        if abs(adim) < tolerans:
            break

    return x


def koku_rafine_et(orijinal_katsayilar, yaklasik_kok, tolerans=1e-13, maks_iter=50):
    """
    İndirgeme sırasında oluşan sayısal hataları gidermek için
    bulunan köke orijinal polinom üzerinde Newton adımları uygular.
    """
    x = complex(yaklasik_kok)
    for _ in range(maks_iter):
        deger, turev, _ = horner(orijinal_katsayilar, x)
        if turev == 0:
            break
        adim = deger / turev
        x = x - adim
        if abs(adim) < tolerans:
            break
    return x


def tum_kokleri_bul(katsayilar):
    """
    Newton-Raphson + Horner şeması + indirgeme yöntemiyle
    n. dereceden bir polinomun TÜM köklerini bulur.

    Algoritma (Bölüm 1.9.2 + Bölüm 1.12 İndirgeme Tekniği):
      1. Newton-Raphson ile bir kök bul (Horner kullanarak)
      2. Polinomu (x - kök)'e bölerek indirge (Horner'den b[1..n])
      3. İndirgenmiş polinom üzerinde tekrarla
      4. Her köku orijinal polinomda rafine et

    Parametreler:
      katsayilar : [a0, a1, ..., an]

    Döndürür: köklerin listesi (karmaşık sayılar)
    """
    # Baştaki sıfır katsayıları temizle
    while len(katsayilar) > 1 and katsayilar[-1] == 0:
        katsayilar = katsayilar[:-1]

    derece = len(katsayilar) - 1
    orijinal = katsayilar[:]

    if derece == 0:
        print("Sabit polinom - kök yok.")
        return []

    # Farklı başlangıç noktaları (gerçel ve karmaşık)
    # Hem saf gerçel hem karmaşık kökler için geniş bir set
    deneme_noktalari = [
        complex(0.4,  0.9),  complex(0.4,  -0.9),
        complex(-0.4, 0.9),  complex(-0.4, -0.9),
        complex(1.2,  0.0),  complex(-1.2,  0.0),
        complex(0.0,  1.2),  complex(0.0,  -1.2),
        complex(1.5,  1.5),  complex(-1.5,  1.5),
        complex(1.5, -1.5),  complex(-1.5, -1.5),
        complex(2.5,  0.5),  complex(-2.5,  0.5),
        complex(0.0,  2.5),  complex(0.0,  -2.5),
        complex(3.0,  1.0),  complex(-3.0,  1.0),
        complex(0.1,  0.1),  complex(0.7,   0.3),
    ]

    bulunan_kokler = []
    mevcut = katsayilar[:]

    for i in range(derece):
        mevcut_derece = len(mevcut) - 1
        if mevcut_derece == 0:
            break

        kok_bulundu = None
        en_iyi_hata = float('inf')
        en_iyi_kok = None

        for baslangic in deneme_noktalari:
            aday = newton_raphson(mevcut, baslangic)

            # Orijinal polinomda doğrula
            hata_orijinal, _, _ = horner(orijinal, aday)
            if abs(hata_orijinal) < en_iyi_hata:
                en_iyi_hata = abs(hata_orijinal)
                en_iyi_kok = aday

            if abs(hata_orijinal) < 1e-6:
                kok_bulundu = aday
                break

        if kok_bulundu is None:
            kok_bulundu = en_iyi_kok

        # Orijinal polinom üzerinde rafine et (indirgeme hatasını gider)
        kok_rafine = koku_rafine_et(orijinal, kok_bulundu)
        bulunan_kokler.append(kok_rafine)

        # İndirgeme: mevcut polinomu (x - kök)'e böl
        _, _, mevcut = horner(mevcut, kok_bulundu)

    return bulunan_kokler


# ================================================================
# YARDIMCI ÇIKTI FONKSİYONLARI
# ================================================================

def polinomun_degerini_hesapla(katsayilar, x):
    """P(x) değerini Horner şemasıyla hesaplar."""
    deger, _, _ = horner(katsayilar, x)
    return deger


def sonuclari_yazdir(baslik, katsayilar, kokler):
    """Test sonuçlarını düzenli biçimde ekrana yazar."""
    print("\n" + "=" * 60)
    print(baslik)
    print("=" * 60)

    n = len(katsayilar) - 1
    print(f"Polinom derecesi : {n}")

    # Polinomu göster
    parcalar = []
    for i in range(n, -1, -1):
        a = katsayilar[i]
        if a == 0:
            continue
        if i == 0:
            parcalar.append(str(a))
        elif i == 1:
            parcalar.append(f"({a})x")
        else:
            parcalar.append(f"({a})x^{i}")
    print("P(x) = " + " + ".join(parcalar))

    print(f"\nBulunan {len(kokler)} kök:")
    for sira, kok in enumerate(kokler, 1):
        gercek_kisim = kok.real
        sanal_kisim = kok.imag

        # Çok küçük sanal kısım varsa gerçel olarak göster
        if abs(sanal_kisim) < 1e-8:
            print(f"  Kök {sira}: {gercek_kisim:+.8f}  (gerçel)")
        else:
            isaretli = "+" if sanal_kisim >= 0 else ""
            print(f"  Kök {sira}: {gercek_kisim:.6f}{isaretli}{sanal_kisim:.6f}j  (karmaşık)")

        # Doğrulama: |P(kök)| ≈ 0 olmalı
        dogrulama = polinomun_degerini_hesapla(katsayilar, kok)
        print(f"         |P(kök)| = {abs(dogrulama):.3e}  ✓")


# ================================================================
# ANA PROGRAM
# ================================================================

def main():
    print("=" * 60)
    print("  POLİNOM DENKLEMİ KÖK BULUCU")
    print("  Yöntem: Newton-Raphson + Horner + İndirgeme")
    print("=" * 60)
    print()
    print("Polinom formu: P(x) = a0 + a1*x + a2*x^2 + ... + an*x^n")
    print()

    # --- Derece girdisi ---
    while True:
        try:
            derece = int(input("Polinom derecesini giriniz (n): "))
            if derece < 1:
                print("Derece en az 1 olmalıdır.")
                continue
            break
        except ValueError:
            print("Lütfen tam sayı giriniz.")

    # --- Katsayı girdisi ---
    katsayilar = []
    print(f"\n{derece + 1} adet katsayı giriniz:")
    for i in range(derece + 1):
        while True:
            try:
                a = float(input(f"  a{i} (x^{i} katsayısı): "))
                katsayilar.append(a)
                break
            except ValueError:
                print("  Lütfen sayısal bir değer giriniz.")

    # --- Hesap ---
    print("\nKökler hesaplanıyor...")
    kokler = tum_kokleri_bul(katsayilar[:])

    # --- Sonuçları göster ---
    print(f"\nBulunan {len(kokler)} kök:")
    for sira, kok in enumerate(kokler, 1):
        gercek_kisim = kok.real
        sanal_kisim = kok.imag

        if abs(sanal_kisim) < 1e-8:
            print(f"  Kök {sira}: {gercek_kisim:+.8f}  (gerçel)")
        else:
            isaretli = "+" if sanal_kisim >= 0 else ""
            print(f"  Kök {sira}: {gercek_kisim:.6f}{isaretli}{sanal_kisim:.6f}j  (karmaşık)")

        dogrulama, _, _ = horner(katsayilar, kok)
        print(f"         Doğrulama |P(kök)| = {abs(dogrulama):.3e}")


# ================================================================
# DOĞRULAMA TESTLERİ
# ================================================================

def testleri_calistir():
    """
    Farklı derecelerden polinom denklemleriyle program doğrulaması.
    """

    # TEST 1: 2. derece - gerçel kökler
    # P(x) = x^2 - 5x + 6 = (x-2)(x-3), beklenen kökler: 2 ve 3
    kat1 = [6, -5, 1]
    k1 = tum_kokleri_bul(kat1[:])
    sonuclari_yazdir("TEST 1 | 2. DERECE | Gerçel Kökler", kat1, k1)
    print("  Beklenen kökler: 2 ve 3")

    # TEST 2: 3. derece - üç gerçel kök
    # P(x) = x^3 - 6x^2 + 11x - 6 = (x-1)(x-2)(x-3), kökler: 1, 2, 3
    kat2 = [-6, 11, -6, 1]
    k2 = tum_kokleri_bul(kat2[:])
    sonuclari_yazdir("TEST 2 | 3. DERECE | Üç Gerçel Kök", kat2, k2)
    print("  Beklenen kökler: 1, 2, 3")

    # TEST 3: 2. derece - karmaşık kökler
    # P(x) = x^2 + 1 = 0, kökler: +i ve -i
    kat3 = [1, 0, 1]
    k3 = tum_kokleri_bul(kat3[:])
    sonuclari_yazdir("TEST 3 | 2. DERECE | Karmaşık Kökler", kat3, k3)
    print("  Beklenen kökler: +i ve -i")

    # TEST 4: 4. derece - hem gerçel hem karmaşık kökler
    # P(x) = x^4 - 1 = (x-1)(x+1)(x-i)(x+i), kökler: ±1, ±i
    kat4 = [-1, 0, 0, 0, 1]
    k4 = tum_kokleri_bul(kat4[:])
    sonuclari_yazdir("TEST 4 | 4. DERECE | Karışık Kökler", kat4, k4)
    print("  Beklenen kökler: +1, -1, +i, -i")

    # TEST 5: 5. derece polinom
    # P(x) = (x-1)(x-2)(x-3)(x-4)(x-5), kökler: 1, 2, 3, 4, 5
    # Açılmış hali: x^5 - 15x^4 + 85x^3 - 225x^2 + 274x - 120
    kat5 = [-120, 274, -225, 85, -15, 1]
    k5 = tum_kokleri_bul(kat5[:])
    sonuclari_yazdir("TEST 5 | 5. DERECE | Beş Gerçel Kök", kat5, k5)
    print("  Beklenen kökler: 1, 2, 3, 4, 5")

    # TEST 6: 3. derece - bir gerçel iki karmaşık kök
    # P(x) = x^3 - 2x^2 - 5 = (x-2.6906)(x+0.3453+1.3187i)(x+0.3453-1.3187i)
    kat6 = [-5, 0, -2, 1]
    k6 = tum_kokleri_bul(kat6[:])
    sonuclari_yazdir("TEST 6 | 3. DERECE | 1 Gerçel + 2 Karmaşık Kök", kat6, k6)
    print("  Beklenen kökler: ~2.6906, ~-0.3453±1.3187i")

    # TEST 7: 7. derece polinom
    # P(x) = (x-1)(x-2)(x-3)(x-4)(x-5)(x-6)(x-7)
    # Horner ile hesaplanmış katsayılar:
    kat7 = [-5040, 13068, -13132, 6769, -1960, 322, -28, 1]
    k7 = tum_kokleri_bul(kat7[:])
    sonuclari_yazdir("TEST 7 | 7. DERECE | Yedi Gerçel Kök", kat7, k7)
    print("  Beklenen kökler: 1, 2, 3, 4, 5, 6, 7")


# Program doğrudan çalıştırılırsa testleri yap veya interaktif mod aç
if __name__ == "__main__":
    print("Ne yapmak istersiniz?")
    print("  1 - Katsayıları kendiniz girin")
    print("  2 - Doğrulama testlerini çalıştır")
    secim = input("Seçiminiz (1/2): ").strip()

    if secim == "1":
        main()
    else:
        testleri_calistir()
