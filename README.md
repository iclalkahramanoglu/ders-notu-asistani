# 🎓 Ders Notu Analiz Asistanı

INP121 Projesi - RAG (Retrieval-Augmented Generation) Teknolojisi ile Ders Notu Asistanı

## 📖 Proje Hakkında

Bu proje, ders notlarınızı PDF formatında yükleyip, yapay zeka ile sorularınıza cevap alabileceğiniz bir asistan uygulamasıdır. RAG teknolojisi kullanılarak, AI sadece yüklediğiniz notlardan bilgi alır ve size cevap verir.

## ✨ Özellikler

- 📚 PDF ders notlarını otomatik analiz eder
- 🤖 Ollama (Llama 3.2) ile yerel AI çalışır
- 🔍 Qdrant vektör veritabanı ile hızlı arama
- 💬 Streamlit ile kullanıcı dostu web arayüzü


## 🛠️ Teknolojiler

- **Python 3.13+**
- **Ollama** (Llama 3.2 + OpenHermes)
- **Qdrant** (Vektör Veritabanı)
- **Agno** (Agent Framework)
- **Streamlit** (Web Arayüzü)
- **Docker** (Qdrant için)

## 📋 Gereksinimler

### Sistem Gereksinimleri
- macOS (Apple Silicon önerilir)
- Python 3.10 veya üzeri
- Docker Desktop
- En az 8GB RAM

### Kurulum Öncesi
1. [Ollama](https://ollama.com/download) kurulumu
2. [Docker Desktop](https://www.docker.com/products/docker-desktop/) kurulumu

## 🚀 Kurulum

### 1. Depoyu Klonlayın

```bash
git clone https://github.com/KULLANICI_ADINIZ/ders-notu-asistani.git
cd ders-notu-asistani
```

### 2. Sanal Ortam Oluşturun

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Gerekli Kütüphaneleri Yükleyin

```bash
pip install -r requirements.txt
```

### 4. Ollama Modellerini İndirin

```bash
ollama pull llama3.2
ollama pull openhermes
```

### 5. Qdrant'ı Başlatın

```bash
docker pull qdrant/qdrant
docker run -d -p 6333:6333 qdrant/qdrant
```

### 6. PDF Notlarınızı Ekleyin

`documents` klasörü oluşturun ve PDF ders notlarınızı buraya kopyalayın:

```bash
mkdir documents
# PDF'lerinizi documents/ klasörüne kopyalayın
```

### 7. Uygulamayı Çalıştırın

```bash
streamlit run ders_asistani.py
```

Tarayıcınızda `http://localhost:8501` açılacaktır.

## 💡 Kullanım

### Örnek Sorular:

- "Hangi konular var?"
- "Python'da döngü nedir?"
- "Bölüm 3'te ne anlatılıyor?"
- "Fonksiyonları açıkla"
- "Liste ve tuple farkı nedir?"

### İpuçları:

- Spesifik sorular sorun (örn: "Bölüm 5'teki for döngüsü örneğini göster")
- PDF dosya isimlerini İngilizce karakterlerle adlandırın
- İlk çalıştırmada PDF'ler analiz edilir, 1-2 dakika sürebilir

## 📁 Proje Yapısı

```
ders-notu-asistani/
├── ders_asistani.py      # Ana uygulama
├── requirements.txt       # Python kütüphaneleri
├── README.md             # Bu dosya
├── .gitignore            # Git ayarları
└── documents/            # PDF ders notları (GitHub'a yüklenmez)
```

## 🔧 Sorun Giderme

### Hata: "Veritabanına bağlanamıyor"
**Çözüm:** Docker çalışıyor mu kontrol edin:
```bash
docker ps
```

### Hata: "Ollama bulunamadı"
**Çözüm:** Ollama kurulu mu kontrol edin:
```bash
ollama list
```

### Hata: "PDF okunamıyor"
**Çözüm:** 
- PDF'ler `documents/` klasöründe mi?
- Dosya isimleri İngilizce karakterlerle mi?

## 👨‍💻 Geliştirici

**İsim:** İclal Kahramanoğlu -Çağatay Koç-Sude Kapramcı-Ekrem Efe Çelik
**Proje:** INP121 - Ders Notu Analiz Asistanı  
**Tarih:** Aralık 2024

## 📄Ön Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

## 🙏 Teşekkürler

- Agno Framework
- Ollama
- Streamlit
