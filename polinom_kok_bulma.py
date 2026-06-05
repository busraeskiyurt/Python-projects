# Polinom Denkleminin Tüm Köklerini Bulan Program
# Yöntem: Newton-Raphson + Horner Şeması + İndirgeme (Deflation)
# Kaynak: Sayısal Analiz Ders Notu, Bölüm 1.9 ve 1.12

def horner(katsayilar, nokta):
    # Horner şeması: P(nokta) ve P'(nokta) değerlerini hesaplar
    # katsayilar listesi: [a0, a1, a2, ..., an] (küçük dereceden büyüğe)
    n = len(katsayilar) - 1

    # b dizisi hesabı - b[n] = a[n], b[k] = a[k] + b[k+1]*nokta
    b = [0] * (n + 1)
    b[n] = katsayilar[n]
    for k in range(n - 1, -1, -1):
        b[k] = katsayilar[k] + b[k + 1] * nokta

    # c dizisi hesabı - türev için, c[n] = b[n], c[k] = b[k] + c[k+1]*nokta
    c = [0] * (n + 1)
    c[n] = b[n]
    for k in range(n - 1, 0, -1):
        c[k] = b[k] + c[k + 1] * nokta

    # b[0] = P(nokta), c[1] = P'(nokta)
    return b[0], c[1], b

def newton_raphson(katsayilar, baslangic):
    # Newton-Raphson iterasyonu
    # Formül: x_yeni = x - P(x) / P'(x)
    x = complex(baslangic)
    tolerans = 1e-10

    for _ in range(500):
        polinom_degeri, turev_degeri, b = horner(katsayilar, x)

        if turev_degeri == 0:
            break  # Türev sıfırsa devam edilemez

        x_yeni = x - polinom_degeri / turev_degeri

        # Yakınsama kontrolü
        if abs(x_yeni - x) < tolerans:
            return x_yeni, b

        x = x_yeni

    return x, b

def tum_kokleri_bul(katsayilar):
    # Tüm kökleri indirgeme yöntemiyle bul
    # Her adımda bir kök çıkarılıp polinom bir derece küçültülür
    guncel_katsayilar = list(katsayilar)
    kokler = []

    # Hem gerçel hem karmaşık kökleri bulabilmek için karmaşık başlangıç noktaları
    deneme_noktalari = [1 + 1j, -1 + 1j, 0.5 - 0.5j, -1 - 1j, 2 + 0.5j]

    while len(guncel_katsayilar) > 2:
        en_iyi_kok = None
        en_iyi_b = None
        en_kucuk_hata = float('inf')

        # En iyi yakınsayan başlangıç noktasını seç
        for baslangic in deneme_noktalari:
            bulunan_kok, b = newton_raphson(guncel_katsayilar, baslangic)
            polinom_degeri, _, _ = horner(guncel_katsayilar, bulunan_kok)
            hata = abs(polinom_degeri)
            if hata < en_kucuk_hata:
                en_kucuk_hata = hata
                en_iyi_kok = bulunan_kok
                en_iyi_b = b

        kokler.append(en_iyi_kok)
        # İndirgeme: yeni polinomun katsayıları b[1], b[2], ..., b[n]
        guncel_katsayilar = en_iyi_b[1:]

    # Son birinci dereceli polinom kökü: a0 + a1*x = 0 => x = -a0/a1
    if len(guncel_katsayilar) == 2:
        son_kok = -guncel_katsayilar[0] / guncel_katsayilar[1]
        kokler.append(complex(son_kok))

    return kokler

# ====== Ana Program ======

print("Polinom Kök Bulucu - Newton-Raphson + Horner + İndirgeme")
print("=" * 55)

polinom_derecesi = int(input("\nPolinomun derecesini girin: "))

print(f"\nP(x) = a0 + a1*x + ... + a{polinom_derecesi}*x^{polinom_derecesi}")
print("Katsayıları küçük dereceden büyüğe (a0'dan başlayarak) girin:\n")

katsayilar = []
for i in range(polinom_derecesi + 1):
    katsayilar.append(float(input(f"  a{i} = ")))

# En yüksek dereceli katsayı kontrolü
if katsayilar[polinom_derecesi] == 0:
    print("Hata: En yüksek dereceli katsayı (a_n) sıfır olamaz!")
else:
    bulunan_kokler = tum_kokleri_bul(katsayilar)

    print(f"\n--- Sonuçlar: {polinom_derecesi}. Derece Polinom Kökleri ---")
    for sira, kok in enumerate(bulunan_kokler, 1):
        gercek_kisim = kok.real
        sanal_kisim = kok.imag
        if abs(sanal_kisim) < 1e-8:
            print(f"  x{sira} = {gercek_kisim:.8f}")
        elif sanal_kisim >= 0:
            print(f"  x{sira} = {gercek_kisim:.8f} + {sanal_kisim:.8f}j")
        else:
            print(f"  x{sira} = {gercek_kisim:.8f} - {abs(sanal_kisim):.8f}j")

    print("\n--- Doğrulama: P(xi) ≈ 0 olmalı ---")
    for sira, kok in enumerate(bulunan_kokler, 1):
        deger, _, _ = horner(katsayilar, kok)
        print(f"  P(x{sira}) = {deger:.3e}")
