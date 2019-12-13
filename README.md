# 📦 YPackage

Kişisel python modüllerim

- 📦 [PYPI](https://pypi.org/project/ypackage/)
- 🐙 [Github](https://github.com/yedhrab/YPackage)

> ✨ Yenilikler için [CHANAGELOG](https://github.com/yedhrab/YPackage/blob/master/CHANGELOG.md) alanına bakın.

## 🔗 Google Drive Link Dönüştürücü

- 🔄 Google Drive bağlantılarını dönüştürmek için `ydrive` komutu kullanılır
- 👁️ Ön izleme bağlantılarını direkt indirme bağlantılarına çevirir
- 🆘 Kullanım detayları için `ygoogledrive -h` yazın

## 🔍 Google Arama Motoru

- 📋 Google üzerinden verilen metne göre çıkan sonuçlarını dosyaya raporlar
- ✨ İsteğe bağlı **html durum kodlarına* sahip bağlantıları raporlar
- 🆘 Kullanım detayları için `ygooglesearch -h` yazın

## 💫 Entegrasyon Scripti

- 🔄 Github - GitBook entegrasyonu için `ygitbookintegration` komutu kullanılır
- 🆘 Kullanım detayları için `ygitbookintegration -h` yazın

> Komut olarak sadece yol verilirse, dizindeki yapılandırma dosyasına (`.ygitbookintegration`) göre çalışır

### 👨‍🔧 Entegrasyon Yapılandırması

Entegrasyon yapılandırması `.ygitbookintegration` dosyası içerisindeki yapı ile sağlanır

| Modül                         | Açıklama                                                  |
| ----------------------------- | --------------------------------------------------------- |
| `[integration "Kişisel not"]` | Entegrasyonu verilen argümanlara göre çalıştırır          |
| `[submodule "kişisel not"]`   | Verilen GitBook sitesinin içeriklerine bağlantı oluşturur |

### 📑 Yapılandırma Dosyası Örneği

```ini
# ygitbookintegration'ı verilern argümanlara göre çalıştırır
# Detaylar: ygitbookintegration . -u olarak komutu çalıştırır
[integration "pre"]
	args = "-u"

# Verilen bilgiler doğrultusunda sitenin içeriklerini bağlantı oluşturur
# Detaylar: GitHub üzerinden url'deki SUMMARY'i içeriğini root'a göre düzenleyip, path'e yazar
[submodule "code/python.md"]
	description = 🐍 Python notlarım
	path = code/python.md
	url = https://github.com/YEmreAk/YPython
	root = https://python.yemreak.com
```

## 👨‍💻 Geliştirici Notları

Temel kullanım `import ypackage` şeklindedir ve modüllere `ypackage.<modül>` şeklinde erişilir.

| Modül        | Açıklama                                 |
| ------------ | ---------------------------------------- |
| `common`     | 🌟 Sık kullandığum metotlar              |
| `filesystem` | 📂 Dosya işlemleri                       |
| `gdrive`     | 🔗 Google drive link dönüştürücü         |
| `gitbook`    | 📖 GitBook için scriptlerim              |
| `github`     | 🐙 GitHub işlemleri                      |
| `integrate`  | 💫 Entegrasyon işlemleri                 |
| `markdown`   | 📑 Markdown scriptlerim                  |
| `regex`      | 💎 Regex scriptlerim (yapılm aşamasında) |

## 💖 Destek ve İletişim

​[​![Github](https://drive.google.com/uc?id=1PzkuWOoBNMg0uOMmqwHtVoYt0WCqi-O5)​](https://github.com/yedhrab) [​![LinkedIn](https://drive.google.com/uc?id=1hvdil0ZHVEzekQ4AYELdnPOqzunKpnzJ)​](https://www.linkedin.com/in/yemreak/) [​![Website](https://drive.google.com/uc?id=1wR8Ph0FBs36ZJl0Ud-HkS0LZ9b66JBqJ)​](https://yemreak.com/) [​![Mail](https://drive.google.com/uc?id=142rP0hbrnY8T9kj_84_r7WxPG1hzWEcN)​](mailto::yedhrab@gmail.com?subject=YPackage%20%7C%20Github)​

​[​![Patreon](https://drive.google.com/uc?id=11YmCRmySX7v7QDFS62ST2JZuE70RFjDG)](https://www.patreon.com/yemreak/)

## 🔏 Lisans

**The** [**Apache 2.0 License**](https://choosealicense.com/licenses/apache-2.0/) **©️ Yunus Emre Ak**

![YEmreAk](https://drive.google.com/uc?id=1Wd_YLVOkAhXPVqFMx_aZyFvyTy_88H-Z)

[geliştiriciler için api yayınlayan yerli girişim ve şirket listesi]: https://webrazzi.com/2017/07/17/uygulama-programlama-arayuzu-api/
