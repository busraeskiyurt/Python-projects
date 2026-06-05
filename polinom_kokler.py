# Newton-Raphson yöntemi ve deflasyon (indirgeme) şeması kullanılarak
# keyfi dereceden bir polinom denkleminin tüm kökleri hesaplanır.


def polinom_hesapla(katsayilar, x):
    # Horner yöntemi: f(x) değerini en verimli şekilde hesaplar
    sonuc = 0
    for k in katsayilar:
        sonuc = k + x * sonuc
    return sonuc


def turev_hesapla(katsayilar, x):
    # Türev katsayılarını çıkar, sonra f() ile değerini bul
    derece = len(katsayilar) - 1
    turev_kats = []
    for i in range(derece):
        turev_kats.append((derece - i) * katsayilar[i])
    return polinom_hesapla(turev_kats, x)


def deflasyon_uygula(katsayilar, bulunan_kok):
    # Bulunan kökü sentetik bölme ile polinomdan çıkar, derece bir azalır
    derece = len(katsayilar) - 1
    yeni_kats = [0] * derece
    kalan = 0
    for i in range(derece):
        yeni_kats[i] = katsayilar[i] + kalan
        kalan = yeni_kats[i] * bulunan_kok
    return yeni_kats


def kok_bul(katsayilar, baslangic):
    x = baslangic
    for _ in range(500):
        fx  = polinom_hesapla(katsayilar, x)
        dfx = turev_hesapla(katsayilar, x)

        if abs(dfx) < 1e-12:
            # Türev sıfıra çok yakınsa döngüden çık
            break

        adim = fx / dfx

        # Adım büyüklüğünü (lambda) yarıya indirerek f(x)'in azaldığından emin ol
        lam = 1.0
        while abs(polinom_hesapla(katsayilar, x - lam * adim)) >= abs(fx) and lam > 1e-4:
            lam /= 2.0

        x_yeni = x - lam * adim

        if abs(x_yeni - x) < 1e-10:
            break

        x = x_yeni

    return x


# -------- Kullanıcıdan giriş --------

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

# Karmaşık kökleri de yakalayabilmek için varsayılan başlangıç sanal kısım içeriyor
baslangic_x = complex(1.0, 0.5)

# -------- Kökleri bul --------

tum_kokler = []
mevcut_kats = katsayilar[:]

# Her adımda bir kök bulunur, deflasyon ile polinom küçültülür
while len(mevcut_kats) > 2:
    kok = kok_bul(mevcut_kats, baslangic_x)
    tum_kokler.append(kok)
    mevcut_kats = deflasyon_uygula(mevcut_kats, kok)

# Polinom doğrusal (ax + b = 0) hale gelince kök direkt hesaplanır
if len(mevcut_kats) == 2:
    son_kok = -mevcut_kats[1] / mevcut_kats[0]
    tum_kokler.append(son_kok)

# -------- Sonuçları yazdır --------

print(f"\n{'Kök No':^10} | {'Kök Değeri':^40}")
print("-" * 55)
for i, kok in enumerate(tum_kokler):
    gercek = kok.real
    sanal  = kok.imag
    if abs(sanal) < 1e-6:
        # Gerçel kök: sanal kısım gösterme
        print(f"{i + 1:^10} | {gercek:.6f}")
    else:
        print(f"{i + 1:^10} | {gercek:.6f} + {sanal:.6f}i")
