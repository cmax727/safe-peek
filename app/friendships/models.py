from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField(max_length=20)

    def __unicode__(self):
        return self.name


# class Posting(models.Model):
#     text_posting = models.TextField()
#     file_posting = models.FileField()
#     image_posting = models.ImageField()
#     created_time = models.TimeField()
#     created_by = models.ForeignKey(User)

#     def __unicode__(self):
#         return self.text_posting
