from django.shortcuts import render, redirect
from .models import *
from django.conf import settings
from django.core.mail import send_mail
import random
from .paytm import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

default_dict = {
    'acc_page' : ['index']
}

def seller_index(request):
    seller = Seller.objects.get(company_name= request.session['company_name'])
    products = Product.objects.filter(seller = seller)
    default_dict['products'] = products
    return render(request, "seller_index.html",default_dict)

def otp(request):
    otp_num = random.randint(1000, 9999)
    print('\n\n\n\nOTP IS :',otp_num)
    request.session['otp'] = otp_num

def index(request):
    try:
        user = Seller.objects.get(company_name = request.session['company_name'])
        if user:
            return redirect(seller_index)
    except Exception as e:
        print(f"\n\n\n{e}\n\n\n")
        default_dict['current_page'] = 'index'
        return render(request, 'index.html',default_dict)

def checkout_page(request):
    default_dict['current_page'] = 'checkout_page'
    return render(request, 'checkout_page.html',default_dict)

def login_page(request):
    default_dict['current_page'] = 'login_page'

    if request.method == "POST":
        try:
            buyer = Buyer.objects.get(email = request.POST['email'],password = request.POST['password'])

            request.session['email'] = buyer.email
            request.session['fullname'] = buyer.fullname

            return redirect(index)
        
        except:
            msg = "Invalid Email or Password"
            default_dict['msg_d'] = msg
            return render(request, "login_page.html",default_dict)
    else:
        return render(request, 'login_page.html',default_dict)

def register_page(request):
    default_dict['current_page'] = 'register_page'

    if request.method == "POST":
        try:
            buyer = Buyer.objects.get(email = request.POST['email'])
            msg = "User already exists"
            default_dict['msg_s'] = msg

            return render(request, 'login_page.html',default_dict)
        except:
            try:
                if request.POST["password"] == "" or request.POST["fullname"] == "" or request.POST["email"] == "" or request.POST["address"] == "":

                    msg = "All fields are mendatory"
                    default_dict['msg_d'] = msg

                    return render(request, 'register_page.html',default_dict)

                elif request.POST['password'] == request.POST['confirm_password']:

                    buyer = Buyer.objects.create(
                        fullname = request.POST['fullname'],
                        email = request.POST['email'],
                        address = request.POST['address'],
                        password = request.POST['password']
                    )

                    buyer.save()
                    msg = "Sign Up was successful."
                    default_dict['msg_s'] = msg

                    return render(request, 'login_page.html',default_dict)
                else:
                    msg = "Password and confirm password does not match"
                    default_dict['msg_d'] = msg
                    return render(request, 'register_page.html',default_dict)
            except:
                msg = "Opps something went wrong. Please try again later"
                default_dict['msg_d'] = msg
                return render(request, 'register_page.html', default_dict)
    else:
        return render(request, 'register_page.html',default_dict)

def contact_page(request):
    default_dict['current_page'] = 'contact_page'

    if request.method == "POST":

        try:
            user = Contact.objects.create(
                email = request.POST['email'],
                fullname = request.POST['fullname'],
                message = request.POST['message'],
            )

            user.save()

            email_to_list = ['kavaravi2@gmail.com', ]

            subject = f'You Have Recived a Message From {user.fullname}'

            email_from = settings.EMAIL_HOST_USER

            message = f'The Message Is {user.message}.'


            send_mail(subject,message,email_from,email_to_list)

            return redirect("index")
        
        except Exception as e:
            print(f'\n\n\n{e}\n\n\n')

            print('Somethin Went Wrong..')

            return render(request, 'contact_page.html',default_dict)
    else:
        return render(request, 'contact_page.html',default_dict)

def profile_page(request):
    default_dict['current_page'] = 'profile_page'

    buyer = Buyer.objects.get(email = request.session['email'])

    default_dict['buyer'] = buyer
    msg = "Welcome To Profile"
    default_dict['msg'] = msg


    print(f"\n\n\n{default_dict}\n\n\n")

    if request.method == "POST":
        buyer.fullname = request.POST['fullname']
        buyer.address = request.POST['address']

        buyer.save()

        msg = "Profile updated successfuly"
        default_dict['msg'] = msg

        return render(request, 'profile_page.html', default_dict)
    else:
        return render(request, 'profile_page.html',default_dict)

def shop_page(request):
    product = Product.objects.all()
    default_dict['product'] = product
    default_dict['current_page'] = "shop_page"
    return render(request, "shop_page.html",default_dict)

def log_out(request):
    if 'email' in request.session:
        del request.session['email']
        del request.session['fullname']
    return redirect(login_page)

def seller_log_out(request):
    if 'email' in request.session:
        del request.session['email']
        del request.session['company_name']
    return redirect(index)

def product_details_page(request,pk):
    product = Product.objects.get(pk=pk)
    default_dict['product'] = product
    default_dict['current_page'] = 'product_details_page'
    return render(request, 'product_details_page.html',default_dict)

def change_pass(request):
    default_dict['current_page'] = 'change_pass'

    buyer = Buyer.objects.get(email = request.session['email'])

    if request.method == "POST":
        if buyer.password == request.POST['old_password']:

            if request.POST['new_password'] == buyer.password:
                msg = "New Password and Old Password can not be same"
                default_dict['msg'] = msg
                return render(request, 'change_pass.html', default_dict)
            elif request.POST['new_password'] == request.POST['confirm_new_password']:
                buyer.password = request.POST['new_password']
                buyer.save()
                return redirect(login_page)
            else:
                msg = "New Password and Confirm New Password does not match"
                default_dict['msg'] = msg
                return render(request, 'change_pass.html', default_dict)
        else:
            msg = "Incorrect OLD Password"
            default_dict['msg'] = msg
            return render(request, 'change_pass.html', default_dict)
    else:    
        return render(request, 'change_pass.html', default_dict)

def seller_register(request):

    if request.method == "POST":
        try:
            seller = Seller.objects.get(email = request.POST['email'])
            msg = "User already exists"
            default_dict['msg'] = msg

            return render(request, 'seller_login.html',default_dict)
        except:

            try:
                if request.POST["fullname"] == "" or request.POST["company_name"] == "" or request.POST["email"] == "" or request.POST["mobile"] == "" or request.POST["address"] == "" or request.POST["business_address"] == "" or request.POST["password"] == ""or request.POST["confirm_password"] == "":


                    msg = "All fields are mendatory"
                    default_dict['msg'] = msg

                    return render(request, 'seller_register.html',default_dict)

                elif request.POST['password'] == request.POST['confirm_password']:

                    seller = Seller.objects.create(
                        fullname = request.POST['fullname'],
                        company_name = request.POST['company_name'],
                        email = request.POST['email'],
                        mobile = request.POST['mobile'],
                        address = request.POST['address'],
                        business_address = request.POST['business_address'],
                        password = request.POST['password']
                    )

                    seller.save()
                    msg = "Sign Up was successful."
                    default_dict['msg'] = msg

                    return render(request, 'seller_login.html',default_dict)
                else:
                    msg = "Password and confirm password does not match"
                    default_dict['msg'] = msg
                    return render(request, 'seller_register.html',default_dict)
            except:
                msg = "Opps something went wrong. Please try again later"
                default_dict['msg'] = msg
                return render(request, 'seller_register.html', default_dict)
    else:
        return render(request, 'seller_register.html')

def seller_login(request):

    if request.method == "POST":
        try:
            seller = Seller.objects.get(email = request.POST['email'],password = request.POST['password'])

            request.session['email'] = seller.email
            request.session['company_name'] = seller.company_name

            return redirect(seller_index)
        
        except:
            msg = "Invalid Email or Password"
            default_dict['msg'] = msg
            return render(request, "seller_login.html",default_dict)
    else:

        return render(request, 'seller_login.html')

def seller_profile(request):

    seller = Seller.objects.get(email = request.session['email'])

    default_dict['seller'] = seller
    msg = "Welcome To Profile"
    default_dict['msg'] = msg


    print(f"\n\n\n{default_dict}\n\n\n")

    if request.method == "POST":
        seller.fullname = request.POST['fullname']
        seller.company_name = request.POST['company_name']
        seller.mobile = request.POST['mobile']
        seller.address = request.POST['address']
        seller.business_address = request.POST['business_address']

        seller.save()

        msg = "Profile updated successfuly"
        default_dict['msg'] = msg

        return render(request, 'seller_profile.html', default_dict)
    else:
        return render(request, 'seller_profile.html',default_dict)

def seller_change_pass(request):

    seller = Seller.objects.get(email = request.session['email'])

    if request.method == "POST":
        if seller.password == request.POST['old_password']:

            if request.POST['new_password'] == seller.password:
                msg = "New Password and Old Password can not be same"
                default_dict['msg'] = msg
                return render(request, 'seller_change_pass.html', default_dict)
            elif request.POST['new_password'] == request.POST['confirm_new_password']:
                seller.password = request.POST['new_password']
                seller.save()
                return redirect(seller_login)
            else:
                msg = "New Password and Confirm New Password does not match"
                default_dict['msg'] = msg
                return render(request, 'seller_change_pass.html', default_dict)
        else:
            msg = "Incorrect OLD Password"
            default_dict['msg'] = msg
            return render(request, 'seller_change_pass.html', default_dict)
    else:    
        return render(request, 'seller_change_pass.html')

def add_product(request):

    if request.method == "POST":
        try:
            seller = Seller.objects.get(company_name = request.session['company_name'])
            print(f"\n\n\n{seller}\n\n\n")
            product = Product.objects.create(
                seller = seller,
                product_name = request.POST['product_name'], 
                product_title = request.POST['product_title'], 
                product_size = request.POST['product_size'], 
                product_price = request.POST['product_price'], 
                product_image = request.FILES['product_image'], 
                product_quantity = request.POST['product_quantity'], 
                product_description = request.POST['product_description'], 
            )

            print("\n\n\nProduct Created\n\n\n")
            product.save()
            print("\n\n\nProduct Saved\n\n\n")
            msg = "Product Added SuccessFully"
            default_dict['msg'] = msg
            default_dict['product'] = product
            
            return render(request, 'add_product.html',default_dict)
        except Exception as e:

            print(f"\n\n\n{e}\n\n\n")
            msg = "Failed To Add Product"
            default_dict['msg'] = msg
            return render(request, 'add_product.html',default_dict)
    else:
        return render(request, 'add_product.html')

def edit_product(request, pk):
    product = Product.objects.get(pk=pk)
    seller = Seller.objects.get(company_name = request.session["company_name"])
    if request.method == "POST":
        product.product_name = request.POST['product_name']
        product.product_title = request.POST['product_title']
        product.product_size = request.POST['product_size']
        product.product_price = request.POST['product_price']
        product.product_quantity = request.POST['product_quantity']
        product.product_description = request.POST['product_description']

        product.save()
        if 'product_image' in request.POST['product_image']:

            product.product_image = request.FILES['product_image']
            product.save()

        return redirect(seller_index)
    else:
        default_dict["product"] = product 
        default_dict["seller"] = seller 
        return render(request, "edit_product.html", default_dict)

def delete_product(request, pk):
    product = Product.objects.get(pk=pk)
    product.delete()
    return redirect(seller_index)

def view_product(request,pk):
    product = Product.objects.get(pk=pk)
    default_dict['product'] = product
    return render(request, 'view_product.html',default_dict)

def wishlist(request):
    buyer = Buyer.objects.get(email=request.session['email'])
    wishlist = Wishlist.objects.filter(buyer=buyer)
    default_dict['current_page'] = 'wishlist'
    default_dict['wishlist'] = wishlist

    return render(request, 'wishlist.html', default_dict)

def add_to_wishlist(request, pk):
    product = Product.objects.get(pk=pk)
    buyer = Buyer.objects.get(email = request.session['email'])
    wishlist = Wishlist.objects.filter(buyer=buyer)
    try:
        Wishlist.objects.get(product=product , buyer=buyer)
        default_dict['msg'] = "Item Already in Wishlist.."
        product = Product.objects.all()
        default_dict['product'] = product
        return render(request, 'shop_page.html',default_dict)
    except:
        Wishlist.objects.create(product=product, buyer=buyer)
        default_dict['msg'] = "Added to Wishlist..."
        product = Product.objects.all()
        default_dict['product'] = product
        return render(request, 'shop_page.html',default_dict)

def delete_wishlist(request, pk):
    product = Product.objects.get(pk=pk)
    buyer = Buyer.objects.get(email = request.session['email'])
    wishlists = Wishlist.objects.get(buyer=buyer,product=product)
    wishlists.delete()
    return redirect(wishlist)
        
def add_to_cart(request,pk):
    product = Product.objects.get(pk=pk)
    buyer = Buyer.objects.get(email = request.session['email'])
    carts = Cart.objects.filter(buyer=buyer)
    try:
        in_cart = Cart.objects.get(product = product , buyer = buyer)
        in_cart.product_quantity += 1
        in_cart.total_price = in_cart.product_price * in_cart.product_quantity
        in_cart.save()
        default_dict['msg'] = "You have this item in Your Cart and We Have Increased The Quantity by 1"
        product = Product.objects.all()
        default_dict['product'] = product
        return render(request, 'shop_page.html',default_dict)
    except:
        Cart.objects.create(
            buyer= buyer, 
            product = product,
            product_price = product.product_price,
            total_price = product.product_price,
        )
        default_dict['msg'] = "Item Added to Cart"
        product = Product.objects.all()
        default_dict['product'] = product
        return render(request, 'shop_page.html',default_dict)

def cart_page(request):
    default_dict['current_page'] = 'cart_page'

    buyer = Buyer.objects.get(email = request.session['email'])
    carts = Cart.objects.filter(buyer = buyer)
    payable_amount = 0
    for i in carts:
        print(f"\n\n\n{i.total_price}\n\n\n")
        payable_amount += i.total_price
    print(f"\n\n\n{payable_amount}\n\n\n")

    default_dict['carts'] = carts
    default_dict['payable_amount'] = payable_amount

    return render(request, 'cart_page.html',default_dict)

def delete_cart_product(request,pk):
    product = Product.objects.get(pk=pk)
    buyer = Buyer.objects.get(email = request.session['email'])
    cart_product = Cart.objects.get(product = product, buyer = buyer)
    cart_product.delete()
    return redirect(cart_page)

# paytm settings Section

def initiate_payment(request):
    
    try:
        buyer = Buyer.objects.get(email = request.session['email'])
        amount = int(request.POST['amount'])
        
        
    except:
        default_dict['msg'] = 'Wrong Accound Details or amount'
        return render(request, 'cart_page.html',default_dict)

    transaction = Transaction.objects.create(made_by=buyer, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'callback.html', context=received_data)
        return render(request, 'callback.html', context=received_data)