# projects/views.py
from django.shortcuts import render, redirect, get_object_or_404

from . import models
from .models import Project, Talent, ProjectTalent
from .forms import ProjectForm, ProjectTalentForm


def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('projects:project_list')
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})


def update_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects:project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'update_project.html', {'form': form, 'project': project})


def project_list(request):
    projects = Project.objects.all()
    return render(request, 'project_list.html', {'projects': projects})


def talent_list(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    talents = ProjectTalent.objects.filter(project=project)
    print(talents)
    return render(request, '_talent_list.html', {'project': project, 'talents': talents})


def create_talent(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ProjectTalentForm(request.POST)
        if form.is_valid():
            talent = form.save(commit=False)
            talent.project = project
            talent.save()
            return redirect('/talents/list/' + project.id)
    else:
        form = ProjectTalentForm()
        form.project = project
        form.award_points = project.award_points
    return render(request, 'create_talent.html', {'form': form, 'project': project})


def update_talent(request, talent_id):
    talent = get_object_or_404(ProjectTalent, pk=talent_id)

    if request.method == 'POST':
        form = ProjectTalentForm(request.POST, instance=talent)
        if form.is_valid():
            form.save()
            return redirect('talents:talent_list', project_id=talent.project.id)
    else:
        form = ProjectTalentForm(instance=talent)

    return render(request, 'update_talent.html', {'form': form, 'talent': talent})


def delete_talent(request, talent_id):
    talent = get_object_or_404(ProjectTalent, pk=talent_id)

    if request.method == 'POST':
        project_id = talent.project.id
        talent.delete()
        return redirect('talents:talent_list', project_id=project_id)

    return render(request, 'delete_talent.html', {'talent': talent})
