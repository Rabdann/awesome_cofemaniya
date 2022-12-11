import os

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import login, logout
from django.contrib import messages
from django.conf import settings
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy

from rest_framework import viewsets

from .models import CoffeeModel, IngredientsModel
from .forms import RegistrationForm, LoginForm, ContactForm, CoffeeForm
from .serializers import CoffeeSerializer

from basket.forms import BasketAddProductForm


def cafe_func(request):
    return render(request, 'cof/cafe.html')


class CoffeeListView(ListView):
    model = CoffeeModel
    template_name = 'cof/coffee_list.html'
    context_object_name = 'list_coffee'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Меню'
        return context


class IngredientsListView(ListView):
    model = IngredientsModel
    template_name = 'cof/ingredient_list.html'
    context_object_name = 'ingredients'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ингредиенты'
        return context


class IngredientDetailView(DetailView):
    model = IngredientsModel
    template_name = 'cof/ingredient_detail.html'
    context_object_name = 'ingredient'
    pk_url_kwarg = 'ingredient_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basket_form'] = BasketAddProductForm()
        return context


# def list_coffee_func(request):
#     coffee_lst = CoffeeModel.objects.all()
#     paginator = Paginator(coffee_lst, 2)
#     page_num = request.GET.get('page', 1)
#     page_obj = paginator.get_page(page_num)
#     context = {
#         'title': 'Напитки',
#         'page_obj': page_obj
#     }
#     return render(request, 'cof/coffee_list.html', context)


# def coffee_detail(request, coffee_id):
#     coffee = get_object_or_404(CoffeeModel, pk=coffee_id)
#     context = {
#         'coffee': coffee,
#     }
#     return render(request, 'cof/coffee_detail.html', context)


class CoffeeDetailView(DetailView):
    model = CoffeeModel
    template_name = 'cof/coffee_detail.html'
    context_object_name = 'coffee'
    pk_url_kwarg = 'coffee_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['basket_form'] = BasketAddProductForm()
        return context


class CoffeeDeleteVeiw(DeleteView):
    model = CoffeeModel
    template_name = 'cof/coffee_delete.html'
    pk_url_kwarg = 'coffee_id'
    success_url = reverse_lazy('list_coffee')

    @method_decorator(permission_required('coffee.delete_coffe'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CoffeeUpdateView(UpdateView):
    model = CoffeeModel
    form_class = CoffeeForm
    template_name = 'cof/coffee_update.html'
    pk_url_kwarg = 'coffee_id'
    success_url = reverse_lazy('list_coffee')

    @method_decorator(permission_required('coffee.change_coffe'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class CoffeeCreateView(CreateView):
    model = CoffeeModel
    form_class = CoffeeForm
    template_name = 'cof/coffee_add.html'
    success_url = reverse_lazy('list_coffee')  # Путь переадресации при успешном добавлении

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


def user_registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('cafe')
    else:
        form = RegistrationForm()
    return render(request, 'auth/registration.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list_coffee')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('cafe')


def contact_email(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            mail = send_mail(
                form.cleaned_data['subject'],
                form.cleaned_data['content'],
                settings.EMAIL_HOST_USER,
                [os.environ['EMAIL_HOST_USER']],
                fail_silently=True,
            )
            if mail:
                messages.success(request, 'Письмо успешно отправлено.')
                return redirect('cafe')
            else:
                messages.error(request, 'Письмо не удалось отправить, попробуйте позже.')
        else:
            messages.warning(request, 'Письмо неверно заполнено, перепроверьте внесенные данные.')
    else:
        form = ContactForm()
    return render(request, 'cof/mail.html', {'form': form})


class CoffeeViewSet(viewsets.ModelViewSet):
    queryset = CoffeeModel.objects.filter(exists=True)
    serializer_class = CoffeeSerializer


def error_404(request, exception):
    response = render(request, 'errors/404.html', {'title': 'Страница не найдена', 'message': exception})
    response.status_code = 404
    return response


def error_400(request, exception):
    response = render(request, 'errors/400.html', {'title': 'Неккоректный запрос', 'message': exception})
    response.status_code = 400
    return response


def error_403(request, exception):
    response = render(request, 'errors/403.html', {'title': 'Доступ запрещен', 'message': exception})
    response.status_code = 403
    return response


def error_500(request):
    response = render(request, 'errors/500.html', {'title': 'Внутренняя ошибка сервера'})
    response.status_code = 500
    return response



