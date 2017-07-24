from django.test import TestCase
from django.contrib.auth.models import User

from Snack.models import Profil, Type, Product


class TestConnectLogout(TestCase):

    # Set up the database
    def setUp(self):
        self.user = User.objects.create(username='user', password='test')
        self.user.set_password('test')
        self.user.save()

    # Redirect to / if the form is not valid
    def test_connect_view_denies_anonymous(self):
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/', follow=True)
        self.assertRedirects(response, '/')

    # Redirect to /purchase/ if the connexion is a success
    def test_connect_success(self):
        response = self.client.post('/', {'username': 'user', 'password': 'test'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/purchase/')

    # Redirect to / if the connexion fail
    def test_connect_fail(self):
        response = self.client.post('/', {'username': 'user', 'password': 'false'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    # Redirect to /purchase/ if the user is already connected
    def test_connect_redirect(self):
        self.client.force_login(self.user)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/purchase/')

    # Redirect to / if the user is connected
    def test_logout_redirect(self):
        self.client.force_login(self.user)
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')


class TestSignUp(TestCase):

    def test_signup_method_get(self):
        response = self.client.get('/signup/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_signup_form_valid(self):
        response = self.client.post(
            '/signup/',
            {
                'username': 'user',
                'password': 'pass',
                'password_verif': 'pass',
                'last_name': 'last name',
                'first_name': 'first name',
                'card_number': ''
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/purchase/')

    def test_signup_form_invalid(self):
        response = self.client.post(
            '/signup/',
            {
                'username': 'user',
                'password': 'pass',
                'last_name': 'last name',
                'first_name': 'first name',
                'card_number': ''
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_signup_different_password(self):
        response = self.client.post(
            '/signup/',
            {
                'username': 'user',
                'password': 'pass',
                'password_verif': 'pass2',
                'last_name': 'last name',
                'first_name': 'first name',
                'card_number': ''
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_signup_card_number(self):
        response = self.client.post(
            '/signup/',
            {
                'username': 'user',
                'password': 'pass',
                'password_verif': 'pass',
                'last_name': 'last name',
                'first_name': 'first name',
                'card_number': 'e8e6e9e1'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/purchase/')


class TestPurchase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='user', password='test')
        self.user.set_password('test')
        self.user.save()
        self.profil = Profil(user=self.user)
        self.profil.save()
        self.client.force_login(self.user)

    def test_method_post(self):
        response = self.client.post(
            '/purchase/',
            {'products': '{"Twix":0, "Mars":1}'}
        )
        self.assertEqual(response.status_code, 200)

    def test_product_exists(self):
        self.type = Type(name="Barre")
        self.type.save()
        self.twix = Product(name="Twix", type=self.type, price=0.6, quantity=10)
        self.twix.save()
        self.mars = Product(name="Mars", type=self.type, price=0.6, quantity=10)
        self.mars.save()
        response = self.client.post(
            '/purchase/',
            {'products': '{"Twix":0, "Mars":1}'}
        )
        self.assertEqual(response.status_code, 200)

    def test_no_product(self):
        response = self.client.post(
            '/purchase/',
            {'products': '{}'}
        )
        self.assertEqual(response.status_code, 200)

    def test_range_product_invalid(self):
        self.type = Type(name="Barre")
        self.type.save()
        self.twix = Product(name="Twix", type=self.type, price=0.6, quantity=10)
        self.twix.save()
        response = self.client.post(
            '/purchase/',
            {'products': '{"Twix":-1}'}
        )
        self.assertEqual(response.status_code, 200)


class TestChangeTheme(TestCase):

    def test_ajax_request(self):
        self.user = User.objects.create(username='user', password='test')
        self.user.set_password('test')
        self.user.save()
        self.profil = Profil(user=self.user)
        self.profil.save()
        self.client.force_login(self.user)
        response = self.client.post(
            '/change_theme/',
            {'color': '"def"'}
        )
        self.assertEqual(response.status_code, 200)
