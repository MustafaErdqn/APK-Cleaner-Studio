# APK Cleaner Studio 0.6.0-dev.16

Bu sürüm, doğrulanmış dış bağlantı kullanılabiliyorsa uygulamayı doğrudan HTTPS üzerinden açar; dış bağlantı kullanılamadığında yerel HTTP erişimini korur.

## Otomatik HTTPS

- Başlangıçta kişisel Keenetic alan adının aynı çalışan uygulama örneğine ulaştığı tek kullanımlık süreç kimliğiyle doğrulanır.
- Doğrulama başarılıysa Windows başlangıç tarayıcısı doğrudan HTTPS adresini açar.
- Yerel ağdaki cihazlar `http://...:8080/` adresini açtığında doğrulanmış HTTPS adresine otomatik yönlendirilir.
- Doğrulama başarısızsa, çevrimdışıysa veya ters vekil kapalıysa uygulama yerel HTTP adresiyle çalışmaya devam eder.
- API çağrıları, indirmeler ve ana bilgisayardaki `127.0.0.1` oturumu zorla yönlendirilmez.
- Başka bir bilgisayarda çalışan uygulama kopyası senin alan adına yönlenmez; süreç kimliği eşleşmesi zorunludur.

## Masaüstü yerleşimi

- Boş başlangıç ekranında sol çalışma kartı, sağdaki oturum ve geçmiş panellerinin yüksekliğine uyum sağlar.
- Yükleme alanı kullanılabilir dikey alanı dengeli biçimde doldurur; sayfanın altında oluşan geniş boşluk kaldırılmıştır.
- Bu düzen yalnızca geniş ekranlarda uygulanır; mobildeki tek sütunlu kart sırası korunur.

## Doğrulama

- Python motor, sunucu ve güvenlik paketi: **53/53 test başarılı**.
- Web arayüzü ve üretilen HTML paketi: **2/2 test başarılı**.
