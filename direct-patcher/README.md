# Direct DEX Patcher

APK Cleaner Studio'nun ara metin veya ayrıştırılmış sınıf ağacı üretmeden çalışan yerel DEX instruction motorudur.

- DexLib2 ile DEX instruction konumlarını doğrudan okur.
- Normal reklam temizliğinde DEX'i yeniden oluşturmaz; yalnızca hedef byte aralığını aynı code-unit uzunluğunda değiştirir.
- Branch hedeflerini, try bloklarını ve register düzenini korur.
- SHA-1 imzasını ve Adler-32 checksum değerini doğrudan yeniler.
- İsteğe bağlı debug temizliği seçilirse DexLib2 nesne yazıcısını kullanır; yine ara metin üretmez.
- Hiçbir aşamada `.smali` dosyası veya Smali klasörü oluşturmaz.
- İsteğe bağlı başlangıç taraması; sınıf adına güvenmeden Activity, Fragment ve Application kalıtımını; oluşturma, görünürlük, pencere odağı ve ertelenmiş görev yaşam döngülerini DEX dosyaları arasında izler. Native Dialog/Toast/Snackbar yanında DialogFragment, PopupWindow ve Compose diyalog uçlarını da tanır. Yalnızca kullanıcı seçerse yaşam döngüsündeki kök yardımcı çağrıyı aynı code-unit uzunluğundaki tek bir ileri geçiş komutuyla etkisizleştirir; terminal gösterim yöntemini veya yaşam döngüsü gövdesini silmez.

Derleme, projedeki yalnızca gerekli DexLib2 ve çalışma zamanı sınıflarını içeren `studio/tools/dexlib2-runtime.jar` paketine karşı Java 8 bytecode hedefiyle yapılır; Java 8–21 ortamlarında çalışır.
