from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from products.models import CategoryModel, ProductModel, CartModel
from django.contrib.auth import logout
from products.forms import SearchForm
from django.views.generic.list import ListView


# def home_page(request):
#     categories = CategoryModel.objects.all()
#     products = ProductModel.objects.all()
#     form = SearchForm
#     context = {"categories": categories, "products": products, "form": form}
#     return render(request, template_name="index.html", context=context)


class HomePage(ListView):
    form = SearchForm
    template_name = 'index.html'
    model = ProductModel
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = CategoryModel.objects.all()
        context["products"] = ProductModel.objects.all()
        return context


class MyLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return "/"


def logout_view(request):
    logout(request)
    return redirect("home")


def search(request):
    if request.method == "POST":
        get_product = request.POST.get("search_product")
        try:
            exact_product = ProductModel.objects.get(product_title__iscontains=get_product)
            return redirect(f"/products/{exact_product.id}")
        except:
            return redirect("/")


def product_page(request, pk):
    product = ProductModel.objects.get(id=pk)
    context = {"product": product}
    return render(request, "product.html", context)


def category_page(request, pk):
    category = CategoryModel.objects.get(id=pk)
    current_products = ProductModel.objects.filter(product_category=category)
    context = {"product": current_products}
    return render(request, "category.html", context)


def add_products_to_user_cart(request, pk):
    if request.method == "POST":
        checker = ProductModel.objects.get(pk=pk)

        if checker.product_count >= int(request.POST.get("pr_count")):
            CartModel.objects.create(user_id=request.user.id,
                                     user_product=checker,
                                     user_product_quantity=int(request.POST.get("pr_count"))
                                     ).save()
            return redirect("/user_cart")
        else:
            return redirect("/")


def user_cart(request):
    cart = CartModel.objects.filter(user_id=request.user.id)
    if request.method == "POST":
        main_text = "New order\n"

        for i in cart:
            main_text += f"Product: {i.user_product}\n" \
                        f"Amount: {i.user_product_quantity}\n" \
                        f"Customer: {i.user_id}\n" \
                        f"Price of product: {i.user_product.product_price}\n"

