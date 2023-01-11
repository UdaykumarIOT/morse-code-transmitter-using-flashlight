from time import sleep
import sys
from machine import Pin
import hotspot
import usocket as socket


MORSE_CODE_DICTIONARY = { ' ':' ',
                          'A':'.-',
                          'B':'-...',
                          'C':'-.-.',
                          'D':'-..',
                          'E':'.',
                          'F':'..-.',
                          'G':'--.',
                          'H':'....',
                          'I':'..',
                          'J':'.---',
                          'K':'-.-',
                          'L':'.-..',
                          'M':'--',
                          'N':'-.',
                          'O':'---',
                          'P':'.--.',
                          'Q':'--.-',
                          'R':'.-.',
                          'S':'...',
                          'T':'-',
                          'U':'..-',
                          'V':'...-',
                          'W':'.--',
                          'X':'-..-',
                          'Y':'-.--',
                          'Z':'--..',
                          '1':'.----',
                          '2':'..---',
                          '3':'...--',
                          '4':'....-',
                          '5':'.....',
                          '6':'-....',
                          '7':'--...',
                          '8':'---..',
                          '9':'----.',
                          '0':'-----',
                          ', ':'--..--',
                          '.':'.-.-.-',
                          '?':'..--..',
                          '/':'-..-.',
                          '-':'-....-',
                          '(':'-.--.',
                          ')':'-.--.-'}


led=Pin(18,Pin.OUT)
led.off()

html="""
<!DOCTYPE html>
<html>
<head>
    <title>Encoder</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">  
    <style>
        body {background-color:black;}
        h2 {color:aqua;}
        button {background-color: aqua;}
        input {background-color: aliceblue;
               color:rgb(0, 0, 0);
               font-size:medium;
              }

    </style>

</head>
<body>
    <br><br><br>
    <center>
        <h2>
            TEXT A MESSAGE TO SEND
        </h2>
    </center>
    <center>
        <form>
        <input type="text" name="Text" value="" size="30" autofocus required><br><br>
        <button type="submit">SEND</button>
        </form>
    </center>
</body>


</html>"""

hotspot.on()

def Text_to_Morse(txt):
    txt=txt.replace('+',' ')
    Converted_code = [MORSE_CODE_DICTIONARY[i.upper()] + ' ' for i in txt if i.upper() in MORSE_CODE_DICTIONARY.keys()]
    morse_code= ''.join(Converted_code)
    print(txt)
    print(morse_code)
    
    for i in morse_code:
        if i=='.':
            dot()
        if i=='-':
            dash()
        if i==' ':
            space()
    
def dot():
    led.on()
    sleep(0.3)
    led.off()
    sleep(0.2)

def dash():
    led.on()
    sleep(0.6)
    led.off()
    sleep(0.2)

def space():
    led.off()
    sleep(0.4)
    
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind(('',80))

s.listen(5)

while True:
    connection,address=s.accept()
   
    request=connection.recv(1024)
    req=str(request)
    first=req.find('=')
    last=req.find('HTTP')
    data=req[first+1:last]
    m=data.strip()
    if m=='exit':
        connection.close()
        hotspot.off()
        sys.exit()

    Text_to_Morse(data)
    
    response=html
    connection.sendall(response)
    connection.close()
