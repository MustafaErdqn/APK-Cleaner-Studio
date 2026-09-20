# APK Cleaner Studio 0.6.0-dev.27

## Kararlılık düzeltmeleri

- Atomik JSON durum yazımları, Windows’ta eşzamanlı `replace` çağrılarının oluşturduğu yarış koşuluna karşı kısa bir yazma kilidi ve benzersiz geçici dosyalarla güçlendirildi.
- Yerel HTTP sunucusunun bağlantı kabul kuyruğu 5’ten 128’e çıkarıldı; çoklu cihaz ve paralel tarayıcı isteklerindeki anlık bağlantı reddi giderildi.
- Uygulama, web arayüzü, npm kilit dosyası, Windows paketi, Termux paketi ve sürüm metni `0.6.0-dev.27` üzerinde eşitlendi.
- Termux paketleyicisi; yerel TLS özel anahtarlarını, sertifika çalışma klasörünü, iş geçmişini, istemci ad/engel kayıtlarını ve geçici dosyaları dağıtımdan kesin olarak dışlar.
- Windows kapanış yöneticisi; pencere kapatma yanında `Ctrl+C` ve `Ctrl+Break` olaylarını da aynı sunucu/Java/alt süreç temizliğinden geçirir.
- Sürüm sabitleyen arayüz testi, paket sürümünü doğrudan `package.json` üzerinden doğrulayacak şekilde güncellendi.

## Yayın kapıları

- 71 Python motor, veri, güvenlik, araç hazırlama, güncelleme ve bütünlük testi başarılı.
- 2 JavaScript arayüz/paket testi, ESLint ve üretim web derlemesi başarılı.
- Direct DEX ve binary XML yardımcıları Java kaynaklarından sıfırdan derlendi.
- Gerçek APK üzerinde Güvenli, Dengeli, Kapsamlı, yalnız dönüştürme, ZIP hizalama, imzalama ve RES kaynak açma akışları başarılı.
- Gerçek APKS üzerinde ABI/DPI/dil envanteri ve universal APK birleştirme başarılı.
- 24 paralel APK analizi aynı SHA-256 sonucunu üretti.
- Aynı portta 200 HTTP + 200 HTTPS isteği, 40 eşzamanlı istemciyle sıfır hatayla tamamlandı.
- Gerçek HTTP yükle → analiz → arka plan işlemi → durum → indir → rapor → geçmiş → sil akışı başarılı.
- Windows EXE ve Termux ZIP dağıtım paketleri içeriden denetlendi; çalışma verisi veya özel anahtar sızıntısı bulunmadı.
- Tek dosyalı EXE kapanışından sonra PyInstaller alt süreci ve dinlenen bağlantı noktası kalmadığı doğrulandı.

Bu paket stabil sürüm adayıdır. Stabil sürüm numarası, kullanıcı kabul testi tamamlanmadan verilmemiştir.
