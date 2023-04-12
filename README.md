# aa-tt

Подключение датчика DHT22 (температура влажность) (если 4 вывода)
1 - питание (можно к выводу 3,3 или 5 вольт)
2 - данные
3 - не используется
4 - Земля (например 20 на плате или любой другой (GRND))
Если три вывода, то 1 - питание, 2 - данные, 3 - земля

Датчик DHT21
http://wiki.amperka.ru/%D0%BF%D1%80%D0%BE%D0%B4%D1%83%D0%BA%D1%82%D1%8B:dht-21

Понадабятся библиотеки Адафрут, установим их их с гитхаба:
sudo apt-get update
sudo apt-get install build-essential python-dev python-openssl ubuntu

Установка Adafruit
pip3 install adafruit-circuitpython-dht

sudo apt-get install libgpiod2

В программе импортируем библиотеку Adafruit_DHT
import adafruit_dht

sensor = adafruit_dht.DHT22(board.D18)
temp = Adafruit_DHT.dhtDevice.temperature
hum = dhtDevice.humidity

далее работа с этими данными
__________________________________________________________________

Датчик CO2 MH-Z19

Подключение
Vin - 5V
GND - GND
TxD и RxD - подключить накрест к таким же пинам распбери пай

Установим библиотеку для работы с датчиком

pip install mh_z19

или с гитхаба
git clone https://github.com/UedaTakeyuki/mh-z19.git
cd mh-z19
./setup.sh 

Код
import mh_z19

CO2 = mh_z19.read();


запись в страницу https://github.com/e-tinkers/simple_httpserver/blob/master/simple_webserver2.py

nextion https://pypi.org/project/nextion/   https://github.com/StableMind/Nextion

Since Nextion instruction sets are sent over serial, you would need to:

Connect your Pi to the Nextion screen through serial.
Connect to the screen in Python.
Assign your temperature reading to your variable:
command = "celcius.val=" + temperature
ser.write(command.encode('utf-8'))
