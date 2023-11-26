# Importar módulos y clases necesarios
import sys
import time
from PySide6 import QtWidgets, QtCore
from ui_interfaz import Ui_MainWindow
from pyquery import PyQuery as pq
from urllib.parse import urlparse
import requests

# Definir la función para obtener la hora en formato ISO
def horaISO():
    hora = QtCore.QTime.currentTime()
    return hora.toString(QtCore.Qt.ISODateWithMs)

# Definir las señales para el hilo de trabajo
class WorkerSignals(QtCore.QObject):
    finished = QtCore.Signal(str, object)
    error = QtCore.Signal(str, object)

# Definir la clase del hilo de trabajo
class Worker(QtCore.QRunnable):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.signals = WorkerSignals()

    @QtCore.Slot()
    def run(self):
        try:
            # Realizar el web scraping con PyQuery
            doc = pq(url=self.url)
            # Emitir señal de finalización con la URL y el documento obtenido
            self.signals.finished.emit(self.url, doc)
        except requests.exceptions.RequestException as req_error:
            # Emitir señal de error en caso de problemas con la solicitud
            self.signals.error.emit(self.url, f"Error de solicitud: {req_error}")
        except Exception as error:
            # Emitir señal de error desconocido
            self.signals.error.emit(self.url, f"Error desconocido: {error}")

# Definir la clase principal de la ventana principal
class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # Configurar la interfaz de usuario
        self.setupUi(self)
        # Conectar el botón a la función de scraping
        self.pushButton.clicked.connect(self.scrappearWeb)
        
        # Configurar la pool de hilos para el trabajo concurrente
        self.threadpool = QtCore.QThreadPool()
        print("Multithreading con un maximo de %d hilos" % self.threadpool.maxThreadCount())
        
    # Reiniciar los elementos de la interfaz
    def reiniciar(self):
        self.title.setText("")
        self.language.setText("")
        self.viewport.setText("")
        self.author.setText("")
        self.description.setPlainText("")
    
    # Verificar si una URL es válida
    def is_valid_url(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    # Función para el scraping de una URL
    def scrappearWeb(self):
        self.reiniciar()
        # Obtener la URL del campo de entrada
        url = self.url.text()
        # Verificar la validez de la URL
        if not self.is_valid_url(url):
            print(f"{horaISO()} (Err) URL no valida: {url}")
            return

        # Imprimir la solicitud de scraping en la consola
        print(f"{horaISO()} (Req) {url}")
        try:
            # Realizar el scraping de la página web
            doc = pq(url=url)
        except Exception as error:
            # Manejar errores durante el scraping
            self.scrapeoFallido(url, error)
        else:
            # Manejar el éxito del scraping
            self.scrapeoCompletado(url, doc)
  
    # Función para el scraping concurrente de una URL
    def scrappearWebConcurrente(self):
        # Obtener la URL del campo de entrada
        url = self.url.text()
        # Verificar la validez de la URL
        if not self.is_valid_url(url):
            print(f"{horaISO()} (Err) URL no valida: {url}")
            return

        # Imprimir la solicitud de scraping en la consola
        print(f"{horaISO()} (Req) {url}")
        # Instanciar el trabajador y configurar sus señales concurrentes
        worker = Worker(url=url)
        worker.signals.finished.connect(self.scrapeoCompletado)
        worker.signals.error.connect(self.scrapeoFallido)
        # Iniciar el trabajador en la pool de hilos
        self.threadpool.start(worker)
     
    # Manejar el scraping fallido
    def scrapeoFallido(self, url, error):
        # Reiniciar la interfaz
        self.reiniciar()
        # Imprimir el mensaje de error en la consola
        print(f"{horaISO()} (Err) {url} {error}")

    # Manejar el scraping completado
    def scrapeoCompletado(self, url, doc):
        # Reiniciar la interfaz
        self.reiniciar()
        # Imprimir el éxito del scraping en la consola
        print(f"{horaISO()} (Suc) {url}")
        # Actualizar los elementos de la interfaz con los datos obtenidos
        self.title.setText(doc("title").text())
        self.language.setText(doc("html").attr("lang"))
        self.viewport.setText(doc("meta[name=viewport]").attr("content"))
        self.author.setText(doc("meta[name=author]").attr("content"))
        self.description.setPlainText(doc("meta[name=description]").attr("content"))

# Punto de entrada principal
if __name__ == '__main__':
    # Inicializar la aplicación Qt
    app = QtWidgets.QApplication(sys.argv)
    # Crear una instancia de la ventana principal
    window = MainWindow()
    # Mostrar la ventana
    window.show()
    # Salir de la aplicación al cerrar la ventana
    sys.exit(app.exec())

