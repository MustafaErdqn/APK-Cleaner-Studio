# APK Cleaner Studio 0.6.0-dev.18

Bu sürüm, masaüstündeki boş başlangıç alanını doğal ve işlevsel bir çalışma rehberiyle düzenler; dış alan adındaki HTTP erişimini bildirim göstermeden HTTPS’e yükseltir.

## Masaüstü başlangıç düzeni

- Dev.16’daki boydan boya esnetilmiş yükleme alanı kaldırıldı ve kart doğal yüksekliğine döndürüldü.
- Sol sütunun altına yalnızca boş başlangıç ekranında görünen dört adımlı çalışma rehberi eklendi.
- Paket seçildiğinde rehber gizlenir; analiz ve işlem ekranlarında gereksiz yer kaplamaz.
- Mobilde mevcut tek sütunlu düzen korunduğu için rehber gösterilmez.

## HTTPS davranışı

- HTTPS öneri bildirimi arayüzden tamamen kaldırıldı.
- Yalnızca güvenilir dış alan adına düz HTTP üzerinden gelen istekler `308 Permanent Redirect` ile aynı yolun HTTPS karşılığına yönlendirilir.
- `127.0.0.1` ve yerel ağ IP adresleri HTTP olarak çalışmaya devam eder; uygulama başlangıçta yine `http://127.0.0.1:8080/` adresini açar.

## 502 teşhisi

- Uygulama güncel olarak `10.10.30.36:8080` adresinde çalışıyor ve bu adresten HTTP 200 yanıtı veriyor.
- Keenetic alan adındaki 502, ters vekilin büyük olasılıkla önceki `10.10.30.33` adresini hedeflemesinden kaynaklanıyor.
- Keenetic hedefi `10.10.30.36:8080` olarak güncellenmeli ve bilgisayara sabit DHCP kiralaması verilmelidir.
