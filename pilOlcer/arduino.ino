#include <LiquidCrystal.h>
LiquidCrystal lcd(12,11,5,4,3,2);

#define pil A0
int gerilim = 0;
int min_deger = 246;
float yuzde = 0;
float deger = 0;

void setup() {
  Serial.begin(9600);
  lcd.begin(16,2);
  lcd.clear();

}

void loop() {
  
  gerilim = analogRead(pil);
  if(gerilim >= 338)
  gerilim = 338;
  
  if(gerilim <=246)
  gerilim = 246;

  yuzde = gerilim - min_deger;
  deger = (100.00/92.00) * yuzde;

  lcd.setCursor(0,1);
  lcd.print("Doluluk: %");
  lcd.print(deger);
  Serial.println(deger);
  delay(500);
  
  
  
}
