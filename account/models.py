from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):  # <-- 상속 부분
    phone_number = models.CharField(max_length=11, verbose_name='전화번호')  # 전화번호(char)
    career = models.IntegerField(default=0, verbose_name='경력')  # 경력 (int)
    rank = models.CharField(max_length=10, verbose_name='직급')  # 직급 (select)
    date_company_joined = models.DateField(verbose_name='입사 날짜')  # 입사 기간
    # TODO: 암호화 처리 필요, 암호화 처리 방안 적용까지 null 값 처리
    personal_id = models.CharField(max_length=13, verbose_name='주민등록번호', null=True)  # 주민등록번호
    company_id = models.CharField(max_length=13, verbose_name='회사고유번호')  # 입사 번호
    DEPARTMENT_CHOICES = [('DEV', '개발부'), ('P&E', '기획&교육팀'), ('BIS', '경영지원부')]
    department = models.CharField(max_length=13, choices=DEPARTMENT_CHOICES, verbose_name='부서')  # 부서
    resume = models.FileField(blank=True, null=True, verbose_name='이력서')  # 이력서
    id_photo = models.ImageField(blank=True, null=True, upload_to='', verbose_name='사진')  # 증명사진
    region = models.CharField(max_length=100, verbose_name='주소')  # 주소

    def __str__(self):
        return self.username


CustomUser._meta.get_field('username').verbose_name = 'ID'
CustomUser._meta.get_field('first_name').verbose_name = '성'
CustomUser._meta.get_field('last_name').verbose_name = '이름'
CustomUser._meta.get_field('email').verbose_name = '이메일'
