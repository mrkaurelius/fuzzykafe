# fuzzykafe

fuzzy metodlar ile kahve kalitesi belirleme.  

## Kullanım

Ubuntu 18 Bionicte test edilmistir. python kodlarını çalıştırıken sistem paketleri ile karışıklık oluşturmama adına virtual enviroment kullanılması **şiddetle** tavsiye edilir.

``` bash
git clone https://github.com/mrkaurelius/fuzzykafe
cd fuzzykafe

# virtual env. aktivasyonu
python3 -m venv venv # python3 virtual env
source ./venv/bin/activate

# bagimliliklarin yuklenmesi
pip3 install -r requirements.txt

# programin calistirilmasi
cd py/fuzzykafe

# tek satir veri icin, gorsellestirme
python3 varset2.py

# modelin testi 
python3 varset2_modeltest.py
```

### bağımlılıklar (dependencies)

bkz. requirements.txt

## Data
[coffee-quality-database](https://github.com/jldbc/coffee-quality-database)
[coffee-quality-database](https://www.kaggle.com/volpatto/coffee-quality-database-from-cqi?select=merged_data_cleaned.csv)

## Katkıda Bulunanlar

- Abdulcelil Kurt
- Abdulhamit Kumru
- Onur Güler
- Yavuz Selimhan Akşahin

### Kaynaklar

- https://caffenero.com/us/the-journal/good-beans-vs-bad-beans-selecting-coffee-at-origin/
