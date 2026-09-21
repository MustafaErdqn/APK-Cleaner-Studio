# APK Cleaner Studio v0.6.2

<p align="center">
  <img src="release-assets/v0.6.2/APK-Cleaner-Studio-v0.6.2-Tanitim-Kapagi.png" alt="APK Cleaner Studio v0.6.2 tanıtım kapağı" width="100%">
</p>

[English README](README-EN.md) · [Termux kurulumu](README-TERMUX.md) · [Kaynaktan derleme](BUILDING.md) · [v0.6.2 sürüm notları](RELEASE-NOTES-v0.6.2.md)

Windows ve Android/Termux üzerinde çalışan, tamamen yerel APK reklam temizleme ve split paket dönüştürme yöneticisi.

## İndirme

Güncel kararlı paketleri [GitHub Releases](https://github.com/MustafaErdqn/APK-Cleaner-Studio/releases/latest) bölümünden indirebilirsin:

| Platform | Paket |
| --- | --- |
| Android | `APK-Cleaner-Studio-v0.6.2-Android.apk` |
| Windows | `APK-Cleaner-Studio-v0.6.2-Windows.exe` |
| Termux | `APK-Cleaner-Studio-v0.6.2-Termux.zip` |

İndirdiğin dosyayı aynı sürümde yayımlanan `SHA256-v0.6.2.txt` ile doğrulayabilirsin. Görselli sürüm özeti [Telegraph sayfasında](https://telegra.ph/APK-Cleaner-Studio-v062--Kararl%C4%B1-S%C3%BCr%C3%BCm-Notlar%C4%B1-09-20) yer alır.

## Yeni sürümde neler var?

- Normal reklam yamasında DEX’i ayıklamaz veya yeniden oluşturmaz; hedef komut baytlarını dosya içinde aynı uzunlukta ve yerinde değiştirir.
- Baksmali/Smali araçlarını kullanmaz ve ara kod klasörü üretmez; yalnızca DEX konumlarını okumak için gereken DexLib2 çalışma sınıflarını taşır.
- Yeniden paketlemede hızlı sıkıştırma kullanır; uygulanan yama kapsamı değişmez.
- Dengeli ve Kapsamlı profillerde aday manifest kayıtları ve reklam bileşenleri denetlenir.
- Bilinen reklam SDK görünümü taşıyan `res/layout*.xml` öğeleri `0dp` ve `gone` ile gizlenir.
- `.apks`, `.apkm` ve `.xapk` paketlerini tek, imzalı `.apk` dosyasına dönüştürür.
- Split dönüştürme sırasında reklam yamalarını isteğe bağlı olarak uygular.
- İsteğe bağlı DEX hata ayıklama verisi temizliği ve kaynak adı normalleştirme sunar.
- Eksik Java çalışma ortamını ve işlem bileşenlerini **Eksik bileşenleri hazırla** düğmesiyle otomatik olarak kurar.
- Daha profesyonel açık, sistem ve koyu tema içerir.

## Windows — tek EXE

`APK-Cleaner-Studio-v0.6.2-Windows.exe` dosyasına çift tıkla. Profesyonel Türkçe başlangıç ekranı gösterilir ve tarayıcı otomatik açılır; Python, BAT dosyası veya önceden Java kurulumu gerekmez. Java eksikse arayüzdeki bileşen hazırlama düğmesi doğrulanmış taşınabilir Java çalışma ortamını kullanıcı klasörüne kurar.

0.6.2 sürümü Motor 2.0 altyapısını; seçilebilir split bileşenleri, işlem iptali, yerel ağ oturum yönetimi, işlem geçmişi, isteğe bağlı yerel HTTPS ve iyileştirilmiş masaüstü/mobil deneyimiyle bir araya getirir. İsteğe bağlı ZIP hizalaması ve RES kaynak korumasını kaldırma seçenekleri korunur.

Windows başlangıç ekranı 110 sütun × 30 satır ölçüsünde düzenlenir; bağlantı, gizlilik, oturum ve güvenli kapatma bilgileri tek bakışta gösterilir. Web arayüzünün alt bölümünde APK Repo Grubu telif bilgisiyle birlikte resmi web sitesi ve Telegram topluluğu bağlantıları yer alır.

Program varsayılan olarak yerel ağda dinler. Konsolda hem bu bilgisayarda kullanılacak `127.0.0.1` adresi hem de aynı Wi‑Fi ağına bağlı telefon ve bilgisayarların kullanacağı yerel ağ adresi gösterilir. Bu erişim yalnızca güvenilen özel ağlarda kullanılmalıdır.

Windows yerel arayüzü HTTPS üzerinden açabilir. İlk çalıştırmada Windows, yalnızca mevcut kullanıcı için bu bilgisayara özel yerel sertifikaya güvenme onayı gösterir. Onay verildiğinde `127.0.0.1` bağlantısı tarayıcıda güvenli HTTPS olarak çalışır; özel anahtar cihazda kalır. Termux sürümü ise sertifika uyarısını önlemek için varsayılan olarak yerel HTTP adresini açar; HTTPS desteği isteğe bağlı olarak kullanılabilir.

Yerel ağa telefondan bağlanıldığında Android bilgisayarın yerel sertifika otoritesini kendiliğinden tanımaz. İsteğe bağlı HTTPS kullanmak için arayüzde **Yerel işlem motoru → Mobil HTTPS sertifikası** bölümünden CA sertifikasını indirip Android güvenlik ayarlarında bir kez CA sertifikası olarak yükle; ardından kullandığın tarayıcıyı tamamen kapatıp yeniden aç. Tarayıcı sertifikayı kabul etmezse yerel HTTP adresi kullanılabilir.

Program açılışta aynı klasördeki daha yeni Windows sürümlerini kontrol eder. HTTPS güncelleme kanalı yapılandırıldığında uzak sürümleri de denetler ve arayüzde sürüm notu ile indirme bildirimi gösterir. Program kendiliğinden mevcut EXE'nin üzerine yazmaz.

LAN erişimi için EXE’yi `--host 0.0.0.0` parametresiyle başlatabilirsin. LAN modu kimlik doğrulaması içermez; yalnızca güvendiğin özel ağda kullan.

## Termux

ZIP’i çıkardıktan sonra önce Termux’ta paketin bulunduğu klasöre gir. Paket Android’in İndirilenler klasöründeyse örnek:

```bash
termux-setup-storage
cd ~/storage/downloads/APK-Cleaner-Studio-v0.6.2-Termux
```

Ardından ilk kurulumda bir kez:

```bash
bash install-termux.sh
```

Sonraki kullanımlarda:

```bash
bash start-termux.sh
```

Klasör konumu farklıysa `cd` komutunda ZIP’i çıkardığın gerçek klasör yolunu kullan. Ayrıntılı adımlar `README-TERMUX.md` dosyasındadır.

Termux:Widget kuruluysa yükleyici ana ekran kısayolu hazırlar.

Kurulum, güncel Termux deposunda mevcutsa OpenJDK 25’i yükler; paket cihaz mimarisi veya kullanılan depo için sunulmuyorsa OpenJDK 21 ile uyumlu kuruluma devam eder. Uygulama `Ctrl+C` ile kapatıldığında başlatıcı kendi sunucu sürecini temizler; beklenmeyen kapanıştan kalan APK Cleaner Studio süreci sonraki başlangıçta güvenli biçimde sonlandırılır.

## İşlem türleri

- **Reklamları temizle:** Güvenli DEX çağrılarını yamar; seçilen temizlik profiline göre manifest kayıtlarını, XML reklam görünümlerini ve doğrulanmış SDK kalıntılarını temizler.
- **Tek APK’ya dönüştür:** APKS, APKM veya XAPK içindeki taban, özellik ve yapılandırma split’lerini birleştirir. İstersen aynı işlemde reklam yamalarını da uygular.

## Profiller

- **Güvenli:** Kesin `void` reklam yükleme/gösterme çağrılarını etkisizleştirir.
- **Dengeli:** DEX yamalarına ek olarak manifesti denetler; bilinen reklam SDK bileşenlerini ve kesin XML reklam görünümlerini temizler.
- **Kapsamlı:** Dengeli profile ek olarak kesin eşleşen reklam asset ve native kütüphane kalıntılarını kaldırır.

## İsteğe bağlı iyileştirmeler

- **Dönüştürme sırasında reklam yaması uygula:** APKS, APKM veya XAPK paketini tek APK’ya dönüştürürken seçtiğin Güvenli, Dengeli ya da Kapsamlı reklam temizleme profilini aynı işlem içinde uygular. Bu seçenek yalnızca split paket dönüşümünde gösterilir.
- **DEX hata ayıklama verilerini kaldır:** DEX kaynak, satır, yerel değişken ve benzeri hata ayıklama kayıtlarını temizler. Bu isteğe bağlı işlemde DEX yeniden yazılır; Smali/Baksmali kullanılmaz.
- **Yamalanan APK’yı optimize et:** İmzalamadan önce standart ZIP hizalaması uygular. DEX, manifest veya RES içeriğini yeniden derlemez ve RES kaynak koruması oluşturmaz; yalnızca APK içindeki dosyaların ZIP yerleşimini düzenler. APK boyutu birkaç KB artabilir.
- **RES kaynak korumasını kaldır:** APKEditor’ün yalın `x` işlemini (`java -jar APKEditor.jar x -i giriş.apk -o çıkış.apk`) paket üzerinde doğrudan çalıştırır. `-fix-types` kullanılmaz; manifest veya diğer binary XML dosyaları ayrıca yedeklenip geri yüklenmez. APKEditor’ün ürettiği paket sonraki aşamaya olduğu gibi aktarılır.

Bu seçenekler birbirinden bağımsızdır. İhtiyacın olanları birlikte seçebilirsin; seçilmeyen iyileştirmeler uygulanmaz.

## Sınırlar ve güvenlik

- Her APK’da yüzde yüz otomatik ve bozulmasız reklam temizliği garanti edilemez.
- Nesne döndüren riskli reklam çağrıları, çökme üretmemek için otomatik olarak `null` yapılmaz; rapora bırakılır.
- Yeniden imzalanan APK, mağaza sürümünün üzerine doğrudan kurulamayabilir.
- Universal APK üretimi, bazı isteğe bağlı özellik modüllerinde uygulamanın kendi split varsayımlarına bağlıdır.
- Üçüncü taraf ücretli özellikleri, satın almaları veya lisans kontrollerini atlatmaz.
- Yalnızca sahibi olduğun ya da değiştirme ve test etme yetkisine sahip olduğun paketlerde kullan.
