from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from .models import Task
def task_list(request):
    tasks = Task.objects.all()
    now = datetime.now()

    for task in tasks:
        due_datetime = datetime.combine(task.due_date, datetime.min.time())
        delta = due_datetime - now

        total_seconds = int(delta.total_seconds())
        days = abs(total_seconds) // 86400
        hours = (abs(total_seconds) % 86400) // 3600
        minutes = (abs(total_seconds) % 3600) // 60

        if total_seconds > 0:
            task.time_left = f"{days} kun {hours} soat {minutes} daqiqa qoldi"
        elif total_seconds == 0:
            task.time_left = "bajjarishga ulgurdingizmi?"
        else:
            task.time_left = f"{days} kun {hours} soat {minutes} daqiqa oldin o‘tgan"

    return render(request, 'task_list.html', {'tasks': tasks})


def add_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        due_date = request.POST['due_date']
        priority = request.POST['priority']
        
        Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            completed=False
        )
        return redirect('task_list')
    return render(request, 'add_task.html')

def edit_task(request, id):
    task = get_object_or_404(Task, pk=id)
    if request.method == 'POST':
        task.title = request.POST['title']
        task.description = request.POST['description']
        task.due_date = request.POST['due_date']
        task.priority = request.POST['priority']
        task.completed = 'completed' in request.POST
        task.save()
        return redirect('task_list')
    return render(request, 'edit_task.html', {'task': task})

def delete_task(request, id):
    task = get_object_or_404(Task, pk=id)
    task.delete()
    return redirect('task_list')

def toggle_complete(request, id):
    task = get_object_or_404(Task, pk=id)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')
