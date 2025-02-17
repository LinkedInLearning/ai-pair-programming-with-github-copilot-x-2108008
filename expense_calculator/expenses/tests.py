# imports for django_rest_framework tests
from rest_framework.test import APITestCase

from .models import Expense
"""
class Expense(models.Model):

    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    # category choice field
    CATEGORY_CHOICES = (
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Entertainment', 'Entertainment'),
        ('Other', 'Other'),
    )
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f'{self.name} - {self.amount}'
"""

class ExpensesTestCase(APITestCase):
    def setUp(self):
        Expense.objects.bulk_create([
            Expense(name='Food', amount='10.00', category='Food'),
            Expense(name='Transport', amount='20.00', category='Transport'),
            Expense(name='Entertainment', amount='30.00', category='Entertainment'),
        ])
    
    def test_expenses_list(self):
        response = self.client.get('/api/expenses/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_expenses_detail(self):
        response = self.client.get('/api/expenses/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Food')
        self.assertEqual(response.json()['amount'], '10.00')
        self.assertEqual(response.json()['category'], 'Food')

    def test_expenses_create(self):
        response = self.client.post('/api/expenses/', {
            'name': 'Food',
            'amount': '10.00',
            'category': 'Food',
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['name'], 'Food')
        self.assertEqual(response.json()['amount'], '10.00')
        self.assertEqual(response.json()['category'], 'Food')
    
    def test_expenses_update(self):
        response = self.client.put('/api/expenses/1/', {
            'name': 'Food',
            'amount': '10.00',
            'category': 'Food',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'Food')
        self.assertEqual(response.json()['amount'], '10.00')
        self.assertEqual(response.json()['category'], 'Food')

    def test_expenses_delete(self):
        response = self.client.delete('/api/expenses/1/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(Expense.objects.all()), 2)
        self.assertRaises(Expense.DoesNotExist, Expense.objects.get, pk=1)
        response = self.client.get('/api/expenses/2/')
        self.assertEqual(response.status_code, 200)
        
    def tearDown(self):
        Expense.objects.all().delete()
