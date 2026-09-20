# APK Cleaner Manager v0.6.0-dev.28

Motor sürümü: **2.0-dev.5**

## Kapsamlı banner ve native reklam temizliği

- XML'e doğrudan reklam SDK sınıfı yazılmayan, çalışma anında doldurulan kesin reklam kapsayıcıları Kapsamlı profilde algılanır.
- `ad_container`, `native_ad_container`, `banner_slot`, `mrec_ad` ve doğrulanmış eşdeğer kimlikler `0dp + gone` uygulanarak gizlenir.
- Native/banner reklamı görünüme bağlayan `setNativeAd`, `bindAd`, `renderAd`, `populateAd` ve ilişkili çağrılar doğrudan DEX üzerinde etkisizleştirilir.
- Doğrulanmış reklam SDK'sı nesnesi alan `onNativeAdLoaded`, `onBannerAdLoaded` ve eşdeğer yükleme geri çağrıları Kapsamlı profilde erken sonlandırılır.
- Kurallar yalnızca pakette bilinen bir reklam SDK'sı doğrulandığında ve yalnızca Kapsamlı profil seçildiğinde uygulanır.
- Genel promosyon bileşenleri ve Güvenli/Dengeli profillerin davranışı korunur.

## Doğrulama

- 75 Python testi geçti.
- 2 web/HTML sözleşme testi ve ESLint geçti.
- Gerçek APK/APKS işlem matrisi, imzalama ve kaynak tablosu koruması geçti.
- 400 eşzamanlı HTTP/HTTPS isteğinde hata oluşmadı.
- Gerçek yükleme, analiz, yama, indirme, geçmiş ve silme akışı tamamlandı.
- Windows ve Termux paket denetimleri geçti; çalışma verisi veya TLS özel anahtarı sızıntısı bulunmadı.

> Bu sürüm test adayıdır. Stabil etiketi kullanıcı kabul testinden sonra verilecektir.
