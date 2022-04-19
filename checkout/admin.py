from django.contrib import admin
from .models import Order, OrderLineItem


# This inline item is going to allow us
# to add and edit line items in the admin
# right from inside the order model.
class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)
    readonly_fields = ('order_number',
                       'date',
                       'delivery_cost',
                       'order_total',
                       'grand_total',
                       )
    # active fields in admin site
    fields = ('order_number', 'date', 'full_name',
              'email', 'phone_number', 'country',
              'postcode', 'town_or_city', 'street_address1',
              'street_address2', 'county', 'delivery_cost',
              'order_total', 'grand_total',)

    # list to be displayed in admin site
    list_display = ('order_number', 'date', 'full_name',
                    'order_total', 'delivery_cost',
                    'grand_total',)

    ordering = ('-date',)

# register the Order model and the OrderAdmin.
admin.site.register(Order, OrderAdmin)