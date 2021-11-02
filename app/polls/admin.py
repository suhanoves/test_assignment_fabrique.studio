from django.contrib import admin

from polls.models import Poll, Question, Choice, Answer


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 0


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'pub_date', 'expiry_date')
    inlines = (QuestionInline,)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('pub_date',)
        return self.readonly_fields


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'question_type', 'poll_id',)
    inlines = (ChoiceInline,)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('respondent', 'question', 'choice', 'choice_text')
    list_select_related = ('question', 'choice')


@admin.register(Choice)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'choice_text')
    list_select_related = ('question',)
    list_display_links = ('question',)
    list_editable = ('choice_text',)
