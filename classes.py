import time
import datetime
#версия для теплицы в вакууме(нет учета внешней среды)
#пик тепла на улице - 15:00 пик холода на улице 6:00
class Sensors :#датчики теплицы
    def __init__(self, temperature, soil_humidity, air_humidity):      
        self.temperature = temperature
        self.soil_humidity = soil_humidity
        self.air_humidity= air_humidity
        
   

    def heat(self):   #допустим, что за итерацию при нагреве температура поднимается на 0.2 градуса
        #если надо, могу родолжить разработку с рассчетом изменения температуры, если будут точные данные кубатуры помещения и мощности нагревательного элемента
        self.temperature += 0.4
        
    def wateringBot(self):
        if self.soil_humidity<100:
            self.soil_humidity += 1
        
    def wateringTop(self):#видел видос от садовода, он разогнал с 50 до 65% за 7 минут, пусть и у нас будет 2% в минуту  
        if self.air_humidity<100:
            self.air_humidity += 3

    def cooling(self):   
        self.temperature -= 0.5
        
    def drainageBot(self):
        if self.soil_humidity>0:
            self.soil_humidity -= 0.1
        
    def drainageTop(self):
        if self.air_humidity>0:
            self.air_humidity -= 1.0
        
    def getTemp(self):        
        return self.temperature
    
    def getSoil_h(self):        
        return self.soil_humidity
    
    def getAir_h(self):        
        return self.air_humidity
        

class Equipment:#оборудование
    def __init__(self, mode_heater, modeBotWV, modemodeTopWV):
        self.mode_heater= mode_heater
        self.modeBotWV= modeBotWV #bottom_water_valve
        self.modeTopWV= modeTopWV#top_water_valve

    def __init__(self):
        self.mode_heater = 0
        self.modeBotWV= 0
        self.modeTopWV= 0
    
    def changeModeHearer(self, new_mode):#1-on, 0-off
        self.mode_heater = new_mode
        
    def changeModeBotWV(self, new_mode):
        self.modeBotWV = new_mode
        
    def changeModeTotWV(self, new_mode):
        self.modeTopWV = new_mode
        
class Controller: 
    def __init__(self, id, custom_temperature, custom_soil_humidity, custom_air_humidity):
        self.id=id
        self.custom_temperature = custom_temperature #10-25
        self.custom_soil_humidity = custom_soil_humidity #0-100
        self.custom_air_humidity = custom_air_humidity #0-100
        
    def __init__(self, id):
        self.id=id
        self.custom_temperature = 0.0
        self.custom_soil_humidity = 0.0
        self.custom_air_humidity = 0.0
    
    def acceptCustomMode(self, temperature, soil_humidity, air_humidity):#прием режима работы от платформы(циферки)(функция-интерфейс)
        self.custom_temperature = temperature 
        self.custom_soil_humidity = soil_humidity
        self.custom_air_humidity = air_humidity
        
        

    def sendReadings(self, temperature, soil_humidity, air_humidity):#заглушка на отправку
        print(self.id, generate_date(), temperature, soil_humidity, air_humidity)
     
def generate_date():
    return str(datetime.datetime.today())



