from django.db import models
from .classification import MyClassifier
# Create your models here.
class Classification(models.Model):
    text = models.CharField(max_length=50)
    classification = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    num_rows = models.CharField(max_length=15)
    deduced_classification = ''


    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        cl = MyClassifier()
        self.deduced_classification = cl._classify(text, num_rows)
        #super().save(*args, **kwargs)
        print(self.num_rows)

        

