# Instagram Çoklu Hesap Oluşturucu

Bu proje, proxy kullanarak otomatik olarak Instagram hesapları oluşturmak için geliştirilmiştir.

## Özellikler

- 🌐 Proxy desteği (HTTP/HTTPS/SOCKS5)
- 🤖 Anti-bot algılama koruması
- 📧 Otomatik e-posta oluşturma
- 🎭 Gerçekçi kullanıcı bilgileri
- 📊 Hesap bilgilerini Excel'e kaydetme
- 🔄 Hata yönetimi ve yeniden deneme

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. Chrome veya Chromium tarayıcısının yüklü olduğundan emin olun.

3. `config.json` dosyasını düzenleyin ve proxy bilgilerinizi ekleyin.

## Kullanım

```bash
python main.py
```

Script otomatik olarak 10 hesap oluşturacak ve bilgileri `accounts.xlsx` dosyasına kaydedecektir.

## Proxy Formatı

Proxy bilgilerini şu formatta ekleyin:
- HTTP/HTTPS: `http://username:password@host:port`
- SOCKS5: `socks5://username:password@host:port`

## Uyarılar

- Bu script sadece eğitim amaçlıdır
- Instagram'ın kullanım koşullarına uygun davranın
- Çok sayıda hesap oluşturmak IP banlanmasına neden olabilir
- Her hesap oluşturma arasında rastgele beklemeler vardır