from django.contrib import admin
from .models import *

admin.site.register(User)

admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Product)
admin.site.register(ProductMedia)

admin.site.register(Review)
admin.site.register(ReviewMedia)

admin.site.register(SurveyResult)

admin.site.register(Magazine)
admin.site.register(MagazineContent)

admin.site.register(Brand)
