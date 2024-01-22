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


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
