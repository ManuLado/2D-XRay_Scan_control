#este script transforma las imagenes tomadas en formato .fits a .jpeg o .png
#se pueden cambiar varios parametros de la imagen, filtros, tamanio,etc (ver documentacion de ds9)
#requiere tener instalado SAOImage DS9

import os

def directory_name(nombre):
    directorio=nombre

    mylist=os.listdir(directorio) #modify to change directory dynamically
    print("number of files:",len(mylist))
    print(mylist)

    input("Enter to continue..")
    for i in mylist:
        string1=str(i)
    
        str2=string1.replace('fits','jpeg') #aca cambiar tambien el formato elejido
        #comandos ds9:
        #-cd> set working directory
        #-file> open .fits file
        #-cmap> mapa de colores (Heat, h5_bone,gray,etc)
        #-export> guardar imagen (png,jpeg,etc)
        os.system("ds9 -cd "+directorio + " -file "+string1+" -cmap h5_bone -export jpeg "+str2+' 75 -exit')
        print(str2,"------Ready!")
    
