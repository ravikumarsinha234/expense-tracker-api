from django.test import TestCase
from restapi import models
from django.urls import reverse

# from unittest import TestCase

# Create your tests here.


class TestModels(TestCase):
    def test_expense(self):
        expense = models.Expense.objects.create(
            amount=249.99,
            merchant="amazon",
            description="anc headphones",
            category="music",
        )
        inserted_expense = models.Expense.objects.get(pk=expense.id)

        self.assertEqual(249.99, inserted_expense.amount)
        self.assertEqual("amazon", inserted_expense.merchant)
        self.assertEqual("anc headphones", inserted_expense.description)
        self.assertEqual("music", inserted_expense.category)


class TestViews(TestCase):
    def test_expense_create(self):
        payload = {
            "amount": 50.0,
            "merchant": "AT&T",
            "description": "cell phone subscription",
            "category": "utlities",
        }

        res = self.client.post(
            reverse("restapi:expense-list-create"), payload, format="json"
        )

        self.assertEqual(201, res.status_code)

        json_res = res.json()

        self.assertEqual(payload["amount"], json_res["amount"])
        self.assertEqual(payload["merchant"], json_res["merchant"])
        self.assertEqual(payload["description"], json_res["description"])
        self.assertEqual(payload["category"], json_res["category"])
        self.assertIsInstance(json_res["id"], int)

    def test_expense_list(self):
        res = self.client.get(reverse("restapi:expense-list-create"), format="json")

        self.assertEqual(200, res.status_code)

        json_res = res.json()

        self.assertIsInstance(json_res, list)

        expenses = models.Expense.objects.all()
        self.assertEqual(len(expenses), len(json_res))

    def test_expense_create_required_fields_missing(self):
        payload = {
            "merchant": "AT&T",
            "description": "cell phone subscription",
            "category": "utlities",
        }
        res = self.client.post("restapi:expense-list-create", payload, format="json")

        self.assertEqual(404, res.status_code)

    def test_expense_retrieve(self):
        expense = models.Expense.objects.create(
            amount=300, merchant="George", description="loan", category="transfer"
        )
        res = self.client.get(
            reverse("restapi:expense-retrieve-delete", args=[expense.id]), format="json"
        )

        self.assertEqual(200, res.status_code)

        json_res = res.json()

        self.assertEqual(expense.id, json_res["id"])
        self.assertEqual(expense.amount, json_res["amount"])
        self.assertEqual(expense.merchant, json_res["merchant"])
        self.assertEqual(expense.description, json_res["description"])
        self.assertEqual(expense.category, json_res["category"])

    def test_expense_delete(self):
        expense = models.Expense.objects.create(
            amount=400, merchant="John", description="loan", category="transfer"
        )
        res = self.client.delete(
            reverse("restapi:expense-retrieve-delete", args=[expense.id]), format="json"
        )

        self.assertEqual(204, res.status_code)
        self.assertFalse(models.Expense.objects.filter(pk=expense.id).exists())
