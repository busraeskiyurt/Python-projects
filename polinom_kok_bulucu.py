# Newton-Raphson yöntemi ve deflasyon (indirgeme) şeması kullanılarak
# keyfi dereceden bir polinom denkleminin tüm kökleri hesaplanır.


def polinom_deger(katsayilar, x):
    # Horner yöntemi ile f(x) hesaplanır (en verimli polinom değerlendirme yolu)
    sonuc = 0
    for k in katsayilar:
        sonuc = k + x * sonuc
    return sonuc


def turev_deger(katsayilar, x):
    # f'(x) için önce türev katsayıları çıkarılır, sonra f() ile değer hesaplanır
    n = len(katsayilar) - 1
    turev_kats = []
    for i in range(n):
        turev_kats.append((n - i) * katsayilar[i])
    return polinom_deger(turev_kats, x)


def deflasyon_uygula(katsayilar, kok):
    # Bulunan kök sentetik bölme ile polinomdan ayrılır, derece bir düşer
    n = len(katsayilar) - 1
    yeni_kats = [0] * n
    kalan = 0
    for i in range(n):
        yeni_kats[i] = katsayilar[i] + kalan
        kalan = yeni_kats[i] * kok
    return yeni_kats


def kok_bul(katsayilar, baslangic):
    x = baslangic
    for _ in range(500):
        fx = polinom_deger(katsayilar, x)
        dfx = turev_deger(katsayilar, x)

        if abs(dfx) < 1e-12:
            break

        adim = fx / dfx

        # İndirgeme şeması: lambda (adim büyüklüğü) yarıya indirilerek
        # her adımda f(x) mutlaka küçülmesi sağlanır
        lam = 1.0
        while abs(polinom_deger(katsayilar, x - lam * adim)) >= abs(fx) and lam > 1e-4:
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
        deger = float(input("Sabit terimin katsayısı: "))
    elif i == 1:
        deger = float(input("x teriminin katsayısı: "))
    else:
        deger = float(input(f"x^{i} teriminin katsayısı: "))
    katsayilar.append(deger)

tahmin_gir = input("\nBaşlangıç tahmini girmek ister misiniz? (E/H): ")
if tahmin_gir.upper() == "E":
    gercek_kisim = float(input("Gerçel kısım: "))
    baslangic_x = complex(gercek_kisim, 0.5)
else:
    # Varsayılan başlangıç: karmaşık kökleri de yakalayabilmek için sanal kısım eklendi
    baslangic_x = 1.0 + 0.5j

# -------- Kökleri bul --------

tum_kokler = []
mevcut_kats = katsayilar[:]

while len(mevcut_kats) > 2:
    kok = kok_bul(mevcut_kats, baslangic_x)
    tum_kokler.append(kok)
    mevcut_kats = deflasyon_uygula(mevcut_kats, kok)

# Polinom doğrusal hale gelince kök doğrudan hesaplanır: ax + b = 0 → x = -b/a
if len(mevcut_kats) == 2:
    son_kok = -mevcut_kats[1] / mevcut_kats[0]
    tum_kokler.append(son_kok)

# -------- Sonuçları yazdır --------

print(f"\n{'Kök No':^10} | {'Kök Değeri':^30}")
print("-" * 45)
for i, kok in enumerate(tum_kokler):
    print(f"{i + 1:^10} | {kok:.6f}")
