# =============================================================
#  Polinom Kök Bulma Programı
#  Newton-Raphson Yöntemi - Horner Şeması ve Deflasyon
#  (Ders notları Bölüm 1.9 - Algorithm 1.25)
# =============================================================
#
#  Yöntemin özeti:
#  1. Horner şeması ile P(x) ve P'(x) hesaplanır.
#  2. Newton-Raphson formülü: x_yeni = x - P(x) / P'(x)
#  3. Bir kök bulununca deflasyon yapılır: P(x) = (x - kok) * Q(x)
#  4. Q üzerinde aynı işlem tekrarlanır, tüm kökler bulunur.
#
#  Polinom biçimi: P(x) = a0 + a1*x + a2*x^2 + ... + an*x^n
# =============================================================


def horner(katsayilar, z):
    """
    Horner şeması ile P(z) ve P'(z) hesaplar.

    katsayilar : [a0, a1, ..., an]  -- artan derecede
    z          : hesaplanacak nokta (gerçel veya karmaşık)

    Döndürür   : (P(z), P'(z), b_listesi)
    b_listesi deflasyon adımında kullanılır.
    """
    n = len(katsayilar) - 1

    # --- P(z) için b dizisi ---
    # b[n] = a[n],  b[k] = a[k] + b[k+1] * z
    b = [0] * (n + 1)
    b[n] = katsayilar[n]
    for k in range(n - 1, -1, -1):
        b[k] = katsayilar[k] + b[k + 1] * z
    # b[0] = P(z)

    # --- P'(z) için c dizisi ---
    # c[n] = b[n],  c[k] = b[k] + c[k+1] * z
    c = [0] * (n + 1)
    c[n] = b[n]
    for k in range(n - 1, 0, -1):
        c[k] = b[k] + c[k + 1] * z
    # c[1] = P'(z)

    return b[0], c[1], b


def newton_raphson(katsayilar, baslangic, tolerans=1e-10, maks_iter=150):
    """
    Newton-Raphson iterasyonu ile tek bir kök bulur.
    Karmaşık başlangıç noktası kullanılabilir; karmaşık kökler de bulunabilir.
    """
    x = complex(baslangic)

    for _ in range(maks_iter):
        pz, pz_turev, _ = horner(katsayilar, x)

        if pz_turev == 0:
            break  # türev sıfır, bu noktada devam edilemez

        x_yeni = x - pz / pz_turev

        if abs(x_yeni - x) < tolerans:
            return x_yeni

        x = x_yeni

    return x


def tum_kokleri_bul(katsayilar):
    """
    Tüm kökleri Newton-Raphson + deflasyon döngüsüyle bulur.

    Her adımda bir kök bulunur, ardından polinom bir derece aşağı indirilir.
    Karmaşık kökler de dahil olmak üzere n adet kök döndürülür.
    """
    kokler = []

    # Karmaşık sayı aritmetiği için katsayıları dönüştür
    polinom = [complex(k) for k in katsayilar]

    # Farklı köklere yakınsayabilmek için birkaç başlangıç noktası kullanılır
    baslangic_noktalari = [1.0, -1.0, complex(1, 1), complex(-1, -1)]

    while len(polinom) > 2:  # derece >= 1 olduğu sürece devam et

        kok_bulundu = False

        for baslangic in baslangic_noktalari:
            aday = newton_raphson(polinom, baslangic)
            pz, _, b = horner(polinom, aday)

            # Kök yeterince iyi yaklaşıyorsa kabul et
            if abs(pz) < 1e-6:

                # Çok küçük sanal kısım varsa gerçel kök kabul edilir
                if abs(aday.imag) < 1e-8:
                    aday = aday.real

                kokler.append(aday)

                # Deflasyon: P(x) = (x - aday) * Q(x)
                # Q'nun katsayıları b[1], b[2], ..., b[n]
                polinom = [b[i] for i in range(1, len(b))]

                kok_bulundu = True
                break

        if not kok_bulundu:
            # Başlangıç noktaları işe yaramadıysa farklı değerler dene
            for yedek in [2.0, -2.0, 0.5, complex(0, 1)]:
                aday = newton_raphson(polinom, yedek)
                pz, _, b = horner(polinom, aday)
                if abs(pz) < 1e-5:
                    if abs(aday.imag) < 1e-8:
                        aday = aday.real
                    kokler.append(aday)
                    polinom = [b[i] for i in range(1, len(b))]
                    kok_bulundu = True
                    break

            if not kok_bulundu:
                break  # kök bulunamadı, döngüden çık

    # Geriye doğrusal bir polinom kaldıysa: a0 + a1*x = 0  =>  x = -a0/a1
    if len(polinom) == 2 and polinom[1] != 0:
        son_kok = -polinom[0] / polinom[1]
        if abs(son_kok.imag) < 1e-8:
            son_kok = son_kok.real
        kokler.append(son_kok)

    return kokler


def polinomu_yazdir(katsayilar):
    """Polinomu okunabilir formatta döndürür."""
    n = len(katsayilar) - 1
    parcalar = []
    for i in range(n, -1, -1):
        k = katsayilar[i]
        if abs(k) < 1e-12:
            continue
        if i == 0:
            parcalar.append(f"{k:g}")
        elif i == 1:
            parcalar.append(f"{k:g}x")
        else:
            parcalar.append(f"{k:g}x^{i}")
    return " + ".join(parcalar) if parcalar else "0"


def koku_yazdir(sira, kok):
    """Bir kökü düzgün biçimde ekrana basar."""
    if isinstance(kok, complex):
        if kok.imag >= 0:
            print(f"  Kök {sira}: {kok.real:.8f} + {kok.imag:.8f}i")
        else:
            print(f"  Kök {sira}: {kok.real:.8f} - {abs(kok.imag):.8f}i")
    else:
        print(f"  Kök {sira}: {kok:.8f}")


def main():
    print("=" * 55)
    print("   Polinom Kök Bulma Programı")
    print("   Yöntem: Newton-Raphson + Horner + Deflasyon")
    print("=" * 55)
    print()

    # Kullanıcıdan polinom bilgilerini al
    derece = int(input("Polinomun derecesini giriniz: "))
    print()
    print(f"Katsayıları giriniz:")
    print(f"  P(x) = a0 + a1*x + ... + a{derece}*x^{derece}")
    print()

    katsayilar = []
    for i in range(derece + 1):
        while True:
            try:
                deger = float(input(f"  a{i} (x^{i} katsayisi) = "))
                katsayilar.append(deger)
                break
            except ValueError:
                print("  Hatalı giriş, sayı giriniz.")

    print()
    print(f"Polinom: P(x) = {polinomu_yazdir(katsayilar)}")
    print()

    # Kökleri hesapla
    kokler = tum_kokleri_bul(katsayilar)

    print(f"Bulunan {len(kokler)} kök:")
    print("-" * 45)
    for sira, kok in enumerate(kokler, 1):
        koku_yazdir(sira, kok)

    # Doğrulama: her kökü orijinal polinoma geri koy
    print()
    print("Doğrulama  |P(kök)| değerleri (sıfıra yakın olmalı):")
    print("-" * 45)
    for sira, kok in enumerate(kokler, 1):
        pz, _, _ = horner(katsayilar, complex(kok))
        print(f"  |P(kök {sira})| = {abs(pz):.3e}")


if __name__ == "__main__":
    main()
