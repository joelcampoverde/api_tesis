from django.db import models

from django.db import models

class Usuario(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    nombre = models.CharField(max_length=100)
    correo_electronico = models.EmailField()
    celular = models.CharField(max_length=20)
    rol = models.CharField(max_length=50)
    fecha_ingreso = models.DateTimeField()

    def __str__(self):
        return self.nombre

class Docente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="docente")
    facultad = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    titulo = models.CharField(max_length=100)
    zona_horaria = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.usuario.nombre} - {self.cargo}"

class ComandoVoz(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    descripcion = models.CharField(max_length=200)
    fecha_uso = models.DateTimeField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="comandos_voz")

    def __str__(self):
        return self.descripcion

class Agenda(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="agendas")

    def __str__(self):
        return f"Agenda de {self.usuario.nombre}"

class TipoEvento(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return self.descripcion

class Evento(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE, related_name="eventos")
    tipo_evento = models.ForeignKey(TipoEvento, on_delete=models.CASCADE, related_name="eventos")
    descripcion = models.CharField(max_length=200)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    modalidad = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

