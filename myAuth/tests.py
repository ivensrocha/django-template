# coding: utf-8
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from int.myAuth.forms import UserCreationCustomForm, AuthenticationCustomForm
import datetime
                
class TestUser(TestCase):
    
    def setUp(self):
        self.client = Client()

        self.user_password = '1'
        self.user_email = 'test@test.com'
        self.user = User.objects.create_user('123456789101', self.user_email, self.user_password)        
        
    def test_if_user_exists(self):        
        user = User.objects.get(email=self.user_email, password=self.user.password)
        self.assertIsInstance(user, User)
    
    def test_if_user_is_active(self):        
        user = User.objects.get(email=self.user_email, password=self.user.password)
        self.assertTrue(user.is_active)
                
    def test_if_authentication_works(self):
        response = self.client.login(email=self.user_email, password=self.user_password)
        self.assertTrue(response)
    
    def test_form_AuthencationCustomForm_logs_the_user_on(self):
        response = self.client.post(reverse('myAuth:login'), {'email': self.user_email, 
                                                            'password': self.user_password})
        self.assertRedirects(response, '/')
        
    def test_form_AuthenticationCustomForm_raises_error_if_email_is_empty(self):
        fields = {
            'email': '',
            'password': self.user_password,
            }
        
        form = AuthenticationCustomForm(data=fields)
        self.assertFalse(form.is_valid())
        
    def test_form_AuthenticationCustomForm_raises_error_if_password_is_empty(self):
        fields = {
            'email': self.user_email,
            'password': '',
            }
        
        form = AuthenticationCustomForm(data=fields)
        self.assertFalse(form.is_valid())        
        
    def test_form_AuthenticationCustomForm_raises_error_if_identification_fails(self):
        fields = {
            'email': self.user_email,
            'password': self.user_password + "abc",
            }
        
        form = AuthenticationCustomForm(data=fields)
        self.assertFalse(form.is_valid())  
                
    def test_form_AuthenticationCustomForm_raises_error_if_email_has_not_at_sign(self):
        fields = {
            'email': 'a.com',
            'password': self.user_password,
            }
        
        form = AuthenticationCustomForm(data=fields)
        self.assertFalse(form.is_valid())    
        
    def test_form_AuthenticationCustomForm_raises_error_if_email_has_not_full_domain(self):        
        fields = {
            'email': 'a@com',
            'password': self.user_password,
            }
        
        form = AuthenticationCustomForm(data=fields)
        self.assertFalse(form.is_valid())

    def test_form_AuthenticationCustomForm_raises_error_if_email_has_accentuation(self):          
        fields = {
            'email': 'áé@a.com',
            'password': self.user_password,
            }
        
        form = AuthenticationCustomForm(data=fields)
        self.assertFalse(form.is_valid())         
        
    def test_confirm_account_true_if_code_exists(self):
        code = self.user.username
        response = self.client.get(reverse('myAuth:confirm_account', args=[code]))

        self.assertTrue(response.context['result'])
                
    def test_confirm_account_2_if_code_does_not_exists(self):
        code = "a06737965e66d701cab878193348b5"
        response = self.client.get(reverse('myAuth:confirm_account', args=[code]))

        self.assertEquals(response.context['result'], 2)

    def test_confirm_account_3_if_code_has_expired(self):
        code = self.user.username
        profile = self.user.get_profile()
        
        profile.confirmation_code_expiration_datetime = datetime.datetime.now() + datetime.timedelta(days=-1)
        profile.save()
        
        response = self.client.get(reverse('myAuth:confirm_account', args=[code]))
        self.assertEquals(response.context['result'], 3)
                    
    def test_send_confirmation_code(self):
        code = self.user.username
        response = self.client.get(reverse('myAuth:send_confirmation_code', args=[code]))
        self.assertEqual(response.status_code, 200)          

    def test_template_used_page_send_confirmation_code(self):
        code = self.user.username        
        response = self.client.get(reverse('myAuth:send_confirmation_code', args=[code]))
        self.assertTemplateUsed(response, 'myAuth/send_confirmation_code.html')
        
    def test_user_has_profile(self):
        from django.core.exceptions import ObjectDoesNotExist 
        try:
            self.user.get_profile()
        except ObjectDoesNotExist:
            raise AssertionError("Usuário não tem perfil")
        
    def test_inactive_user_can_not_login(self):
        self.user.is_active = False
        self.user.save()
        
        response = self.client.login(email=self.user_email, password=self.user_password)
        self.assertFalse(response)
    
    
class TestAccountConfirmation(TestCase):
    
    def setUp(self):
        pass
    
       
class TestUserCreation(TestCase):

    def setUp(self):
        self.client = Client()

    def test_form_UserCreationCustomForm_if_fields_email_password1_and_password2_exists(self):
        form = UserCreationCustomForm()
        fields = form.fields.keyOrder
        
        # garante que tem email e senhas
        self.assertTrue("email" in fields)
        self.assertTrue("fullname" in fields)
        self.assertTrue("password1" in fields)
        self.assertTrue("password2" in fields)        
          
    def test_form_UserCreationCustomForm_if_email_is_first_field_on_the_form(self):
        form = UserCreationCustomForm()
        fields = form.fields.keyOrder
        self.assertEqual(fields[0], "email", "Email deve ser o primeiro campo do formulário")
        
    def test_form_UserCreationCustomForm_if_password2_is_after_password1(self):
        form = UserCreationCustomForm()
        fields = form.fields.keyOrder
        self.assertGreater(fields.index('password2'), fields.index('password1'), 
                           "Campo de confirmação de senha deve vir após o campo de senha")     
        
    def test_form_UserCreationCustomForm_if_username_is_generated_properly(self):
        fields = {
                  'fullname':'John Doe',
                  'email': 'john@doe.com',
                  'password1':'1',
                  'password2':'1'
                  }

        form = UserCreationCustomForm(data=fields)
        form.full_clean()
        from utils.generate_username import generate_username
        username = generate_username(fields['email'])
        
        self.assertEqual(username, form.cleaned_data.get('username'))
        
    def test_form_UserCreationCustomForm_raises_error_if_passwords_does_not_match(self):
        fields = {
                  'fullname':'John Doe',
                  'email': 'john@doe.com',
                  'password1':'1',
                  'password2':'2'
                  }
        form = UserCreationCustomForm(fields)
        self.assertFalse(form.is_valid())

    def test_form_UserCreationCustomForm_in_page_create_account(self):
        fullname = "John Doe"
        email = 'teste2@visionetecnologia.com.br'
        password = '1'
        
        response = self.client.post(reverse('myAuth:create_account'), {
                                                                     'email': email, 'fullname': fullname, 
                                                                     'password1': password, 'password2': password
                                                                     }
                                    )    
        self.assertEqual(response.status_code, 302, "Formulário com erros")
        
        user = User.objects.get(email=email)
        self.assertIsInstance(user, User)
        
        expected_url = reverse('myAuth:create_account_success', args=[str(user.pk)]) 
        self.assertRedirects(response, expected_url)        
        
    def test_if_firstname_and_lastname_were_splitted_correctly(self):
        fields = {
                  'fullname':'Pedro Oliveira Rocha',
                  'email': 'pedro@oliveira.com',
                  'password1':'1',
                  'password2':'1'
                  }
        
        form = UserCreationCustomForm(data=fields)
        form.full_clean()

        self.assertEquals(form.cleaned_data.get('first_name'), "Pedro")
        self.assertEquals(form.cleaned_data.get('last_name'), "Oliveira Rocha")
    
    def test_form_UserCreationCustomForm_raises_error_if_fullname_is_empty(self):          
        fields = {
            'email': 'pedro@oliveira.com',
            'password1': '1',
            'password2': '1',
            'fullname': '',
            }
        
        form = UserCreationCustomForm(data=fields)
        self.assertFalse(form.is_valid())     
        
    def test_form_UserCreationCustomForm_raises_error_if_fullname_has_only_one_part_of_the_name(self):          
        fields = {
            'email': 'pedro@oliveira.com',
            'password1': '1',
            'password2': '1',
            'fullname': 'João ',
            }
        
        form = UserCreationCustomForm(data=fields)
        self.assertFalse(form.is_valid(), form.errors)
                
    def test_form_UserCreationCustomForm_raises_error_if_email_has_not_at_sign(self):
        fields = {
            'email': 'pedrooliveira.com',
            'password1': '1',
            'password2': '1',
            'fullname': 'Pedro Alcântara',
            }
        
        form = UserCreationCustomForm(data=fields)
        self.assertFalse(form.is_valid())    
        
    def test_form_UserCreationCustomForm_raises_error_if_email_has_not_full_domain(self):
        fields = {        
            'email': 'pedro@com',
            'password1': '1',
            'password2': '1',
           'fullname': 'Pedro Alcântara',
           }
        
        form = UserCreationCustomForm(data=fields)
        self.assertFalse(form.is_valid())

    def test_form_UserCreationCustomForm_raises_error_if_email_has_accentuation(self):
        fields = {          
            'email': 'pedro.alcântara@oliveira.com',
            'password1': '1',
            'password2': '1',
            'fullname': 'Pedro Alcântara',
            }
        
        form = UserCreationCustomForm(data=fields)
        self.assertFalse(form.is_valid())    
                    
    def test_new_user_is_created_as_inactive(self):
        fields = {        
            'email': 'ivens@teste.com',
            'password1': '1',
            'password2': '1',
           'fullname': 'Ivens Teste',
           }
        
        form = UserCreationCustomForm(data=fields)    
        form.save()    
        
        user = User.objects.get(email=fields['email'])
        self.assertFalse(user.is_active)                    
                    
class TestPages(TestCase):
    
    def test_page_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_template_used_page_index(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'index.html')        
        
    def test_page_login(self):
        response = self.client.get(reverse('myAuth:login'))
        self.assertEqual(response.status_code, 200)
        
    def test_context_exists_page_login(self):
        response = self.client.get(reverse('myAuth:login'))
        self.assertTrue('form' in response.context)
        
    def test_template_used_page_login(self):
        response = self.client.get(reverse('myAuth:login'))
        self.assertTemplateUsed(response, 'myAuth/login.html')        
        
    def test_page_logout(self):
        response = self.client.get(reverse('myAuth:logout'))
        self.assertRedirects(response, '/')            
        
    def test_page_cadastrar(self):
        response = self.client.get(reverse('myAuth:create_account'))
        self.assertEqual(response.status_code, 200)
    
    def test_context_exists_page_cadastrar(self):
        response = self.client.get(reverse('myAuth:create_account'))
        self.assertTrue('form' in response.context)
                
    def test_template_used_page_cadastrar(self):
        response = self.client.get(reverse('myAuth:create_account'))
        self.assertTemplateUsed(response, 'myAuth/create_account.html')      
        
    def test_page_confirm_account(self):
        response = self.client.get(reverse('myAuth:confirm_account', args=["myRandomConfirmationCode"]))
        self.assertEqual(response.status_code, 200)  
        
    def test_template_used_page_confirm_account(self):
        response = self.client.get(reverse('myAuth:confirm_account', args=["myRandomConfirmationCode"]))
        self.assertTemplateUsed(response, 'myAuth/confirm_account.html')
        
    def test_context_exists_page_confirm_account(self):
        response = self.client.get(reverse('myAuth:confirm_account', args=["myRandomConfirmationCode"]))
        self.assertTrue('result' in response.context) 