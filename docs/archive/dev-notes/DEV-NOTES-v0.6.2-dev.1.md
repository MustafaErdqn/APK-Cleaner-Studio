# APK Cleaner Studio v0.6.2-dev.1

Bu paket, kararlı v0.6.1 sürümünün yerini almayan ilk 0.6.2 test yapısıdır.

## Deneme kapsamı

- Android yatay üst çubuğu daha kompakt hâle getirildi.
- Android dikey işlem ve sonuç görünümlerindeki yatay taşmalar sınırlandı.
- İşlem başladığında ilerleme kartına, tamamlandığında sonuç kartına otomatik odaklanma eklendi.
- Tarayıcının eski sistem pencereleri yerine temayla uyumlu uygulama içi onay ve metin giriş pencereleri eklendi.
- RES korumasını kaldırma akışı yalın APKEditor `x` işlemiyle düzeltildi.
- XML reklam alanı denetimi RES çözümünden sonra çalışacak şekilde yeniden sıralandı.
- İstemcinin indirmeyi/bağlantıyı kapatmasıyla oluşan zararsız konsol traceback çıktısı susturuldu.

Android test paketi kararlı uygulamayla yan yana kurulabilmesi için `com.apkrepo.apkcleanerstudio.dev` paket adını kullanır.
