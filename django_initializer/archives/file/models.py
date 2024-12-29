from django.db import models


# Create your models here.
class File(models.Model):
    # file content
    file_content = models.FileField(verbose_name='파일')
    # 파일 이름
    file_name = models.CharField(max_length=100, verbose_name='이름')
    # 파일 설명
    file_desc = models.TextField(null=True, blank=True, verbose_name='설명')
    # 파일 확장자
    file_ext = models.CharField(max_length=10, null=True, verbose_name='확장자')
    # 파일 용량
    file_size = models.IntegerField(verbose_name='용량')
    # 문서 업로드 시간
    file_upload_datetime = models.DateTimeField(verbose_name='업로드 시간')
    # 문서 생성 시간
    file_creation_date = models.DateField(null=True, blank=True, verbose_name='파일 생성 시간')

