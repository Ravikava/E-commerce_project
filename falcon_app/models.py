from django.db import models
import django.utils.timezone as timezone

# Create your models here.

gender_choice = (
    ('m','male'),
    ('f','female')
)

class Contact(models.Model):
    fullname = models.CharField(max_length=25)
    email = models.EmailField()
    message = models.TextField()


    def __str__(self):
        return self.fullname

class Buyer(models.Model):
    fullname = models.CharField(max_length=25)
    email = models.EmailField()
    address = models.TextField()
    password = models.CharField(max_length=8)

    def __str__(self):
        return self.fullname

class Seller(models.Model):
    fullname = models.CharField(max_length=25)
    company_name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.PositiveIntegerField()
    address = models.TextField()
    business_address = models.TextField()
    password = models.CharField(max_length=8)    

    def __str__(self):
        return self.fullname

class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete = models.CASCADE)
    product_name = models.CharField(max_length=50)
    product_title = models.CharField(max_length=50)
    product_size = models.CharField(max_length=10)
    product_price = models.PositiveIntegerField(default=1)
    product_image = models.ImageField(upload_to = "images/")
    product_quantity = models.PositiveIntegerField(default=1)
    product_description = models.TextField(default="some_text")

    def __str__(self):
        return self.product_name

class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete= models.CASCADE)
    date = models.DateField(auto_created = True , default=timezone.now)

    def __str__(self):
        return f"{self.buyer.fullname} --- {self.product.product_title}"

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete= models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete= models.CASCADE)
    date = models.DateField(auto_created = True , default=timezone.now)
    product_price = models.PositiveIntegerField()
    product_quantity = models.PositiveIntegerField(default=1)
    total_price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.buyer.fullname} --- {self.product.product_title}"

class Transaction(models.Model):
    made_by = models.ForeignKey(Buyer, related_name='transactions', 
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)