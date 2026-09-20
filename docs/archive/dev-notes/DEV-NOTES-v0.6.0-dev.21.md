# APK Cleaner Studio 0.6.0-dev.21

- Kişisel dış erişim adresleri uygulama kaynaklarından ve dağıtım yapılandırmasından kaldırıldı.
- Keenetic ters vekil desteği belirli bir alan adına bağlı kalmadan genel `*.keenetic.link` biçimiyle çalışır.
- Dış HTTPS adresi yalnızca güvenilir yerel ters vekilden gelen istek sırasında bellekte öğrenilir; diske yazılmaz ve sonraki açılışta geri yüklenmez.
- Uygulama başlangıçta her zaman kendi yerel adresini açar.
