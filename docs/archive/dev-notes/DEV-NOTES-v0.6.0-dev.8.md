# APK Cleaner Studio 0.6.0-dev.8

Bu test sürümü, split paketlerin ilk yükleme ekranını hızlandırır ve yerel ağ oturum görünürlüğü ekler. Stabil sürüm olarak etiketlenmemiştir.

## Motor 2.0-dev.4

- APKS, APKM ve XAPK paketleri seçim ekranından önce universal APK'ya dönüştürülmez.
- Ön analiz, base ve feature APK modüllerini doğrudan tarar; kullanıcı seçiminden sonra yalnızca bir kez birleştirme yapılır.
- Dosyanın SHA-256 değeri yükleme akışı sırasında hesaplanır; analiz için ikinci tam dosya okuması kaldırılmıştır.
- Mimari, DPI ve dil seçimi yapıldıktan sonra oluşan gerçek APK doğruluk için yeniden analiz edilir.

## Yerel dosyalar

- Windows EXE: `%LOCALAPPDATA%\\APKCleanerManager\\jobs\\<iş-kimliği>`
- Kaynak/Termux çalıştırması: `manager/jobs/<iş-kimliği>`
- Kaynak paket, analiz kaydı ve çıktı aynı iş klasöründe tutulur.
- Dosyalar işlem biter bitmez silinmez; uygulama başlatıldığında 14 günden eski geçici işler temizlenir.

## Yerel ağ oturumları

- Arayüz, aynı oturumda görülen IP adresini, yaklaşık cihaz/tarayıcı türünü ve ilk/son bağlantı saatini gösterir.
- Bu liste yalnızca bellekte tutulur, diske yazılmaz ve uygulama kapanınca silinir.
- MAC adresi, gerçek cihaz adı veya kullanıcı kimliği toplanmaz.
