# APK Cleaner Studio 0.6.0-dev.11

Bu sürüm cihaz modelini otomatik tanıma zincirini güçlendiren test sürümüdür.

## Yenilikler

- Güvenli HTTPS açılışlarında Android model bilgisinin ilk sayfa yüklemesinde istenmesi için `Critical-CH` desteği eklendi.
- `Sec-CH-UA-Model`, platform, mobil/form faktörü ve platform sürümü Client Hint istekleri genişletildi.
- Yeni Chromium yüksek entropili istemci bilgisi izin politikası eklendi.
- Android User-Agent model çözümlemesi Samsung, Google Pixel, Oppo/Realme ve benzeri yaygın model kalıpları için güçlendirildi.
- Tarayıcının model kodunu paylaşması hâlinde kod mevcut Google Play cihaz kataloğından otomatik pazarlama adına dönüştürülür.

## Teknik sınır

- Web tarayıcıları kullanıcının telefona verdiği özel cihaz adını standart bir API ile paylaşmaz. Bu sürüm otomatik olarak model/pazarlama adını bulmayı hedefler; tarayıcı gizlilik politikası modeli de saklarsa kullanıcı **Adını değiştir** seçeneğini kullanabilir.

## Doğrulama

- Python birim, güvenlik ve bütünlük testleri: 47/47 başarılı.
- Arayüz yapı testleri: 2/2 başarılı.
- Windows EXE yerel açılış testi ve Client Hint yanıt başlıkları doğrulandı.
