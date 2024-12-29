from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from account.forms import CustomUserCreationForm, CustomUserProfileForm
from account.models import CustomUser
from helper import base_form_detail, h_tag, card_row
from standard import standard_detail, standard_create
from django.contrib.staticfiles import finders

base_layout = 'doctris'


# Create your views here.
@login_required(login_url='account:login')
def index(request):
    HttpResponse('Hello')


@csrf_exempt
def signup(request):
    def _callback(**kwargs):
        # parsing
        request = kwargs['request']
        form = kwargs['form']

        # POST & form 유효성 검사 통과시
        if request.method == 'POST' and form.is_valid():
            valid_inst = kwargs['valid_inst']
            id_photo = form.cleaned_data['id_photo']
            if id_photo:
                valid_inst.id_photo.save(id_photo.name, id_photo)
            else:
                alt_image_path = finders.find('account/not_image_found.jpg')
                with open(alt_image_path, 'rb') as alt_image:
                    valid_inst.id_photo.save('alt_image.jpg', ContentFile(alt_image.read()), save=False)

        # POST & form 유효성 실패시
        elif request.method == 'POST' and not form.is_valid():
            pass
        # GET
        elif request.method == 'GET':
            pass
        else:
            raise NotImplementedError

    return standard_create(request, 'account/doctris_signup.html', CustomUserCreationForm, None, 'login', {},
                           None,
                           _callback)


@login_required(login_url='account:login')
@csrf_exempt
def profile(request):
    def _callback(**kwargs):
        added_contents = kwargs['added_contents']
        project_title = h_tag(2, '유저 프로필')  # h2 tag 제목
        added_contents[0] = project_title + card_row(
            (added_contents[0], 12))  # added_contents 내 첫번째 요소 : detail_content

    user = CustomUser.objects.get(username=request.user)
    return standard_detail(request, user.id, 'account/profile.html', CustomUserProfileForm, None, base_form_detail,
                           None,
                           _callback)


@csrf_exempt
def createsuperuser(request):
    CustomUser.objects.create_superuser(username='admin',
                                        email='admin@admin.com',
                                        password='q1w2e3r4Q!W@E#R$',
                                        first_name='admin',
                                        last_name='admin',
                                        phone_number='01062766596',
                                        career=2,
                                        rank='manager',
                                        date_company_joined='2022-02-02',
                                        personal_id='admin',
                                        company_id='BIS',
                                        department='관리부',
                                        region='서울').save()
    return HttpResponse('Create Superuser : admin ')
