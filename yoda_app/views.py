from django.shortcuts import render
from django.http import HttpResponse
from yoda_app.models import Category, Page
from yoda_app.forms import CategoryForm, PageForm


def index(request):

    category_list = Category.objects.order_by('-view')[:5]
    # context_dict = {'boldmessage': "I am bold front from the context"}
    context_dict = {'categories': category_list}

    return render(request, 'yoda_app/index.html', context_dict)


def about(request):
    return HttpResponse("Yoda says this is about page")


def category(request, category_name_slug):

    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name

        pages = Page.objects.filter(category=category).order_by('-views')[:5]

        context_dict['pages'] = pages
        context_dict['category'] = category
        context_dict['category_name_slug'] = category_name_slug
    except Category.DoesNotExist:
        pass

    return render(request, 'yoda_app/category.html', context_dict)


def add_category(request):

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return index(request)

        else:
            print form.errors

    else:
        form = CategoryForm()


    return render(request, 'yoda_app/add_category.html', {'form': form})


def add_page(request, category_name_slug):

    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()

                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form': form, 'category': cat, 'category_name_slug': category_name_slug}

    return render(request, 'yoda_app/add_page.html', context_dict)

