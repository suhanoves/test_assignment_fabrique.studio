from rest_framework import serializers

from polls.models import Poll, Choice, Question


class ChoiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'choice_text')


class QuestionListSerializer(serializers.ModelSerializer):
    choices = ChoiceListSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Question
        fields = ('id', 'question_type', 'question_text', 'choices')


class PollDetailSerializer(serializers.ModelSerializer):
    questions = QuestionListSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Poll
        fields = ('id', 'title', 'description',
                  'pub_date', 'expiry_date', 'questions')


class PollListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('id', 'title', 'description', 'pub_date', 'expiry_date')
