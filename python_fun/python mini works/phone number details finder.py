#Phone number details py
import phonenumbers
from phonenumbers import timezone, geocoder, carrier
number1=input("type in the number for which u want the info \n")
number2="+91"+number1
phoneNumber = phonenumbers.parse(number2)
timeZone = timezone.time_zones_for_number(phoneNumber)
Carrier = carrier.name_for_number(phoneNumber, 'en')
Region=geocoder.description_for_number(phoneNumber, 'en')
print(phoneNumber)
print(timeZone)
print(Carrier)
print(Region)
