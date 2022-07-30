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
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        #  id
        self.id = id
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment


    def __str__(self):
        return "Dealer name: " + self.full_name
