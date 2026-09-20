# APK Cleaner Studio · Android

Bu modül, Windows ve Termux sürümlerindeki ortak web arayüzünü uygulama içindeki WebView'e taşır. Python sunucusu, DEX/AXML yardımcıları, APKEditor ve APK imzalama bileşeni uygulama sürecinde gömülü çalışır; Termux, komut satırı, haricî Java veya ayrı tarayıcı gerekmez.

## Hedef paket

- Uygulama kimliği: `com.apkrepo.apkcleanerstudio`
- Sürüm adı: `0.6.2`
- Sürüm kodu: `62`
- Minimum Android: 8.0 / API 26
- Hedef mimariler: `arm64-v8a`, `armeabi-v7a`
- Paketlenen diller: varsayılan İngilizce ve Türkçe
- Paketlenen yoğunluklar: `xhdpi`, `xxhdpi`

Doğrudan dağıtılan APK, **Yüklü uygulamalardan seç** işlevinde başlatıcısı olmayan
paketleri de gösterebilmek için geniş paket görünürlüğü iznini kullanır. Google
Play dağıtımı planlanırsa bu izin ve yayın beyanı ayrıca değerlendirilmelidir.

## Derleme

PowerShell'de proje kökünden:

```powershell
.\android\build-android.ps1 -Variant Release
```

Betik her derlemeden önce `packaging/sync_android.py` aracını çalıştırır. Böylece `studio/` altındaki ortak Python motoru ve aynı web arayüzü Android paketine otomatik taşınır. Masaüstü sürümünde yapılan ortak bir değişikliğin Android'e aktarılması tek komutla gerçekleşir.

Uygulama dağıtım imzası ve parola yapılandırması kaynak ağacının dışındaki yerel, korumalı imza dizininde tutulur. Bu özel anahtar gelecekteki bütün Android güncellemelerinde aynen korunmalı ve güvenli biçimde yedeklenmelidir. Anahtar ve parolalar Git tarafından izlenmez ve APK'nın içine eklenmez. Uygulama dağıtım imzası, işlenen APK çıktılarının imzalanmasında kullanılan gömülü anahtardan tamamen ayrıdır.

Android SDK bulunamazsa `ANDROID_SDK_ROOT`, Gradle bulunamazsa `APK_CLEANER_GRADLE_HOME` ayarlanabilir. Depodaki Gradle Wrapper üretildikten sonra betik onu otomatik kullanır.

## Güncelleme modeli

`studio/update-channel.json` içindeki HTTPS manifesti Android için `android_url` alanını destekler. Android güvenlik modeli gereği yeni APK kullanıcı onayı olmadan sessizce kurulmaz; uygulama yeni sürümü bildirir, imzalı APK'yı açar ve standart Android güncelleme ekranına bırakır.

Örnek manifest:

```json
{
  "version": "0.6.2",
  "android_url": "https://example.org/APK-Cleaner-Studio-v0.6.2-Android.apk",
  "windows_url": "https://example.org/APK-Cleaner-Studio-v0.6.2-Windows.exe",
  "termux_url": "https://example.org/APK-Cleaner-Studio-v0.6.2-Termux.zip",
  "notes": "Yeni sürüm kullanıma hazır.",
  "sha256": "..."
}
```

Uygulama kabuğunda değişiklik gerekmeyen arayüz, profil ve Python motor güncellemeleri için derleme betiği ortak kaynakları yeniden eşitler. Android izinleri veya yerel Java katmanı değiştiğinde yeni APK yayımlanır.
