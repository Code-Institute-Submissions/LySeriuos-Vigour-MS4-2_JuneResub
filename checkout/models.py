import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings

from django_countries.fields import CountryField

from shop.models import Product
from profiles.models import UserProfile


# payment form
class Order(models.Model):
    # editable=False is to create unique order number, generated automatically
    order_number = models.CharField(max_length=32, null=False, editable=False)
    # models.SET_NULL allow us to keep order history in the admin even if the profile is deleted.
    # null or blank gives users possibility to buy who don't have an account.
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    # And updating the delivery cost, order total,
    # and grand total after customer create order insatnce.
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0)
        # original shoping bag that was created
    original_bag = models.TextField(null=False, blank=False, default='')
    # the unique value of stripe payment intent ID
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default='')    

    def _generate_order_number(self):
        """ Generate random and unique order number ysing UUID """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """ Update grand total each time a line item is added,
        accounting for delivery costs """
        # The '0' will prevent an error if manually deleted all the line items from an order
        # by making sure that this sets the order total to zero instead of none.
        self.order_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            self.delivery_cost = self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100
        else:
            self.delivery_cost = 0
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def save(self, *args, **kwargs):
        """ Override the original save method to set the order number
        if it hasn't been set already """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    # standard string method, returning the order number for the order model
    def __str__(self):
        return self.order_number

# A line-item will be like an individual shopping bag item.
# Relating to a specific order
# Use the information they put into the
# payment form to create an order instance.
# After it will iterate through the items in the shopping bag.
# Creating an order line item for each one. Then attaching it to the order.


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems')
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE)
    product_size = models.CharField(
        max_length=4, null=True, blank=True)  # 2kg, 3kg, 4kg, 5kg, 6kg
    quantity = models.IntegerField(
        null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """ Override the original save method to set the order number
        if it hasn't been set already """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

# returning just the order number for the order model.
# And the SKU of the product along with the order number
# it's part of for each order line item

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'
