# Keyfi dereceden bir polinom denkleminin tüm köklerini bulan program.
# Newton-Raphson yöntemi + indirgeme şeması (bölüm 1.9) kullanılmıştır.
# Karmaşık kökler de hesaplanabilmektedir.


def polinom_deger(katsayilar, x):
    # Horner yöntemiyle p(x) hesapla: sayısal olarak kararlı ve verimli
    sonuc = 0
    for k in katsayilar:
        sonuc = k + x * sonuc
    return sonuc


def turev_deger(katsayilar, x):
    # Türev katsayılarını üret, sonra yine Horner ile hesapla
    derece = len(katsayilar) - 1
    turev_katsayilari = []
    for i in range(derece):
        turev_katsayilari.append((derece - i) * katsayilar[i])
    return polinom_deger(turev_katsayilari, x)


def deflasyon(katsayilar, kok):
    # Sentetik bölme: polinomu (x - kok) ile bölerek derecesini bir düşür
    # Böylece aynı kökü tekrar bulmayız
    derece = len(katsayilar) - 1
    yeni_katsayilar = [0] * derece
    kalan = 0
    for i in range(derece):
        yeni_katsayilar[i] = katsayilar[i] + kalan
        kalan = yeni_katsayilar[i] * kok
    return yeni_katsayilar


def kok_bul(katsayilar, baslangic):
    # Newton-Raphson iterasyonu
    # İndirgeme şeması: her adımda lambda ile adım boyutunu küçülterek
    # f(x)'in mutlak değerinin artmasını engelle
    x = baslangic
    tolerans = 1e-10
    maksimum_iterasyon = 500

    for _ in range(maksimum_iterasyon):
        fx = polinom_deger(katsayilar, x)

        if abs(fx) < tolerans:
            break

        dfx = turev_deger(katsayilar, x)

        # Türev sıfıra çok yakınsa çökmeyi önlemek için küçük bir değer ata
        if abs(dfx) < 1e-14:
            dfx = 1e-6

        adim = fx / dfx

        # İndirgeme şeması: lambda = 1'den başla, koşul sağlanana dek yarıya böl
        lam = 1.0
        while abs(polinom_deger(katsayilar, x - lam * adim)) >= abs(fx) and lam > 1e-5:
            lam /= 2.0

        x = x - lam * adim

    return x


# ──────────────────────────────────────────────
#  Kullanıcıdan giriş alma
# ──────────────────────────────────────────────

derece = int(input("Polinomun derecesini girin: "))

katsayilar = []
for i in range(derece, -1, -1):
    if i == 0:
        deger = float(input("Sabit terimin katsayısını girin: "))
    elif i == 1:
        deger = float(input("x teriminin katsayısını girin: "))
    else:
        deger = float(input(f"x^{i} teriminin katsayısını girin: "))
    katsayilar.append(deger)

# Başlangıç noktası: kullanıcı isterse kendi değerini girebilir
tercih = input("\nKendi başlangıç noktasını girmek ister misin? (E/H): ")

if tercih.upper() == "E":
    try:
        gercek_kisim = float(input("Gerçel kısmı gir: "))
        baslangic_x = complex(gercek_kisim, 0.1)
    except ValueError:
        print("Geçersiz giriş, varsayılan değer kullanılıyor.")
        baslangic_x = 1.0 + 0.1j
else:
    # Küçük bir sanal kısım ekleyerek karmaşık köklere de ulaşılabilir
    baslangic_x = 1.0 + 0.1j

# ──────────────────────────────────────────────
#  Tüm kökleri sırayla bul
# ──────────────────────────────────────────────

kokler = []
mevcut_katsayilar = katsayilar[:]

while len(mevcut_katsayilar) > 2:
    bulunan_kok = kok_bul(mevcut_katsayilar, baslangic_x)
    kokler.append(bulunan_kok)
    mevcut_katsayilar = deflasyon(mevcut_katsayilar, bulunan_kok)

# Polinom lineer kaldıysa (ax + b = 0) doğrudan çöz
if len(mevcut_katsayilar) == 2:
    son_kok = -mevcut_katsayilar[1] / mevcut_katsayilar[0]
    kokler.append(son_kok)

# ──────────────────────────────────────────────
#  Sonuçları yazdır
# ──────────────────────────────────────────────

print(f"\n{'Kök No':^10} | {'Kök Değeri':^35}")
print("-" * 50)

for sira, kok in enumerate(kokler):
    gercek = kok.real
    sanal = kok.imag

    # Sanal kısım ihmal edilebilir küçüklükteyse gerçek kök olarak göster
    if abs(sanal) < 1e-8:
        print(f"  {sira + 1:^8}  |  {gercek:.8f}")
    else:
        isaret = "+" if sanal >= 0 else "-"
        print(f"  {sira + 1:^8}  |  {gercek:.6f} {isaret} {abs(sanal):.6f}j")
