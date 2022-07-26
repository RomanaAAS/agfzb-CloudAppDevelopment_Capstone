from django.db import models
from django.utils.timezone import now

# Create your models here.
class CarMake(models.Model):
    make_id = models.IntegerField(primary_key=True)
    name_make = models.CharField(null=False, max_length=30, default="Auto")
    description = models.TextField()
    
    def __str__(self):
        return "Name: " + str(self.name_make) + ", Description: " + str(self.description)

# <HINT> Create a Car Model model `class CarModel(models.Model):
class CarModel(models.Model):
    SEDAN = "sedan"
    SUV = "suv"
    WAGON = "wagon"
    SPORT = "sport"
    CAR_MODEL_CHOICES = [(SEDAN, "Sedan"), (SUV, "SUV"), (WAGON, "Wagon"), (SPORT, "Sport"),]
    NEW = "new"
    USED = "used"
    CAR_MODEL_USAGE = [(NEW, "new car"), (USED, "pre-owned"),]
    model_id = models.IntegerField(primary_key=True)
    name_make = models.ForeignKey(CarMake, null=False, on_delete=models.CASCADE)
    name_model = models.CharField(null=False, default="Model A", max_length=30)
    dealership = models.IntegerField(default='13')
    type = models.CharField(null=False, choices=CAR_MODEL_CHOICES, default=SEDAN, max_length=30)
    year = models.DateField()
    usage = models.CharField(null=False, choices=CAR_MODEL_USAGE, default=NEW, max_length=10)
    
    def __str__(self):
        return "Maker: " + str(self.name_make) + ", Model: " + str(self.name_model) + " " +str(self.type)+ " " + str(self.year)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
