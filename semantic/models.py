from django.db import models
from .classification import MyClassifier
# Create your models here.
class Classification(models.Model):
    text = models.CharField(max_length=50)
    classification = models.CharField(max_length=50, editable = False)
    date_created = models.DateTimeField(auto_now_add=True)
    num_rows = models.IntegerField(blank=False, null=False)
    deduced_classification = ''


    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        cl = MyClassifier()
        self.classification = cl._classify(self.text, self.num_rows)
        #super().save(*args, **kwargs)
        print(self.deduced_classification)
        super().save(*args, **kwargs)

        

