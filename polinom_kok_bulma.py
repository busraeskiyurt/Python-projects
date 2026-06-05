# Polinom Kök Bulma Programı
# Newton-Raphson Yöntemi + Horner Şeması + Deflasyon (İndirgeme)
# Kaynak: Bölüm 1.9 - "The Newton Method for Polynomials"
#
# Yöntemin özeti:
#   1. Horner şeması ile P(z) ve P'(z) hesapla
#   2. Newton iterasyonu: x = x - P(x)/P'(x)
#   3. Kök bulunca deflasyon: P(x) = (x - kok) * Q(x)
#   4. Q(x) üzerinde aynı işlemi tekrarla


def horner(katsayilar, z):
    # Horner şeması: P(z) ve P'(z) değerlerini hesaplar
    # katsayilar[0] = en yüksek dereceli katsayı (a_n)
    # katsayilar[-1] = sabit terim (a_0)
    #
    # Algoritma (Bölüm 1.9, Algoritma 1.25):
    #   b_n = a_n
    #   b_k = a_k + b_{k+1} * z   (k = n-1, ..., 0)
    #   P(z) = b_0
    #
    # Türev için:
    #   c_n = b_n
    #   c_k = b_k + c_{k+1} * z   (k = n-1, ..., 1)
    #   P'(z) = c_1

    n = len(katsayilar) - 1

    # b dizisini hesapla
    b = [complex(0)] * (n + 1)
    b[0] = complex(katsayilar[0])
    for i in range(1, n + 1):
        b[i] = katsayilar[i] + b[i - 1] * z

    polinom_degeri = b[n]  # P(z)

    if n < 1:
        return polinom_degeri, complex(0), b

    # c dizisini hesapla (türev için)
    c = [complex(0)] * n
    c[0] = b[0]
    for i in range(1, n):
        c[i] = b[i] + c[i - 1] * z

    turev_degeri = c[n - 1]  # P'(z)

    return polinom_degeri, turev_degeri, b


def newton_raphson(katsayilar, baslangic_nokta):
    # Newton-Raphson iterasyonu: x_{k+1} = x_k - P(x_k) / P'(x_k)
    # Yakınsama sağlanana veya maksimum iterasyona ulaşana kadar devam eder

    tolerans = 1e-10
    maks_iterasyon = 500

    x = complex(baslangic_nokta)

    for _ in range(maks_iterasyon):
        polinom_deger, turev_deger, _ = horner(katsayilar, x)

        # Türev sıfırsa iterasyonu durdur
        if abs(turev_deger) < 1e-30:
            break

        adim = polinom_deger / turev_deger
        x = x - adim

        # Yakınsama koşulu: adım yeterince küçükse
        if abs(adim) < tolerans:
            return x

    # Son doğrulama: P(x) sıfıra yeterince yakın mı?
    polinom_deger, _, _ = horner(katsayilar, x)
    if abs(polinom_deger) < 1e-5:
        return x

    return None  # Yakınsamadı


def tum_kokleri_bul(katsayilar):
    # Deflasyon yöntemi ile polinomun tüm köklerini bulur
    #
    # Her adımda:
    #   1. Aktif polinomun bir kökünü Newton-Raphson ile bul
    #   2. Deflasyon: P(x) = (x - kok) * Q(x)
    #      Q'nun katsayıları Horner'dan gelen b[0], ..., b[n-1]
    #   3. Q üzerinde aynı işlemi tekrarla

    aktif_katsayilar = [complex(k) for k in katsayilar]
    bulunan_kokler = []

    while len(aktif_katsayilar) > 1:
        aktif_derece = len(aktif_katsayilar) - 1

        # Derece 1 ise doğrudan çöz: a*x + b = 0
        if aktif_derece == 1:
            kok = -aktif_katsayilar[1] / aktif_katsayilar[0]
            bulunan_kokler.append(kok)
            break

        # Başlangıç noktaları için ölçek hesapla (Cauchy sınırı)
        # Tüm kökler |x| <= 1 + max|a_k / a_n| çemberinde yer alır
        a_n = aktif_katsayilar[0]
        olcek = 1.0 + max(abs(aktif_katsayilar[i] / a_n)
                          for i in range(1, len(aktif_katsayilar)))
        olcek = min(olcek, 50.0)  # aşırı büyümesini engelle

        # Farklı başlangıç noktaları: gerçel ve karmaşık düzlemi kapsar
        # Hem birim çember üzerinde hem de ölçeklenmiş noktalarda dene
        baslangic_listesi = [
            complex(olcek, 0),
            complex(-olcek, 0),
            complex(0, olcek),
            complex(0, -olcek),
            complex(olcek * 0.7, olcek * 0.7),
            complex(-olcek * 0.7, olcek * 0.7),
            complex(olcek * 0.7, -olcek * 0.7),
            complex(-olcek * 0.7, -olcek * 0.7),
            complex(olcek * 0.4, olcek * 0.9),
            complex(-olcek * 0.4, -olcek * 0.9),
            complex(olcek * 0.9, -olcek * 0.4),
            complex(-olcek * 0.9, olcek * 0.4),
            complex(1, 0),
            complex(-1, 0),
            complex(0.5, 0.5),
            complex(-0.5, 0.5),
            complex(0.5, -0.5),
            complex(-0.5, -0.5),
            complex(0, 1),
            complex(0, -1),
        ]

        bulunan_kok = None

        for baslangic in baslangic_listesi:
            sonuc = newton_raphson(aktif_katsayilar, baslangic)
            if sonuc is not None:
                bulunan_kok = sonuc
                break

        if bulunan_kok is None:
            print("  Uyarı: Bu adımda kök bulunamadı.")
            break

        bulunan_kokler.append(bulunan_kok)

        # Deflasyon: aktif polinomu bulunan köke göre böl
        # Horner'ın b dizisinin ilk n elemanı Q_{n-1}(x) katsayılarını verir
        _, _, b_dizisi = horner(aktif_katsayilar, bulunan_kok)
        aktif_katsayilar = b_dizisi[:-1]  # son eleman P(kok) ≈ 0, atılır

    return bulunan_kokler


def ana():
    print("=" * 58)
    print("  Polinom Kök Bulma Programı")
    print("  Yöntem: Newton-Raphson + Horner Şeması + Deflasyon")
    print("=" * 58)

    while True:
        print()

        # --- Derece girişi ---
        while True:
            try:
                derece = int(input("  Polinomun derecesini girin (n >= 1): "))
                if derece >= 1:
                    break
                print("  Hata: Derece en az 1 olmalıdır.")
            except ValueError:
                print("  Hata: Lütfen tam sayı girin.")

        # --- Katsayı girişi (yüksek dereceden düşüğe) ---
        katsayilar = []
        print(f"\n  Katsayıları {derece}. dereceden 0. dereceye girin:")
        for i in range(derece, -1, -1):
            while True:
                try:
                    giri = input(f"    x^{i} katsayisi: ")
                    deger = float(giri)
                    if i == derece and deger == 0:
                        print("  Hata: En yüksek dereceli katsayı sıfır olamaz!")
                        continue
                    katsayilar.append(deger)
                    break
                except ValueError:
                    print("  Hata: Sayısal değer girin.")

        # --- Girilen polinomu göster ---
        print("\n  Girilen polinom:")
        terimler = []
        for i, a in enumerate(katsayilar):
            ust = derece - i
            if abs(a) < 1e-15:
                continue
            if ust == 0:
                terimler.append(f"({a:g})")
            elif ust == 1:
                terimler.append(f"({a:g})x")
            else:
                terimler.append(f"({a:g})x^{ust}")
        print("  P(x) = " + " + ".join(terimler) if terimler else "  P(x) = 0")

        # --- Kökleri hesapla ---
        print("\n  Hesaplanıyor...")
        kokler = tum_kokleri_bul(katsayilar)

        # --- Sonuçları göster ---
        if not kokler:
            print("  Sonuç: Kök bulunamadı.")
        else:
            print(f"\n  Bulunan {len(kokler)} kök:")
            for i, kok in enumerate(kokler, 1):
                gercek_kisim = kok.real
                hayali_kisim = kok.imag
                if abs(hayali_kisim) < 1e-8:
                    print(f"    Kok {i}: {gercek_kisim:.8f}")
                else:
                    isaret = "+" if hayali_kisim >= 0 else "-"
                    print(f"    Kok {i}: {gercek_kisim:.8f} {isaret} {abs(hayali_kisim):.8f}i")

            # --- Doğrulama ---
            print("\n  Dogrulama - |P(kok)| degerleri (0'a ne kadar yakin?):")
            katsayilar_k = [complex(k) for k in katsayilar]
            for i, kok in enumerate(kokler, 1):
                pz, _, _ = horner(katsayilar_k, kok)
                print(f"    |P(Kok {i})| = {abs(pz):.2e}")

        # --- Tekrar sor ---
        print()
        cevap = input("  Yeni bir polinom girmek ister misiniz? (e/h): ").strip().lower()
        if cevap != 'e':
            print("  Program sonlandırıldı.")
            break
        print("\n" + "=" * 58)


ana()
