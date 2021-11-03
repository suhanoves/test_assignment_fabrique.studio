from django.contrib import admin
from nested_admin import nested

from polls.models import Poll, Question, Choice, Answer


class ChoiceInline(nested.NestedStackedInline):
    model = Choice
    extra = 0


class QuestionInline(nested.NestedStackedInline):
    model = Question
    extra = 0
    inlines = [ChoiceInline]


@admin.register(Poll)
class PollAdmin(nested.NestedModelAdmin):
    list_display = ('title', 'description', 'pub_date', 'expiry_date')
    inlines = (QuestionInline,)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('pub_date',)
        return self.readonly_fields


@admin.register(Answer)
class AnswerAdmin(nested.NestedModelAdmin):
    list_display = ('respondent', 'question', 'choice', 'choice_text')
    list_filter = ('respondent', 'question')
    list_select_related = ('question',)
    list_display_links = ('question',)
