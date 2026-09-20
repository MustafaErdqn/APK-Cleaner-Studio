# APK Cleaner Studio 0.6.0-dev.19

Bu sürüm, iç ağ cihazlarını yerel olarak doğrulanmış HTTPS adresine otomatik taşır ve boş masaüstü başlangıç alanını ikinci bir işlevsel bilgi bölümüyle tamamlar.

## İç ağda HTTPS

- Ana bilgisayardaki `127.0.0.1` oturumu HTTP olarak yerel kalır.
- Aynı ağdaki başka bir cihaz, bilgisayarın LAN IP adresini HTTP ile açarsa yalnızca bu bilgisayarda daha önce öğrenilip saklanan HTTPS adresine yönlendirilir.
- Dağıtılan başka bir uygulama kopyasında kayıtlı HTTPS adresi yoksa özel bağlantıya yönlendirme yapılmaz.
- Dış alan adındaki HTTP→HTTPS yükseltmesi korunmuştur.
- Güvenli bağlantı bildirimi gösterilmez; geçiş doğrudan `308 Permanent Redirect` ile yapılır.

## Başlangıç alanı

- Dört adımlı çalışma rehberinin altına “Kontrollü düzenleme, izlenebilir sonuç” bölümü eklendi.
- Kaynağın korunması, rapor üretimi ve geçmişten yeniden işleme özellikleri dengeli üç sütunda anlatılır.
- Her iki başlangıç bölümü paket seçildiğinde birlikte gizlenir ve mobil görünümde yer kaplamaz.

## Keenetic notu

- Bilgisayarın güncel LAN adresi `10.10.30.36` olduğundan Keenetic ters vekil hedefi `http://10.10.30.36:8080` olmalıdır.
- Genel HTTPS Keenetic üzerinde sonlandırılmalı; uygulamaya giden iç arka uç bağlantısı HTTP kalmalıdır.
