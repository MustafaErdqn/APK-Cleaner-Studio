# APK Cleaner Studio v0.6.2 — Kararlı Sürüm Notları

**Motor 2.0 · 19 Eylül 2026 · Android, Windows ve Termux**

v0.6.2; reklam temizliğini zorunlu olmaktan çıkaran, başlangıç diyalogu ve Toast analizini daha akıllı hâle getiren, split paket iş akışını güçlendiren ve üç platformdaki arayüzü kararlı sürüme hazırlayan kapsamlı bir güncellemedir.

Önceki kararlı sürüm: **v0.6.1**

## Öne çıkan yenilikler

- **Reklam izlerini temizle** işlemi tek APK’larda bağımsız olarak kapatılabilir; reklam kapsamı kartları bu seçimle birlikte gerçekten etkinleşir veya devre dışı kalır.
- Split paketlerde **Tek APK oluştur** ve reklam temizleme işlemleri arasında güvenli seçim yapılır; boş veya çelişkili işlem durumu oluşmaz.
- Başlangıç mesajı analizi Activity, Fragment, Application, pencere odağı ve ek yaşam döngüsü yollarını bağlama göre puanlar; yüksek olasılıklı sonradan eklenmiş diyalog ve Toast adaylarını öne çıkarır.
- Yalnızca kullanıcının seçtiği başlangıç çağrısı aynı komut uzunluğu korunarak etkisizleştirilir; ortak `show()` yöntemleri veya Activity gövdeleri topluca silinmez.
- Yüklü uygulamalar doğrudan seçilip işlenebilir; uygulama adı ve sürüm numarası kaynak paket adına birlikte eklenir.

## Düzeltmeler ve iyileştirmeler

- Manifestte kalan Play split metadata’sının tek başına kesin hata sayılması önlendi; gerçek kurulum riski açıklayıcı uyarı olarak gösterilir.
- DEX düzenlemesinde gereksiz uzun NOP dizileri kaldırıldı; hedef çağrılar sabit uzunluklu güvenli ileri geçişle etkisizleştirilir.
- Çok sayıdaki reklam ağı ve işlem geçmişi sonuçları sabit ölçülü, ortak görünümlü ve geçişli kaydırma alanlarında sunulur.
- Masaüstünde işlem seçimi, çalışma ve sonuç ekranlarında ana panel, sağ durum kartları, çalışma alanı kartı ve yetenek şeridi tutarlı biçimde korunur.
- Açık/koyu tema yüzeyleri, üst bar kontrolleri, ilerleme animasyonu, modal geçişleri ve farklı ekran genişlikleri yeniden dengelendi.
- Android uygulama ikonlarının yüklenmesi ve uzun yüklü-uygulama listelerindeki kaydırma davranışı iyileştirildi.
- Windows’ta HTTP–HTTPS güven yoklamasının aynı bilgisayarı iki yerel ağ oturumu gibi göstermesi giderildi; loopback bağlantıları tek cihaz kimliğinde birleştirildi.
- Paketleme, yerel HTTPS, işlem iptali, araç zinciri, Android yaşam döngüsü ve çıktı imzalama kontrolleri güçlendirildi.

## Platform paketleri

- `APK-Cleaner-Studio-v0.6.2-Android.apk`
- `APK-Cleaner-Studio-v0.6.2-Windows.exe`
- `APK-Cleaner-Studio-v0.6.2-Termux.zip`

Android kararlı paketi `com.apkrepo.apkcleanerstudio` kimliği ve `62` sürüm koduyla v0.6.1’in üzerine güncellenebilir. Üç platform aynı Motor 2.0 çalışma mantığını ve ortak arayüz kaynaklarını kullanır.
