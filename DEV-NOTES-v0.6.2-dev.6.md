# APK Cleaner Studio v0.6.2-dev.6

## 6 Eylül — Kompakt teşekkürler alanı

- Ahmet Göktekin, Destekçi unvanıyla eklendi; mevcut isimler, daimi destekçi unvanları ve ʙʏᴛᴇᴄʜɴᴏ teşekkür mesajı korundu.
- Ayrı küçük kartlar yerine ince ayraçlı isim/rol satırları kullanıldı; boşluklar azaltıldı. Saydam ana yüzey ve açık/koyu tema renkleri korunur. Düzen Android, Windows ve Termux için ortaktır.

## 5 Eylül — İkon yoğunluğu, kesintisiz kaydırma ve çalışma animasyonu

- Domino’s v8.0.2 APK’sındaki sabit 18dp iç boşluklu adaptif ikon incelendi. Yüksek yoğunlukta logo alanını sıfırlayan doğrudan 72px çizim yerine, kaynak ölçülerinde yerleşim ve ölçeklenmiş canvas kullanılır; çıktı yine 72px kalır. Paket adına özel yama yapılmaz.
- Uygulama satırının gecikmeli görünür alana alınması yeni dokunma, tekerlek veya klavye hareketinde iptal edilir; hareket yalnız listeyle sınırlandırılır. Modern tarayıcılarda kaydırmayı ana iş parçacığına bağlayan touchmove engelleyicisi yerine mevcut sabit sayfa/CSS kaydırma sınırı kullanılır; eski WebView yedeği korunur.
- İlerleme dairesinin v0.6.1 paketinden doğrulanan özgün nefes animasyonu geri getirildi: 2,2 saniyelik döngüde 0–12px genişleyen, en fazla %9 yoğunlukta yeşil gölge. Önceki sarı halka ve videodaki işaretleme çizgisinin yanlış yorumlanmasıyla eklenen turkuaz yay kaldırıldı. Yüzde metni sabittir; azaltılmış hareket tercihi ve arka plan duraklatması korunur.
- Buton basma, popup açma/kapatma ve liste satırı geçişleri korunur. Sonuç ekranında yazıları üst üste oynatan eski iç içe hareketler yerine mevcut tek ana ekran geçişi sürer.
- Ortak arayüz Android, Windows ve Termux dev.6 paketlerinde aynıdır. Dokunmatik cihazdaki hissiyat ve gerçek ikon görüntüsü için cihaz doğrulaması ayrıca gerekir.

## 5 Eylül — Kararlılık ve başlangıç mesajı filtresi

- Android WebView çizim süreci sonlandığında uygulamadan çıkmak yerine kullanıcı kontrollü yeniden açma ekranı sunulur. Kapanmış veya yenilenmiş ekrana gecikmiş sonuç gönderilmez.
- Android yardımcı iş parçacıkları sınırlandırıldı; boşta serbest bırakılır. Motorun eski servis kapanışı ve yeni servis açılışı aynı sırada yürütülür.
- Yüklü uygulama simgelerinde başlatıcı Activity/alias ikonu önceliklidir; paket ikonu yedektir. Duruma bağlı çizimler ve hata durumunda bitmap belleğinin bırakılması düzeltildi.
- Sistem paylaşım/kurulum ekranının izin nedeniyle açılamaması yakalanır; başarısız indirmeler ve ağ bağlantıları temizlenir.
- Genel toast bildirimleri tekrar popup pencerelerinin altında kalır. Etki onayı uyarısı yalnızca ilgili satırda gösterilir.
- Büyük çoklu-DEX uygulamalarda tüm yöntemleri peşinen belleğe alan dizin yerine sınırlı, ihtiyaç üzerine yüklenen yöntem önbelleği kullanılır. MYT örneğinde taramayı engelleyen yöntem sayısı sınırı giderildi; boyut ve çalışma sınırları korunur.
- Ana listede farklı kod alanından, üst sınıf başlangıcından önce çağrılan ve taraması yarıda kalmayan adaylar öne çıkarılır. Daha belirsiz/orijinal işlevleri içerebilen sonuçlar kapalı bir bölümde tutulur; hiçbir sonuç otomatik seçilmez.
- MYT örneğindeki ayrı diyalog ve Toast köklerinin seçmeli kaldırılması geçici DEX kopyasında doğrulandı; kalan beş aday ve kaynak APK korundu. Bu test, fiziksel cihazda uygulama çalıştırma testi değildir.
- Filtre ve arayüz değişiklikleri Android, Windows ve Termux için ortaktır. Nadir kapanmanın kesin nedeni cihaz çökme kaydı olmadan doğrulanamaz; Domino's ikonu fiziksel cihazda ayrıca kontrol edilmelidir.

- Yüklü uygulama seçiminde yalnızca seçilen satır güncellenir; listedeki uygulama ikonları artık yeniden yüklenip göz kırpmaz.
- Geçmişteki bir paketi yeniden işleme, eski dosya izinlerini taşımadan yazılabilir ve uygulamaya özel yeni bir kaynak kopyası oluşturur.
- Android yerel motor istekleri sistem/VPN vekilini atlayarak doğrudan `127.0.0.1` oturumuna ulaşır; VPN kaynaklı boş HTTP 503 yanıtları önlenir.
- Yüklü uygulama kartı, işlem düğmeleri açıldığında da normal 14 px köşe formunu korur.
- Android WebView'in tüm dokunulabilir alanlarda oluşturduğu yarı saydam dokunma maskesi kaldırıldı; tasarıma ait basma/küçülme geri bildirimi korundu.
- Popup, rapor, mesaj inceleme, uygulama listesi, onay ve Özel Teşekkürler yüzeylerinde eski belirgin cam saydamlığı geri getirildi; ek renk tonu kaldırıldı ve açık/koyu tema okunabilirliği metin renkleriyle korundu.
- Yüklü uygulama işlem satırı açılıp kapanırken alttaki kartlar daha soft bir yükseklik ve saydamlık animasyonuyla kayar.
- Popup işlem düğmelerinde eski tasarımdan kalan kalın alt gölgeler kaldırıldı; normal basma/küçülme geri bildirimi korundu.
- Çift katmanlı ağır popup bulanıklıkları ve gereksiz kalıcı grafik katmanı ipuçları kaldırıldı; geçiş ve kaydırma sırasında GPU/bellek yükü azaltıldı.
- Açık tema popup perdesi koyu gri yerine aydınlık nötr cama dönüştürüldü; arama alanı ve uygulama satırları daha yumuşak yarı saydam yüzeylerle koyu temanın görsel dengesine yaklaştırıldı.
- Sonuç ekranındaki **APK’yı indir** etiketi, sağdaki ok korunarak butonun gerçek yatay merkezine alındı.
- Yüklü uygulama satırı açılırken yapılan çoklu yükseklik/marj hesaplamaları kaldırıldı; görünür satırlar GPU-dostu FLIP geçişiyle taşınıyor ve liste yeniden çizimi kendi alanında sınırlandırılıyor.

## İyileştirmeler

- Temizleme, seçili işlemleri başlatma ve APK oluşturma düğmesinin metni de indirme düğmesiyle aynı şekilde gerçek merkeze alındı; sağdaki ok için simetrik boşluk ayrıldı.
- Masaüstünde popup açılırken kaydırma çubuğunun kaybolmasıyla oluşan yatay kayma giderildi. Pencere ve ekran geçişleri metinleri ölçeklemeden solma animasyonuyla çizilir; mobilin mevcut geçişleri korunur.
- Buton basma tepkisi tüm platformlarda hafifletildi. PC'de metin netliği için ölçekleme yerine 1 piksellik basma hareketi, dokunmatik arayüzde daha küçük ölçek farkı kullanılır. Çakışan hover hareketleri ve masaüstü profil seçiminin kenarlık sıçraması giderildi.
- Özel Teşekkürler alanı, isimleri ve destekçi rollerini koruyan kompakt, ekran genişliğine uyarlanan bir ızgaraya dönüştürüldü; ʙʏᴛᴇᴄʜɴᴏ için ayrı teşekkür satırı eklendi. Tasarım ve hiyerarşi Android, Windows ve Termux'ta ortak tutulur.
- Özel Teşekkürler ikinci kez sıkılaştırıldı: masaüstünde tanıtım metni ile dört sütunlu isim listesi yan yana yerleşir; kart iç boşlukları, isim satırı yükseklikleri ve rol etiketleri küçültülür. Dar ekranda roller isimlerin altında kalır ve iki sütunlu okunabilir düzen korunur.
- Analiz sonuçlarındaki tek harfli işaretler, 18 reklam ağına özel, temaya uyumlu yerel SVG rozetlerle yenilendi. Rozetler resmî marka logoları değildir; harici görsel isteği gerektirmez.
- Etkileşimli kontrollerde tek, kısa basma animasyonu kullanılıyor. Rapor, onay, karşılaştırmalı mesaj ve uygulama listesi pencereleri kontrollü açılış/kapanış geçişlerine sahip; kapanış tamamlanana kadar arka sayfa kilidi korunuyor.
- Aynı kalan geçmiş ve cihaz listeleri yeniden oluşturulmuyor; liste geçişlerindeki yerleşim okumaları gruplanıyor. İlerleme çubuğu genişlik yerine dönüşümle çiziliyor; gereksiz sürekli gölge animasyonu kaldırıldı.
- Arayüz gizlendiğinde periyodik durum/geçmiş sorguları, işlem durumu yoklaması ve dekoratif animasyonlar duruyor; geri dönüldüğünde devam ediyor. Başlatılmış paket işlemleri ve dosya aktarımları iptal edilmiyor.
- Android'de görünmeyen WebView duraklatılıyor, boşta kalan yardımcı iş parçacıkları daha erken bırakılıyor ve bellek baskısında yeniden üretilebilir yerel simge önbelleği boşaltılıyor. Kullanıcı dosyaları ve bekleyen kurulum bilgileri korunuyor.
- Ortak arayüz değişiklikleri Android, Windows ve Termux paketlerinde aynıdır. Azaltılmış hareket tercihi desteklenir; belirli bir FPS veya pil tasarrufu oranı garanti edilmez, fiziksel cihaz ölçümü ayrıca gerekir.
- Yüklü uygulama listesi artık paket adına göre mevcut satırları ve ikon düğümlerini koruyarak güncellenir. Arama, yeniden açma veya Android'den aynı listenin tekrar gelmesi ikon kaynağını yeniden yüklemez; ikon giriş animasyonu kaldırıldı.
- Başlangıç çağrısı etki onayı verilmediğinde uyarı açık inceleme penceresinin içinde satır içi gösterilir; seçim uygulanmaz. Genel toast katmanı popup'ların altındadır.
- Mesaj incelemesi artık özgün APK yüklenmesini istemez. Gerçek Activity kalıtımı üzerinden `onCreate` ve `onResume` içindeki yardımcı başlangıç çağrıları, DEX dosyaları arasında diyalog/Toast/Snackbar gösterimine kadar izlenir; sınıf adı MainActivity veya FragmentActivity ile sınırlı değildir.
- Başlangıç taraması Activity yanında Fragment ve Application yaşam döngülerini, ek başlangıç geri çağrılarını, parametresiz/örnek yardımcıları, dönüş değeri kullanılmayan yardımcıları ve `Object` üzerinden taşınan gerçek Runnable türlerini de izler. Pawxy örneğinde daha önce kaçırılan iki `onResume` kökü genel kurallarla yakalandı; bu, APK adına veya paket adına yazılmış özel bir kural değildir.
- İncelemede seçilen başlangıç çağrısı kaldırılır; Activity'nin tamamı, `super.onCreate` veya ortak `show()` metodu silinmez. Gecikmeli görev bağlantıları ve başka işlevler de içeren çağrılar raporlanır. Hiçbir aday kendiliğinden seçilmez; başka başlangıç işlevlerinin etkilenebileceği onaylanır. Tek APK'dan bir çağrının sonradan eklendiği kesin kanıtlanamaz; şifreli veya yansımalı çağrıların tamamı çözülemez.
- Eski veya başka pakete ait mesaj seçimleri reddedilir; seçilen çağrılar yamadan hemen önce yeniden doğrulanır. Tekrarlanan split taramaları ayrı geçici alanlarda yürütülür.
- Reklam ağı rozetleri 28 px, iç simgeleri 20 px olacak şekilde kompaktlaştırıldı; ortak tema ve hiyerarşi korundu.
- İlerleme animasyonundaki 24 ms kare atlama sınırı kaldırıldı; hareket süresi 60/90/120/144 Hz'de kare sayısından bağımsızdır. Hızlı liste seçimlerinde kesilen animasyon mevcut görsel konumdan sürer. Boşta veya arka planda sürekli çizim yapılmaz; fiziksel 120 Hz cihazda ölçülmüş FPS garantisi verilmez.
- Reklam ağı bulunmayan paketlerde reklam temizleme profilleri artık gerçekten devre dışıdır; bağımsız iyileştirmeler kullanılmaya devam eder.

## Android yenilikleri

- İşlem sonucuna akıllı **APK’yı yükle** seçeneği eklendi. Android sürümü, işlemci mimarisi, imza ve sürüm çakışmaları kurulumdan önce denetlenir.
- Farklı imza veya daha yeni kurulu sürüm bulunduğunda veri kaybı uyarısı gösterilir ve kaldırma işlemi yalnızca kullanıcı onayıyla başlatılır.
- Bilinmeyen kaynak izni ve kaldırma ekranından dönüş güvenli biçimde beklenir; uygulama yeniden oluşturulsa bile bekleyen kurulum bilgisi korunur.
- İşlenmiş APK doğrudan paylaşılabilir.
- Cihazda yüklü tek APK veya split paketler, uygun `.apk`/`.apks` biçiminde paylaşılabilir.
- Yüklü uygulama kartına dokunulduğunda ikinci bir pencere açılmaz; kartın hemen altında tasarımla uyumlu **İşleme al** ve **Paylaş** seçenekleri satır içinde gösterilir.
- Paylaşılan yüklü uygulama dosyasına uygulama sürümü eklenir (ör. `APK Repo v1.2.apk`). Tek APK geçici kopya oluşturmadan doğrudan paylaşılır; split uygulama ise yalnızca **Paylaş** komutunda, yeniden sıkıştırılmadan bir kez `.apks` kapsayıcısına alınır ve güncel paket önbelleğiyle tekrar kullanılır.

## Düzeltmeler

- Karşılaştırmalı mesaj denetimindeki uzun özgün APK dosya adının mobil pencere dışına taşması engellendi.
- Geçmişteki **Tekrar işle** eylemi artık tamamlanmış iş durumunu yeniden kullanmak yerine özgün kaynak paketten bağımsız, yeni bir iş oluşturur.
- Android sistem kaldırma ekranının hiç açılmamasına yol açan eksik kaldırma isteği yetkisi ve intent uyumluluğu düzeltildi; kaldırma tamamlandıktan sonra paket durumu doğrulanarak kurulum açılır.
- Yüklü uygulama seçimindeki işlem penceresinin uygulama listesinin arkasında kalması, ikinci pencere kaldırılarak kökten giderildi.
- Başlangıç çağrısı etki onayı verilmediğinde uyarı yalnızca ilgili kutunun altında gösterilir; aynı metni tekrarlayan sarı toast kaldırıldı.
- Android yerel motoru uygulamaya dönüşte ve işlem öncesinde arka iş parçacığında kontrol edilir; erişilemiyorsa yeniden başlatılması istenir. Yüklü uygulama aktarımı motor hazır olmadan başlamaz. Okuma istekleri bağlantı onarımından sonra bir kez denenir; yükleme ve yama istekleri yanıt kaybında otomatik tekrarlanmaz.

## Paketler

- Windows: `APK-Cleaner-Studio-v0.6.2-dev.6-Windows.exe`
- Termux: `APK-Cleaner-Studio-v0.6.2-dev.6-Termux.zip`
- Android: `APK-Cleaner-Studio-v0.6.2-dev.6-Android.apk`

## Kaynak düzeni ve çalışma alanı temizliği

- Ortak Python motoru ve web arayüzü `manager/` yerine `studio/` altında tutulur. Windows spec'i, Windows/LAN başlatıcıları, Android eşitleyici, Termux paket yapısı ve tüm etkin test yolları aynı adlandırmaya taşındı.
- Sunucu sınıfları ile ürün sunucu tanımlayıcısı `StudioServer`, `StudioHandler` ve `APKCleanerStudio` adlarını kullanır. Güncelleyicideki eski `Manager` dosya adı desteği yalnızca daha eski kurulumlardan yükseltme uyumluluğu için korunur.
- Eski sürümlere ait tarihsel notlar ve yayımlanmış kararlı çıktılar korunur. Yeniden üretilebilir derleme klasörleri, test APK kopyaları, video inceleme kareleri, önbellekler ve aynı Windows dosyasının `-guncel` kopyası çalışma alanından kaldırıldı; Android SDK araç zinciri ve çıkarılmış FFmpeg korunur.
