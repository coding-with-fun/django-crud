from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from crudApp.forms import UserForm, UserProfileInfoForm, ProjectForm
from crudApp.models import Project


def index(request):
    return render(request, 'crudApp/index.html')


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
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
                return HttpResponseRedirect('/crudApp')
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(
                username, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'crudApp/login.html', {})


def project_list(request, template_name='crudApp/project_list.html'):
    projects = Project.objects.all()
    data = {}
    project_list = []
    if request.method == 'GET':
        search_query = request.GET.get('search', "None")
    
    searched = False
    for project in projects:
        if search_query in project.title or search_query is project.slug:
            project_list.append(project)
            data['object_list'] = project_list
            searched = True
    if not searched:
        data['object_list'] = projects

    return render(request, template_name, data)


def project_view(request, slug, template_name='crudApp/project_detail.html'):
    project = get_object_or_404(Project, slug=slug)
    print(project)
    return render(request, template_name, {'object': project})


def project_create(request, template_name='crudApp/project_form.html'):
    form = ProjectForm(request.POST or None)
    if form.is_valid():
        form.save()
        print(form.data)
        return redirect('/crudApp')
    else:
        print(form.errors)
    return render(request, template_name, {'form': form})


def project_update(request, slug, template_name='crudApp/project_form.html'):
    project = get_object_or_404(Project, slug=slug)
    form = ProjectForm(request.POST or None, instance=project)
    if form.is_valid():
        form.save()
        return redirect('/crudApp')
    return render(request, template_name, {'form': form})


def project_delete(request, slug, template_name='crudApp/project_confirm_delete.html'):
    project = get_object_or_404(Project, slug=slug)
    if request.method == 'POST':
        project.delete()
        return redirect('/crudApp')
    return render(request, template_name, {'object': project})
