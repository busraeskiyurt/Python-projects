# Polinom denkleminin tüm köklerini bulan program
# Yöntem: Newton-Raphson + Horner Şeması + İndirgeme (Bölüm 1.9)
# Polinom: P(x) = a0 + a1*x + a2*x^2 + ... + an*x^n

def horner(katsayilar, z):
    """
    Horner şemasıyla P(z) ve P'(z) değerlerini aynı anda hesaplar.
    katsayilar: [a0, a1, ..., an] -> küçük kuvvetten büyüğe sıralı
    Döndürür: (P(z), P'(z), b_dizisi)
    b_dizisi[1..n] -> indirgeme için kullanılır
    """
    n = len(katsayilar) - 1

    # b dizisi: Algorithm 1.25 - P(z) hesabı
    b = [0] * (n + 1)
    b[n] = katsayilar[n]

    # c dizisi: P'(z) hesabı
    c = [0] * (n + 1)
    c[n] = b[n]

    # j = n-1 den 1'e kadar b ve c birlikte hesaplanır
    for j in range(n - 1, 0, -1):
        b[j] = katsayilar[j] + z * b[j + 1]
        c[j] = b[j] + z * c[j + 1]

    # b[0] = P(z), c[1] = P'(z)
    b[0] = katsayilar[0] + z * b[1]

    return b[0], c[1], b


def newton_raphson(katsayilar, baslangic_noktasi, tolerans=1e-12, max_iter=200):
    """
    Horner şemasını kullanan Newton-Raphson iterasyonu.
    x_{k+1} = x_k - P(x_k) / P'(x_k)
    Tek bir kök yaklaşımı döndürür.
    """
    x = complex(baslangic_noktasi)  # karmaşık aritmetik için

    for _ in range(max_iter):
        pz, turev, _ = horner(katsayilar, x)

        if turev == 0:
            break  # türev sıfırsa iterasyon durur

        x_yeni = x - pz / turev

        # Yakınsama kriteri: |x_yeni - x| < tolerans
        if abs(x_yeni - x) < tolerans:
            return x_yeni

        x = x_yeni

    return x


def indirgeme(katsayilar, kok):
    """
    Polinomu bulunan köke göre (x - kök) ile böler.
    Horner şemasından elde edilen b[1..n] katsayıları indirgenmiş polinomu verir.
    P(x) = (x - kök) * Q(x) -> Q katsayıları döndürülür.
    """
    _, _, b = horner(katsayilar, kok)
    # b[1], b[2], ..., b[n] -> indirgenmiş polinom katsayıları
    return b[1:]


def tum_kokleri_bul(katsayilar):
    """
    Newton-Raphson + İndirgeme şeması ile tüm kökleri bulur.
    Her kök bulunduktan sonra polinom bir derece indirgenir.
    """
    # Farklı başlangıç noktaları: gerçel ve karmaşık kombinasyonlar
    baslangic_noktalari = [
        complex(0.5, 0.5),
        complex(-0.5, 0.5),
        complex(0.5, -0.5),
        complex(-0.5, -0.5),
        complex(1.5, 0),
        complex(-1.5, 0),
        complex(0, 1.5),
        complex(3, 1),
        complex(-3, 1),
        complex(0.1, 0.1),
    ]

    kökler = []
    guncel = katsayilar[:]

    # Polinom derecesi 1'den büyük olduğu sürece kök ara
    while len(guncel) > 2:
        kok_bulundu = False

        for baslangic in baslangic_noktalari:
            aday = newton_raphson(guncel, baslangic)

            # Adayı orijinal polinom üzerinde doğrula
            deger, _, _ = horner(guncel, aday)

            if abs(deger) < 1e-6:
                kökler.append(aday)
                guncel = indirgeme(guncel, aday)  # polinomu indirgeme
                kok_bulundu = True
                break

        if not kok_bulundu:
            # Hiçbir başlangıç noktası işe yaramadıysa döngüyü kır
            print("  Uyari: Bir kok bulunamadi, farkli baslangic deneyin.")
            break

    # Son lineer polinom: a0 + a1*x = 0 -> x = -a0 / a1
    if len(guncel) == 2:
        son_kok = -guncel[0] / guncel[1]
        kökler.append(complex(son_kok))

    return kökler


def kokleri_yazdir(kökler, orijinal_katsayilar):
    """Kökleri ve doğrulama değerlerini ekrana yazar."""
    print("\n--- Sonuclar ---")
    for i, kok in enumerate(kökler, 1):
        gercek = kok.real
        sanal = kok.imag

        # Doğrulama: orijinal polinomda P(kök) hesapla
        deger, _, _ = horner(orijinal_katsayilar, kok)

        if abs(sanal) < 1e-8:
            print(f"  Kok {i}: {gercek:.8f}   |P(kok)| = {abs(deger):.2e}")
        elif sanal > 0:
            print(f"  Kok {i}: {gercek:.8f} + {sanal:.8f}i   |P(kok)| = {abs(deger):.2e}")
        else:
            print(f"  Kok {i}: {gercek:.8f} - {abs(sanal):.8f}i   |P(kok)| = {abs(deger):.2e}")


def main():
    print("=" * 55)
    print("  Newton-Raphson + Horner Indirgemesi ile Kok Bulucu")
    print("  (Bolum 1.9 - Algorithm 1.25)")
    print("=" * 55)

    while True:
        print()

        # Derece girişi
        try:
            derece = int(input("Polinom derecesini girin (cikis icin 0): "))
        except ValueError:
            print("Gecersiz giris, lutfen tam sayi girin.")
            continue

        if derece == 0:
            print("Program sonlandiriliyor.")
            break

        if derece < 1:
            print("Derece en az 1 olmalidir.")
            continue

        # Katsayı girişi: büyük kuvvetten küçüğe (kullanıcı dostu sıra)
        print(f"Katsayilari girin (a{derece}'den a0'a dogru):")
        ham_katsayilar = []
        hata = False

        for k in range(derece, -1, -1):
            try:
                girdi = float(input(f"  a{k} (x^{k} katsayisi): "))
                ham_katsayilar.append(girdi)
            except ValueError:
                print("Gecersiz katsayi, tekrar deneyin.")
                hata = True
                break

        if hata:
            continue

        if ham_katsayilar[0] == 0:
            print("En yuksek dereceli katsayi sifir olamaz!")
            continue

        # İç format: katsayilar[i] = x^i katsayısı -> listeyi ters çevir
        katsayilar = ham_katsayilar[::-1]

        print("\nKokler hesaplaniyor...")
        kökler = tum_kokleri_bul(katsayilar)

        kokleri_yazdir(kökler, katsayilar)

        # Döngü başa döner, yeni polinom sorulur


main()
