from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class Poll(models.Model):
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    pub_date = models.DateField('date published')
    expiry_date = models.DateField('expiration date')

    class Meta:
        verbose_name = 'poll'
        verbose_name_plural = 'polls'

        constraints = [
            models.CheckConstraint(
                check=models.Q(expiry_date__gt=models.F('pub_date')),
                name='expiry_date_gt_pub_date'
            )
        ]

    def __str__(self):
        return self.title


class Question(models.Model):
    TEXT = 'text'
    RADIO = 'radio'
    CHECKBOX = 'checkbox'
    QUESTION_TYPES_CHOICES = (
        (TEXT, 'text'),
        (RADIO, 'radio'),
        (CHECKBOX, 'checkbox')
    )

    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name='questions',
        related_query_name='question',
    )
    question_text = models.CharField(max_length=500)
    question_type = models.CharField(
        max_length=8,
        choices=QUESTION_TYPES_CHOICES,
        default=RADIO,
    )

    class Meta:
        verbose_name = 'question'
        verbose_name_plural = 'questions'
        ordering = ('pk', )

        constraints = [
            models.UniqueConstraint(
                fields=('poll', 'question_text', 'question_type'),
                name='unique_poll_question_question_type',
            ),
        ]

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices',
        related_query_name='choice',
    )
    choice_text = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = 'choice'
        verbose_name_plural = 'choices'
        ordering = ('pk', )

        constraints = [
            models.UniqueConstraint(
                fields=('question', 'choice_text'),
                name='unique_question_choice_text',
            ),
        ]

    def clean(self):
        super().clean()
        if self.question.question_type == Question.TEXT:
            raise ValidationError(
                'You cannot add Choice for text question'
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.question_id}. {self.choice_text}'


class Answer(models.Model):
    respondent = models.IntegerField(verbose_name='respondent_id')
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 related_name='answers',
                                 related_query_name='answer')
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE,
                               blank=True, null=True)
    choice_text = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        verbose_name = 'answer'
        verbose_name_plural = 'answers'

        constraints = [
            models.UniqueConstraint(
                fields=('respondent', 'question_id', 'choice'),
                name='unique_respondent_question_choice'
            ),
            models.UniqueConstraint(
                fields=('respondent', 'question_id', 'choice_text'),
                condition=Q(choice_text__isnull=False),
                name='unique_respondent_question_choice_text'
            ),
            models.CheckConstraint(
                check=(Q(choice__isnull=True, choice_text__isnull=False)
                       | Q(choice__isnull=False, choice_text__isnull=True)),
                name='choice_id_or_text_choice_required',
            )
        ]

    def clean(self):
        super().clean()
        question_type = self.question.question_type

        # check if get a Choice for text question
        if question_type == Question.TEXT and self.choice is not None:
            raise ValidationError(
                'For a text question the answer can only be plain text, '
                'not a Choice.'
            )

        # check if get a text for choice question
        if question_type != Question.TEXT and self.choice_text is not None:
            raise ValidationError(
                'For a choice question the answer can only be a Choice, '
                'not a plain text.'
            )

        # checking that the Choice belong to the Question
        if self.choice is not None and self.choice.question != self.question:
            raise ValidationError(
                'The Choice does not belong to the Question'
            )

        # check that the user has already answered this question
        if question_type in (Question.TEXT, Question.RADIO):
            answer = Answer.objects.filter(respondent=self.respondent,
                                           question=self.question)
            if answer.exists():
                raise ValidationError(
                    'You have already answered this question'
                )
        elif question_type == Question.CHECKBOX:
            answer = Answer.objects.filter(respondent=self.respondent,
                                           question=self.question,
                                           choice=self.choice)
            if answer.exists():
                raise ValidationError(
                    'We have already recorded this answer.'
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'answer to {self.question_id} from {self.respondent}'
