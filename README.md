# Pil Ölçer Projesi

Bu proje, **Arduino** ve **Python** (PyQt5) kullanarak bir **pil seviyesi ölçer** uygulaması geliştirmektedir. Arduino, pil gerilimini ölçerek seri port üzerinden Python uygulamasına aktarır. Python uygulaması, bu veriyi alıp bir grafik arayüzde gösterir.

---

## 🚀 Projenin Çalışma Mantığı

### **Arduino Tarafı**
- **Analog giriş pini (A0)** üzerinden pil gerilimi okunur.
- Okunan değer belirli bir aralıkta kalacak şekilde sınırlandırılır.
- % cinsinden pil doluluk oranı hesaplanır ve LCD ekrana yazdırılır.
- Seri haberleşme (Serial) ile bu değer **Python uygulamasına** gönderilir.

### **Python Tarafı (PyQt5 GUI)**
- **PyQt5** kullanılarak pil seviyesini gösteren bir arayüz oluşturulur.
- **Seri port** üzerinden gelen pil verisi işlenir.
- Pil seviyesi yüzde (%) olarak gösterilir.
- Pilin durumu belirli eşik değerlere göre belirlenir ve kullanıcıya gösterilir.
- Veri **her 500 ms'de bir güncellenir**.

---

## 🛠 Gerekli Bileşenler
### **Donanım**
- Arduino (Uno, Mega vb.)
- Pil (Ölçülecek güç kaynağı)
- **10kΩ direnç (gerilim bölücü için opsiyonel)**
- Bağlantı kabloları
- **16x2 LCD Ekran (Opsiyonel)**

### **Yazılım**
- **Arduino IDE** (Arduino kodlarını yüklemek için)
- **Python 3.x**
- **PyQt5** kütüphanesi (GUI için)
- **pyserial** kütüphanesi (Arduino ile haberleşme için)

Kurulum için aşağıdaki komutları çalıştırabilirsiniz:

```bash
pip install pyqt5 pyserial
```

---

## 📜 Arduino Kodu Açıklaması (arduino.ino)

### **📌 LCD Kütüphanesi ve Değişken Tanımları**
```cpp
#include <LiquidCrystal.h>
LiquidCrystal lcd(12,11,5,4,3,2);

#define pil A0
int gerilim = 0;
int min_deger = 246;
float yuzde = 0;
float deger = 0;
```
📌 **Bu kod ne yapıyor?**  
- `LiquidCrystal` kütüphanesi LCD ekranı kontrol etmek için kullanılır.
- `lcd(12,11,5,4,3,2);` LCD ekranın Arduino üzerindeki **bağlantı pinlerini** tanımlar.
- `#define pil A0;` Pil voltajını okuyacak **analog giriş pinini** belirler.
- `gerilim`, `min_deger`, `yuzde`, `deger` gibi değişkenler pil seviyesi hesaplamada kullanılır.

### **📌 Arduino Kurulumu (`setup` Fonksiyonu)**
```cpp
void setup() {
  Serial.begin(9600);
  lcd.begin(16,2);
  lcd.clear();
}
```
📌 **Bu kod ne yapıyor?**  
- `Serial.begin(9600);` Arduino'nun **bilgisayar ile haberleşmesini** başlatır.
- `lcd.begin(16,2);` LCD ekranın **16 sütun ve 2 satır** olarak yapılandırılmasını sağlar.
- `lcd.clear();` Ekranı temizler.

### **📌 Pil Gerilimi Okuma ve Gösterme (`loop` Fonksiyonu)**
```cpp
void loop() {
  gerilim = analogRead(pil);
  if(gerilim >= 338) gerilim = 338;
  if(gerilim <=246) gerilim = 246;

  yuzde = gerilim - min_deger;
  deger = (100.00/92.00) * yuzde;

  lcd.setCursor(0,1);
  lcd.print("Doluluk: %");
  lcd.print(deger);
  Serial.println(deger);
  delay(500);
}
```
📌 **Bu kod ne yapıyor?**  
- `analogRead(pil);` ile **A0 pininden pil voltajı okunur**.
- Okunan değer belirlenen sınırların dışına çıkarsa, 338 veya 246 ile sınırlandırılır.
- Pil yüzdesi hesaplanır: `(100.00/92.00) * yuzde`
- Sonuç **LCD ekrana** yazdırılır.
- **Seri port** üzerinden Python'a gönderilir.
- **500 ms bekleyerek** işlem tekrarlanır.

---

## 🖥 Python Kodu Açıklaması (batteryScreen.py)

- **Seri port (COM8)** üzerinden gelen veriyi okur.
- **PyQt5 arayüzü** ile kullanıcıya gösterir.
- Pil durumu **"İyi", "Ortalama", "Düşük"** olarak sınıflandırılır.
- **QTimer** kullanılarak her 500 ms'de bir veri güncellenir.

### **📌 Python Seri Port ve Arayüz Ayarları**
```python
import serial
arduino = serial.Serial("COM8",9600)
veri = arduino.readline().decode('utf-8').rstrip()
```
📌 **Bu kod ne yapıyor?**  
- `serial.Serial("COM8",9600)` ile Arduino'dan gelen veriyi okumak için **seri bağlantı** başlatılır.
- `readline().decode('utf-8').rstrip()` ile **gelen verinin temizlenmesi ve düzenlenmesi** sağlanır.

### **📌 Arayüzü Oluşturma (`BatteryWidget` Sınıfı)**
```python
class BatteryWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
```
📌 **Bu kod ne yapıyor?**  
- `QWidget` sınıfını kullanarak **PyQt5 arayüzünü oluşturur**.
- `initUI()` fonksiyonu çağrılarak **arayüzün başlangıç ayarları yapılır**.

### **📌 Pil Seviyesi Güncelleme (`update_label` Fonksiyonu)**
```python
def update_label(self):
    veri = arduino.readline().decode('utf-8').rstrip()
    int_veri2 = float(veri)
    self.battery_Label.setText(f"%{veri}")
    bataryaDurumu = degerHesaplama(int_veri2)
    self.status_label.setText(bataryaDurumu)
```
📌 **Bu kod ne yapıyor?**  
- **Arduino'dan gelen veri her 500 ms'de bir okunur.**
- Pil yüzdesi güncellenir ve **ekrana yazdırılır**.
- `degerHesaplama()` fonksiyonu ile **pil durumu belirlenir**.

---

## 🔧 Kurulum ve Çalıştırma

1. **Arduino kodunu** Arduino IDE kullanarak yükleyin.
2. **Arduino'yu USB ile bağlayın.**
3. **Python kodunu çalıştırın:**
   ```bash
   python batteryScreen.py
   ```
4. **Pil seviyesini ve durumunu ekranda görün.**

---

## 📝 Sonuç
Bu proje, **Arduino ve Python kullanarak bir pil seviyesi ölçme sistemi** oluşturur. Sensörden okunan veriler **LCD ekranda** ve **bilgisayar ekranında** gerçek zamanlı olarak görüntülenir. Daha gelişmiş bir versiyonda, **verilerin kaydedilmesi ve grafik olarak gösterilmesi** eklenebilir.

🚀 **Projeyi genişletmek için önerilerinizi paylaşabilirsiniz!**
