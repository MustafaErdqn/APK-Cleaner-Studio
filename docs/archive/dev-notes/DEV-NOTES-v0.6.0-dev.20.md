# APK Cleaner Studio 0.6.0-dev.20

Bu sürüm, bu bilgisayarda doğrulanıp yerel olarak kaydedilmiş HTTPS adresi bulunduğunda localhost dâhil tüm HTTP girişlerini güvenli bağlantıya taşır.

## HTTPS önceliği

- Uygulama başlangıç tarayıcısı, yerel ayarlarda kayıtlı HTTPS adresi varsa doğrudan bu adresi açar.
- `127.0.0.1`, LAN IP adresi ve dış alan adındaki HTTP istekleri aynı yol korunarak HTTPS’e yönlendirilir.
- Yönlendirme bildirimsiz ve doğrudan `308 Permanent Redirect` ile yapılır.
- Özel HTTPS adresi uygulama paketinin başlangıç hedefi olarak gömülmez; çalışma bilgisayarının yerel veri klasöründen okunur.
- Başka bir kullanıcının bilgisayarında kayıtlı HTTPS yapılandırması yoksa senin özel adresine yönlendirme yapılmaz ve yerel HTTP geri dönüşü korunur.

## Arayüz

- Dev.19’daki dört adımlı çalışma rehberi ve ikinci izlenebilir sonuç bölümü korunmuştur.
