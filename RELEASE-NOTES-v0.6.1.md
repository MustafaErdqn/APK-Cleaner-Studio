# APK Cleaner Studio v0.6.1 — Kararlı Sürüm Notları

**Motor 2.0 · 15 Ağustos 2026 · Windows, Termux ve Android**

v0.6.1, APK Cleaner Studio’yu ilk kez bağımsız bir Android uygulaması olarak sunarken Windows ve Termux paketlerinde de kullanılabilirlik, bağlantı yönetimi ve arayüz kararlılığına odaklanan bir bakım güncellemesidir. Üç platform aynı Motor 2.0 işleme altyapısını ve ortak arayüz dilini kullanır.

Önceki kararlı sürüm: **v0.6.0**

## ✨ Yeni özellikler

### Android için bağımsız APK

APK Cleaner Studio artık Android’de Termux, komut satırı, haricî Java kurulumu veya ayrı bir tarayıcı gerektirmeden çalışır. Yerel işleme motoru, web arayüzü ve gerekli çalışma bileşenleri uygulama paketine gömülüdür.

- Paket adı: `com.apkrepo.apkcleanerstudio`
- Sürüm adı: `0.6.1`
- Android sürüm kodu: `61`
- Desteklenen mimariler: `arm64-v8a` ve `armeabi-v7a`
- Dil kaynakları: varsayılan dil ve Türkçe
- Görsel kaynaklar: ARM hedefleri için xhdpi ve xxhdpi

### Üç platformda ortak deneyim

Windows, Termux ve Android sürümleri aynı paket analizini, doğrudan DEX düzenleme akışını, split APK birleştirmeyi, manifest/XML denetimini ve raporlama sistemini kullanır. Ortak web arayüzündeki düzeltmeler platform paketlerine birlikte aktarılır; böylece arayüz ve motor davranışının sürümler arasında ayrışması önlenir.

### İşlemi güvenli biçimde iptal etme

Çalışan bir temizleme veya dönüştürme işi, sonuç beklenmeden arayüzdeki **İptal et** seçeneğiyle durdurulabilir. İptal isteği motorun güvenli kontrol noktalarında ele alınır; yarım çıktı kullanıcıya tamamlanmış paket olarak sunulmaz.

### Platforma duyarlı yerel HTTPS

Windows ve Termux sunucularında yerel CA sertifikası isteğe bağlı olarak kullanılabilir. Doğrulanmış HTTPS bağlantısında sertifika yönlendirmesi gizlenir; sertifika tanınmıyorsa HTTP erişimi korunur. Bağımsız Android uygulamasında haricî yerel sunucu bulunmadığı için ana sertifika yönlendirmesi gösterilmez.

### Android’e özgü uygulama deneyimi

Uygulama logosuyla uyumlu yerel açılış ekranı, Android durum çubuğuyla bütünleşen kenardan kenara yerleşim ve açık/koyu/sistem teması eklendi. Bağımsız uygulamada gereksiz olan **Yerel Ağ Oturumları** paneli gizlendi; motor ve işlem geçmişi kartları cihaz içi kullanıma göre korundu.

## 🛠 Hata düzeltmeleri ve iyileştirmeler

### Android

- Android çalışma önbelleği temizlendiğinde oluşabilen `No usable temporary directory found` hatası giderildi; uygulamaya ait geçici klasör artık başlangıçta ve her işlem öncesinde otomatik olarak yeniden hazırlanıyor.
- Android 16’da açılış sırasında oluşabilen `WindowInsetsController` kaynaklı çökme giderildi.
- Durum çubuğu yüksekliğinin fiziksel piksel yerine CSS pikseli gibi uygulanması nedeniyle oluşan fazla üst boşluk düzeltildi.
- Uygulama başlığına dokunulduğunda temanın açık moda dönmesi önlendi; sistem teması köprüsü düzeltildi.
- İşlenmiş APK’nın `download.bin` adıyla kaydedilmesi giderildi; motorun ürettiği gerçek APK dosya adı korunuyor.
- Açılış ekranı ve üst bar görsel bütünlüğü geliştirildi.
- Yerel ağ ve sertifika bileşenleri bağımsız Android çalışma biçimine göre sadeleştirildi.
- Kullanılmayan kaynaklar ve hata ayıklama kalıntıları release paketinden ayıklandı.

### Windows ve Termux

- Başlangıç bağlantısının sertifika durumuna uygun HTTP/HTTPS protokolüyle açılması düzeltildi.
- Termux oturumu kapandıktan sonra eski sunucu sürecinin 8080 numaralı bağlantı noktasını açık tutması önlendi.
- Termux başlangıç hata ekranı mobil terminal genişliğine uyumlu hâle getirildi; kurulum ve kullanım belgeleri v0.6.1’e göre yenilendi.
- Çıktı ve dağıtım adlarında eski **Manager** ifadesi kaldırılarak **APK Cleaner Studio** adı standartlaştırıldı.

### Ortak arayüz

- Cihaz modeli alınamadığında tarayıcı markasına bağlı olmayan **Android · cihaz adı alınamadı** açıklaması kullanılıyor.
- Sabit üst çubuk, ekran boyutları arasında tutarlı buzlu/sıvı cam görünümüyle yenilendi.
- Ana başlıktaki hareket animasyonu yumuşaklığı korunarak yeniden dengelendi.
- Açık temada düşük kontrastlı simge, işaret ve metinlerin görünürlüğü artırıldı.
- Mobil ve masaüstü üst barlarının bulanıklık yoğunluğu eşitlendi.
- İlk sayfa yüklemesindeki geçici yerleşim bozulmaları ve kart sıçramaları azaltıldı.
- Boş işlem geçmişi kartının gereksiz alan kaplaması giderildi.

## ⚙️ Platform özeti

### Windows

Tek EXE paketiyle çalışır. Yerel motoru başlatır, arayüzü varsayılan tarayıcıda açar ve aynı ağdaki izin verilen istemcilere erişim sunabilir.

### Termux

Kurulum ve başlatma betikleriyle aynı Motor 2.0 altyapısını Android terminal ortamında çalıştırır. Eski süreç temizliği ve bağlantı noktası yönetimi otomatik uygulanır.

### Android

Bağımsız APK olarak çalışır. Termux, haricî Java, komut satırı veya ayrı tarayıcı gerektirmez; işlem motoru ve arayüz uygulamanın içindedir.

## 🔐 Android paketleme ve doğrulama

- Release derlemesinde R8 küçültme ve kullanılmayan kaynak temizliği etkinleştirildi.
- Uygulama `debuggable=false` ve `jniDebuggable=false` olarak paketlendi.
- DEX satır/yerel değişken hata ayıklama tabloları ve native hata ayıklama sembolleri temizlendi.
- APK Repo özel anahtarıyla APK Signature Scheme **v2 + v3** kullanılarak imzalandı.
- Standart ZIP hizalaması ve 16 KB native sayfa uyumluluğu doğrulandı.
- Paket doğrulama, hizalama ve imza denetimleri kararlı derleme akışına eklendi.

## ✅ Doğrulama özeti

- **96/96** otomatik test başarılı.
- Android Lint ve release derlemesi başarılı.
- Android paket kimliği, sürüm adı/kodu ve mimari kaynakları doğrulandı.
- APK Signature Scheme v2 ve v3 doğrulaması başarılı.
- ZIP ve 16 KB native hizalama denetimi başarılı.
- Windows, Termux ve Android dağıtım adları ortak sürümle eşleştirildi.

## 📦 v0.6.1 dağıtım dosyaları

- `APK-Cleaner-Studio-v0.6.1-Windows.exe`
- `APK-Cleaner-Studio-v0.6.1-Termux.zip`
- `APK-Cleaner-Studio-v0.6.1-Android.apk`
- `SHA256-v0.6.1.txt`

**Önemli:** Düzenlenen APK’lar yeniden imzalanır. Orijinal uygulamayla imza uyuşmazlığı varsa yeni paket mevcut kurulumun üzerine yüklenmeyebilir; uygulama verilerini koruma gereksinimini gözeterek önce mevcut sürümü kaldırmak gerekebilir.

Bu sürüm Motor 2.0 altyapısını kullanır ve kararlı güncelleme kanalındadır.
