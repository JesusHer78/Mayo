class Persona:
    """
    Clase base que representa una entidad de persona general.
    Proporciona la estructura fundamental (nombre, edad, género) para otras clases derivadas.
    Demuestra principios de Encapsulación mediante el uso de atributos protegidos (_).
    """

    def __init__(self, nombre, edad, genero):
        """
        Constructor de la clase Persona.
        :param nombre: Nombre completo de la persona (string).
        :param edad: Edad de la persona (entero positivo).
        :param genero: Género de la persona (string).
        """
        self._nombre = nombre  # Atributo protegido
        self._edad = edad
        self._genero = genero

    @property
    def nombre(self):
        """Getter para obtener el nombre de la persona."""
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        """Setter para modificar el nombre de la persona."""
        self._nombre = value

    @property
    def edad(self):
        """Getter para obtener la edad de la persona."""
        return self._edad

    @edad.setter
    def edad(self, value):
        """
        Setter para la edad con validación de datos.
        Asegura que la edad sea un valor lógico y positivo.
        """
        if value > 0:
            self._edad = value
        else:
            raise ValueError("La edad debe ser mayor a 0")

    @property
    def genero(self):
        """Getter para obtener el género de la persona."""
        return self._genero

    def mostrar_info(self):
        """
        Genera una cadena de texto con la información básica de la persona.
        Este método es polimórfico y puede ser sobrescrito por clases hijas.
        """
        return f"Nombre: {self._nombre}, Edad: {self._edad}, Género: {self._genero}"
