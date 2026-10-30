import json
from datetime import datetime, time, timedelta

from companies.models import Company
from contacts.models import Contact
from deals.models import Deal
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from tasks.models import Task


class CRMTestCase(TestCase):
   

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='sales', password='pass12345')
        cls.company = Company.objects.create(name='Acme', industry='Software', city='Haifa')
        cls.contact = Contact.objects.create(
            company=cls.company,
            name='Dana Levi',
            job_title='CTO',
            email='dana@acme.com',
            phone='050-1234567',
        )
        cls.deal = Deal.objects.create(
            title='Acme licenses',
            company=cls.company,
            contact=cls.contact,
            value=1000,
        )

    def setUp(self):
        self.client.force_login(self.user)

    @staticmethod
    def at_noon(day):
        return timezone.make_aware(datetime.combine(day, time(12, 0)))


class AuthenticationTests(CRMTestCase):
    def setUp(self):
        pass

    def test_pages_require_login(self):
        for name in ['dashboard_home', 'company_list', 'contact_list', 'deal_list', 'task_list']:
            url = reverse(name)
            response = self.client.get(url)
            self.assertRedirects(
                response,
                f'{reverse("login")}?next={url}',
                fetch_redirect_response=False,
            )

    def test_login_with_valid_credentials_redirects_to_dashboard(self):
        response = self.client.post(
            reverse('login'), {'username': 'sales', 'password': 'pass12345'}
        )
        self.assertRedirects(response, reverse('dashboard_home'))

    def test_login_with_wrong_password_shows_error(self):
        response = self.client.post(reverse('login'), {'username': 'sales', 'password': 'wrong'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password.')
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_logout_requires_post(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse('logout')).status_code, 405)

        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
        self.assertNotIn('_auth_user_id', self.client.session)


class CreateUserTests(CRMTestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='admin12345')

    def test_regular_user_cannot_open_create_user_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('create_user'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('login')))

    def test_superuser_creates_user(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse('create_user'),
            {'username': 'newbie', 'password': 'secret123', 'confirm_password': 'secret123'},
        )
        self.assertRedirects(response, reverse('create_user'))
        self.assertTrue(User.objects.filter(username='newbie').exists())

    def test_mismatched_passwords_do_not_create_user(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse('create_user'),
            {'username': 'newbie', 'password': 'secret123', 'confirm_password': 'other'},
        )
        self.assertContains(response, 'Passwords do not match.')
        self.assertFalse(User.objects.filter(username='newbie').exists())

    def test_duplicate_username_is_rejected(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse('create_user'),
            {'username': 'sales', 'password': 'secret123', 'confirm_password': 'secret123'},
        )
        self.assertContains(response, 'This username already exists.')


class CompanyTests(CRMTestCase):
    def test_create_company(self):
        response = self.client.post(reverse('addcompany'), {'name': 'Globex', 'industry': 'Retail'})
        self.assertRedirects(response, reverse('company_list'))
        self.assertTrue(Company.objects.filter(name='Globex').exists())

    def test_create_company_without_required_fields_shows_form_again(self):
        response = self.client.post(reverse('addcompany'), {'name': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(Company.objects.count(), 1)

    def test_edit_company(self):
        response = self.client.post(
            reverse('company_edit', args=[self.company.id]),
            {'name': 'Acme Ltd', 'industry': 'Software'},
        )
        self.assertRedirects(response, reverse('company_list'))
        self.company.refresh_from_db()
        self.assertEqual(self.company.name, 'Acme Ltd')

    def test_delete_company(self):
        company = Company.objects.create(name='Temp', industry='Other')
        response = self.client.post(reverse('company_delete', args=[company.id]))
        self.assertRedirects(response, reverse('company_list'))
        self.assertFalse(Company.objects.filter(id=company.id).exists())

    def test_search_filters_companies(self):
        Company.objects.create(name='Globex', industry='Retail')
        response = self.client.get(reverse('company_list'), {'q': 'glob'})
        names = [company.name for company in response.context['companies']]
        self.assertEqual(names, ['Globex'])

    def test_detail_shows_open_and_won_values(self):
        Deal.objects.create(title='Won deal', company=self.company, value=500, stage='won')
        Deal.objects.create(title='Lost deal', company=self.company, value=300, stage='lost')

        response = self.client.get(reverse('company_detail', args=[self.company.id]))

        self.assertEqual(response.context['open_deals_count'], 1)
        self.assertEqual(response.context['open_deals_value'], 1000)
        self.assertEqual(response.context['won_deals_value'], 500)

    def test_detail_of_missing_company_returns_404(self):
        response = self.client.get(reverse('company_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)


class ContactTests(CRMTestCase):
    def test_create_contact(self):
        response = self.client.post(
            reverse('contact_create'),
            {
                'company': self.company.id,
                'name': 'Yossi Cohen',
                'job_title': 'Buyer',
                'email': 'yossi@acme.com',
                'phone': '052-7654321',
            },
        )
        self.assertRedirects(response, reverse('contact_list'))
        self.assertTrue(Contact.objects.filter(name='Yossi Cohen', company=self.company).exists())

    def test_create_contact_with_invalid_email_fails(self):
        response = self.client.post(
            reverse('contact_create'),
            {
                'company': self.company.id,
                'name': 'Bad Email',
                'job_title': 'Buyer',
                'email': 'not-an-email',
                'phone': '1',
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('email', response.context['form'].errors)

    def test_search_by_company_name(self):
        other = Company.objects.create(name='Globex', industry='Retail')
        Contact.objects.create(
            company=other, name='Other Person', job_title='CEO', email='o@globex.com', phone='1'
        )
        response = self.client.get(reverse('contact_list'), {'q': 'acme'})
        names = [contact.name for contact in response.context['contacts']]
        self.assertEqual(names, ['Dana Levi'])

    def test_delete_contact(self):
        response = self.client.post(reverse('contact_delete', args=[self.contact.id]))
        self.assertRedirects(response, reverse('contact_list'))
        self.assertFalse(Contact.objects.filter(id=self.contact.id).exists())

    def test_detail_shows_deals_and_tasks(self):
        Task.objects.create(title='Call Dana', contact=self.contact)
        Task.objects.create(title='Old call', contact=self.contact, is_completed=True)

        response = self.client.get(reverse('contact_detail', args=[self.contact.id]))

        self.assertEqual(response.context['open_deals_count'], 1)
        self.assertEqual(response.context['open_tasks_count'], 1)
        self.assertEqual(response.context['completed_tasks_count'], 1)


class DealTests(CRMTestCase):
    def deal_data(self, **overrides):
        data = {
            'title': 'New deal',
            'company': self.company.id,
            'contact': self.contact.id,
            'value': 2500,
            'stage': 'new',
        }
        data.update(overrides)
        return data

    def test_create_deal(self):
        response = self.client.post(reverse('deal_create'), self.deal_data())
        self.assertRedirects(response, reverse('deal_list'))
        self.assertTrue(Deal.objects.filter(title='New deal', contact=self.contact).exists())

    def test_contact_must_belong_to_selected_company(self):
        other = Company.objects.create(name='Globex', industry='Retail')
        response = self.client.post(reverse('deal_create'), self.deal_data(company=other.id))
        self.assertEqual(response.status_code, 200)
        self.assertIn('contact', response.context['form'].errors)
        self.assertFalse(Deal.objects.filter(title='New deal').exists())

    def test_edit_deal(self):
        response = self.client.post(
            reverse('deal_edit', args=[self.deal.id]),
            self.deal_data(title='Renamed', stage='proposal'),
        )
        self.assertRedirects(response, reverse('deal_list'))
        self.deal.refresh_from_db()
        self.assertEqual(self.deal.title, 'Renamed')
        self.assertEqual(self.deal.stage, 'proposal')

    def test_delete_deal(self):
        response = self.client.post(reverse('deal_delete', args=[self.deal.id]))
        self.assertRedirects(response, reverse('deal_list'))
        self.assertFalse(Deal.objects.filter(id=self.deal.id).exists())

    def test_kanban_has_a_column_per_stage(self):
        response = self.client.get(reverse('deal_list'))
        columns = {column['code']: column['count'] for column in response.context['columns']}
        self.assertEqual(list(columns), [code for code, _ in Deal.STAGE_CHOICES])
        self.assertEqual(columns['new'], 1)
        self.assertEqual(response.context['open_deals_count'], 1)

    def post_stage(self, body):
        return self.client.post(
            reverse('update_deal_stage', args=[self.deal.id]),
            data=body,
            content_type='application/json',
        )

    def test_update_stage(self):
        response = self.post_stage(json.dumps({'stage': 'won'}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['stage'], 'won')
        self.deal.refresh_from_db()
        self.assertEqual(self.deal.stage, 'won')

    def test_update_stage_rejects_unknown_stage(self):
        response = self.post_stage(json.dumps({'stage': 'maybe'}))
        self.assertEqual(response.status_code, 400)
        self.deal.refresh_from_db()
        self.assertEqual(self.deal.stage, 'new')

    def test_update_stage_rejects_invalid_json(self):
        response = self.post_stage('not json')
        self.assertEqual(response.status_code, 400)

    def test_update_stage_requires_post(self):
        response = self.client.get(reverse('update_deal_stage', args=[self.deal.id]))
        self.assertEqual(response.status_code, 405)


class TaskTests(CRMTestCase):
    def test_tasks_are_grouped_by_due_date(self):
        today = timezone.localdate()
        Task.objects.create(title='Overdue', due_date=self.at_noon(today - timedelta(days=1)))
        Task.objects.create(title='Today', due_date=self.at_noon(today))
        Task.objects.create(title='Upcoming', due_date=self.at_noon(today + timedelta(days=2)))
        Task.objects.create(title='Done', due_date=self.at_noon(today), is_completed=True)

        context = self.client.get(reverse('task_list')).context

        def titles(key):
            return [task.title for task in context[key]]

        self.assertEqual(titles('overdue_tasks'), ['Overdue'])
        self.assertEqual(titles('today_tasks'), ['Today'])
        self.assertEqual(titles('upcoming_tasks'), ['Upcoming'])
        self.assertEqual(titles('completed_tasks'), ['Done'])

    def test_create_task(self):
        response = self.client.post(
            reverse('task_create'), {'title': 'Send proposal', 'priority': 'high'}
        )
        self.assertRedirects(response, reverse('task_list'))
        self.assertTrue(Task.objects.filter(title='Send proposal', priority='high').exists())

    def test_create_task_from_deal_page(self):
        response = self.client.post(
            f'{reverse("task_create")}?deal={self.deal.id}',
            {'title': 'Follow up', 'priority': 'medium'},
        )
        self.assertRedirects(response, reverse('deal_detail', kwargs={'deal_id': self.deal.id}))
        self.assertEqual(Task.objects.get(title='Follow up').deal, self.deal)

    def test_complete_toggles_task(self):
        task = Task.objects.create(title='Call')
        url = reverse('task_complete', args=[task.id])

        self.client.post(url)
        task.refresh_from_db()
        self.assertTrue(task.is_completed)

        self.client.post(url)
        task.refresh_from_db()
        self.assertFalse(task.is_completed)

    def test_delete_task(self):
        task = Task.objects.create(title='Call')
        response = self.client.post(reverse('task_delete', args=[task.id]))
        self.assertRedirects(response, reverse('task_list'))
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_task_cannot_be_deleted_with_get(self):
        task = Task.objects.create(title='Call')
        response = self.client.get(reverse('task_delete', args=[task.id]))
        self.assertEqual(response.status_code, 405)
        self.assertTrue(Task.objects.filter(id=task.id).exists())


class DashboardTests(CRMTestCase):
    def test_dashboard_counts_and_deals_by_stage(self):
        Deal.objects.create(title='Big win', company=self.company, value=4000, stage='won')
        Task.objects.create(title='Next week', due_date=timezone.now() + timedelta(days=7))

        context = self.client.get(reverse('dashboard_home')).context

        self.assertEqual(context['companies_count'], 1)
        self.assertEqual(context['contacts_count'], 1)
        self.assertEqual(context['deals_count'], 2)
        self.assertEqual(context['tasks_count'], 1)
        by_stage = {row['stage']: row['total_value'] for row in context['deals_by_stage']}
        self.assertEqual(by_stage, {'new': 1000, 'won': 4000})
        self.assertEqual([task.title for task in context['upcoming_tasks']], ['Next week'])