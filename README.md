# 2D-XRay Scan Control

![superponer](https://user-images.githubusercontent.com/77543157/135559269-e34afabd-3760-43ed-93ca-e18cb184d90e.jpg)

_Scripts python para el control de un sistema de movimiento automatizado para la adquisicion de imagenes radiografi-cas de muestras biologicas.
Implementa una captura de im ́agenes cada vezque el sistema se detiene, y guarda la imagen en un directorio nuevo cada vez quese corre el programa, con nombre ordenado segun las coordenadas en las cuales se tomo. Se controla la cantidad de im ́agenes que se quiere adquirir ası como la distancia maxima que se mueve el sistema entre adquisiciones. El sistema realiza un barridoen *y* para cada *x*, con una distancia por paso igual a la mitad del ancho H y alto V del sensor de imagen. 

## Comenzando 🚀

Descargar los archivos de la version v2.0 : 
* xray_scanner.py y 
* procesado.py
* engraver.py
* take_images.py

Guardarlos en un directorio en Raspberry Pi (probado en una Raspberry Pi 3 con OS Raspbian 2020-12-02)
correr xray_scanner.py desde un interprete con Python 3 o 
```
sudo python3 xray_scanner.py
```

### Pre-requisitos 📋

_Estos scripts utilizan los paquetes para manipular el sensor Arducam MT9M001 (ArduCAM_REV_A_USB_Camera_Shield-master)
y un sistema de movimiento KKMoon Laser Engraver: _
```
sudo raspi-config

sudo apt-get install saods9

sudo apt-get install python

sudo apt-get install python-opencv

sudo pip install astropy
```

### Instalación 🔧

_Una serie de ejemplos paso a paso que te dice lo que debes ejecutar para tener un entorno de desarrollo ejecutandose_

_Dí cómo será ese paso_

```
Da un ejemplo
```

_Y repite_

```
hasta finalizar
```

_Finaliza con un ejemplo de cómo obtener datos del sistema o como usarlos para una pequeña demo_

## Ejecutando las pruebas ⚙️

_Explica como ejecutar las pruebas automatizadas para este sistema_

### Analice las pruebas end-to-end 🔩

_Explica que verifican estas pruebas y por qué_

```
Da un ejemplo
```

### Y las pruebas de estilo de codificación ⌨️

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

