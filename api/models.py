from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, nickname, password=None):
        if not email:
            raise ValueError('User must have email')
        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password):
        user = self.create_user(
            email=self.normalize_email(email),
            nickname=nickname,
            password=password
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    objects = UserManager()

    GENDER_CHOICE = [
        ('Female', 'Female'),
        ('Male', 'Male'),
    ]

    name = models.CharField(max_length=20)
    email = models.CharField(max_length=200, unique=True)
    nickname = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICE)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']


class Magazine(models.Model):

    MAGAZINE_CHOICE = [
        ('Founder Story', 'Founder Story'),
        ('Daily Curation', 'Daily Curation'),
    ]

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=20)
    tag_arr = models.TextField(null=True)
    created_at = models.DateTimeField()
    episode_num = models.IntegerField(null=True)
    main_img = models.URLField()
    magazine_type = models.CharField(max_length=20, choices=MAGAZINE_CHOICE)
    intro_title = models.TextField()
    intro_content = models.TextField()


class MagazineContent(models.Model):
    magazine = models.ForeignKey(Magazine, on_delete=models.CASCADE, related_name='magazine_magazinecontent')

    detail_title = models.CharField(max_length=100, null=True)
    detail_content = models.TextField(null=True)
    detail_img = models.URLField(null=True)


class Brand(models.Model):
    magazine_content = models.ForeignKey(MagazineContent, null=True, blank=True, on_delete=models.SET_NULL, related_name='magazinecontent_brand')

    brand_name = models.CharField(max_length=20)
    brand_logo = models.URLField()
    brand_link = models.URLField()
    brand_desc = models.TextField()
    brand_bg_img = models.URLField()


class Category(models.Model):

    CATEGORY_CHOICE = [
        ('Food', 'Food'),
        ('Beverage', 'Beverage'),
        ('Goods', 'Goods'),
        ('Health', 'Health'),
    ]
    category_name = models.CharField(max_length=20, choices=CATEGORY_CHOICE)


class Type(models.Model):

    TYPE_CHOICE = [
        ('Milk', 'Milk'),
        ('Shake', 'Shake'),
        ('Yogurt', 'Yogurt'),
        ('Salad', 'Salad'),
        ('FriedRice', 'FriedRice'),
        ('Cereal', 'Cereal'),
        ('Bread', 'Bread'),
        ('Chicken', 'Chicken'),
        ('CoffeeCold', 'CoffeeCold'),
        ('CoffeeMix', 'CoffeeMix'),
        ('CoffeeBeans', 'CoffeeBeans'),
        ('CoffeeCapsule', 'CoffeeCapsule'),
        ('Tea', 'Tea'),
        ('ShampooBar', 'ShampooBar'),
        ('Pad', 'Pad'),
        ('Soap', 'Soap'),
        ('Teeth', 'Teeth'),
        ('Pack', 'Pack'),
        ('Cotton', 'Cotton'),
        ('Lens', 'Lens'),
        ('Shaver', 'Shaver'),
        ('Lacto', 'Lacto'),
        ('Supplement', 'Supplement'),
        ('CarePack', 'CarePack'),
        ('Protein', 'Protein'),
        ('Collagen', 'Collagen'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_type')

    type_name = models.CharField(max_length=20, choices=TYPE_CHOICE)
    type_desc = models.CharField(max_length=100)
    type_tag_arr = models.TextField()
    order = models.IntegerField()


class Product(models.Model):

    DELIVERY_CHOICE = [
        ('Weekly', 'Weekly'),
        ('Monthly', 'Monthly'),
        ('Weekly/Monthly', 'Weekly/Monthly')
    ]

    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='type_product')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_product')

    product_name = models.CharField(max_length=20)
    product_main_img = models.URLField()
    custom_flag = models.BooleanField(default=False)
    delivery_cycle_main = models.CharField(max_length=20, choices=DELIVERY_CHOICE)
    delivery_cycle_detail = models.TextField()
    min_price = models.IntegerField()
    max_price = models.IntegerField()
    star_rate_avg = models.FloatField(default=0.0)
    volume = models.IntegerField()
    pcs = models.IntegerField()
    std_price = models.FloatField()
    discount_flag = models.BooleanField()
    purchase_link = models.URLField()
    main_product_flag = models.BooleanField()
    default_rec_flag = models.BooleanField()


class ProductMedia(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_productmedia')

    product_img = models.URLField()
    img_num = models.IntegerField()


class Review(models.Model):

    RATE_CHOICE = [
        (5, 5),
        (4, 4),
        (3, 3),
        (2, 2),
        (1, 1),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_review')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_review')

    star_rate = models.IntegerField(choices=RATE_CHOICE)
    review_text = models.TextField()
    review_tag_arr = models.TextField()
    review_main_img = models.URLField(null=True)
    created_at = models.DateTimeField()


class ReviewMedia(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_reviewmedia')

    review_img = models.URLField(null=True)
    img_num = models.IntegerField(null=True)


class SurveyResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_surveyresult')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='type_surveyresult')

    rec_result = models.BooleanField(null=True, default=False)

class Survey(models.Model):
    question_num = models.IntegerField()
    answer_num = models.IntegerField()
    type_arr = models.TextField()