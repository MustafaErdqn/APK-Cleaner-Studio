# APK Cleaner Studio v0.6.0-dev.27 — Stabil Uygunluk Raporu

Tarih: 12 Ağustos 2026  
Uygulama: `0.6.0-dev.27`  
Motor: `2.0-dev.4`  
Karar: **Kullanıcı kabul testine hazır stabil sürüm adayı**

## Kapsam

Stabil `0.5.3` tabanından `dev.1`–`dev.26` boyunca eklenen bütün işlevler sürüm notlarından çıkarılarak aşağıdaki alanlarla eşleştirildi:

- APK/APKS/APKM/XAPK yükleme, akışlı dosya yazımı ve SHA-256 üretimi
- 18 reklam ağı profili, doğrudan DEX yaması, hata ayıklama verisi temizliği
- Güvenli, Dengeli ve Kapsamlı temizlik profilleri
- Binary manifest denetimi, XML `0dp + gone`, kaynak tablosunu koruyan arşiv yazımı
- RES kaynak korumasını kaldırma ve sayısal kaynak adı denetimi
- Split ABI, otomatik DPI, Türkçe/İngilizce dil seçimi ve universal APK üretimi
- ZIP hizalama, imzalama, imza doğrulama ve rapor üretimi
- Araç zinciri algılama/hazırlama, indirme SHA-256 kontrolü ve süre aşımı
- Atomik JSON durumları, bozuk JSON geri dönüşü, geçmiş, sahiplik, saklama ve silme
- Eşzamanlı iş talebi, ilerleme, uzak bağlantı tekrarları ve tek çalıştırma garantisi
- Oturum, cihaz adı, tarayıcı, public IPv4, ters vekil, engelleme ve erişim isteği
- HTTP/HTTPS aynı port, yerel CA, kaynak doğrulaması ve kapalı cihaz erişimi
- Windows kapanışı, aktif Java süreçlerinin sonlandırılması ve Termux konsol uyumu
- Dev/stabil güncelleme kanalı, HTTPS manifest ve güvenli indirme adresi denetimi

## Otomatik doğrulamalar

| Kapı | Sonuç |
|---|---:|
| Python birim/güvenlik/bütünlük testleri | 71/71 |
| JavaScript arayüz/paket testleri | 2/2 |
| ESLint | Hatasız |
| Python bytecode derleme | Hatasız |
| Web üretim derlemesi | Hatasız |
| Direct DEX Java kaynak derlemesi | Hatasız |
| Binary XML Java kaynak derlemesi | Hatasız |
| Gömülü JAR CRC/manifest denetimi | Hatasız |
| Windows PE ve Termux ZIP bütünlüğü | Hatasız |

## Gerçek motor sonuçları

Temsilî reklam çağrısı içeren gerçek APK ve çok modüllü APKS paketi kullanıldı.

| İşlem | Süre / sonuç |
|---|---:|
| 24 paralel APK analizi | ort. 224,11 ms; maks. 281,25 ms; tüm SHA-256 değerleri aynı |
| Dengeli + debug + ZIP hizalama | 2,71 sn |
| Güvenli profil | 0,92 sn |
| Kapsamlı profil | 2,34 sn |
| Yalnız dönüştürme/imzalama | 0,71 sn |
| RES kaynak korumasını kaldırma | 2,62 sn |
| RES sonrası sayısal `@0x...`/`@7f...` başvurusu | 0 |
| Normal yama sonrası `resources.arsc` | SHA-256 düzeyinde değişmedi |
| Universal APKS çıktısı | 5 DEX, geçerli ZIP, imzalı |

Bütün üretilen APK’lar ZIP CRC, DEX varlığı, META-INF ve Uber APK Signer kriptografik imza doğrulamasından geçti.

## Sunucu ve veri dayanıklılığı

- 240 eşzamanlı atomik JSON yazımı: sıfır hata, son dosya eksiksiz JSON, artık `.tmp` yok.
- Bozuk JSON: güvenli varsayılan duruma döndü.
- 40 eşzamanlı istemciyle 400 durum isteği: 200 HTTP + 200 HTTPS, sıfır hata.
- Yük testi gecikmesi: ort. 464,39 ms, p95 513,81 ms, maks. 612,38 ms.
- Web API uçtan uca akışı: 610.352 bayt yükleme + analiz 0,116 sn; toplam işlem 2,15 sn.
- İş isteği `202 Accepted` ile ayrıldı; ilerleme geriye gitmedi ve sonuç yazılmadan `%100` olmadı.
- İndirme, rapor, geçmiş sahipliği ve silme işlemleri gerçek dosyalarla doğrulandı.

Uygulamada SQL/D1/SQLite etkin değildir. Kalıcı veri katmanı atomik JSON dosyaları ve iş klasörlerinden oluşur; “veritabanı” denetimleri bu gerçek mimari üzerinde yapılmıştır.

## Dağıtım doğrulaması

- Windows EXE açılışı: 1,14 sn.
- EXE içindeki Java, DEX, manifest/XML, split, RES, zipalign ve imzalama bileşenlerinin tamamı hazır.
- EXE aynı portta HTTP ve HTTPS API yanıtı verdi; `Ctrl+Break` kapanışından sonra başlatıcı, PyInstaller alt süreci ve dinlenen port kalmadı.
- Termux ZIP: 32 dosya, CRC hatası yok, güncel kaynaklarla bayt düzeyinde eşleşiyor.
- Termux ZIP içinde TLS özel anahtarı, iş geçmişi, engellenmiş cihaz listesi, görünen ad, `.pyc`, `.tmp` veya `.part` yok.
- Kullanıcıya özel alan adı veya özel LAN IP adresi çalışma kaynaklarına gömülü değil.

## Denetimde bulunan ve giderilen sorunlar

1. NPM sürüm meta verisi eski `dev.9` değerinde kalmıştı; bütün sürüm kaynakları `dev.27` üzerinde eşitlendi.
2. Aynı JSON dosyasına eşzamanlı Windows yazımları `PermissionError` üretebiliyordu; atomik yazma kilidiyle giderildi.
3. HTTP sunucusunun varsayılan 5 bağlantılık kuyruğu yük testinde bağlantı reddine yol açtı; 128’e çıkarıldı.
4. Termux ZIP’e cihazın yerel TLS özel anahtarları girebiliyordu; paketleme filtresi düzeltildi ve sızıntı kapı testi eklendi.
5. Arayüz testi önceki build numarasına sabitlenmişti; çalışan paket sürümünü dinamik doğruluyor.
6. İlk EXE denetimi yalnız PyInstaller başlatıcı PID’sini izlediği için zorla kapatmada alt süreci kaçırıyordu. Windows kapanış yöneticisi `Ctrl+C`/`Ctrl+Break` olaylarını da kapsayacak şekilde genişletildi; paket kapısı artık kapanıştan sonra portun da kapandığını doğruluyor.

## Kabul öncesi dürüst sınırlar

- Windows üzerinde gerçek Termux/Android `pkg` kurulumu emüle edilmedi; Termux betikleri, paket içeriği ve Termux’a özel Python/konsol dalları doğrulandı. Son cihaz kabul testi gereklidir.
- Keenetic veya başka bir gerçek dış ters vekil altyapısına bu test ortamından bağlanılmadı; proxy/IP/HTTPS davranışları birim ve yerel entegrasyon testleriyle doğrulandı.
- Her üreticinin bütün APK çeşitlerini kapsamak mümkün değildir. Temsilî gerçek APK/APKS ve sentetik uç durumlar kullanıldı; otomatik reklam temizliği için uygulamaya özgü uyumluluk garantisi verilemez.
- Uzak güncelleme manifesti henüz yapılandırılmamıştır; güvenli HTTPS doğrulama ve hata davranışı mock testlerle geçmiştir.

## Sonuç

Bilinen yayın engelleyici hata kalmadı. `v0.6.0-dev.27`, stabil etiketi verilmeden önce Windows ve gerçek bir Termux cihazında kullanıcı kabul testine sunulabilir. Önceki talimata uygun olarak stabil sürüm numarası kullanıcı onayı gelmeden oluşturulmamıştır.
