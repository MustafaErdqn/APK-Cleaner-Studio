# APK Cleaner Studio v0.6.2-dev.7

## Düzeltmeler

- Manifestte kalan Play split metadata’sı artık tek başına kesin “eksik split” kanıtı sayılmaz. Paket işleme engellenmez; gerçek bir kurulum riski varsa kullanıcıya açıklayıcı uyarı gösterilir.
- **Reklam izlerini temizle** seçimi tekrar dokunularak kapatılabilir. Başlangıç çağrısı kaldırma, DEX düzenleme, kaynak düzenleme veya APK optimizasyonu reklam temizliği olmadan bağımsız çalıştırılabilir.
- Reklam temizliği kapatıldığında Güvenli, Dengeli ve Gelişmiş kapsam kartları artık pasif görünmekle kalmaz; gerçekten devre dışı kalır ve seçilemez. Temizlik yeniden açıldığında geçerli kapsam geri yüklenir.
- Büyük masaüstü ekranlarda işlem ve sonuç sırasında ana panel solda, durum kartları sağ sütunda kalır. Ana ekrandaki “Paket içeride kalır” çalışma alanı kartı ve üçlü yetenek şeridi işlem ve sonuç boyunca görünür tutularak sol sütundaki gereksiz boşluk giderilir.
- Açık temadaki isteğe bağlı HTTPS simge kutusu, koyu temadaki yüzey hiyerarşisini koruyan belirgin bir açık tema kaplamasına kavuştu.
- Masaüstünde çok sayıda reklam ağı bulunduğunda Analiz Sonuçları kartı artık sayfayı uzatmaz; kart ölçüsü sınırlı kalır ve yalnızca sonuç listesi kendi içinde kaydırılır.
- Split paketlerde “Tek APK oluştur” seçeneği bulunduğunda reklam temizliği boş seçime düşmez; kullanıcı iki işlem arasında geçiş yapar. Tek APK dosyasında reklam temizliği yine isteğe bağlı olarak kapatılabilir.
- Yüklü uygulamadan alınan kaynak paket adı, paylaşım adıyla aynı biçimde uygulama adı ve sürüm numarasını içerir.
- DEX çağrıları sabit uzunluk korunarak tek bir ileri geçiş komutuyla etkisizleştirilir. Gelişmiş callback temizliği yalnızca ilk komutu erken dönüşe çevirir; uzun ve gereksiz NOP dizileri oluşturmaz.

## Başlangıç mesajı taraması

- Activity, Fragment ve Application köklerine ek olarak pencere odağı, `onNewIntent`, pencereye bağlanma ve ek Fragment yaşam döngüsü yolları izlenir.
- Native, AppCompat ve Material diyaloglarının yanında DialogFragment, PopupWindow ve Compose diyalog uçları tanınır.
- Sonuçlar yalnızca eşleşme sayısına göre listelenmez. Üst sınıf çağrısına göre yerleşim, kod alanı ilişkisi, zincirin yan etkileri, çözümleme bütünlüğü ve aynı hedefin kaç başlangıç kökünde kullanıldığı birlikte puanlanır.
- Yüksek olasılıklı adaylar ana listede tutulur; belirsiz çağrılar inceleme bölümüne, uygulamanın kendi akışına benzeyen düşük olasılıklı sonuçlar ayrı ve kapalı bir bölüme süzülür.
- Güvenli seçmeli davranış korunur: yalnızca kullanıcı tarafından seçilen yaşam döngüsü kök çağrısı aynı code-unit uzunluğundaki ileri geçiş komutuyla kaldırılır; ortak `show()` yöntemi veya Activity gövdesi topluca silinmez.

## Platformlar

- Ortak motor ve arayüz Android, Windows ve Termux’ta aynıdır.
- Paketler: `APK-Cleaner-Studio-v0.6.2-dev.7-Android.apk`, `APK-Cleaner-Studio-v0.6.2-dev.7-Windows.exe`, `APK-Cleaner-Studio-v0.6.2-dev.7-Termux.zip`.
