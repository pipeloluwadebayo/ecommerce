from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from django.views import  View


#Create your views here.
# def all_items(request):
#     # query database for all objects in products table
#     products = Product.objects.all
#     # load the data on the associated template
#     return render(request, 'shop/home.html', {'products': products})
class Index(View):

    def post(self , request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        return redirect('homepage')



    def get(self , request):
        # print()
        return render(request , 'shop/home.html')

def store(request):
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products();

    data = {}
    data['products'] = products
    data['categories'] = categories

    return render(request, 'shop/home.html', data)

def categories(request):
    # collect and return all the category information from the category table
    return{
        'categories': Category.objects.all()
    }
# def basket(request):
#     cart = request.session.get('cart')
#     if not cart:
#         request.session['cart'] = {}
#     products = None
#     categories = Category.get_all_categories()
#     categoryID = request.GET.get('category')
#     if categoryID:
#         products = Product.get_all_products_by_categoryid(categoryID)
#     else:
#         products = Product.get_all_products();

    # data = {}
    # data['products'] = products
    # data['categories'] = categories

    # print('you are : ', request.session.get('email'))
    # return render(request, 'shop/home.html', data)


def item_detail(request, slug):
    # select from the products table, the item which slug equals slug
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, 'shop/item.html', {'product':product})


def category_list(request, category_slug):
    category = get_object_or_404(Category,slug=category_slug)
    # filter the products table by the category column
    products =  Product.objects.filter(category=category)
    return render(request, 'shop/category.html', {'category': category, 'products':products})