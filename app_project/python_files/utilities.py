import datetime as dt

##Función que muestra la fecha de un archivo en un formato amigable para el usuario.
def translateDate(date):
    aux = dt.datetime.fromtimestamp(date)
    res = dt.datetime.strftime(aux,"%Y-%m-%d %H:%M:%S")
    return res

##Función que muestra el tamaño fecha de un archivo en un formato amigable para el usuario.
def translateBytes(size):
    for elem in ['','K','M','G','T','P','E','Z']:
        if abs(size) < 1024:
            return "%3.1f%s%s" % (size, elem, 'B')
        size = size/1024
    
    return "%.1f%s%s" % (size, 'Y', 'B')

##Función que transforma que hace uso de las dos anteriores y devuelve un diccionario con el nombre del archivo, el tamaño amigable y la fecha amigable.
def formater(x):
    fStat= x.stat()
    fBytes = translateBytes(fStat.st_size)
    fTime = translateDate(fStat.st_mtime)
    return {'name': x.name, 'size': fBytes,'time': fTime }