# Web Scraper Concurrente con PySide6 y PyQuery

Este programa en Python utiliza las bibliotecas PySide6 y PyQuery para realizar web scraping de manera concurrente. La interfaz gráfica está diseñada con Qt, permitiendo a los usuarios ingresar una URL y obtener información sobre la página web de manera eficiente gracias al uso de hilos.

## Características Principales

- **Interfaz Gráfica Intuitiva:** Diseño simple que permite a los usuarios ingresar la URL de la página web que desean analizar.
- **Web Scraping Concurrente:** Utiliza hilos para realizar el web scraping de manera concurrente, evitando bloqueos en la interfaz de usuario.
- **Información Extraída:** Muestra información relevante de la página web, como el título, el idioma, la vista previa del meta viewport, el autor y la descripción.

## Requisitos Previos

Asegúrate de tener Python instalado en tu sistema. Puedes instalar las dependencias necesarias ejecutando el siguiente comando:

`
pip install PySide6 pyquery
`

## Ventanas

Ventana Principal:
<p align="center">
  <img src="https://github.com/Nivaniz/Proyectos-2/blob/main/WebScrapper/img/Captura%20de%20pantalla%202023-11-26%20124314.png" alt="Main Window" style="width: 50%; max-width: 200px;">
</p>

## Cómo Ejecutar
1. Clona o descarga este repositorio.
2. Abre una terminal y navega al directorio del repositorio.
3. Ejecuta el programa

## Configuración de Hilos
El programa utiliza una pool de hilos para realizar el web scraping concurrente. Puedes ajustar el número máximo de hilos editando el siguiente fragmento de código en MainWindow:
```
self.threadpool = QtCore.QThreadPool()
print("Multithreading con un máximo de %d hilos" % self.threadpool.maxThreadCount())
```

## Autoría

¡Tus contribuciones son bienvenidas! Si encuentras errores o mejoras para el proyecto, no dudes en enviar tus pull requests. Si tienes alguna pregunta o comentario, puedes encontrarme y visitar mi sitio web https://codingwithnirvana.pythonanywhere.com.

Espero que esta versión del README sea útil.
Creado por **Nirvana Belen González López** 
