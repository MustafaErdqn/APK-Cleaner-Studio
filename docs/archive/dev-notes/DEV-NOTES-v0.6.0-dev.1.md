# APK Cleaner Studio 0.6.0-dev.1

Bu paket yalnızca geliştirme ve kullanıcı testi içindir. Stabil 0.5.3 sürümü değiştirilmemiştir.

## Dev değişiklikleri

- Yerel motor kimliği `2.0-dev.1` olarak ayrıldı.
- APKS, APKM ve XAPK paketlerinde bulunan ABI modülleri ayrı ayrı seçilebilir.
- ARMv7 ve x86 için `xhdpi`, ARM64 ve x86_64 için `xxhdpi` bileşeni pakette mevcutsa otomatik eklenir.
- Pakette mevcutsa Türkçe ve İngilizce dil modülleri ayrı ayrı seçilebilir.
- RES kaynak korumasını kaldırma işlemine özgün `public.xml` ad–kimlik haritası eklendi.
- Binary XML hızlı taramada görünmese bile Dengeli ve Kapsamlı profiller XML katmanını ilk çalıştırmada denetler.
- XML görünüm tespiti `tag`, `class` ve `android:name` alanlarını birlikte değerlendirir.
- Reklam motoruna doğrulanmış yeni çağrı kalıpları ve altı ek SDK profili eklendi.
- Dev kanalında stabil otomatik güncelleme bildirimi gösterilmez.

## Doğrulama

- 21 Python testi başarılı.
- 2 arayüz testi başarılı.
- Web üretim derlemesi başarılı.
- Gerçek örnek APK üzerinde adlandırılmış XML kaynak başvuruları işlem öncesi ve sonrasında `7500`; sayısal `@0x...` başvuruları her iki durumda da `0` olarak doğrulandı.
- Windows dev EXE yerel API, Motor v2 kimliği ve tam kapanma denetiminden geçti.

Stabil sürüm numarasına yalnızca kullanıcı testinden ve açık onaydan sonra geçilecektir.
