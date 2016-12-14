from django.db import models

# Create your models here.
class TodoList(models.Model):
    item = models.CharField(max_length=144)
    is_done = models.BooleanField(default=False)
    in_progress = models.BooleanField(default=False)
    # check = models.ImageField(upload_to='media/checkmark image.jpg')

    def __str__(self):
        if self.is_done == True:
            return 'Completed: ' + self.item
        elif self.in_progress == True:
            return 'In progress: ' + self.item
        else:
            return 'Not started: ' + self.item
    class Meta:
        ordering = ["in_progress"]
