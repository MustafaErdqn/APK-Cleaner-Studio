# APK Cleaner Studio v0.6.2-dev.3

Bu geliştirme paketi kullanıcı onayı alınana kadar kararlı sürümün yerini almaz.

## Değişiklikler

- Android durum çubuğu ve ekran çentiği için tüm uygulama içi popup pencerelerine güvenli üst boşluk eklendi.
- İşlem raporu uygulama içinde görüntülenmeye devam ederken ayrıca metin dosyası olarak indirilebilir hale getirildi.
- Footer öncesine profesyonel bir **Özel Teşekkürler** alanı eklendi; destekçi isimleri tek bölümden kolayca düzenlenebilir.
- Android çıktı üretimi ve imzalama sonrası dosya doğrulaması güçlendirildi; eksik çıktı hataları artık gerçek araç hatasıyla raporlanır.
- Android çıktıları v2/v3 imzası ve 16 KB uyumlu ZIP hizalamasıyla doğrulanır.
- Tek başına kurulamayacak split `base.apk` dosyaları algılanarak Paket Yükleyici `-22` hatasına yol açan çıktı engellenir; kullanıcıdan özgün APKS/APKM/XAPK paketi istenir.
- Reklam ağı bulunmasa bile seçilen DEX, RES ve optimizasyon işlemleri **İşlemi başlat** düğmesiyle çalıştırılabilir.
- En geniş temizlik profili için **Gelişmiş** terminolojisine geçildi.
- Standart DEX yapısını doğrulayıp yeniden yazan güvenli **DEX yapısını yeniden düzenle** seçeneği eklendi. Bu işlem eşleme dosyası olmadan özgün yöntem adlarını tahmin etmez ve özel şifrelemeyi atlamaz.
- Google reklam çağrıları ve programatik banner görünümleri için doğrulanmış temizleme kapsamı genişletildi.
- Mobil yatay görünümde üst çubuk, durum rozeti, tamamlanma ekranı ve çentik alanı hizalandı.
- Play Store kaynak/bütünlük denetimi riski analiz aşamasında algılanarak kullanıcıya açıklayıcı uyarı gösterilir; doğrulama mekanizması değiştirilmez.
- Toast, Snackbar ve diyalog çağrıları analiz edilip rapora aday olarak eklenir. Arayüz, bunların yalnızca raporlandığını ve otomatik kaldırılmadığını açıkça belirtir.

## Paketler

- Windows: `APK-Cleaner-Studio-v0.6.2-dev.3-Windows.exe`
- Termux: `APK-Cleaner-Studio-v0.6.2-dev.3-Termux.zip`
- Android: `APK-Cleaner-Studio-v0.6.2-dev.3-Android.apk`
