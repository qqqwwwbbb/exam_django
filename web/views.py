from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, DeleteView

from .filters import ApplicationFilter
from .forms import *
from .models import Application, Category


def index(request):
    num_applications_in_progress = Application.objects.all().filter(status='in progress').count()
    applications_done = Application.objects.filter(status='done')

    return render(request, 'index.html', context={'num_applications_in_progress': num_applications_in_progress,
                                                  'applications_done': applications_done})


class ViewApplicationsBorrower(LoginRequiredMixin, generic.ListView):
    model = Application
    template_name = 'view_applications.html'
    context_object_name = 'applications_borrower'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ApplicationFilter(self.request.GET, queryset=self.get_queryset())
        return context

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Application.objects.all()
        else:
            return Application.objects.filter(borrower=self.request.user)


def profile(request):
    return render(request, 'profile.html')


class DesLogoutView(LogoutView):
    template_name = 'registration/logout.html'


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')


class CreateApplication(CreateView):
    template_name = 'create_application.html'
    model = Application
    form_class = CreateApplicationForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        fields = form.save(commit=True)
        fields.borrower = self.request.user
        fields.save()
        return super().form_valid(form)


class DeleteApplication(LoginRequiredMixin, DeleteView):
    model = Application
    success_url = reverse_lazy('view_applications')


class ViewCategory(LoginRequiredMixin, generic.ListView):
    model = Category
    template_name = 'view_categories.html'
    context_object_name = 'categories_list'


class CreateCategory(CreateView):
    template_name = 'create_category.html'
    model = Category
    form_class = CreateCategoryForm
    success_url = reverse_lazy('view_categories')


class DeleteCategory(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('view_categories')


def confirm_update(request, pk, st):
    newApplication = Application.objects.get(id=pk)
    newApplication.save()

    if st == 'done':
        if request.method == 'POST':
            form = AddDesignApplications(request.POST, request.FILES)
            if form.is_valid():
                newApplication.design = form.cleaned_data['design']
                newApplication.status = st
                newApplication.save()
                return redirect('view_applications')
        else:
            form = AddDesignApplications()
        return render(request, 'update_application.html', {'form': form})

    if st == 'in progress':
        if request.method == 'POST':
            form = AddCommentApplications(request.POST, request.FILES)
            if form.is_valid():
                newApplication.comment = form.cleaned_data['comment']
                newApplication.status = st
                newApplication.save()
                return redirect('view_applications')
        else:
            form = AddCommentApplications()
        return render(request, 'update_application.html', {'form': form})

