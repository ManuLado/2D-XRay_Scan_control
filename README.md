# 2D-XRay Scan Control 🔬☢

![superponer](https://user-images.githubusercontent.com/77543157/135559269-e34afabd-3760-43ed-93ca-e18cb184d90e.jpg)

Scripts python para el control de un sistema de movimiento automatizado para la adquisicion de imagenes radiograficas de muestras biologicas.
Implementa una captura de imagenes cada vezque el sistema se detiene, y guarda la imagen en un directorio nuevo cada vez quese corre el programa, con nombre ordenado segun las coordenadas en las cuales se tomo. Se controla la cantidad de imagenes que se quiere adquirir ası como la distancia maxima que se mueve el sistema entre adquisiciones. El sistema realiza un barrido en *y* para cada *x*, con una distancia por paso igual a la mitad del ancho H y alto V del sensor de imagen. 

## Comenzando 🚀

Descargar los archivos de la version v2.0 : 
* *xray_scanner.py* y 
* *procesado.py*
* *engraver.py*
* *take_images.py*

Guardarlos en un directorio en Raspberry Pi (probado en una Raspberry Pi 3 con OS Raspbian 2020-12-02)
correr *xray_scanner.py* desde un interprete con Python 3 o 
```
sudo python3 xray_scanner.py
```
El programa tiene como input el tamaño de barrido en el plano x-y. Luego de insertar estas dimensiones, el programa imprime en pantalla el tamaño de la matriz de barrido calculada, y un tiempo estimado de duracion del escaneo completo.
```
xstep: 7
ystep: 8
duracion estimada: 214.66 minutos (  3.57  horas)
x-->
y
|
v
[[0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0.]]
....................................................................................
press enter
```

Al presionar ENTER se comenzara el ciclo de escaneo.

☢ ⚠ Mantener la distancia al tubo de RX! ⚠ ☢

La matriz se ira actualizando a medida que se capturen las imagenes

Una vez finalizado el escaneo, las imagenes obtenidas apareceran guardadas en formato .fits en el nuevo directorio */fecha_nombredemuestra_run_numero*

para procesar estas imagenes (sumarlas, eliminar imagenes oscuras y filtrar ruido), ejecutar el script *procesado.py*

```
sudo python3 procesado.py
```
las imagenes procesadas apareceran guardadas en formato .jpg en el nuevo directorio */fecha_nombredemuestra_run_numero_FFT*
### Pre-requisitos 📋
* python 3
* astropy
* opencv 2
* numpy
* matplotlib
* Pillow>=5.2.0
* pyserial>=3.4

_Estos scripts utilizan los paquetes para manipular el sensor Arducam MT9M001 (ArduCAM_REV_A_USB_Camera_Shield-master.zip)
y un sistema de movimiento KKMoon Laser Engraver (kkengraver-master.zip). Controla un tubo de RX Imax 70 mediante rele_

Manuales de usuario 

- [ArducamMT9M001 ](Arducam_MT9M001_DataSheet_C.pdf)

- [Manual imax70 ](https://github.com/ManuLado/2D-XRay_Scan_control/blob/e308626ca804fb6c267cc8a0bede5e536d1170f2/Manual%20imax70.pdf)
### Instalación 🔧



El primer paso es configurar el puerto de la camara y habilitar los puertos seriales en caso de ser necesario entrando a 

```
sudo raspi-config
```

Para listar los puertos USB escribir

```
lsusb
```

Instalar los paquetes necesarios

```
sudo apt-get install saods9

sudo apt-get install python

sudo apt-get install python-opencv

sudo pip install astropy

pip3 install matplotlib
```

_Es recomendable controlar la Raspberry Pi remotamente, para reducir el riesgo a exposicion a radiacion ionizante. Se puede manejer desde Windows siempre que ambos dispositivos se encuentren conectados a la misma red. Para ello instalar xrdp en la raspberry_
```
sudo apt-get install xrdp
```
y encontrar su ip con
```
ifconfig
```
Acceder desde Windows (10) a la aplicacion  ‘Remote Desktop Connection’, escribir la direccion ip de la raspberry y conectar.
El usuario y contraseña para acceder a la Raspberry son los predeterminados:
* Username: pi
* password: raspberry


## Ejecutando las pruebas y checklist ⚙️✅

* Primero testear si funciona el sensor de la camara
```
sudo python take_images.py imtst 1
```
* Testear que el sistema KKMoon funcione correctamente
```
python3 engraver.py -d /dev/ttyUSB0 --no-fan -H       #home
python3 engraver.py -d /dev/ttyUSB0 --no-fan -m 50    #mueve 50 pasos en x
python3 engraver.py -d /dev/ttyUSB0 --no-fan -m -50   #mueve -50 pasos en x
python3 engraver.py -d /dev/ttyUSB0 --no-fan -m 0:50  #mueve 50 pasos en y
python3 engraver.py -d /dev/ttyUSB0 --no-fan -m 0:-50 #mueve -50 pasos en y
```

### Pausado del ciclo ⏸

El programa puede ser pausado durante el ciclo de escaneo, presionando

```
Ctrl + C
```
Para continuar se debe presionar cualquier tecla o ENTER
### Posibles problemas ❌ ⁉️ 

* La camara no responde/las imagenes no son capturadas. Aparecera un mensaje indicando

   ```
   ...
   Device open fail!
   ```
   Para resolver esto, pausar el script y

   ➡️ revisar los cables de conexion a la camara

* El tubo RX no enciende/ el rele se activa pero el buzzer del tubo RX no suena.

   ➡️ pausar el script y esperar mas tiempo para que el tubo RX se enfrie
      
   ➡️ comprobar que la puerta del blindaje este bien cerrada
   
   ➡️ comprobar que las conexiones del rele al tubo funcionen


## Autores ✒️


* **Gerardo Manuel Lado** - *Trabajo Inicial* - [Lado](https://github.com/ManuLado)


## Licencia 📄

Este proyecto está bajo la Licencia MIT . No se provee ninguna garantia de funcionamiento- mira el archivo [LICENSE.md](https://github.com/ManuLado/2D-XRay_Scan_control/blob/3eca928331250517cc78e94c35404e0f9dcaa60b/LICENCE.md) para detalles
Los autores se eximen de cualquier responsabilidad por el uso de este software.


---

![zebra](https://github.com/ManuLado/2D-XRay_Scan_control/blob/3bbab40012a6ca1ad8d53f07fede8cd1fd8991b2/zebra3-yodo.jpg)

