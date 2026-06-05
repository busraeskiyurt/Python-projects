# Polinom denkleminin tüm köklerini bulan program
# Yöntem: Newton-Raphson + Horner şeması (Bölüm 1.9) + Deflasyon (Bölüm 1.12)


def horner(katsayilar, nokta):
    # Horner şemasıyla P(nokta) ve P'(nokta) değerlerini hesaplar
    # katsayilar listesi: [a0, a1, ..., an] (a0 sabit terim, an en yüksek kuvvet)
    n = len(katsayilar) - 1
    b = katsayilar[n]   # b_n = a_n den başla
    c = b               # c_n = b_n
    for j in range(n - 1, 0, -1):
        b = katsayilar[j] + b * nokta   # b_j = a_j + b_{j+1} * z
        c = b + c * nokta               # c_j = b_j + c_{j+1} * z
    b = katsayilar[0] + b * nokta       # b_0 = P(nokta)
    return b, c  # b polinom değeri, c türev değeri


def deflasyon(katsayilar, kok):
    # Bulunan kökü bölerek polinomun derecesini bir düşürür
    # P_n(x) = (x - kok) * Q_{n-1}(x) şeklinde yazar
    n = len(katsayilar) - 1
    yeni = [0.0] * n
    yeni[n - 1] = katsayilar[n]   # en yüksek katsayı aynı kalır
    for j in range(n - 2, -1, -1):
        yeni[j] = katsayilar[j + 1] + yeni[j + 1] * kok
    return yeni


def newton_raphson(katsayilar, baslangic):
    # x_{k+1} = x_k - P(x_k) / P'(x_k) iterasyonu
    x = baslangic
    for _ in range(500):
        deger, turev = horner(katsayilar, x)
        if turev == 0:
            break
        x_yeni = x - deger / turev
        if abs(x_yeni - x) < 1e-10:
            return x_yeni
        x = x_yeni
    return x


def tum_kokleri_bul(katsayilar):
    kokler = []
    mevcut = katsayilar[:]

    # Hem reel hem karmaşık kökleri yakalayabilmek için farklı başlangıç noktaları
    baslangiclar = [1.0, -1.0, complex(1, 1), complex(-1, -1)]

    while len(mevcut) > 2:
        bulundu = False
        for baslangic in baslangiclar:
            aday = newton_raphson(mevcut, baslangic)
            deger, _ = horner(mevcut, aday)
            if abs(deger) < 1e-6:
                kokler.append(aday)
                mevcut = deflasyon(mevcut, aday)  # polinomu daralt
                bulundu = True
                break
        if not bulundu:
            print("Uyari: Bazi kokler bulunamadi. Farkli bir polinom deneyin.")
            break

    # Son kalan doğrusal polinom: a1*x + a0 = 0 => x = -a0/a1
    if len(mevcut) == 2:
        kokler.append(-mevcut[0] / mevcut[1])

    return kokler


def polinomu_yazdir(katsayilar, derece):
    # Polinomu ekranda göster
    ifade = ""
    for i in range(derece, -1, -1):
        kat = katsayilar[i]
        if kat == 0:
            continue
        if i == 0:
            ifade += f" + {kat}" if kat > 0 and ifade else f"{kat}"
        elif i == 1:
            ifade += f" + {kat}x" if kat > 0 and ifade else f"{kat}x"
        else:
            ifade += f" + {kat}x^{i}" if kat > 0 and ifade else f"{kat}x^{i}"
    print(f"P(x) = {ifade} = 0")


# ==================== ANA PROGRAM ====================
while True:
    print("\n====================================")
    print("   Polinom Kok Bulucu  (Newton-Raphson + Horner)")
    print("====================================")

    derece = int(input("Polinomun derecesini girin: "))

    print(f"\nKatsayilari girin (a0 sabit terim, a{derece} en buyuk kuvvetin katsayisi):")
    katsayilar = []
    for i in range(derece + 1):
        kat = float(input(f"  a{i} (x^{i} katsayisi): "))
        katsayilar.append(kat)

    print("\nGirilen polinom:")
    polinomu_yazdir(katsayilar, derece)

    kokler = tum_kokleri_bul(katsayilar)

    print(f"\nBulunan {len(kokler)} kok:")
    for i, kok in enumerate(kokler):
        print(f"  Kok {i + 1}: {kok}")

    devam = input("\nYeni bir polinom cozmek ister misiniz? (e/h): ")
    if devam.lower() != "e":
        print("Program sonlandirildi.")
        break
