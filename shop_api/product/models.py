from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def products_count(self):
        return self.products.count()

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='products')

    def __str__(self):
        return self.title

    def review_list(self):
         return [i.text for i in self.reviews.all()]

    def rating(self):
        result = self.reviews.aggregate(avg=models.Avg('stars'))
        return result['avg'] or 0

STARS = (
     (i, '* ' * i) for i in range(1, 6)
)

class Review(models.Model):
    text = models.TextField(null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='reviews')
    stars = models.IntegerField(choices=STARS, default=3)

    def __str__(self):
        return self.text