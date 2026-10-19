from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from .models import Course, Question, Choice, Submission


def course_list(request):
    courses = Course.objects.all().order_by("name")
    return render(request, "onlinecourse/course_list.html", {"course_list": courses})


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    questions = course.questions.prefetch_related("choices").all()
    return render(request, "onlinecourse/course_details_bootstrap.html", {
        "course": course,
        "question_list": questions,
    })


@login_required
@transaction.atomic
def submit_exam(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    if request.method != "POST":
        return redirect("course_details", course_id=course.id)

    questions = course.questions.prefetch_related("choices").all()
    score = 0

    for question in questions:
        selected_id = request.POST.get(f"choice_{question.id}")
        if not selected_id:
            continue
        selected_choice = Choice.objects.filter(
            pk=selected_id, question=question
        ).first()
        if selected_choice and selected_choice.is_correct:
            score += question.grade

    submission = Submission.objects.create(
        learner=request.user,
        course=course,
        total_score=score,
    )
    messages.success(request, "Your assessment has been submitted successfully.")
    return redirect("show_exam_result", submission_id=submission.id)


@login_required
def show_exam_result(request, submission_id):
    submission = get_object_or_404(
        Submission.objects.select_related("course", "learner"),
        pk=submission_id,
        learner=request.user,
    )
    questions = submission.course.questions.prefetch_related("choices").all()
    max_score = sum(q.grade for q in questions)
    percentage = round((submission.total_score / max_score) * 100) if max_score else 0

    return render(request, "onlinecourse/exam_result.html", {
        "submission": submission,
        "question_list": questions,
        "max_score": max_score,
        "percentage": percentage,
    })
