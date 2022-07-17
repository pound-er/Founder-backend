from django.contrib import admin
from .models import *

# admin 다중 이미지 등록
class ReviewMediaInline(admin.TabularInline):
    model = ReviewMedia


class ReviewAdmin(admin.ModelAdmin):
    inlines = (ReviewMediaInline,)


admin.site.register(Review, ReviewAdmin)


admin.site.register(User)

admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Product)

admin.site.register(SurveyResult)
admin.site.register(Survey)

admin.site.register(Magazine)
admin.site.register(MagazineContent)

admin.site.register(Brand)
