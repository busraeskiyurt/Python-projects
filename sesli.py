sesli_harfler = "aeıioöuü"
sessiz_harfler = "bcçdfgğhjklmnprsştvyz"
sesliler = ""
sessizler = ""
kelime = input("enter text")
for i in kelime:
    if i in sesli_harfler:
        sesliler += i
    else:
        sessizler += i
print("vowels: ", sesliler)
print("consonants: ", sessizler)
