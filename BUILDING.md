# APK Cleaner Studio — Kaynaktan derleme

Bu belge APK Cleaner Studio v0.6.2 kaynak ağacını doğrulamak ve Android, Windows veya Termux paketlerini yeniden üretmek isteyen geliştiriciler içindir.

## Kaynak ağacında bulunmayan özel dosyalar

Depoda hiçbir gerçek yayın anahtarı, API anahtarı, token, parola dosyası veya yerel TLS özel anahtarı tutulmaz. Aşağıdaki dosyalar bilinçli olarak Git dışında bırakılır:

- `studio/tools/output-signing.p12`
- `android/app/src/main/assets/output-signing.p12`
- `android/signing/*.jks` ve `android/signing/*.p12`
- `android/signing.properties`
- `.env*`, `work/`, `studio/tls/` ve yerel derleme klasörleri

İşlenen APK çıktıları için kendi yerel anahtarını oluştur. Aşağıdaki geliştirme anahtarı yalnızca kendi derlemelerin içindir; resmî APK Cleaner Studio çıktılarıyla aynı imza kimliğini üretmez:

```powershell
keytool -genkeypair -alias apkcleaner-output -keyalg RSA -keysize 2048 -validity 36500 -storetype PKCS12 -keystore studio/tools/output-signing.p12 -storepass apkcleaner -keypass apkcleaner -dname "CN=APK Cleaner Studio Local Output,O=Local Build"
```

`packaging/sync_android.py` bu dosyayı Android varlıklarına kopyalar. Özel anahtarı hiçbir zaman Git deposuna ekleme.

Android uygulamasının kendi yayın imzası, çıktı imzalama anahtarından ayrıdır. Yayın anahtarı yapılandırması için [android/signing/README.md](android/signing/README.md) belgesini kullan.

## Web arayüzü ve testler

Gereksinimler:

- Node.js 22.13 veya daha yeni bir 22.x sürümü
- npm

```bash
npm ci
npm run lint
npm test
```

## Windows paketi

Gereksinimler:

- Python 3.11 veya daha yeni bir sürüm
- `cryptography`
- PyInstaller
- JDK 21 veya daha yeni bir sürüm

```powershell
python -m pip install cryptography pyinstaller
python -m PyInstaller packaging/APK-Cleaner-Studio-Windows.spec --noconfirm
```

Üretilen Windows paketi `dist/` altında oluşturulur. Taşınabilir Java ve işlem araçları eksikse uygulama ilk çalıştırmada **Eksik bileşenleri hazırla** akışıyla bunları kullanıcı alanında hazırlar.

## Android paketi

Gereksinimler:

- JDK 21
- Android SDK ve güncel build-tools
- Gradle veya Gradle Wrapper
- Python 3
- Yerel çıktı imzalama anahtarı

Proje kökünde PowerShell ile:

```powershell
./android/build-android.ps1 -Variant Release
```

`ANDROID_SDK_ROOT`, `APK_CLEANER_GRADLE_HOME`, `APK_CLEANER_ANDROID_JDK` ve `APK_CLEANER_PYTHON` ortam değişkenleri gerektiğinde özel araç yollarını göstermek için kullanılabilir. Çıktı `outputs/APK-Cleaner-Studio-v0.6.2-Android.apk` olarak hazırlanır ve imza ile ZIP hizalaması doğrulanır.

## Termux paketi

Python 3 ile:

```bash
python packaging/build_termux.py
```

Çıktı `outputs/APK-Cleaner-Studio-v0.6.2-Termux.zip` olarak oluşturulur.

## Sürüm bütünlüğü

Dağıtımdan önce üç platform paketi için SHA-256 değerlerini yeniden üret ve yayımlanan `SHA256-v0.6.2.txt` dosyasıyla birlikte paylaş. Kaynak ağacındaki geçici çalışma dosyaları ile yerel anahtarlar paketlere eklenmemelidir.
