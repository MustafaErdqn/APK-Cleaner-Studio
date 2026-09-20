# APK Cleaner Studio v0.6.0

Yayın kanalı: **Kararlı**  
Yerel motor: **2.0**  
Yayın tarihi: **12 Ağustos 2026**  
Önceki kararlı sürüm: **v0.5.3**

## Öne çıkan yenilikler

### Motor 2.0 ve daha hızlı paket işleme

- APK dosyaları Smali metnine dönüştürülmeden doğrudan DEX komutları üzerinde düzenlenir.
- Yükleme sırasında hazırlanan güvenilir analiz yeniden kullanılır; aynı APK ikinci kez gereksiz yere taranmaz.
- APKS, APKM ve XAPK paketleri seçimden önce birleştirilmez; yalnızca seçilen ABI, dil ve otomatik DPI bileşenleriyle tek APK üretilir.
- Büyük paketler belleğe bütünüyle alınmadan bloklar hâlinde diske yazılır.
- DEX dosyaları uygun donanımlarda kontrollü olarak paralel işlenir.

### Geliştirilmiş reklam temizliği

- Güvenli, Dengeli ve Kapsamlı temizlik profilleri korunmuştur.
- 18 doğrulanmış reklam ağı için DEX, manifest, XML, asset ve native kitaplık denetimi uygulanır.
- Kapsamlı profil; dinamik `AdView`, native reklam ve banner kapsayıcılarını algılar.
- `ad_container`, `native_ad_container`, `banner_slot`, `mrec_ad` gibi kesin reklam alanları `0dp + gone` ile gizlenir.
- Native reklamı görünüme bağlayan çağrılar ve doğrulanmış reklam yükleme geri çağrıları doğrudan DEX üzerinde etkisizleştirilir.
- Genel uygulama bannerları ve promosyon alanları yanlış pozitifleri önlemek amacıyla korunur.

### Split paket ve kaynak yönetimi

- ARMv7, ARM64, x86 ve x86_64 bileşenleri ayrı ayrı seçilebilir.
- Uygun ekran yoğunluğu paketi seçilen mimariye göre otomatik eklenir.
- Pakette varsa Türkçe ve İngilizce dil bileşenleri ayrı seçilebilir.
- RES kaynak korumasını kaldırma işlemi özgün `public.xml` ad–kimlik haritasını kullanır.
- Normal yama akışlarında `resources.arsc` ve adlandırılmış kaynak başvuruları korunur.
- İsteğe bağlı ZIP hizalama ve DEX hata ayıklama verisi temizliği desteklenir.

### Yerel ağ, geçmiş ve cihaz yönetimi

- Windows ve Termux aynı yerel motoru ve web arayüzünü kullanır.
- Yerel ağ oturumları, bağlantı durumu ve algılanabilen cihaz/tarayıcı bilgileri ana makinede gösterilir.
- Android model kodları çevrimdışı cihaz kataloğuyla pazarlama adına dönüştürülür.
- Brave, Microsoft Edge, Opera, Samsung Internet, Firefox, Google Chrome ve Safari ayrıştırılır.
- Ana makine uzak istemciyi engelleyebilir, engeli kaldırabilir veya oturum listesinden silebilir.
- Engellenen istemci arayüze erişemez ve yöneticiden erişim isteyebilir.
- Son 14 gündeki yerel işler yeniden işlenebilir; rapor, çıktı ve kayıt yönetimi arayüzden yapılabilir.

### HTTPS, gizlilik ve güvenlik

- HTTP ve HTTPS aynı yerel bağlantı noktasında isteğe bağlı olarak birlikte çalışır.
- Güvenilir yerel sertifika varsa HTTP oturumu sessizce HTTPS'e yükseltilebilir.
- Yerel CA ve özel anahtar cihazdan dışarı çıkarılmaz; Termux ve Windows dağıtım paketlerine eklenmez.
- APK dosyaları uzak bir hizmete gönderilmez; analiz ve düzenleme yerel cihazda tamamlanır.
- İstemci yönetimi, geçmiş ve dosya erişimleri cihaz/iş sahibi kapsamıyla sınırlandırılır.
- JSON durum kayıtları eşzamanlı yazma yarışlarına karşı atomik ve kilitli olarak güncellenir.

### Arayüz ve kullanım deneyimi

- Mobil sabit başlık, açık/koyu tema ve duyarlı tek/çok sütunlu düzen geliştirildi.
- Mimari, dil, profil ve isteğe bağlı özellik kartlarının seçim durumu belirginleştirildi.
- İlerleme akışı tek iş çalıştırma güvencesiyle yumuşatıldı; sonuç yazılmadan `%100` gösterilmez.
- Türkçe metinler, masaüstü ve mobil tipografi ölçekleri ile konsol renk hiyerarşisi yenilendi.
- Varsayılan yerel erişim noktası `127.0.0.1:8080` olarak sadeleştirildi.
- Windows uygulaması kapatıldığında sunucu, tarayıcı zamanlayıcısı ve yardımcı süreçler birlikte sonlandırılır.

## Doğrulama özeti

- 76 Python motor, veri, güvenlik, güncelleme ve bütünlük testi başarılıdır.
- 2 web arayüzü sözleşme testi, ESLint ve üretim derlemesi başarılıdır.
- Gerçek APK üzerinde Güvenli, Dengeli, Kapsamlı, yalnız dönüştürme, RES düzenleme, ZIP hizalama ve imzalama akışları doğrulanmıştır.
- Gerçek APKS üzerinde ABI, DPI, dil seçimi ve universal APK üretimi doğrulanmıştır.
- 24 paralel analiz aynı SHA-256 sonucunu üretmiştir.
- Aynı portta 200 HTTP ve 200 HTTPS isteği, 40 eşzamanlı istemciyle hatasız tamamlanmıştır.
- Gerçek yükleme → analiz → yama → durum → indirme → rapor → geçmiş → silme yaşam döngüsü doğrulanmıştır.
- Windows EXE ve Termux ZIP içinde çalışma verisi veya TLS özel anahtarı bulunmadığı doğrulanmıştır.
- Windows uygulaması kapatıldıktan sonra açık alt süreç ve dinlenen bağlantı noktası kalmadığı doğrulanmıştır.

## Bilinen sınırlar

- Her üçüncü taraf APK'nın özel reklam uygulaması farklı olabilir; Kapsamlı profil doğrulanmış kalıpları hedefler.
- Tarayıcı Android modelini gizlerse cihaz adı otomatik alınamaz; görünen ad kullanıcı tarafından değiştirilebilir.
- Yerel HTTPS güveni, sertifikanın istemci cihazda güvenilir olarak kurulmasına ve tarayıcının kullanıcı CA politikasına bağlıdır.
- Yeniden imzalanan APK, kaynak uygulamanın özgün imzasıyla kurulmuş sürümünün üzerine doğrudan kurulamayabilir.

## Dağıtım dosyaları

- `APK-Cleaner-Manager-v0.6.0-Windows.exe`
- `APK-Cleaner-Manager-v0.6.0-Termux.zip`
- `SHA256-v0.6.0.txt`
