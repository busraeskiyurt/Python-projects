# Newton-Raphson yöntemi ve indirgeme şeması kullanarak
# keyfi dereceden bir polinomun tüm köklerini bulan program.

# Horner yöntemi: polinom değerini ve türevini aynı anda hesaplar
def horner(katsayilar, x):
    derece = len(katsayilar) - 1
    p = katsayilar[0]   # polinom değeri
    dp = 0              # türev değeri
    for i in range(1, derece + 1):
        dp = dp * x + p
        p = p * x + katsayilar[i]
    return p, dp

# Newton-Raphson ile tek bir kök bul
def newton_raphson(katsayilar, baslangic):
    x = baslangic
    for _ in range(200):
        p, dp = horner(katsayilar, x)
        if dp == 0:
            break
        yeni_x = x - p / dp
        if abs(yeni_x - x) < 1e-10:
            return yeni_x
        x = yeni_x
    return x

# Bulunan kökü kullanarak polinomu bir derece indir (sentetik bölme)
def polinom_indir(katsayilar, kok):
    n = len(katsayilar) - 1
    yeni_katsayilar = [katsayilar[0]]
    for i in range(1, n):
        yeni_katsayilar.append(yeni_katsayilar[-1] * kok + katsayilar[i])
    return yeni_katsayilar

# Tüm kökleri bul: her adımda bir kök bul, polinomu indir, tekrarla
def tum_kokleri_bul(katsayilar):
    kokler = []
    mevcut = katsayilar[:]

    # Farklı başlangıç noktaları deneyerek kök aranır
    baslangic_noktalari = [1.0, -1.0, complex(1, 1), complex(-1, -1)]

    while len(mevcut) > 1:
        bulunan = None
        for baslangic in baslangic_noktalari:
            aday = newton_raphson(mevcut, baslangic)
            deger, _ = horner(mevcut, aday)
            if abs(deger) < 1e-6:
                bulunan = aday
                break

        if bulunan is None:
            print("Kök bulunamadi!")
            break

        kokler.append(bulunan)
        mevcut = polinom_indir(mevcut, bulunan)

    return kokler

# Ana program döngüsü
def main():
    while True:
        print("\n--- Polinom Kok Bulma Programi ---")
        derece = int(input("Polinomun derecesini girin: "))

        # Katsayıları yüksek dereceden düşüğe al
        katsayilar = []
        print(f"Katsayilari yuksek dereceden dusuge girin ({derece + 1} adet):")
        for i in range(derece, -1, -1):
            k = float(input(f"  x^{i} katsayisi: "))
            katsayilar.append(k)

        kokler = tum_kokleri_bul(katsayilar)

        print("\nBulunan kokler:")
        for i, kok in enumerate(kokler):
            print(f"  x{i + 1} = {kok}")

        tekrar = input("\nYeni bir denklem cozmek ister misiniz? (e/h): ")
        if tekrar.lower() != 'e':
            print("Program sonlandiriliyor.")
            break

main()
