# APK Cleaner Studio 0.6.0-dev.12

Bu sürüm cihaz engellemesini tam arayüz erişim engeline dönüştüren test sürümüdür.

## Yenilikler

- Engellenen istemcilerin yalnızca APK işlemleri değil, ana sayfa ve statik arayüz dosyaları dâhil tüm erişimi reddedilir.
- Engellenen cihaz normal uygulama yerine bağımsız bir **Erişim engellendi** sayfası görür.
- Açık durumda engellenen bir istemci, 10 saniyelik durum yenilemesinde otomatik olarak kilit ekranına geçer.
- Kalıcı tarayıcı kimliği güvenli bir SameSite çereziyle ilk sayfa isteklerine de taşınır; böylece engel sayfa yenilendiğinde ve uygulama yeniden başlatıldığında korunur.
- Ana makinenin yerel oturumu engelleme denetiminin dışında tutulmaya devam eder.
- Dış IPv4 adresi doğrulanan bağlantılarda Keenetic veya başka bir ters proxy/router ana makine adı istemci adı olarak kullanılmaz.

## Doğrulama

- Python birim, güvenlik ve bütünlük testleri: 48/48 başarılı.
- Arayüz yapı testleri: 2/2 başarılı.
- Gerçek LAN erişim denemesinde engellenen istemci için ana sayfa, tema dosyası ve API isteklerinin tamamı `403` ile reddedildi; uygulama varlıklarının gönderilmediği doğrulandı.
