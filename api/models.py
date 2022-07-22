from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)


def magazine_path(instance, filename):
    return f'magazine/{instance.title}/{filename}'


def brand_path(instance, filename):
    return f'brand/{instance.brand_name}/{filename}'


def product_path(instance, filename):
    return f'product/{instance.product_name}/{filename}'


def type_path(instance, filename):
    return f'type/{instance.type_name}/{filename}'


def review_path(instance, filename):
    return f'review/{instance.product.product_name}/{instance.user.email}/{filename}'


def review_media_path(instance, filename):
    return f'review-media/{instance.review.product.product_name}/{instance.review.user.email}/{filename}'


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
        ('female', 'female'),
        ('male', 'male'),
    ]

    nickname = models.CharField(max_length=20)
    email = models.CharField(max_length=200, unique=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICE)
    set_curation = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']


class Magazine(models.Model):

    MAGAZINE_CHOICE = [
        ('founder-story', 'founder-story'),
        ('daily-curation', 'daily-curation'),
    ]

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=20)
    tag_arr = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    episode_num = models.IntegerField(null=True, blank=True)
    main_img = models.ImageField(upload_to=magazine_path, null=True, blank=True)
    magazine_type = models.CharField(max_length=20, choices=MAGAZINE_CHOICE)
    intro_title = models.TextField()
    intro_content = models.TextField()


class MagazineContent(models.Model):
    magazine = models.ForeignKey(Magazine, on_delete=models.CASCADE, related_name='magazine_magazinecontent')

    detail_title = models.CharField(max_length=100, null=True, blank=True)
    detail_content = models.TextField(null=True, blank=True)
    detail_img = models.ImageField(upload_to=magazine_path, blank=True, null=True)


class Brand(models.Model):
    magazine_content = models.ForeignKey(MagazineContent, null=True, blank=True, on_delete=models.SET_NULL, related_name='magazinecontent_brand')

    brand_name = models.CharField(max_length=20)
    brand_logo = models.ImageField(upload_to=brand_path, null=True)
    brand_link = models.URLField()
    brand_desc = models.TextField()
    brand_bg_img = models.ImageField(upload_to=brand_path, null=True)


class Category(models.Model):

    CATEGORY_CHOICE = [
        ('food', 'food'),
        ('beverage', 'beverage'),
        ('goods', 'goods'),
        ('health', 'health'),
    ]
    category_name = models.CharField(max_length=20, choices=CATEGORY_CHOICE)

    def __str__(self):
        return '{}. {}'.format(self.id, self.category_name)


class Type(models.Model):

    TYPE_CHOICE = [
        ('milk', 'milk'),
        ('shake', 'shake'),
        ('yogurt', 'yogurt'),
        ('salad', 'salad'),
        ('fried-rice', 'fried-rice'),
        ('cereal', 'cereal'),
        ('bread', 'bread'),
        ('chicken', 'chicken'),
        ('coffee-cold', 'coffee-cold'),
        ('coffee-beans', 'coffee-beans'),
        ('coffee-capsule', 'coffee-capsule'),
        ('tea', 'tea'),
        ('pad', 'pad'),
        ('teeth', 'teeth'),
        ('pack', 'pack'),  # 팩
        ('cotton', 'cotton'),
        ('lens', 'lens'),
        ('shaver', 'shaver'),
        ('lacto', 'lacto'),
        ('supplement', 'supplement'),
        ('skin-care-pack', 'skin-care-pack'),  # 스킨케어 팩
        ('care-pack', 'care-pack'),  # 개인 맞춤 영양팩
        ('protein', 'protein'),
        ('collagen', 'collagen'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_type')

    type_name = models.CharField(max_length=20, choices=TYPE_CHOICE)
    type_desc = models.CharField(max_length=100)
    type_desc_detail = models.CharField(max_length=100)
    type_tag_arr = models.TextField()
    type_img = models.ImageField(upload_to=type_path)
    order = models.IntegerField()

    def __str__(self):
        return '{}. {}'.format(self.id, self.type_name)


class Product(models.Model):

    DELIVERY_CHOICE = [
        ('weekly', 'weekly'),
        ('monthly', 'monthly'),
        ('weekly/monthly', 'weekly/monthly')
    ]

    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='type_product')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_product')

    product_name = models.CharField(max_length=20)
    product_main_img = models.ImageField(upload_to=product_path, null=True)
    product_detail_img = models.ImageField(upload_to=product_path, null=True)
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


class Review(models.Model):

    RATE_CHOICE = [
        (5, 5),
        (4, 4),
        (3, 3),
        (2, 2),
        (1, 1),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_review', blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_review', blank=True)

    star_rate = models.IntegerField(choices=RATE_CHOICE)
    review_text = models.TextField()
    review_tag_arr = models.TextField()
    review_main_img = models.ImageField(upload_to=review_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ReviewMedia(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reviewMedia')

    review_img = models.ImageField(upload_to=review_media_path, blank=True, null=True)
    img_num = models.IntegerField(null=True)


class SurveyResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_surveyresult')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='type_surveyresult')

    rec_result = models.BooleanField(null=True, default=False)

    def __str__(self):
        return '{}. [ {} ] {} : {}'.format(self.id, self.user.email, self.type.type_name, self.rec_result)


class Survey(models.Model):
    question_num = models.IntegerField()
    answer_num = models.IntegerField()
    type_arr = models.TextField()

    def __str__(self):
        return 'Q{}. {} : {}'.format(self.question_num, self.answer_num, self.type_arr)