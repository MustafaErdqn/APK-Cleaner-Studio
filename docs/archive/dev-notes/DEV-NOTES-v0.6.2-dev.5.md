# APK Cleaner Studio v0.6.2-dev.5

Bu test sürümü Android uyumluluğu ve mobil iş akışı iyileştirmelerine odaklanır.

## Yenilikler

- Android uygulamasında cihazdaki yüklü uygulamalar doğrudan seçilip yerel motora aktarılabilir.
- Yüklü uygulama seçicisi beklemeden açılır; paket taraması arka planda ve arayüzü kilitlemeden tamamlanır.
- Uygulama listesinde harf yer tutucuları yerine cihazdaki gerçek uygulama ikonları gösterilir.
- Uygulama seçicisi açıldığında arama alanı otomatik odaklanmaz; klavye yalnızca kullanıcı arama kutusuna dokunduğunda açılır.
- Split kurulumlu uygulamaların base ve split paketleri otomatik olarak birlikte hazırlanır.
- Sonradan eklenen mesaj karşılaştırması Toast, Snackbar, AlertDialog, Material Dialog, DialogFragment ve BottomSheet gösterimlerini kapsar.
- Özellikle `onCreate` içindeki doğrulanmış, sonradan eklenmiş mesaj çağrıları listenin başında gösterilir.

## Düzeltmeler

- Bazı Android üreticilerinde görülen PKCS#12 `NoSuchAlgorithmException` imzalama hatası giderildi.
- Çıktı anahtarının `CN=APK Cleaner Studio` kimliği ile APK Signature Scheme v2/v3 desteği korunur.
- Uygulamanın özgün mesajları korunur; temizleme yalnızca aynı sürümün orijinal APK’sına göre eklenen ve kullanıcının seçtiği çağrılara uygulanır.

## Paketler

- Windows: `APK-Cleaner-Studio-v0.6.2-dev.5-Windows.exe`
- Termux: `APK-Cleaner-Studio-v0.6.2-dev.5-Termux.zip`
- Android: `APK-Cleaner-Studio-v0.6.2-dev.5-Android.apk`
