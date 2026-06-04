# =============================================================================
# Newton-Raphson Yöntemi ile Polinom Kök Bulma Programı
# Yöntem: Horner Şeması (Bölüm 1.9) + Deflasyon Tekniği (Bölüm 1.12)
#
# Dış modül KULLANILMAMAKTADIR.
# Gerçel ve karmaşık kökler dahil her dereceden polinom desteklenir.
# =============================================================================


def horner_hesapla(katsayilar, nokta):
    """
    Horner şeması ile P(nokta) ve P'(nokta) değerlerini hesaplar.

    Polinom: P(x) = a0 + a1*x + a2*x^2 + ... + an*x^n
    katsayilar listesi: [a0, a1, a2, ..., an]  (düşük dereceden yükseğe)

    Özyinelemeli formül:
        b_n = a_n
        b_k = a_k + b_{k+1} * z    (k = n-1, n-2, ..., 0)
        P(z) = b_0

    Türev için:
        c_n = b_n
        c_k = b_k + c_{k+1} * z    (k = n-1, n-2, ..., 1)
        P'(z) = c_1

    Döndürür: (p_degeri, p_turev, b_listesi)
    """
    n = len(katsayilar) - 1   # polinom derecesi
    z = complex(nokta)         # karmaşık aritmetik kullan

    # --- b katsayılarını hesapla (P değeri için) ---
    b = [complex(0)] * (n + 1)
    b[n] = complex(katsayilar[n])
    for k in range(n - 1, -1, -1):
        b[k] = complex(katsayilar[k]) + b[k + 1] * z

    p_degeri = b[0]   # P(z) = b_0

    # --- c katsayılarını hesapla (P' değeri için) ---
    p_turev = complex(0)
    if n >= 1:
        c = [complex(0)] * (n + 1)
        c[n] = b[n]
        for k in range(n - 1, 0, -1):
            c[k] = b[k] + c[k + 1] * z
        p_turev = c[1]   # P'(z) = c_1

    return p_degeri, p_turev, b


def newton_raphson_kok(katsayilar, baslangic, tolerans=1e-12, maks_iter=500):
    """
    Newton-Raphson iterasyonu ile tek bir kök bulur.

    Formül: x_{k+1} = x_k - P(x_k) / P'(x_k)

    Durdurma kriteri: |x_{k+1} - x_k| < tolerans
    """
    x = complex(baslangic)

    for _ in range(maks_iter):
        p_val, p_turev, _ = horner_hesapla(katsayilar, x)

        # Türev çok küçükse düz noktaya yaklaştık; küçük sapma ekle
        if abs(p_turev) < 1e-14:
            x += complex(1e-7, 1e-7)
            continue

        x_yeni = x - p_val / p_turev

        if abs(x_yeni - x) < tolerans:
            return x_yeni

        x = x_yeni

    return x   # maks iterasyona ulaşıldı, son değeri döndür


def deflasyon_yap(katsayilar, kok):
    """
    Deflasyon tekniği: P(x) = (x - kök) * Q(x)

    Horner şemasındaki b katsayıları sayesinde Q_{n-1}(x) elde edilir:
        Q katsayıları = [b_1, b_2, ..., b_n]

    Bu sayede bir kök bulunduktan sonra aynı işlem n-1 dereceli
    polinom üzerinde tekrarlanabilir.
    """
    _, _, b = horner_hesapla(katsayilar, kok)
    return b[1:]   # Q_{n-1}(x)'in katsayıları (düşük dereceden yükseğe)


def kokleri_temizle(kok):
    """
    Sayısal hataları temizler:
    - Çok küçük hayali kısım → gerçel kök
    - Çok küçük gerçel kısım → saf sanal kök
    """
    gercek = kok.real if abs(kok.real) > 1e-9 else 0.0
    hayali = kok.imag if abs(kok.imag) > 1e-9 else 0.0

    if hayali == 0.0:
        return gercek          # gerçel sayı
    return complex(gercek, hayali)


def tum_kokleri_bul(katsayilar, tolerans=1e-10):
    """
    Tüm kökleri deflasyon döngüsüyle bulur.

    Her adımda:
      1. Newton-Raphson ile bir kök aranır.
      2. Kök doğrulanır: |P(kök)| küçük mü?
      3. Polinom o kökle indirgenir (deflasyon).
      4. Derece 1 kalana kadar tekrar edilir.
    """
    kokler = []
    suanki = [complex(k) for k in katsayilar]

    # Hem gerçel hem karmaşık kökleri yakalamak için çeşitli başlangıç noktaları
    baslangiclar = [
        1.0, -1.0, 2.0, -2.0, 0.5, -0.5, 3.0, -3.0, 0.0,
        5.0, -5.0, 7.0, -7.0, 10.0, -10.0, 0.1, -0.1,
        complex(1, 1),  complex(1, -1),
        complex(-1, 1), complex(-1, -1),
        complex(0, 1),  complex(0, -1),
        complex(0, 2),  complex(2, 2),
        complex(-2, 2), complex(3, 1),
        complex(0.5, 0.5), complex(4, 1),
    ]

    while len(suanki) > 2:   # derece >= 1 olduğu sürece devam et
        kok_bulundu = False

        for bas in baslangiclar:
            aday = newton_raphson_kok(suanki, bas, tolerans=1e-12)
            p_kontrol, _, _ = horner_hesapla(suanki, aday)

            # Kökü kabul etme eşiği
            if abs(p_kontrol) < 1e-6:
                temiz = kokleri_temizle(aday)
                kokler.append(temiz)
                suanki = deflasyon_yap(suanki, aday)   # polinomu indirge
                kok_bulundu = True
                break

        if not kok_bulundu:
            print("  [Uyari] Kök bulunamadı, döngü durduruluyor.")
            break

    # Geriye kalan derece-1 polinom: a0 + a1*x = 0  →  x = -a0 / a1
    if len(suanki) == 2:
        son = -suanki[0] / suanki[1]
        kokler.append(kokleri_temizle(son))

    return kokler


# -------------------- Yardımcı yazdırma fonksiyonları --------------------

def kok_str(kok):
    """Kökü okunabilir biçimde döndürür."""
    if isinstance(kok, complex):
        if kok.imag >= 0:
            return f"{kok.real:>12.7f}  +  {kok.imag:.7f}i"
        else:
            return f"{kok.real:>12.7f}  -  {abs(kok.imag):.7f}i"
    return f"{kok:>12.7f}"


def polinom_yaz(katsayilar):
    """Katsayı listesinden okunabilir polinom ifadesi oluşturur."""
    n = len(katsayilar) - 1
    parcalar = []
    for i in range(n, -1, -1):
        k = katsayilar[i]
        if k == 0:
            continue
        mutlak = abs(k)
        isaret = "+" if k >= 0 else "-"

        if i == 0:
            parcalar.append(f"{isaret} {mutlak:g}")
        elif i == 1:
            parcalar.append(f"{isaret} {mutlak:g}x" if mutlak != 1 else f"{isaret} x")
        else:
            parcalar.append(f"{isaret} {mutlak:g}x^{i}" if mutlak != 1 else f"{isaret} x^{i}")

    if not parcalar:
        return "0"
    # ilk parçanın işaretini düzenle
    sonuc = " ".join(parcalar).strip()
    if sonuc.startswith("+ "):
        sonuc = sonuc[2:]
    return sonuc


def test_calistir(katsayilar, baslik):
    """Tek bir test senaryosunu çalıştırır ve sonuçları ekrana yazar."""
    n = len(katsayilar) - 1
    print(f"\n{'=' * 68}")
    print(f"TEST  : {baslik}")
    print(f"Derece: {n}")
    print(f"P(x)  = {polinom_yaz(katsayilar)}")
    print("-" * 68)

    kokler = tum_kokleri_bul(katsayilar)

    print(f"Bulunan {len(kokler)} kök:\n")
    print(f"  {'No':<4}  {'Kök Değeri':<40}  {'|P(kök)| (hata)':>15}")
    print(f"  {'--':<4}  {'-'*40}  {'-'*15}")

    for i, kok in enumerate(kokler, 1):
        p_kontrol, _, _ = horner_hesapla([complex(k) for k in katsayilar], complex(kok))
        print(f"  {i:<4}  {kok_str(kok):<40}  {abs(p_kontrol):>15.3e}")

    return kokler


# ========================== ANA PROGRAM ==========================

if __name__ == "__main__":
    print("=" * 68)
    print("  Newton-Raphson + Horner Şeması + Deflasyon  —  Kök Bulucu")
    print("  Dış modül kullanılmamıştır.")
    print("=" * 68)

    # ------------------------------------------------------------------
    # Test 1: 2. derece — gerçel kökler
    # P(x) = x^2 - 5x + 6 = (x-2)(x-3)
    # Beklenen kökler: 2, 3
    # katsayilar = [a0, a1, a2] = [6, -5, 1]
    # ------------------------------------------------------------------
    test_calistir([6, -5, 1],
                  "2. Derece  |  x^2 - 5x + 6  |  Beklenen: 2,  3")

    # ------------------------------------------------------------------
    # Test 2: 3. derece — gerçel kökler (ders notundaki örnek)
    # P(x) = x^3 - 6x^2 + 11x - 6 = (x-1)(x-2)(x-3)
    # Beklenen kökler: 1, 2, 3
    # katsayilar = [-6, 11, -6, 1]
    # ------------------------------------------------------------------
    test_calistir([-6, 11, -6, 1],
                  "3. Derece  |  x^3 - 6x^2 + 11x - 6  |  Beklenen: 1, 2, 3")

    # ------------------------------------------------------------------
    # Test 3: 4. derece — karmaşık kökler
    # P(x) = x^4 + 2x^3 + 3x^2 + 2x + 2 = (x^2+1)(x^2+2x+2)
    # Beklenen kökler: +i, -i, -1+i, -1-i
    # katsayilar = [2, 2, 3, 2, 1]
    # ------------------------------------------------------------------
    test_calistir([2, 2, 3, 2, 1],
                  "4. Derece  |  x^4+2x^3+3x^2+2x+2  |  Beklenen: ±i, -1±i")

    # ------------------------------------------------------------------
    # Test 4: 5. derece — sıfır köklü polinom
    # P(x) = x(x+1)(x-1)(x-2)(x-3) = x^5 - 5x^4 + 5x^3 + 5x^2 - 6x
    # Beklenen kökler: 0, -1, 1, 2, 3
    # katsayilar = [0, -6, 5, 5, -5, 1]
    # ------------------------------------------------------------------
    test_calistir([0, -6, 5, 5, -5, 1],
                  "5. Derece  |  x(x+1)(x-1)(x-2)(x-3)  |  Beklenen: 0,-1,1,2,3")

    # ------------------------------------------------------------------
    # Test 5: 3. derece — bir gerçel, iki karmaşık kök
    # P(x) = x^3 - 2x^2 - 5
    # Beklenen kökler: ~2.6906,  ~-0.3453 ± 1.3187i
    # katsayilar = [-5, 0, -2, 1]
    # ------------------------------------------------------------------
    test_calistir([-5, 0, -2, 1],
                  "3. Derece  |  x^3 - 2x^2 - 5  |  Beklenen: ~2.69, ~-0.35±1.32i")

    # ------------------------------------------------------------------
    # Test 6: 7. derece — tüm gerçel kökler (ders notundaki deflasyon örneği)
    # P(x) = (x-1)(x-3)(x-5)(x-6)(x-7)(x-9)(x-10)
    # Beklenen kökler: 1, 3, 5, 6, 7, 9, 10
    # katsayilar = [-56700, 116460, -84969, 30689, -6130, 690, -41, 1]
    # ------------------------------------------------------------------
    test_calistir([-56700, 116460, -84969, 30689, -6130, 690, -41, 1],
                  "7. Derece  |  (x-1)(x-3)(x-5)(x-6)(x-7)(x-9)(x-10)  |  Beklenen: 1,3,5,6,7,9,10")

    print(f"\n{'=' * 68}")
    print("  Tüm testler tamamlandı.")
    print("=" * 68)
