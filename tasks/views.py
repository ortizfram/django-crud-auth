from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone


# the form comes from this same file
def signup(request):
    if request.method == "GET":
        # send signup page
        return render(request, "signup.html", {"form": UserCreationForm})
    else:
        # if same password Register User
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect("tasks")
            # User already exists
            except IntegrityError:
                return render(
                    request,
                    "signup.html",
                    {"form": UserCreationForm, "error": "Username already exists"},
                )
        # password does not match
        return render(
            request,
            "signup.html",
            {"form": UserCreationForm, "error": "Password do not match"},
        )

def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {"form": AuthenticationForm})
    else:
        # If not user --> return 'Incorrect data'
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user is None:
            return render(
                request,
                "signin.html",
                {
                    "form": AuthenticationForm,
                    "error": "Username or password is incorrect",
                },
            )
        # If user in table --> save session & redirect
        else:
            login(request, user)
            return redirect("tasks")

@login_required
def signout(request):
    logout(request)
    return redirect("home")
# -----------------------------------

# exe smt when URL is visited
def home(request):
    return render(request, "home.html")


@login_required
def tasks(request):
    # render user tasks
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, "tasks.html", {
        'tasks': tasks,

    })

@login_required
# View tasks mark as completed
def tasks_completed(request):
    # render user tasks
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, "tasks.html", {
        'tasks': tasks,

    })

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task':task, 'form':form})
    else:
        # update and save
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        # error
        except ValueError:
            return render(request, 'task_detail.html', {'task':task, 'form':form, 'error':"Error updating tasks"})

@login_required
# mark as completed + time
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
#delete
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.delete()
        return redirect('tasks')

@login_required
def create_task(request):
    # return creation form
    if request.method == 'GET':
        return render(request, 'create_task.html', {
        'form': TaskForm
        })
    # save task, redirect
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect("tasks")
        except ValueError:
            return render(request, 'create_task.html', {
            'form': TaskForm,
            'error': 'Please provide valid data'
            })
        



