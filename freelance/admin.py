from django.contrib import admin
from .models import Freelancer, Gig, Order

# admin.site.register(Freelancer)
# admin.site.register(Gig)
# admin.site.register(Order)

class GigInline(admin.TabularInline):
    model = Gig
    extra = 0

@admin.register(Freelancer)
class FreelancerAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'num_clients')
    search_fields = ('user__username', 'user__email')
    inlines = [GigInline]

    def num_clients(self, obj):
        return obj.clients.count()
    num_clients.short_description = 'Clients'

@admin.register(Gig)
class GigAdmin(admin.ModelAdmin):
    list_display = ('title', 'freelancer', 'price', 'created_at')
    search_fields = ('title', 'freelancer__user__username')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'gig', 'status', 'ordered_at')
    list_filter = ('status',)