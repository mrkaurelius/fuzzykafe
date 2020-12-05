# Fuzzy Sistem Kuralları


## Örnek Kural
- Suyun sıcaklığına ve hava basıncına göre suyun kaynama durumunu belirlemek.
- Hava basıncı:  Düşük[0.5 atm,0.8 atm], Orta[0.8 atm,1,5 atm], Yüksek[1 atm,2 atm]
- Sıcaklık: Düşük[0 °C,40 °C], Orta[30 °C,75 °C], Yüksek[70 °C, 150 °C]
- Kural 1: EĞER hava basıncı Orta VE sıcaklık Yüksek ise, O HALDE su kaynıyordur.

## Değerler
Dataset degerleri

### Tüm veriler
#### Quality Measures
- Aroma
- Flavor
- Aftertaste
- Acidity
- Body
- Balance
- Uniformity
- Cup Cleanliness
- Sweetness
- Moisture
- Defects

#### Bean Metadata
- Processing Method
- Color
- Species (arabica / robusta)

#### Farm Metadata
- Owner
- Country of Origin
- Farm Name
- Lot Number
- Mill
- Company
- Altitude
- Region


### Bizim Kullandıklarımız
- Aroma (Aroma)
- Flavor (Lezzet)
- Acidity (Asitlik)
- Aftertaste (Ağızda kalan tat) 

#### Aftertaste (Ağızda kalan tat) 
- [6 - 7] Düşük 
- [7 - 8] Orta
- [8 - 9] Yüksek

Bu 4 değişkeni kullanarak oluşturduğumuz kurallar.

### Kural 1
Kural 1: EGER []