# Polinom Denkleminin Tum Koklerini Bulan Program
# Yontem: Newton-Raphson + Horner Semasi + Deflasyon (Bolum 1.9)
# Herhangi bir dereceden polinom icin calisir, karmasik kokler de bulunur.

def horner(katsayilar, nokta):
    # Horner semasi: P(nokta) ve P'(nokta) degerlerini tek geciste hesapla
    # katsayilar listesi: [a0, a1, a2, ..., an] seklinde (sabiten buyuge dogru)
    # Ornek: x^3 - 6x^2 + 11x - 6 icin -> [-6, 11, -6, 1]
    n = len(katsayilar) - 1

    # --- Polinom degeri (b dizisi) ---
    # b[n] = a[n], b[k] = a[k] + b[k+1] * nokta
    b = [0] * (n + 1)
    b[n] = katsayilar[n]
    for k in range(n - 1, -1, -1):
        b[k] = katsayilar[k] + b[k + 1] * nokta

    polinom_degeri = b[0]  # P(nokta) = b[0]

    if n == 0:
        return polinom_degeri, 0, b

    # --- Turev degeri (c dizisi) ---
    # c[n] = b[n], c[k] = b[k] + c[k+1] * nokta
    c = [0] * (n + 1)
    c[n] = b[n]
    for k in range(n - 1, 0, -1):
        c[k] = b[k] + c[k + 1] * nokta

    turev_degeri = c[1]  # P'(nokta) = c[1]

    return polinom_degeri, turev_degeri, b


def newton_raphson(katsayilar, baslangic, tolerans=1e-10, maks_iterasyon=150):
    # Newton-Raphson iterasyonu: x_yeni = x_eski - P(x) / P'(x)
    x = baslangic

    for _ in range(maks_iterasyon):
        polinom_degeri, turev_degeri, _ = horner(katsayilar, x)

        # Zaten cok kucukse kok bulundu say
        if abs(polinom_degeri) < tolerans:
            return x

        # Turev sifirsa devam edemeyiz
        if turev_degeri == 0:
            break

        x_yeni = x - polinom_degeri / turev_degeri

        # Degisim cok kucukse yakinsadi
        if abs(x_yeni - x) < tolerans:
            return x_yeni

        x = x_yeni

    return x


def deflasyon(katsayilar, kok):
    # Bulunan koku polinom disina cikart: P(x) = (x - kok) * Q(x)
    # Q'nun katsayilari Horner hesabindaki b[1], b[2], ..., b[n]
    _, _, b = horner(katsayilar, kok)
    return b[1:]  # Kucultulmus polinom katsayilari


def tum_kokleri_bul(katsayilar):
    derece = len(katsayilar) - 1
    koklar = []
    gecici_katsayilar = list(katsayilar)

    # Farkli baslangic noktalari - gercek ve karmasik
    # Karmasik baslangic noktalari karmasik koklerin bulunmasini saglar
    baslangic_noktalari = [1.0, -1.0, complex(0, 1), complex(0, -1), 0.5]

    while len(koklar) < derece:
        mevcut_derece = len(gecici_katsayilar) - 1
        if mevcut_derece == 0:
            break

        bulunan_kok = None

        # Her baslangic noktasindan dene, gecerli kok bulununca dur
        for baslangic in baslangic_noktalari:
            aday_kok = newton_raphson(gecici_katsayilar, baslangic)
            kontrol_degeri, _, _ = horner(gecici_katsayilar, aday_kok)

            if abs(kontrol_degeri) < 1e-6:
                # Bu kok daha once bulunmus mu?
                yeni_kok = True
                for onceki_kok in koklar:
                    if abs(aday_kok - onceki_kok) < 1e-4:
                        yeni_kok = False
                        break

                if yeni_kok:
                    bulunan_kok = aday_kok
                    break

        if bulunan_kok is None:
            break

        koklar.append(bulunan_kok)

        # Deflasyon: bulunan koku polinom disina cikar, derecesi bir azalir
        gecici_katsayilar = deflasyon(gecici_katsayilar, bulunan_kok)

    return koklar


def main():
    print("=" * 50)
    print("    POLINOM KOK BULUCU")
    print("    Newton-Raphson + Horner Semasi + Deflasyon")
    print("=" * 50)
    print()

    derece = int(input("Polinom derecesini girin: "))

    print()
    print(f"Katsayilari girin (P(x) = a0 + a1*x + a2*x^2 + ... + a{derece}*x^{derece})")
    print()

    katsayilar = []
    for i in range(derece + 1):
        deger = float(input(f"  a{i}  (x^{i} onundeki katsayi): "))
        katsayilar.append(deger)

    # Polinomu ekrana yazdir
    print()
    print("Girilen polinom:")
    terimler = []
    for i in range(derece, -1, -1):
        if katsayilar[i] != 0:
            if i == 0:
                terimler.append(f"{katsayilar[i]:g}")
            elif i == 1:
                terimler.append(f"{katsayilar[i]:g}x")
            else:
                terimler.append(f"{katsayilar[i]:g}x^{i}")
    print("  P(x) = " + " + ".join(terimler))
    print()

    print("Hesaplaniyor...")
    koklar = tum_kokleri_bul(katsayilar)

    print()
    print(f"Bulunan kok sayisi: {len(koklar)}")
    print("-" * 40)

    for i, kok in enumerate(koklar, 1):
        # Karmasik kismı cok kucukse gercek sayi olarak goster
        if isinstance(kok, complex):
            if abs(kok.imag) > 1e-6:
                print(f"  Kok {i}: {kok.real:.8f} + ({kok.imag:.8f})i")
            else:
                print(f"  Kok {i}: {kok.real:.8f}")
        else:
            print(f"  Kok {i}: {kok:.8f}")

    print()
    print("Dogrulama - P(kok) degerleri (sifira yakin olmali):")
    print("-" * 40)
    for i, kok in enumerate(koklar, 1):
        deger, _, _ = horner(katsayilar, kok)
        print(f"  P(Kok {i}) = {deger:.4e}")

    print()
    print("Hesaplama tamamlandi.")


if __name__ == "__main__":
    main()
