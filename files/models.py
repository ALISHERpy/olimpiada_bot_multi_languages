from django.db import models

class IMAGES(models.Model):
    file_id=models.CharField(max_length=300)
    description=models.TextField(blank=True)
    def __str__(self):
        return f"{self.file_id[:5]} : {self.description[:5]}"

class VIDEOS(models.Model):
    file_id=models.CharField(max_length=300)
    description=models.TextField(blank=True)
    def __str__(self):
        return f"{self.file_id[:5]} : {self.description[:5]}"

class TestFile(models.Model):
    file_id=models.CharField(max_length=300)
    language_code=models.CharField(max_length=4)
    description=models.TextField(blank=True)
    def __str__(self):
        return f"{self.file_id[:5]} : {self.description[:5]}"

class ChannelId(models.Model):
    channel_id=models.CharField(max_length=16,blank=True)

    def __str__(self):
        return f"hozirgi channel id: {self.id}"