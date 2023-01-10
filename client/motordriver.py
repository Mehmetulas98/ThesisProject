import RPi.GPIO as GPIO          
import time

rin1 = 24
rin2 = 23
ren = 25 # PWM Pin
lin1 = 13
lin2 = 19
leftenable = 26
temp1=1
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(rin1,GPIO.OUT)
GPIO.setup(rin2,GPIO.OUT)
GPIO.setup(ren,GPIO.OUT)
GPIO.output(rin1,GPIO.LOW)
GPIO.output(rin2,GPIO.LOW)

GPIO.setup(lin1,GPIO.OUT)
GPIO.setup(lin2,GPIO.OUT)
GPIO.setup(leftenable,GPIO.OUT)
GPIO.output(lin1,GPIO.LOW)
GPIO.output(lin2,GPIO.LOW)

p=GPIO.PWM(ren,1000)
pleft=GPIO.PWM(leftenable,1000)

p.start(50)
pleft.start(50)
print("\n")
print("Baslangic olarak dusuk hiz ve ileri olarak calisir")
print("r-ileri s-dur f-ileri b-geri l-dusuk m-orta h-hizli e-cikis")
print("\n")    

while(1):

    x=input()
    
    if x=='r':
        print("ileri")
        if(temp1==1):
         GPIO.output(rin1,GPIO.HIGH)
         GPIO.output(rin2,GPIO.LOW)
         GPIO.output(lin1,GPIO.HIGH)
         GPIO.output(lin2,GPIO.LOW)
         print("forward")
         x='z'
        else:
         GPIO.output(rin1,GPIO.LOW)
         GPIO.output(rin2,GPIO.HIGH)
         print("backward")
         x='z'
    # sola dön
    elif x == 'ı':
        print("Sağa Dön")
        p.ChangeDutyCycle(100)
        pleft.ChangeDutyCycle(30) 
        GPIO.output(rin1,GPIO.HIGH)
        GPIO.output(rin2,GPIO.LOW)
        
        GPIO.output(lin1,GPIO.LOW)
        GPIO.output(lin2,GPIO.HIGH)
        
    #sağa dön    
    elif x == 'u':
        print("Sola Dön")
        p.ChangeDutyCycle(30)
        pleft.ChangeDutyCycle(100)
        GPIO.output(rin1,GPIO.LOW)
        GPIO.output(rin2,GPIO.HIGH)
        GPIO.output(lin1,GPIO.HIGH)
        GPIO.output(lin2,GPIO.LOW)
        
        
    elif x=='s':
        print("Dur")
        GPIO.output(rin1,GPIO.LOW)
        GPIO.output(rin2,GPIO.LOW)
        GPIO.output(lin1,GPIO.LOW)
        GPIO.output(lin2,GPIO.LOW)
         
        x='z'

    elif x=='f':
        print("ileri")
        GPIO.output(rin1,GPIO.HIGH)
        GPIO.output(rin2,GPIO.LOW)
        temp1=1
        x='z'

    elif x=='b':
        print("Geri")
        GPIO.output(rin1,GPIO.LOW)
        GPIO.output(rin2,GPIO.HIGH)
        GPIO.output(lin1,GPIO.LOW)
        GPIO.output(lin2,GPIO.HIGH)
        temp1=0
        x='z'

    elif x=='l':
        print("Dusuk")
        p.ChangeDutyCycle(25)
        pleft.ChangeDutyCycle(25)
        x='z'

    elif x=='m':
        print("Orta")
        p.ChangeDutyCycle(50)
        pleft.ChangeDutyCycle(50)
        x='z'

    elif x=='h':
        print("Yuksek")
        p.ChangeDutyCycle(75)
        pleft.ChangeDutyCycle(75)
        x='z'
    elif x== 'i':
        print("ultra yüksek")
        p.ChangeDutyCycle(100)
        pleft.ChangeDutyCycle(100)
        x='z'
     
    
    elif x=='e':
        GPIO.cleanup()
        break
    
    else:
        print("<<<  hatali data  >>>")
        print("normal komutlari yaziniz.....")

