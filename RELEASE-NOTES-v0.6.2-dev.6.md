# APK Cleaner Studio v0.6.2-dev.6 — Telegram paylaşım metni

🚀 Dostlar, APK Cleaner Studio **v0.6.2-dev.6 test sürümü** yayımlandı. Bu sürümde dev.6 boyunca yaptığımız önemli düzenlemeler tek pakette birleştirildi. Android, Windows ve Termux’ta ortak motor ve arayüz hiyerarşisi korunur.

🛠️ **Önemli düzeltmeler ve iyileştirmeler:**

🔧 Başlangıç mesajı denetimi; MainActivity, SplashActivity, SettingsActivity, Fragment ve Application yaşam döngülerindeki `onCreate`, `onResume`, `onStart` ve benzeri çağrıları tarayacak şekilde genişletildi. Diyalog, Toast ve Snackbar’a ulaşan yardımcı çağrılar önceliklendirilir; belirsiz/orijinal işlevler ayrı tutulur ve hiçbir aday otomatik seçilmez.
🔧 Büyük ve çoklu-DEX paketlerde tarama sınırları, yöntem önbelleği ve çağrı zinciri takibi geliştirildi. Eski işlemi tekrar işleme, geçici klasör izinleri, failed patch ve motorun bekleme sonrası durması gibi sorunlar için güvenli yeniden bağlantı akışı eklendi.
🔧 Yüklü uygulama listesindeki ikon göz kırpması, adaptif ikonların boş/kırmızı görünmesi ve kaydırma takılması azaltıldı. Satır içi seçenekler daha kararlı çalışır.
🔧 Popup’lar, açık/koyu tema, saydam cam yüzeyler, buton hizaları, eski gölgeler ve istenmeyen dokunma maskeleri düzeltildi. Liste satırı ve popup geçişleri yumuşatıldı; ilerleme dairesinin özgün yeşil nefes animasyonu geri getirildi.
🔧 Arayüz gizlendiğinde gereksiz sorgu ve çizimler durur; boşta CPU, bellek ve pil kullanımı azaltılır. Animasyon süreleri 60/90/120/144 Hz ekranlara uyarlanır.
🔧 Reklam ağı rozetleri kompaktlaştırıldı; reklam algılanmayan paketlerde reklam temizleme seçenekleri artık gerçekten devre dışıdır.

✨ **Yeni özellikler:**

📲 Android’e akıllı **APK’yı yükle** seçeneği eklendi. SDK, mimari, imza ve sürüm uyumluluğu kurulumdan önce kontrol edilir; farklı imza veya daha yeni sürüm varsa kaldırma yalnızca kullanıcı onayıyla başlatılır.
📤 İşlenmiş ve cihazdaki yüklü uygulamalar doğrudan paylaşılabilir. Tek paket `.apk`, split paket `.apks` olarak çıkarılır; gereksiz tekrar paketleme yapılmaz ve dosya adına sürüm bilgisi eklenir.
📱 Yüklü uygulama kartına dokunulduğunda seçenekler ikinci pencere yerine kartın hemen altında **Paylaş** ve **İşleme al** olarak açılır.
🧹 Diyalog/Toast incelemesi tek uygulamanın çağrı zincirinden çalışır. Seçilen başlangıç çağrıları kullanıcı onayından sonra işlenir; normal uygulama mesajlarından kaynaklanan gereksiz adaylar mümkün olduğunca filtrelenir.
💚 **Özel Teşekkürler** alanı daha kompakt ve saydam hâle getirildi. **Ahmet Göktekin — Destekçi** eklendi; mevcut destekçiler, daimi destekçiler ve ʙʏᴛᴇᴄʜɴᴏ’ya özel teşekkür mesajı korunuyor.

📦 **Paketleme ve doğrulama:**

✅ Android release paketinde R8/kaynak küçültme, DEX hata ayıklama temizliği, imza, ZIP ve 16 KB hizalama kontrolleri uygulandı. Son doğrulamada 138 Python ve 25 JavaScript testi başarılı oldu.

📱 **APK sürüm (Test kanalı):**
➡️ APK Cleaner Studio — Android

Bu sürüm test kanalındadır. Farklı APK’ların şifreli/yansıtmalı akışları ve fiziksel cihaz davranışları için geri bildirimlerinizi bekliyoruz. ❤️
