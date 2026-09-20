# APK Cleaner Studio 0.6.0-dev.15

Bu sürüm, uzun süren dış ağ işlemlerinin ters vekil zaman aşımı nedeniyle yeniden başlatılmasını engeller ve yerel HTTP istemcilerine öğrenilmiş güvenli HTTPS adresini önerir.

## Uzak işlem güvenilirliği

- `/api/clean` isteği artık motor tamamlanana kadar açık tutulmaz; iş hemen kabul edilip arka planda yalnızca bir kez çalıştırılır.
- Aynı iş kimliğiyle gelen Keenetic veya başka bir ters vekil tekrarı çalışan motoru yeniden başlatmaz.
- Tamamlanmış işe gelen tekrar isteği mevcut sonucu döndürür.
- Arayüz sonucu kısa ve çakışmayan durum sorgularıyla izler; geçici ağ kesintilerinde artan bekleme aralığıyla devam eder.
- Motor sonucu gerçekten yazılmadan ilerleme durumu `%100` yapılmaz; çalışma aşamaları en fazla `%99` gösterilir.

## Güvenli bağlantı

- Uygulama, güvenilir ters vekil üzerinden kullanılan HTTPS adresini yerel olarak hatırlar.
- Yerel IP üzerinden düz HTTP ile bağlanan uzak cihazlara, model bilgisinin alınabilmesi için **HTTPS ile aç** önerisi gösterilir.
- Yönlendirme zorunlu değildir; yerel ve çevrimdışı kullanım korunur.

## Doğrulama

- Python motor, sunucu ve güvenlik paketi: **51/51 test başarılı**.
- Web arayüzü ve üretilen HTML paketi: **2/2 test başarılı**.
- Windows EXE üzerinde iş başlatma isteğinin **HTTP 202** ile yaklaşık **31 ms** içinde serbest bırakıldığı, arka plan durumunun bağımsız yazıldığı ve güvenilir HTTPS adresinin öğrenildiği doğrulandı.
