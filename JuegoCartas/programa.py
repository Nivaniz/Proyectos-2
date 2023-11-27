from PySide6 import QtCore, QtGui, QtWidgets
from helpers import absPath
import random
import sys


class Carta(QtWidgets.QLabel):
    def __init__(self, imagenPath, numero, nombre, palo, parent=None):
        super().__init__(parent)
        # Propiedades de la carta
        self.imagenPath = imagenPath
        self.numero = numero
        self.nombre = nombre
        self.palo = palo
        self.visible = False

        # Configuración de la imagen reversa por defecto
        self.imagen = QtGui.QPixmap(absPath("images/Reverso.png"))
        self.setPixmap(self.imagen)
        self.setScaledContents(True)

        # Tamaño base de la carta
        self.anchoBase = self.sizeHint().width()
        self.altoBase = self.sizeHint().height()

        # Grupo de animaciones para movimiento y reescalado
        self.animaciones = QtCore.QSequentialAnimationGroup()

    def mostrar(self):
        # Mostrar la imagen de la carta
        self.imagen = QtGui.QPixmap(absPath(f"images/{self.imagenPath}.png"))
        self.setPixmap(self.imagen)
        self.visible = True

    def esconder(self):
        # Esconder la carta mostrando la imagen reversa
        self.imagen = QtGui.QPixmap(absPath("images/Reverso.png"))
        self.setPixmap(self.imagen)
        self.visible = False

    def posicionar(self, x, y, sobreponer=True):
        # Posicionar la carta en la posición especificada
        if sobreponer:
            self.raise_()  # Sobreponer la carta si es necesario
        self.move(x, y)

    def mover(self, x, y, duracion=1000, escalado=1, sobreponer=True):
        # Mover la carta con animación de posición y reescalado
        if sobreponer:
            self.raise_()  # Sobreponer la carta
        self.animaciones = QtCore.QParallelAnimationGroup()
        # Animación de movimiento
        pos = QtCore.QPropertyAnimation(self, b"pos")
        pos.setEndValue(QtCore.QPoint(x, y))
        pos.setDuration(duracion)
        self.animaciones.addAnimation(pos)
        # Animación de reescalado
        size = QtCore.QPropertyAnimation(self, b"size")
        size.setEndValue(QtCore.QSize(self.anchoBase * escalado, self.altoBase * escalado))
        size.setDuration(duracion)
        self.animaciones.addAnimation(size)
        # Iniciar las animaciones
        self.animaciones.start()

    def reestablecer(self):
        # Detener las animaciones actuales
        self.animaciones.stop()
        # Reiniciar el grupo de animaciones
        self.animaciones = QtCore.QParallelAnimationGroup()
        # Restaurar los tamaños originales
        self.resize(self.anchoBase, self.altoBase)

    def mousePressEvent(self, event):
        # Manejar el evento de clic del mouse
        if self.visible:
            print(f"{self.nombre} de {self.palo}")


class Baraja(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Nombres y palos de las cartas
        nombres = ["As", "Dos", "Tres", "Cuatro", "Cinco", "Seis", "Siete", "Ocho", "Nueve", "Diez", "Jota", "Reina", "Rey"]
        palos = ["Treboles", "Diamantes", "Corazones", "Picas"]
        # Listas de cartas en la pila y cartas fuera de la pila
        self.cartas = []  # Lista de cartas en la pila
        self.jugadas = []  # Lista de cartas fuera de la pila
        # Crear cartas y añadirlas a la lista
        for palo in palos:
            for i, nombre in enumerate(nombres):
                carta = Carta(f"{i+1}{palo[0]}", i+1, nombre, palo, self)
                self.cartas.append(carta)  # Añadir a la lista
        self.mezclar()  # Mezclar las cartas

    def mezclar(self):
        # Mezclar las cartas en la pila
        random.shuffle(self.cartas)

    def extraer(self):
        # Extraer una carta de la pila
        try:
            carta = self.cartas.pop()  # Sacar la última carta (la de arriba)
            self.jugadas.append(carta)  # Añadir a la lista de cartas jugadas
            return carta
        except IndexError:
            return None

    def reiniciar(self):
        # Reiniciar el juego: esconder, reestablecer y mezclar las cartas
        for carta in self.jugadas:
            carta.esconder()  # Esconder las cartas jugadas
            carta.reestablecer()  # Restablecer tamaños y animaciones
            self.cartas.append(carta)  # Recuperar las cartas jugadas
        self.jugadas = []  # Borrar todas las cartas jugadas
        self.mezclar()  # Mezclar la baraja


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Configuración de la ventana principal
        self.setFixedSize(480, 320)
        self.setStyleSheet("QMainWindow {background-color: #144b12}")

        # Instanciar la baraja y configurar como widget central
        self.baraja = Baraja(self)
        self.setCentralWidget(self.baraja)
        self.preparar()  # Posicionar las cartas iniciales

        # Botones de la interfaz
        tomarBtn = QtWidgets.QPushButton("Tomar carta", self)
        tomarBtn.move(365, 15)
        tomarBtn.clicked.connect(self.tomar)

        reiniciarBtn = QtWidgets.QPushButton("Reiniciar juego", self)
        reiniciarBtn.move(250, 15)
        reiniciarBtn.clicked.connect(self.reiniciar)

    def preparar(self):
        # Posicionar las cartas iniciales en la baraja
        offset = 0
        for carta in self.baraja.cartas:
            carta.posicionar(40 + offset, 60 + offset)
            offset += 0.25

    def tomar(self):
        # Tomar una carta de la baraja y realizar animaciones
        carta = self.baraja.extraer()
        if carta:
            carta.mover(300, 110, 750, 0.75)
            carta.mostrar()

    def reiniciar(self):
        # Reiniciar el juego: esconder, reestablecer y mezclar las cartas
        self.baraja.reiniciar()
        self.preparar()


if __name__ == '__main__':
    # Ejecutar la aplicación
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
