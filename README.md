# 2D-XRay Scan Control

![superponer](https://user-images.githubusercontent.com/77543157/135559269-e34afabd-3760-43ed-93ca-e18cb184d90e.jpg)

_Scripts python para el control de un sistema de movimiento automatizado para la adquisicion de imagenes radiografi-cas de muestras biologicas.
Implementa una captura de im ́agenes cada vezque el sistema se detiene, y guarda la imagen en un directorio nuevo cada vez quese corre el programa, con nombre ordenado segun las coordenadas en las cuales se tomo. Se controla la cantidad de im ́agenes que se quiere adquirir ası como la distancia maxima que se mueve el sistema entre adquisiciones. El sistema realiza un barridoen *y* para cada *x*, con una distancia por paso igual a la mitad del ancho H y alto V del sensor de imagen. 

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



### Pre-requisitos 📋
* python 3
* astropy
* opencv 2
* numpy
* matplotlib
* Pillow>=5.2.0
* pyserial>=3.4

_Estos scripts utilizan los paquetes para manipular el sensor Arducam MT9M001 (ArduCAM_REV_A_USB_Camera_Shield-master.zip)
y un sistema de movimiento KKMoon Laser Engraver (kkengraver-master.zip)_
```
```

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
Acceder desdee Windows (10) a la aplicacion  ‘Remote Desktop Connection’, escribir la direccion ip de la raspberry y conectar.
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
python3 engraver.py -d /dev/ttyUSB0 --no-fan -m 0:-50 #mueve -50 pasos en x
```

### Analice las pruebas end-to-end 🔩

_Explica que verifican estas pruebas y por qué_

```
Da un ejemplo
```
 
### Posibles problemas ❌ ⁉️ 

_Explica que verifican estas pruebas y por qué_

```
Da un ejemplo
```

## Despliegue 📦

_Agrega notas adicionales sobre como hacer deploy_

## Construido con 🛠️

_Menciona las herramientas que utilizaste para crear tu proyecto_

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - El framework web usado
* [Maven](https://maven.apache.org/) - Manejador de dependencias
* [ROME](https://rometools.github.io/rome/) - Usado para generar RSS

## Contribuyendo 🖇️

Por favor lee el [CONTRIBUTING.md](https://gist.github.com/villanuevand/xxxxxx) para detalles de nuestro código de conducta, y el proceso para enviarnos pull requests.

## Wiki 📖

Puedes encontrar mucho más de cómo utilizar este proyecto en nuestra [Wiki](https://github.com/tu/proyecto/wiki)

## Versionado 📌

Usamos [SemVer](http://semver.org/) para el versionado. Para todas las versiones disponibles, mira los [tags en este repositorio](https://github.com/tu/proyecto/tags).

## Autores ✒️

_Menciona a todos aquellos que ayudaron a levantar el proyecto desde sus inicios_

* **Gerardo Manuel Lado** - *Trabajo Inicial* - [villanuevand](https://github.com/villanuevand)
* **Fulanito Detal** - *Documentación* - [fulanitodetal](#fulanito-de-tal)

También puedes mirar la lista de todos los [contribuyentes](https://github.com/your/project/contributors) quíenes han participado en este proyecto. 

## Licencia 📄

Este proyecto está bajo la Licencia (Tu Licencia) - mira el archivo [LICENSE.md](LICENSE.md) para detalles




---
⌨️ con ❤️ por [Villanuevand](https://github.com/ManuLado/) 😊

