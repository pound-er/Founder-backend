from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)


def type_path(instance, filename):
    return f'type/{instance.type_name}/{filename}'


def brand_path(instance, filename):
    return f'brand/{instance.brand_name}/{filename}'


def product_path(instance, filename):
    return f'product/{instance.product_name}/{filename}'


def review_path(instance, filename):
    return f'review/{instance.product.product_name}/{instance.user.email}/{filename}'


def review_media_path(instance, filename):
    return f'review-media/{instance.review.product.product_name}/{instance.review.user.email}/{filename}'


def magazine_path(instance, filename):
    return f'magazine/{instance.title}/{filename}'


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


class Category(models.Model):

    CATEGORY_CHOICE = [
        ('food', 'Food'),
        ('beverage', 'Beverage'),
        ('goods', 'Goods'),
        ('health', 'Health'),
    ]

    category_name = models.CharField(max_length=20, choices=CATEGORY_CHOICE)

    def __str__(self):
        return '[{}] {}'.format(self.id, self.category_name)


class Type(models.Model):

    TYPE_CHOICE = [
        ('yogurt', '그릭요거트'),
        ('salad', '샐러드'),
        ('fried-rice', '도시락/볶음밥'),
        ('cereal', '그래놀라(시리얼)'),
        ('bread', '빵'),
        ('chicken', '닭가슴살'),

        ('milk', '우유'),
        ('shake', '쉐이크'),
        ('tea', '차'),
        ('coffee-beans', '원두커피'),
        ('coffee-capsule', '캡슐커피'),
        ('coffee-cold', '원액커피'),

        ('pad', '생리용품'),
        ('teeth', '치아 관리'),
        ('pack', '스킨케어팩(팩)'),
        ('lens_cotton_collagen', '렌즈, 화장솜, 콜라겐'),
        ('shaver', '면도기'),

        ('lacto', '유산균'),
        ('supplement-pack', '개인 맞춤 케어 영양제 팩(영양제)'),
        ('protein', '프로틴'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_type')

    type_name = models.CharField(max_length=20, choices=TYPE_CHOICE)
    type_desc = models.CharField(max_length=100)
    type_desc_detail = models.CharField(max_length=100)
    type_tag_arr = models.TextField(null=True, blank=True)
    type_img_footer = models.FileField(upload_to=type_path)

    def __str__(self):
        return '[{}] {}'.format(self.id, self.type_name)


class Brand(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='type_brand')

    brand_name = models.CharField(max_length=20)
    brand_name_eng = models.CharField(max_length=20, null=True, blank=True)
    brand_img_logo = models.ImageField(upload_to=brand_path)
    brand_link = models.URLField()
    brand_desc = models.TextField()
    brand_img_bg = models.ImageField(upload_to=brand_path)
    curation = models.BooleanField(default=False)

    def __str__(self):
        return '[{}] {}'.format(self.id, self.brand_name)


class Product(models.Model):

    DELIVERY_CHOICE = [
        ('weekly', '주간'),
        ('monthly', '월간'),
        ('weekly/monthly', '주간/월간')
    ]

    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='type_product')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_product', null=True, blank=True)

    product_name = models.CharField(max_length=20)
    product_img = models.ImageField(upload_to=product_path)
    product_img_detail = models.ImageField(upload_to=product_path)
    custom_flag = models.BooleanField(default=False)
    discount_flag = models.BooleanField(default=False)
    delivery_cycle = models.CharField(max_length=20, choices=DELIVERY_CHOICE)
    delivery_cycle_detail = models.TextField(null=True, blank=True)
    min_price = models.IntegerField()
    min_std_price = models.FloatField(null=True, blank=True)
    max_std_price = models.FloatField(null=True, blank=True)
    star_rate_avg = models.FloatField(default=0.0)
    purchase_link = models.URLField()

    def __str__(self):
        return '[{}] {}'.format(self.id, self.product_name)


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
    review_tag_arr = models.TextField(null=True, blank=True)
    review_text = models.TextField(null=True, blank=True)
    review_img_main = models.ImageField(upload_to=review_path)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '[{}] {} - {}'.format(self.id, self.product.product_name, self.user.nickname)


class ReviewMedia(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_reviewmedia')

    review_img = models.ImageField(upload_to=review_media_path, blank=True)

    def __str__(self):
        return '[{}]'.format(self.id)


class Magazine(models.Model):

    MAGAZINE_CHOICE = [
        ('founder-story', 'founder-story'),
        ('daily-curation', 'daily-curation'),
    ]

    magazine_type = models.CharField(max_length=20, choices=MAGAZINE_CHOICE)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=20)
    tag_arr = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    episode_num = models.IntegerField(null=True, blank=True)
    img_main = models.ImageField(upload_to=magazine_path)
    img_header = models.ImageField(upload_to=magazine_path)
    intro = models.TextField()

    def __str__(self):
        return '{}. {}'.format(self.id, self.title)


class MagazineContent(models.Model):
    magazine = models.ForeignKey(Magazine, on_delete=models.CASCADE, related_name='magazine_magazinecontent')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='brand_magazinecontent', null=True, blank=True)

    detail_title = models.CharField(max_length=100, null=True, blank=True)
    detail_content = models.TextField(null=True, blank=True)
    detail_img = models.ImageField(upload_to=magazine_path, null=True, blank=True)

    def __str__(self):
        return '[{}]'.format(self.id)


class Survey(models.Model):
    question_num = models.IntegerField()
    answer_num = models.IntegerField()
    type_arr = models.TextField()

    def __str__(self):
        return '[Q{}] {} : {}'.format(self.question_num, self.answer_num, self.type_arr)


class SurveyResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_surveyresult')
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='type_surveyresult')

    rec_result = models.BooleanField(default=False)

    def __str__(self):
        return '[{}] ({}) {} : {}'.format(self.id, self.user.email, self.type.type_name, self.rec_result)

