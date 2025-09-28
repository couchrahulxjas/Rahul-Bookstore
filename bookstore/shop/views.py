from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F
from .models import Book, CartItem, Order

# List all books
def book_list(request):
    books = Book.objects.all()
    return render(request, 'catalog/book_list.html', {'books': books})

# Book details
def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'catalog/book_detail.html', {'book': book})

# Add to cart
def add_to_cart(request, book_id):
    session_key = request.session.session_key or request.session.save()
    book = get_object_or_404(Book, id=book_id)
    cart_item, created = CartItem.objects.get_or_create(book=book, session_key=request.session.session_key)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')

# View cart
def view_cart(request):
    cart_items = CartItem.objects.filter(session_key=request.session.session_key)
    total = sum(item.book.price * item.quantity for item in cart_items)
    return render(request, 'catalog/cart.html', {'cart_items': cart_items, 'total': total})

# Checkout
def checkout(request):
    cart_items = CartItem.objects.filter(session_key=request.session.session_key)
    total = sum(item.book.price * item.quantity for item in cart_items)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        items_text = ", ".join([f"{item.book.title} x{item.quantity}" for item in cart_items])
        order = Order.objects.create(name=name, email=email, items=items_text, total=total)
        cart_items.delete()  # clear cart after order
        return render(request, "catalog/order_success.html", {"order": order})

    return render(request, "catalog/checkout.html", {"cart_items": cart_items, "total": total})
