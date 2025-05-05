# Software de aplicación de pruebas de evaluación neuropsicológica y autoevaluación para estudiantes de educación superior

## Descripción
Las pruebas como PASAT y N-Back suelen medir la capacidad de memoria, sin embargo, se presentan situaciones de estrés con los aplicantes, siendo de vital importancia el resguardo de los datos estresores para un análisis posterior.
Este software es capaz de aplicar las pruebas PSAT y N-Back mientras graba al aplicante, además, registra aquellos momentos de posible estrés basado en las respuestas del aplicante.

## Instalación
```
sudo docker build -t 'cog_sw' .
sudo docker run -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY --privileged cog_sw
```

## Documentación
[Manual de usuario](https://drive.google.com/file/d/1x2-wkUh1GPvgYFC5rfqj622KonUrH2b6/view?usp=sharing)

[Manual técnico](https://drive.google.com/file/d/1JJDbpxMXr0kuNv4R0UuJbgMgBAri9tiE/view?usp=sharing)

## Interfaz
Pestaña de prueba PASAT:
![image](https://github.com/user-attachments/assets/e51051bf-d82f-4f5c-bbf4-bf0ef203856e)

Configuraciones de prueba PASAT
![image](https://github.com/user-attachments/assets/9e857211-22de-40d3-8755-1a7f82f3378b)

Pestaña de prueba N-Back
![image](https://github.com/user-attachments/assets/2d40aa18-06c3-4ec4-91a7-a6f410196ffc)

Configuraciones de prueba N-Back
![image](https://github.com/user-attachments/assets/5e136e12-bace-40e6-9fbb-064232b8bf8e)
