# Импорт необходимых библиотек
import io                                                               # для работы с файлами
import RPi.GPIO as GPIO                                                 # для работы с пинами Raspberry Pi
import Adafruit_DHT                                                     # для работы с датчиком DHT22
import mh_z19                                                           # для работы с датчиком CO2
import serial
from http.server import BaseHTTPRequestHandler, HTTPServer              # для сервера

# Считываем HTML из файла
file = io.open("index.html", 'r', encoding='utf-8-sig')                 # открываем файл в кодировке UTF-8
html = file.read()                                                      # читаем его в переменную html

# Класс сервера
class ServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))
        else:
            self.send_error(404, "Page Not Found {}".format(self.path))

# Функция, создающая отдельный поток для работы сервера
def server_thread(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ServerHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

# Запуск сервера
if __name__ == '__main__':
    port = 8000                                                         # порт, на котором работает сервер
    print("Starting server at port %d" % port)
    server_thread(port)

###################################################################################################################

# Настройка пинов
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(26, GPIO.OUT)        # pump
GPIO.setup(20, GPIO.OUT)        # light1
GPIO.setup(21, GPIO.OUT)        # light2
GPIO.setup(22, GPIO.IN)         # niz
GPIO.setup(23, GPIO.IN)         # verh

# Устанавливаем конец файлов для экрана
eof = "\xff\xff\xff"

# Настраиываем соединение с экраном
con = serial.Serial(

    port='/dev/ttyAMA0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
)

# Настройка датчика температуры и влажности
sensorHT = Adafruit_DHT.DHT22                                       # задаем подключенный датчик
pinHT = 10                                                          # задаем pin, к которому датчик подключен

# Начальные состояния
pump = 0
light1 = 0
light2 = 0
tank=''

# Функция включения/отключения насоса
def Pump():
    if(pump==0 & tank != 'Пуст'):
        GPIO.output(26, GPIO.HIGH)
        pump = 1
    else:
        GPIO.output(26, GPIO.LOW)
        pump = 0
        
# Функция включения/отключения свет 1 уровень
def Light(level):
    if(level == 1):
        if(light1 == 0):
            GPIO.output(20, GPIO.HIGH)
            light1 = 1
        else:
            GPIO.output(20, GPIO.LOW)
            light1 = 0
    elif(level == 2):
        if(light2 == 0):
            GPIO.output(21, GPIO.HIGH)
            light2 = 1
        else:
            GPIO.output(21, GPIO.LOW)
            light2 = 0

# Бесконечный цикл работы программы
while(True):
    # Получаем инфо с датчиков
    
    # Датчик температуры и влажности
    H, T = Adafruit_DHT.read_retry(sensorHT, pinHT)                     # считываем показания датчика H и T
    print(H+' '+T)
    
    # Датчик CO2
    CO2 = mh_z19.read()                                                 # считываем показания датчика CO2

    # Датчики уровней
    niz = GPIO.input(22)
    verh = GPIO.input(23)
    if(niz & verh): tank='Полон'
    elif(niz): tank='Не полон'
    else: tank='Пуст'
    
    # выводим данные в web-интерфейс
    # проверить на системе
    
    # выводим данные на экран
    # Записываем данные на страницу Page 0 c EOF
    con.write('page0.temp.val='+T+eof)
    con.write('page0.hum.val='+H+eof)
    con.write('page0.co2.val='+CO2+eof)
    con.write('page0.tank.txt='+tank+eof)

    # получаем данные с экрана (нажатие кнопок)
    readTxt = con.readline()
    #print output to screen with repr (returns a string containing a printable representation of an object)
    #print "Data Recieved:" + repr(readText)
    if(repr(readTxt)=="Насос"):Pump()
    elif(repr(readTxt)=="Свет1"):Light(1)
    elif(repr(readTxt)=="Свет2"):Light(2)
    else: print("Ошибка считывания!")
    
