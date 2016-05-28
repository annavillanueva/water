from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Question, Answer


class QuestionModelTest(TestCase):
    def test_string_representation(self):
        question = Question(title="When is the mother's day?")
        self.assertEqual(str(question), question.title)


class ProjectTests(TestCase):
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class HomePageTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='some_user')

    def test_one_question(self):
        title = 'Where is the best place to get ramen in Sydney CBD?'
        description = 'One for the foodies.'
        Question.objects.create(title=title, description=description)
        response = self.client.get('/')
        self.assertContains(response, title)
        self.assertContains(response, description)

    def test_two_questions(self):
        first_title = 'Where is the best place to get ramen in Sydney CBD?'
        first_description = 'One for the foodies.'
        second_title = 'Why is it important to manage your time?'
        second_description = 'Time management'
        Question.objects.create(title=first_title, description=first_description)
        Question.objects.create(title=second_title, description=second_description)
        response = self.client.get('/')
        self.assertContains(response, first_title)
        self.assertContains(response, first_description)
        self.assertContains(response, second_title)
        self.assertContains(response, second_description)


class QuestionViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='some_user')
        self.question = Question.objects.create(title='Android or iPhone?', description='Help a non-techy person out!')
        text = 'I am using Android now, but missing some iPhone features.'
        answer = Answer.objects.create(text=text, question=self.question)

    def test_basic_view(self):
        response = self.client.get(self.question.get_absolute_url())
        self.assertEqual(response.status_code, 200)
    
    def test_question_and_answer_relationship(self):
        number_of_answers = len(self.question.answers.all())
        self.assertEqual(number_of_answers, 1)


class AnswerModelTest(TestCase):
    def test_string_representation(self):
        text = 'I personally like Android.'
        answer = Answer(text=text)
        self.assertEqual(str(answer), text)
