from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from crudApp.forms import ProjectForm, UserForm, UserProfileInfoForm
from crudApp.models import Project, UserProfileInfo


def index(request):
    user = UserProfileInfo.objects.all()
    user_data = {}
    user_data['object_list'] = user
    return render(request, 'crudApp/index.html', user_data)


@login_required(login_url='/user_login')
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'crudApp/registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/projects')
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(
                username, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'crudApp/login.html', {})


@login_required(login_url='/user_login')
def project_list(request, template_name='crudApp/project_list.html'):
    projects = Project.objects.all()
    projects = projects.order_by('title')
    data = {}
    project_list = []
    if request.method == 'GET':
        search_query = request.GET.get('search', None)

    if search_query is not None:
        for project in projects:
            if search_query in project.title:
                project_list.append(project)
        data['object_list'] = project_list
    else:
        data['object_list'] = projects
    return render(request, template_name, data)


@login_required(login_url='/user_login')
def project_view(request, slug, template_name='crudApp/project_detail.html'):
    project = get_object_or_404(Project, slug=slug)
    return render(request, template_name, {'object': project})


@login_required(login_url='/user_login')
def project_create(request, template_name='crudApp/project_form.html'):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print(form.data)
            return redirect('/projects')
        else:
            print(form.errors)
        return render(request, template_name, {'form': form})
    else:
        form = ProjectForm()
        return render(request, template_name, {'form': form})


@login_required(login_url='/user_login')
def project_update(request, slug, template_name='crudApp/project_form.html'):
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('/projects')
        return render(request, template_name, {'form': form})
    else:
        form = ProjectForm(instance=project)
        return render(request, template_name, {'form': form})


@login_required(login_url='/user_login')
def project_delete(request, slug, template_name='crudApp/project_confirm_delete.html'):
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        project.delete()
        return redirect('/projects')
    return render(request, template_name, {'object': project})
