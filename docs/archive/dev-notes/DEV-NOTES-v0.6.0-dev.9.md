# APK Cleaner Studio 0.6.0-dev.9

Bu sürüm kararlı sürüm adayı öncesindeki test sürümüdür.

## Yenilikler

- Android model kodları, Google Play'in resmî desteklenen cihaz kataloğundaki pazarlama adına dönüştürülür. Örneğin `SM-S928B`, arayüzde `Samsung Galaxy S24 Ultra` olarak görünür.
- Uygulamaya 42 binden fazla Android modelini içeren çevrimdışı cihaz kataloğu eklendi. Tanınmayan yeni modeller için katalog arka planda yenilenir ve yerel olarak önbelleğe alınır.
- Yerel Windows bilgisayarında tanımlı bilgisayar adı; ağdaki bilgisayarlarda çözümlenebildiği ölçüde LAN ana makine adı gösterilir.
- Cihaz bağlantı durumu 10 saniyede bir yenilenir. Son sinyali kesilen cihazlar oturum listesinde `Bağlantı kesildi` durumuna geçer.
- Kullanıcı isterse otomatik bulunan adı yerel bir görünen adla değiştirebilir.
- `Eski İşlemler` kartı eklendi. Son 14 gündeki paketler yeniden işlenebilir; mevcutsa rapor ve çıktı tekrar açılabilir.
- Ağdan bağlanan kullanıcılar yalnızca kendi tarayıcı kimlikleriyle oluşturdukları işlem geçmişini görür; ana bilgisayar bütün yerel işleri görebilir.
- Windows kapatma zinciri güçlendirildi. Pencerenin kapatma düğmesi tarayıcı zamanlayıcısını, yerel sunucuyu ve uygulamaya ait araç süreçlerini kapattıktan sonra EXE sürecinin Görev Yöneticisi'nde kalmamasını kesinleştirir.
- Android model tespiti güçlendirildi: Client Hints başlıkları istenir, tam User-Agent içindeki model kodu yedek olarak okunur ve Android cihazlarda LAN ana makine adı çözümlemesi de denenir.
- Bağlı cihaz listesi gizlilik kapsamına alındı: ana bilgisayar bütün oturumu, ağdan bağlanan kullanıcı yalnızca kendi cihazını görür.
- Tarayıcı Android modelini paylaşmadığında kullanıcıdan kendi telefonunda yalnızca bir kez görünen ad istenir; kaydedilen ad sonraki bağlantılarda otomatik kullanılır.
- Bağlantısı kesilen cihazlar 5 dakika boyunca gri durumda görünür, ardından oturum listesinden otomatik kaldırılır.
- Bağlantı durum noktasının panel kenarında kesilmesine neden olan cihaz satırı yerleşimi düzeltildi.
- Keenetic ters proxy/alt alan adı erişiminde güvenilir yerel proxy başlıkları okunur; dış ağ istemcisinin public IP adresi router IP’si yerine oturum kartında gösterilir.
- Proxy üzerinden gelen public adreslerde router ana makine adı cihaz adı olarak kullanılmaz; tarayıcı model paylaşmıyorsa tek seferlik görünen ad akışı devreye girer.
- KeenDNS bulut geçidi gerçek-IP başlığı iletmediğinde, yalnızca `.keenetic.link` üzerinden açılan istemci public IP’sini IPify JSONP uç noktasıyla doğrulayıp yerel oturumuna bildirir.
- Cihaz paneli masaüstünde genişletildi; liste yüksekliği artırıldı, kaydırma çubuğuna ayrı pay bırakıldı ve durum LED’i/metinleri yeniden kenara yaklaştırıldı.
- Kullanıcıya gösterilen oturum açıklaması altyapı sağlayıcı adlarından arındırılarak genel bir ifadeyle sadeleştirildi.
- Dış ağ adresi gösterimi yalnızca genel IPv4 adresini kabul edecek şekilde sınırlandı; IPv6 adresleri oturum kartına yazılmaz.
- Uzun cihaz adları ekran genişliğine göre en fazla iki satıra yayılır; bağlantı durumu ve zaman sütunu sabit kalır.
- Bağlanan istemcilerde Brave, Microsoft Edge, Opera, Samsung Internet, Firefox, Google Chrome ve Safari ayrı tarayıcı adlarıyla gösterilir; doğrulanan tarayıcı adı durum yenilemelerinde korunur.

## Gizlilik

- Cihaz kataloğu sorgusu model kodu üzerinden yerel yapılır; APK hiçbir uzak sunucuya gönderilmez.
- Oturum cihaz listesi bellektedir ve uygulama kapanınca silinir.
- Kullanıcının verdiği görünen ad, katalog güncellemesi ve son işler yalnızca APK Cleaner Studio'nun yerel veri klasöründe tutulur.

## Doğrulama

- Python birim ve bütünlük testleri: 44/44 başarılı.
- Arayüz yapı testleri: 2/2 başarılı.
