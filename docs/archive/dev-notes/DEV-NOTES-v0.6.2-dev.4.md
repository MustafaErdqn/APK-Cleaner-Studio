# APK Cleaner Studio v0.6.2-dev.4

Bu geliştirme paketi kullanıcı onayı alınana kadar kararlı sürümün yerini almaz.

## Değişiklikler

- Uygulama içi Toast, Snackbar ve diyalog çağrıları için kontrollü karşılaştırma akışı eklendi.
- Modlanmış paket, aynı sürümün orijinal APK’sıyla karşılaştırılır; yalnızca orijinalde bulunmayan çağrılar listelenir.
- Mesaj çağrıları varsayılan olarak değiştirilmez; yalnızca kullanıcının açıkça seçtiği sonradan eklenmiş gösterimler devre dışı bırakılır.
- Orijinal uygulamanın kendi izin, hata, güvenlik ve bilgilendirme pencerelerinin korunması hedeflenir.
- Özel Teşekkürler alanı destekçi listesiyle dolduruldu ve daimi destekçiler görsel olarak ayrıştırıldı.
- v0.6.2-dev.3 çizgisindeki Android/Windows/Termux düzeltmeleri korunur.

## Paketler

- Windows: `APK-Cleaner-Studio-v0.6.2-dev.4-Windows.exe`
- Termux: `APK-Cleaner-Studio-v0.6.2-dev.4-Termux.zip`
- Android: `APK-Cleaner-Studio-v0.6.2-dev.4-Android.apk`

## Doğrulama

- 107 Python motor/sunucu/paket testi ve 2 arayüz render testi başarılıdır.
- Windows paketinde HTTP, HTTPS, hazır araç zinciri ve güvenli kapanış denetlenmiştir.
- Android paketinde yalnızca ARM64/ARMv7 mimarileri, v2/v3 imza ve 16 KB/ZIP hizalaması doğrulanmıştır.
