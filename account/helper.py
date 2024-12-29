from account.models import CustomUser


def createsuperuser():
    CustomUser.objects.create_superuser(username='admin',
                                        email='admin@admin.com',
                                        password='q1w2e3r4Q!W@E#R$',
                                        first_name='admin',
                                        last_name='admin',
                                        phone_number='01062766596',
                                        career=2,
                                        rank='manager',
                                        date_company_joined='2022-02-02',
                                        id_number='admin',
                                        department='관리부',
                                        region='서울').save()
    return 'Create Superuser : admin '


if __name__ == '__main__':
    createsuperuser()
