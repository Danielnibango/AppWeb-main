from django.db import models

# Create your models here.

class Formateur(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE)
    adress = models.CharField(max_length= 20)
    telephone = models.CharField(max_length= 20)
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name 
    
    
    
class Apprenant(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE)
    adress = models.CharField(max_length= 20)
    telephone = models.CharField(max_length= 20)
    status = models.BooleanField(default= False)
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
    
    
    
class Stagiaire(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE)
    adress = models.CharField(max_length= 20)
    telephone = models.CharField(max_length= 20)
    lettrestage =models.FileField(upload_to="lettre")
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
    
    
    
class Encadreur(models.Model):
    user = models.OneToOneField(User,on_delete= models.CASCADE)
    adress = models.CharField(max_length= 20)
    telephone = models.CharField(max_length= 20)
    
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name



