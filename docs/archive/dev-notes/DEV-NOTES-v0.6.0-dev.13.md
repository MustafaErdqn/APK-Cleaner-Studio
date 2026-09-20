# APK Cleaner Studio 0.6.0-dev.13

Bu sürüm engelleme ekranının mobil uyumluluğunu ve model bilgisi bulunmayan cihaz açıklamasını iyileştirir.

## Yenilikler

- Engelleme sayfası telefonların güvenli ekran boşlukları, dikey/yatay yönleri ve küçük ekran yükseklikleri için yeniden düzenlendi.
- Açık arayüz engellendiğinde gösterilen istemci tarafı kilit ekranı, sunucunun bağımsız engel sayfasıyla aynı mobil yerleşimi kullanır.
- Tarayıcı model kodunu paylaşmadığında genel `Android cihazı` adı yerine `Android · model bilgisi paylaşılmadı` açıklaması gösterilir; böylece bunun bir tanıma hatası değil tarayıcı gizlilik kısıtı olduğu açıkça belirtilir.
- Engellenen cihaz kayıtları uygulama yeniden başlatıldığında da ana makinenin oturum listesine geri yüklenir.
- Engelleme sayfasına **Yöneticiden erişim iste** düğmesi eklendi. Ana makine isteği **İzin ver** veya **Reddet** seçenekleriyle yanıtlayabilir.

## Doğrulama

- Python motor, sunucu ve güvenlik paketi: **48/48 test başarılı**.
- Web arayüzü ve üretilen HTML paketi: **2/2 test başarılı**.
- Windows paketinde mobil engelleme sayfası, erişim isteği, izin/red akışı ve yeniden başlatma sonrası engelli cihaz kaydının geri yüklenmesi uçtan uca doğrulandı.
- Test tamamlandıktan sonra dev.13 çalıştırılabilir dosyasına ait açık süreç kalmadığı denetlendi.
