# APK Cleaner Studio 0.6.0-dev.14

Bu sürüm, özellikle engellenmiş Brave istemcilerinde cihaz modelini yeniden algılama zincirini güçlendirir.

## Yenilikler

- Engelleme sayfası Android model istemci ipucunu doğrudan talep eder.
- Engellenen istemci, normal arayüze erişmeden tarayıcının izin verdiği model ve tarayıcı bilgisini güvenli bir uç noktaya iletebilir.
- Toplanan bilgi yalnızca ilgili engelli oturum kaydını günceller; istemciye yerel ağ oturum listesi verilmez.
- Erişim isteği gönderilmeden önce cihaz bilgisi toplama denemesi tamamlanır.
- Güncellenen model bilgisi engelli cihaz kayıtlarıyla birlikte kalıcı olarak saklanır.

## Gizlilik sınırı

Brave veya başka bir tarayıcı model kodunu hem User-Agent hem de Client Hints üzerinden gizlerse web sayfası Android’in özel cihaz adını zorla okuyamaz. Bu durumda kullanıcı tarafından verilen **Adını değiştir** seçeneği geçerli kesin yöntemdir.

## Doğrulama

- Python motor, sunucu ve güvenlik paketi: **49/49 test başarılı**.
- Web arayüzü ve üretilen HTML paketi: **2/2 test başarılı**.
- Windows EXE üzerinde engellenmiş bir Brave istemcisinin sonradan gönderdiği `SM-G998B` kodunun **Samsung Galaxy S21 Ultra 5G** adına dönüştürüldüğü uçtan uca doğrulandı.
