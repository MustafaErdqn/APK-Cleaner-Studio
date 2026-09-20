# APK Cleaner Studio 0.6.0-dev.25

- Masaüstündeki çalışma mimarisi alanı sadeleştirildi; büyük dekoratif yazı ve tekrar eden açıklamalar kaldırıldı.
- Sol ana sütunun alt yüzeyi sağ yan panel yüksekliğine göre esnek büyüyecek şekilde yeniden ölçülendirildi.
- Tarayıcı cihaz modelini paylaşmadığında genel bir cihaz adı uydurmak yerine hangi tarayıcının model bilgisini gizlediği açıkça belirtilir.
- Paylaşılan Android model kodları, yerel cihaz kataloğunda gerçek pazarlama adına çevrilmeye devam eder.
- Yerel ağ istemcileri için zorunlu HTTP → HTTPS yönlendirmesi kaldırıldı; HTTP ve HTTPS aynı portta isteğe bağlı olarak birlikte çalışır.
- Konsolda yerel ağ erişim adresi sertifika uyarısı oluşturmayan HTTP bağlantısı olarak gösterilir; ana bilgisayar HTTPS kullanmaya devam eder.
- HTTP üzerinden açılan arayüz, aynı adresin HTTPS sertifikasını sessizce sınar; sertifika güvenilir durumdaysa bağlantıyı otomatik olarak HTTPS’e yükseltir, değilse kesintisiz biçimde HTTP’de kalır.
