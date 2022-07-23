from django.contrib import admin
from .models import *

# admin 다중 이미지 등록
class ReviewMediaInline(admin.TabularInline):
    model = ReviewMedia


class ReviewAdmin(admin.ModelAdmin):
    inlines = (ReviewMediaInline,)


admin.site.register(Review, ReviewAdmin)


class MagazineContentInline(admin.TabularInline):
    model = MagazineContent


class MagazineAdmin(admin.ModelAdmin):
    inlines = (MagazineContentInline,)


admin.site.register(Magazine, MagazineAdmin)


admin.site.register(User)

admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Product)

admin.site.register(SurveyResult)
admin.site.register(Survey)

admin.site.register(Brand)
