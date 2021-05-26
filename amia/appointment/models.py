from django.db import models


class Appointment(models.Model):
    date_appointment = models.DateField(verbose_name="Дата записи")
    time_appointment = models.TimeField(verbose_name="Время записи")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия, имя, отчество", blank=True, null=True)
    date_of_birth = models.CharField(max_length=20, verbose_name="Дата рождения", blank=True, null=True)
    email = models.EmailField(verbose_name="E-mail", blank=True, null=True)
    date_of_write = models.DateTimeField(verbose_name="Дата записи", blank=True, null=True, auto_now=True)
    is_booked = models.BooleanField(verbose_name="Забронировано", default=False)
    comment = models.TextField(verbose_name="Комментарий к записи", blank=True, null=True)

    def __str__(self):
        return str(self.date_appointment) + ' ' + str(self.time_appointment) + ' ' + str(self.last_name)

    class Meta:
        ordering = ('-date_appointment',)
        verbose_name = 'Запись на тестирование'
        verbose_name_plural = 'Записи на тестирование'
