from django.db import models
class Project_wizard(models.Model):
	name = models.CharField(max_length=100)
	desc = models.TextField(null=True, blank=True)

	sidenavi = models.TextField(max_length=100)
	topnavi = models.TextField(max_length=100)

	# 계정 정보
	AUTH_CHOICE = [('sss', "세션"), ('TKN', "토큰")]
	authtype = models.CharField(max_length=3, null=True, blank=True, choices=AUTH_CHOICE)

	# 템플릿
	TMP_CHOICE = [('doc', "닥터리스")]
	template = models.CharField(max_length=3, null=True, blank=True, choices=TMP_CHOICE)
