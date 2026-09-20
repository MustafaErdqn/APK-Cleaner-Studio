# APK Cleaner Studio 0.6.0-dev.10

Bu sürüm kararlı sürüm adayı öncesindeki test sürümüdür.

## Yenilikler

- İstemcilere ilk açılışta cihaz adı soran otomatik pencere kaldırıldı. Kullanıcı isterse oturum kartındaki **Adını değiştir** seçeneğini kullanabilir.
- Ana makine arayüzüne uzak cihazlar için **Engelle**, **Engeli kaldır** ve **Listeden sil** seçenekleri eklendi. Bu yönetim seçenekleri uzak istemcilerde gösterilmez.
- Engellenen tarayıcı kimlikleri yerel olarak saklanır ve uygulama yeniden başlatıldığında erişim engeli korunur.
- Oturum listesinden silinen bağlı cihaz yeniden istek gönderirse tekrar görünebilir; kalıcı erişim reddi için **Engelle** kullanılmalıdır.
- Eski İşlemler kartına **Sil** seçeneği eklendi. İşlem sahibi kendi kayıtlarını, ana makine ise erişebildiği tüm kayıtları ilişkili yerel dosyalarıyla birlikte silebilir.
- Devam eden analiz veya yama işlemlerinin yanlışlıkla silinmesi engellendi.

## Gizlilik ve yetkilendirme

- Cihaz yönetimi yalnızca sunucuyu çalıştıran ana makineden yapılabilir.
- Uzak kullanıcılar diğer cihazları göremez, engelleyemez veya silemez.
- Engelleme IP adresine değil kalıcı tarayıcı/istemci kimliğine uygulanır; aynı ağ geçidini kullanan diğer cihazlar etkilenmez.

## Doğrulama

- Python birim, güvenlik ve bütünlük testleri: 46/46 başarılı.
- Arayüz yapı testleri: 2/2 başarılı.
