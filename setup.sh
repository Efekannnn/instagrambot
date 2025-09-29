#!/bin/bash

echo "Instagram Çoklu Hesap Oluşturucu - Kurulum"
echo "=========================================="

# Python sürümünü kontrol et
python_version=$(python3 --version 2>&1)
if [[ $? -ne 0 ]]; then
    echo "❌ Python 3 yüklü değil!"
    echo "Lütfen Python 3.8 veya üzeri bir sürüm yükleyin."
    exit 1
fi

echo "✓ $python_version bulundu"

# Virtual environment oluştur
echo "📦 Virtual environment oluşturuluyor..."
python3 -m venv venv

# Virtual environment'ı aktif et
source venv/bin/activate

# Pip'i güncelle
echo "📦 pip güncelleniyor..."
pip install --upgrade pip

# Gereksinimleri yükle
echo "📦 Gereksinimler yükleniyor..."
pip install -r requirements.txt

# Chrome/Chromium kontrolü
echo "🌐 Chrome/Chromium kontrolü..."
if command -v google-chrome &> /dev/null; then
    echo "✓ Google Chrome bulundu"
elif command -v chromium-browser &> /dev/null; then
    echo "✓ Chromium bulundu"
else
    echo "⚠️  Chrome veya Chromium bulunamadı!"
    echo "Lütfen Google Chrome veya Chromium yükleyin."
fi

# Klasörleri oluştur
echo "📁 Gerekli klasörler oluşturuluyor..."
mkdir -p screenshots

echo ""
echo "✅ Kurulum tamamlandı!"
echo ""
echo "Kullanım:"
echo "1. config.json dosyasını düzenleyin ve proxy bilgilerinizi ekleyin"
echo "2. Virtual environment'ı aktif edin: source venv/bin/activate"
echo "3. Programı çalıştırın: python main.py"
echo ""