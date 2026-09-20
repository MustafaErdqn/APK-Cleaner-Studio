# Binary XML Patcher

AndroidManifest.xml dosyasını metne dönüştürmeden doğrudan ikili AXML ağacında düzenler.

- Yalnızca seçili reklam bileşenlerini, metadata kayıtlarını ve reklam izinlerini kaldırır.
- `resources.arsc` dosyasını yeniden üretmez.
- Kalan resource reference değerlerinin tür ve kimliklerini yazma sonrasında tekrar doğrular.
- Kaynak başvurularını `@style/...` biçiminden farklı bir sayısal kimliğe dönüştürmez.
