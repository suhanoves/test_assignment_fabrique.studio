from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone

from polls.models import Poll, Question, Choice, Answer


class AnswerTest(TestCase):
    def setUp(self):
        today = timezone.now().date()

        self.poll = Poll.objects.create(
            title='Test poll',
            description='Test poll description',
            pub_date=today,
            expiry_date=today + timedelta(days=2)
        )

        self.text_question = Question.objects.create(
            poll=self.poll,
            question_text="How do you do?",
            question_type=Question.TEXT,
        )

        self.choice_question = Question.objects.create(
            poll=self.poll,
            question_text="What's up bro?",
            question_type=Question.RADIO,
        )

        self.choice1 = Choice.objects.create(
            question=self.choice_question,
            choice_text="I'm fine"
        )

        self.choice2 = Choice.objects.create(
            question=self.choice_question,
            choice_text="So-so"
        )

    def test_create_valid_text_answer(self):
        Answer.objects.create(
            respondent=1,
            question=self.text_question,
            choice_text='Not bad',
        )

        answer = Answer.objects.last()

        self.assertEqual(answer.question, self.text_question)
        self.assertIsNone(answer.choice)
        self.assertEqual(answer.choice_text, "Not bad")

    def test_create_invalid_text_answer_without_text(self):
        with self.assertRaises(IntegrityError):
            Answer.objects.create(
                respondent=1,
                question=self.text_question,
            )

    def test_create_invalid_text_answer_with_choice_and_text(self):
        with self.assertRaises(ValidationError):
            Answer.objects.create(
                respondent=1,
                question=self.text_question,
                choice=self.choice1,
                choice_text='Not bad',
            )

    def test_create_invalid_text_answer_with_only_choice(self):
        with self.assertRaises(ValidationError):
            Answer.objects.create(
                respondent=1,
                question=self.text_question,
                choice=self.choice1,
            )

    def test_create_valid_radio_answer(self):
        Answer.objects.create(
            respondent=1,
            question=self.choice_question,
            choice=self.choice1,
            choice_text=None,
        )

        answer = Answer.objects.last()

        self.assertEqual(
            answer.choice.question.question_text,
            "What's up bro?"
        )

        self.assertEqual(answer.question, self.choice_question)
        self.assertEqual(answer.choice, self.choice1)
        self.assertIsNone(answer.choice_text)

    def test_create_invalid_choice_answer_without_choice(self):
        with self.assertRaises(IntegrityError):
            Answer.objects.create(
                respondent=1,
                question=self.choice_question,
            )

    def test_create_invalid_choice_answer_with_choice_and_text(self):
        with self.assertRaises(ValidationError):
            Answer.objects.create(
                respondent=1,
                question=self.choice_question,
                choice=self.choice1,
                choice_text='Not bad',
            )

    def test_create_invalid_choice_answer_with_only_text(self):
        with self.assertRaises(ValidationError):
            Answer.objects.create(
                respondent=1,
                question=self.choice_question,
                choice_text='Not bad',
            )
