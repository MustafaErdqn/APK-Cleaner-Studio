# APK Cleaner Studio 0.6.0-dev.7

Bu geliştirme sürümü, kararlı sürüm öncesi son dayanıklılık ve performans denetimidir. Henüz stabil sürüm olarak etiketlenmemiştir.

## Motor 2.0-dev.3

- Normal APK işlerinde yükleme sırasında üretilen güvenilir analiz raporu yeniden kullanılır; yama başlarken APK ikinci kez taranmaz ve yeniden hash hesaplanmaz.
- Reklam profilleri süreç boyunca bir kez yüklenerek tekrar eden JSON okuması kaldırılmıştır.
- Araç zinciri durumu işlem başına bir kez hesaplanır.
- Kullanıcı tarafından farklı split bileşenleri seçildiğinde doğruluk için yeni birleşen APK yeniden analiz edilmeye devam eder.

## Bellek ve veri yaşam döngüsü

- Büyük APK/APKS/APKM/XAPK yüklemeleri artık RAM'e bütünüyle alınmadan 1 MB bloklarla doğrudan iş klasörüne yazılır.
- 14 günden eski geçici iş klasörleri uygulama başlangıcında güvenli biçimde temizlenir; yakın tarihli çıktılar korunur.
- D1/SQLite etkin değildir. Yerel iş durumu atomik JSON dosyalarıyla tutulmaya devam eder.

## Arayüz akıcılığı

- İlerleme göstergesinin her karesinde tekrar yapılan DOM sorguları kaldırılmıştır.
- Yavaş bağlantıda üst üste binebilen durum sorguları engellenmiş, aktif işin çift başlatılması önlenmiştir.
- Ekranın altında kalan özellik ve footer alanlarında ertelenmiş çizim kullanılmıştır.
- Mevcut animasyonlar korunmuştur; azaltılmamış veya kapatılmamıştır.
