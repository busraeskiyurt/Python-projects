# Polinom denkleminin tüm köklerini bulan program
# Yöntem: Newton-Raphson + Horner Şeması + Deflasyon (Bölüm 1.9 ve 1.12)
#
# Polinom formu: P(x) = a0 + a1*x + a2*x^2 + ... + an*x^n
# Katsayılar a0'dan (sabit terim) an'a (en yüksek derece) sırasıyla girilir.

# ---------------------------------------------------------------
# HORNER ŞEMASI
# ---------------------------------------------------------------
def horner(katsayilar, nokta):
    """
    P(z) ve P'(z) değerlerini Horner şemasıyla hesaplar.
    Algoritma 1.25'e göre uygulanmıştır.

    Parametreler:
        katsayilar: [a0, a1, ..., an]  (düşük dereceden yüksek dereceye)
        nokta     : z değeri (gerçel veya karmaşık)

    Döndürür:
        (P(z), P'(z), b_katsayilari)
    """
    derece = len(katsayilar) - 1

    # Adım 1: b dizisini hesapla  →  P(z) = b[0]
    b = [0] * (derece + 1)
    b[derece] = katsayilar[derece]
    for k in range(derece - 1, -1, -1):
        b[k] = katsayilar[k] + b[k + 1] * nokta

    # Adım 2: c dizisini hesapla  →  P'(z) = c[1]
    c = [0] * (derece + 1)
    c[derece] = b[derece]
    for k in range(derece - 1, 0, -1):
        c[k] = b[k] + c[k + 1] * nokta

    return b[0], c[1], b


# ---------------------------------------------------------------
# DEFLASYON (Bölüm 1.12)
# ---------------------------------------------------------------
def deflasyon(katsayilar, kok):
    """
    Bulunan bir köke göre polinomu (x - kök) ile bölerek
    derecesi 1 azaltılmış yeni polinomun katsayılarını döndürür.

    P(x) = (x - kök) * Q(x)  →  Q(x)'in katsayıları döndürülür.
    Horner şemasından çıkan b[1..n] katsayıları Q'yu verir.
    """
    _, _, b = horner(katsayilar, kok)
    return b[1:]   # b[1], b[2], ..., b[n]  →  Q'nun katsayıları


# ---------------------------------------------------------------
# NEWTON-RAPHSON YÖNTEMİ (tek kök için)
# ---------------------------------------------------------------
def newton_raphson(katsayilar, baslangic_noktasi, tolerans=1e-12, maks_iter=200):
    """
    Newton-Raphson iterasyonu: x_{k+1} = x_k - P(x_k) / P'(x_k)
    Horner şeması kullanılarak her adımda P ve P' hesaplanır.

    Parametreler:
        katsayilar       : polinom katsayıları [a0, a1, ..., an]
        baslangic_noktasi: ilk tahmin (gerçel veya karmaşık olabilir)
        tolerans         : yakınsama koşulu için eşik değer
        maks_iter        : maksimum iterasyon sayısı

    Döndürür:
        Bulunan yaklaşık kök
    """
    x = baslangic_noktasi

    for _ in range(maks_iter):
        p_degeri, p_turev, _ = horner(katsayilar, x)

        # Türev sıfırsa devam edemeyiz, iterasyonu sonlandır
        if abs(p_turev) == 0:
            break

        x_yeni = x - p_degeri / p_turev

        # Yakınsama kontrolü: iki ardışık tahmin arasındaki fark küçüldüyse dur
        if abs(x_yeni - x) < tolerans:
            return x_yeni

        x = x_yeni

    return x


# ---------------------------------------------------------------
# TÜM KÖKLERİ BULMAK: Newton-Raphson + Deflasyon Döngüsü
# ---------------------------------------------------------------
def tum_kokleri_bul(katsayilar):
    """
    Deflasyon döngüsüyle polinomun tüm köklerini bulur.

    Mantık:
      1. Bir başlangıç noktasından Newton-Raphson ile bir kök bul.
      2. Bulunan köke göre deflasyon yap (polinomun derecesini 1 düşür).
      3. Kalan derece 1 olana kadar tekrarla.
      4. Son 1. derece polinom için doğrudan çöz.

    Karmaşık köklere ulaşmak için hem gerçel hem karmaşık başlangıç
    noktaları denenir.
    """
    kokler = []
    mevcut_katsayilar = list(katsayilar)

    # Farklı bölgeleri tararken kullanılacak başlangıç noktaları
    # (gerçel ve karmaşık kökleri kapsayacak şekilde seçildi)
    baslangic_noktalari = [
        1.0, -1.0, 2.0, -2.0,
        complex(1, 1), complex(-1, 1), complex(1, -1), complex(-1, -1)
    ]

    # Her adımda bir kök bul, deflasyon yap
    while len(mevcut_katsayilar) > 2:
        kok_bulundu = False

        for baslangic in baslangic_noktalari:
            aday = newton_raphson(mevcut_katsayilar, baslangic)
            p_degeri, _, _ = horner(mevcut_katsayilar, aday)

            # P(aday) yeterince sıfıra yakınsa gerçek kök kabul et
            if abs(p_degeri) < 1e-7:
                kokler.append(aday)
                mevcut_katsayilar = deflasyon(mevcut_katsayilar, aday)
                kok_bulundu = True
                break

        if not kok_bulundu:
            print("  [Uyarı] Bu adımda kök bulunamadı, döngü sonlandırıldı.")
            break

    # Kalan polinom 1. derece ise: a0 + a1*x = 0  →  x = -a0 / a1
    if len(mevcut_katsayilar) == 2:
        son_kok = -mevcut_katsayilar[0] / mevcut_katsayilar[1]
        kokler.append(son_kok)

    return kokler


# ---------------------------------------------------------------
# ÇIKTIYI DÜZGÜN FORMATLA
# ---------------------------------------------------------------
def koku_yazdir(indeks, kok):
    """Bir kökü okunabilir biçimde ekrana yazar."""
    if isinstance(kok, complex):
        gercek_kisim = kok.real
        sanal_kisim  = kok.imag
    else:
        gercek_kisim = float(kok)
        sanal_kisim  = 0.0

    if abs(sanal_kisim) < 1e-8:
        # Gerçel kök
        print(f"  Kök {indeks}: {gercek_kisim:.8f}  (gerçel)")
    else:
        # Karmaşık kök
        isaret = "+" if sanal_kisim >= 0 else "-"
        print(f"  Kök {indeks}: {gercek_kisim:.6f} {isaret} {abs(sanal_kisim):.6f}i  (karmaşık)")


# ---------------------------------------------------------------
# ANA PROGRAM
# ---------------------------------------------------------------
def main():
    print("=" * 55)
    print("  POLİNOM KÖK BULMA PROGRAMI")
    print("  Yöntem: Newton-Raphson + Horner + Deflasyon")
    print("=" * 55)

    # Kullanıcıdan derece al
    while True:
        try:
            derece = int(input("\nPolinomun derecesini girin: "))
            if derece < 1:
                print("  Derece en az 1 olmalıdır.")
                continue
            break
        except ValueError:
            print("  Lütfen tam sayı girin.")

    # Katsayıları al
    print(f"\nKatsayıları a0'dan a{derece}'ye kadar girin:")
    print(f"  (P(x) = a0 + a1*x + ... + a{derece}*x^{derece})\n")

    katsayilar = []
    for i in range(derece + 1):
        while True:
            try:
                girdii = input(f"  a{i}  (x^{i} katsayısı): ")
                katsayilar.append(float(girdii))
                break
            except ValueError:
                print("  Geçerli bir sayı girin.")

    # En yüksek derecenin katsayısı sıfır olamaz
    if katsayilar[-1] == 0:
        print("\nHata: En yüksek derecenin katsayısı (a{}) sıfır olamaz!".format(derece))
        return

    print("\nKökler hesaplanıyor...\n")

    bulunan_kokler = tum_kokleri_bul(katsayilar)

    # Sonuçları yazdır
    print(f"Bulunan {len(bulunan_kokler)} kök:")
    print("-" * 45)
    for i, kok in enumerate(bulunan_kokler, start=1):
        koku_yazdir(i, kok)

    # Doğrulama: her kökü orijinal polinoma koy, değer sıfıra yakın olmalı
    print("\nDoğrulama  |P(kök)| değerleri (sıfıra yakın olmalı):")
    print("-" * 45)
    for i, kok in enumerate(bulunan_kokler, start=1):
        p_degeri, _, _ = horner(katsayilar, kok)
        print(f"  |P(Kök {i})| = {abs(p_degeri):.3e}")


if __name__ == "__main__":
    main()
