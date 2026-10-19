from django.contrib import admin
from .models import Course, Lesson, Learner, Enrollment, Question, Choice, Submission


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "course", "grade")
    list_filter = ("course",)
    search_fields = ("question_text",)
    inlines = [ChoiceInline]


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    list_display = ("name", "pub_date")
    search_fields = ("name",)
    inlines = [LessonInline]


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("learner", "course", "total_score", "submitted_at")
    list_filter = ("course", "submitted_at")
    readonly_fields = ("submitted_at",)


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson)
admin.site.register(Learner)
admin.site.register(Enrollment)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission, SubmissionAdmin)
