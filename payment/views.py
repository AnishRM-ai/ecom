from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect, render
from cart.cart import Cart
from .forms import ShippingForm, PaymentForm, CancellationForm
from .models import ShippingAddress, Order, OrderItem, CancellationOrder
from django.contrib import messages
from django.contrib.auth.models import User
from store.models import Product


def cancel_order(request, pk):
    # Retrieve the order belonging to the current user
    order = get_object_or_404(Order, pk=pk, user=request.user)

    if request.method == 'POST':
        form = CancellationForm(request.POST)
        if form.is_valid():
            # Get the reason for cancellation from the form
            reason = form.cleaned_data['reason']
            
            # Create a CancellationOrder instance
            cancellation_order = CancellationOrder(order=order, reason=reason)
            cancellation_order.save()
            
            #Update status
            order.status='Cancelled'
            order.save()

            messages.success(request, "Your Order has been Cancelled!")

            # Redirect to order tracking page
            return redirect('order_tracking')
    else:
        # Render the cancellation form
        form = CancellationForm()
    return render(request, 'payment/cancel_order.html', {'form': form, 'order': order})

            
    
    
#Tracking Order 
def order_tracking(request):
    # get the order of current user
    user_orders = Order.objects.filter(user=request.user)
    user_order_item = OrderItem.objects.filter(order__in = user_orders)
    return render(request, 'payment/order_tracking.html', {'user_orders': user_orders, 'order_item': user_order_item})

#Process the customer order
def process_order(request):
    if request.POST:
       cart = Cart(request)
       cart_products = cart.get_prods()
       quantities = cart.get_quants
       totals = cart.cart_total()
        # Get Billing info from the user
       payment_form = PaymentForm(request.POST or None)
       
       my_shipping = request.session.get('my_shipping')
       
       # Gather Order Info
       fullname=my_shipping['shipping_fullname']
       email=my_shipping['shipping_email']
       # Create shipping address from session info
       shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']} \n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']} \n {my_shipping['shipping_country']}"
       amount_paid = totals
       
       if request.user.is_authenticated:
           #logged in user
           user = request.user
           #Create order
           create_order = Order(user=user, fullname = fullname, email=email, shipping_address=shipping_address, amount_paid=totals)
           create_order.save()
           #Order Item Create
           order_id = create_order.pk
           #Get product Info
           for product in cart_products:
               # Get product Id
               product_id = product.id
               # Get product Price
               if product.is_sale:
                   price = product.sale_price
               else:
                   price = product.price
                   
                # Get Quantity
               for key, value in quantities().items():
                    if int(key) == product_id:
                        # Create order Item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price )
                        create_order_item.save()
            # Delete our cart after checkout          
           for key in list(request.session.keys()):
               if key == "session_key":
                #Delete the key
                    del request.session[key]
                
               
           messages.success(request, "Ordered Placed!")
           return redirect('home')
       else:
           #logged out user/no user account
           create_order = Order(fullname = fullname, email=email, shipping_address=shipping_address, amount_paid=totals)
           create_order.save()
           
            #Order Item Create
           order_id = create_order.pk
           #Get product Info
           for product in cart_products:
               # Get product Id
               product_id = product.id
               # Get product Price
               if product.is_sale:
                   price = product.sale_price
               else:
                   price = product.price
                   
                # Get Quantity
               for key, value in quantities().items():
                    if int(key) == product_id:
                        # Create order Item
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price )
                        create_order_item.save()
                        
                        
                  # Delete our cart after checkout          
           for key in list(request.session.keys()):
               if key == "session_key":
                #Delete the key
                    del request.session[key]
                    
           messages.success(request, "Ordered Placed!")
           return redirect('home')
       
       
       
     
       
        
    else:
        messages.success(request, "Access Denied, You must be logged in to view this page!")
        return redirect('home')





#Function to get billing info of the customer.
def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        
        #GET shipping info session
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
   # checking if the user is logged in
        if request.user.is_authenticated:
           #Get Billing Form
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {"cart_products": cart_products, "quantities": quantities, "totals":totals, "shipping_info": request.POST, "billing_form":billing_form})
        else:
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html', {"cart_products": cart_products, "quantities": quantities, "totals":totals, "shipping_info": request.POST, "billing_form":billing_form})
    else:
        messages.success(request, "Access Denied, You must be logged in to view this page!")
        return redirect('home')


# Create your views here.
def payment_sucess(request):
    return render(request, 'payment/payment_sucess.html', {})

#Checkout Page
def check_out(request):
   # Get Cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        # Checkout as user
        try:
            shipping_user = ShippingAddress.objects.get(user=request.user)
        except ShippingAddress.DoesNotExist:
            shipping_user = ShippingAddress(user=request.user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
    else:
        # Checkout as guest
        shipping_form = ShippingForm(request.POST or None)

    if request.method == "POST":
        if shipping_form.is_valid():
            shipping_form.save()
            # Redirect to a success page or payment processing page
            return redirect('payment:process')  # Assuming you have a named URL for payment processing

    return render(request, "payment/checkout.html", {
        'cart_products': cart_products,
        'quantities': quantities,
        'totals': totals,
        'shipping_form': shipping_form
    })

   