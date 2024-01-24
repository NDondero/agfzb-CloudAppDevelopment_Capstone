from django.db import models
from django.utils.timezone import now


# Create your models here.


class CarMake(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name + ", " + self.description


class CarModel(models.Model):
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    dealer_id = models.IntegerField()
    SEDAN = "sedan"
    SUV = "suv"
    WAGON = "wagon"
    TYPE_CHOICES = [(SEDAN, "Sedan"), (SUV, "SUV"), (WAGON, "Wagon")]
    type = models.CharField(
        null=False, max_length=10, choices=TYPE_CHOICES, default=SEDAN
    )
    year = models.DateField(null=True)

    def __str__(self):
        return f"{self.make} {self.name} {self.year} {self.type}"


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


class DealerReview:
    def __init__(
        self,
        dealership,
        name,
        purchase,
        review,
        purchase_date,
        car_make,
        car_model,
        car_year,
        sentiment,
        id,
    ):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id


def __str__(self):
    return self.name
