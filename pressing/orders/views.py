from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.views import PasswordResetView
from .models import CustomUser, AbstractUser
from .forms import CustomUserCreationForm
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from .forms import RegistrationForm
import yagmail
from .models import Contact
from .forms import ReplyForm
from .forms import ContactForm
from django.contrib import messages
from .models import PressingProfile, Photo, Video
from .forms import PressingProfileForm, PhotoForm, VideoForm
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests
from io import BytesIO
from django.core.files.base import ContentFile
from xhtml2pdf import pisa
import json
from .models import Receipt
from campay.sdk import Client as CamPayClient
from .models import ChatMessage
from .forms import ChatMessageForm


# Authentication view


def home(request):
    return render(request, 'home/home.html')


def services(request):
    return render(request, 'home/services.html')




def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('contact')  # Redirect to the same page after saving
    else:
        form = ContactForm()
    
    return render(request, 'home/contact.html', {'form': form})

def about(request):
    return render(request, 'home/about.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = RegistrationForm()
    
    return render(request, 'auth/register.html', {'form': form})



def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
          
            if user.role == 'admin':
                return redirect('admin_panel')  # Adjust this to match your URL pattern name
            elif user.role == 'deliver':
                return redirect('deliver_panel')  
            elif user.role == 'pressing_manager':
                return redirect('pressing_manager')  
            else:
                return redirect('clients_panel')  # Adjust this to match your URL pattern name
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})



def forgot_password(request):
    if request.method == 'POST':
        form = CustomPasswordResetView.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('password_reset_done')  # Redirect to success page
    else:
        form = CustomPasswordResetView.form_class()

    return render(request, 'auth/forgot_password.html', {'form': form})

class CustomPasswordResetView(PasswordResetView):
    template_name = 'forgot_password.html'  # Specify your template here
    success_url = reverse_lazy('password_reset_done')  # Redirect after a successful reset request
    email_template_name = 'password_reset_email.html'  # Template for the password reset email



@login_required
def logout(request):
    auth_logout(request)
    return redirect('home')



##  user dashboard

@login_required
def pressing_manager(request):
    return render(request, 'panel/manager/pressing_manager.html')

@login_required
def admin_panel(request):
    # Fetch all PressingProfile instances that are not approved yet
    pending_profiles = PressingProfile.objects.filter(approved=False)
    
    if request.method == 'POST':
        # Handle approval or rejection
        profile_id = request.POST.get('profile_id')
        action = request.POST.get('action')

        profile = get_object_or_404(PressingProfile, id=profile_id)

        if action == 'approve':
            profile.approved = True
            profile.save()
            messages.success(request, f'Pressing profile for {profile.business_name} has been approved.')
        elif action == 'reject':
            profile.delete()
            messages.success(request, f'Pressing profile for {profile.business_name} has been rejected and deleted.')

        return redirect('admin_panel')

    context = {
        'pending_profiles': pending_profiles,
    }

    return render(request, 'panel/admin/admin_panel.html', context)
@login_required
def clients_panel(request):
    return render(request, 'panel/clients/clients_panel.html')

@login_required
def deliver_panel(request):
    return render(request, 'panel/deliver/deliver_panel.html')


## manager dashbaord

def about_us(request):
    return render(request, 'panel/manager/about/about_us.html')

def setting(request):
    return render(request, 'panel/manager/setting/setting.html')




# Replace with your Gmail credentials
username = "yvangodimomo@gmail.com"
password = "pzls apph esje cgdl"

# Create a yagmail object
yag = yagmail.SMTP(username, password)


@login_required
def customer_feedback(request):
    contacts = Contact.objects.all()

    if request.method == 'POST':
        if 'reply' in request.POST:
            contact_id = request.POST.get('contact_id')
            contact = Contact.objects.get(id=contact_id)
            reply_message = request.POST.get('message')
            yag = yagmail.SMTP('your_email@gmail.com', 'your_email_password')
            yag.send(to=contact.email, subject="Reply to your message", contents=reply_message)
            return redirect('customer_feedback')  # redirect after sending reply
        elif 'delete' in request.POST:
            contact_id = request.POST.get('delete')  # Use 'delete' here as it matches the button name
            Contact.objects.filter(id=contact_id).delete()
            return redirect('customer_feedback')

    return render(request, 'panel/manager/setting/customer_feedback.html', {'contacts': contacts, 'reply_form': ReplyForm()})




from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse, HttpResponse



# views.py
from .models import PressingProfile, Region, Town, Quarter, Photo, Video
from .forms import PressingProfileForm, PhotoForm, VideoForm, MediaForm




# Initialize CamPay client
campay = CamPayClient({
    "app_username": "JByBUneb4BceuEyoMu1nKlmyTgVomd-QfokOrs4t4B9tPJS7hhqUtpuxOx5EQ7zpT0xmYw3P6DU6LU0mH2DvaQ",
    "app_password": "m-Xuj9EQIT_zeQ5hSn8hLjYlyJT7KnSTHABYVp7tKeHKgsVnF0x6PEcdtZCVaDM0BN5mX-eylX0fhrGGMZBrWg",
    "environment": "PROD"  # use "DEV" for demo mode or "PROD" for live mode
})



@login_required
def apply_portfolio(request):
    if request.method == 'POST':
        profile_form = PressingProfileForm(request.POST)
        photos = request.FILES.getlist('photos')
        videos = request.FILES.getlist('videos')

        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()

            for photo in photos:
                Photo.objects.create(image=photo, pressing_profile=profile)
            for video in videos:
                Video.objects.create(video_file=video, pressing_profile=profile)

            return redirect('payment_page')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        profile_form = PressingProfileForm()
    
    # Fetch regions, towns, and quarters for use in the dynamic fields
    regions = Region.objects.all()
    towns = Town.objects.all()
    quarters = Quarter.objects.all()

    context = {
        'profile_form': profile_form,
        'regions': regions,
        'towns': towns,
        'quarters': quarters,
    }
    return render(request, 'panel/manager/manage_order/apply_portfolio.html', context)



def load_towns(request):
    region_id = request.GET.get('region_id')
    towns = Town.objects.filter(region_id=region_id).all()
    return JsonResponse(list(towns.values('id', 'name')), safe=False)

def load_quarters(request):
    town_id = request.GET.get('town_id')
    quarters = Quarter.objects.filter(town_id=town_id).all()
    return JsonResponse(list(quarters.values('id', 'name')), safe=False)
    






@csrf_exempt
@login_required
def payment_page(request):
    pressing_count = request.session.get('pressing_count', 1)
    mobile_number = request.session.get('mobile_number')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cart_total = pressing_count * 100  # Calculate total based on pressing count
            phone_number = data.get('phoneNumber')

            # Process payment with CamPay
            collect = campay.collect({
                "amount": str(cart_total),
                "currency": "XAF",
                "from": "237" + phone_number,
                "description": "Portfolio Payment",
                "external_reference": "",  # Optional: your unique transaction ID
            })

            if collect.get('status') == 'SUCCESSFUL':
                receipt_id = generate_receipt(cart_total)
                return JsonResponse({
                    'success': True,
                    'receiptId': receipt_id,
                    'receiptUrl': reverse('download_receipt', args=[receipt_id])
                })
            else:
                return JsonResponse({'success': False, 'message': collect.get('reason', 'Payment failed')}, status=400)

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)

    return render(request, 'panel/manager/manage_order/payment_page.html', {
        'pressing_count': pressing_count,
        'mobile_number': mobile_number,
    })

@login_required
def generate_receipt(cart_total):
    receipt = Receipt.objects.create(total=cart_total)

    context = {
        'cart_total': cart_total,
        'receipt_id': receipt.id,
        'business_name': "Your Business Name",
        'date': timezone.now(),
    }
    html = render_to_string('panel/manager/manage_order/receipt.html', context)
    result = BytesIO()
    
    pdf = pisa.CreatePDF(BytesIO(html.encode('utf-8')), dest=result)

    if not pdf.err:
        receipt_file = ContentFile(result.getvalue())
        receipt.pdf.save(f'receipt_{receipt.id}.pdf', receipt_file)
        return receipt.id

    return None

@login_required
def download_receipt(request, receipt_id):
    receipt = get_object_or_404(Receipt, id=receipt_id)
    html = render_to_string('panel/manager/manage_order/receipt.html', {'receipt': receipt})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{receipt.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    return response





@login_required
def view_portfolio(request, user_id):
    # Retrieve all PressingProfile objects for the given user_id
    pressing_profiles = PressingProfile.objects.filter(user__id=user_id).prefetch_related('photos', 'videos')

    if not pressing_profiles.exists():
        return render(request, '404.html')  # Handle case where no profile exists

    context = {
        'pressing_profiles': pressing_profiles,
    }
    return render(request, 'panel/manager/manage_order/view_portfolio.html', context)





from .models import Geolocation


@login_required
def track_deliveries(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        location_type = request.POST.get('location_type')
        
        # Save geolocation to the database
        Geolocation.objects.create(latitude=latitude, longitude=longitude, location_type=location_type)
        
        return redirect('track_deliveries')
    
    # Get the latest geolocation entry
    latest_geolocation = Geolocation.objects.last()
    
    context = {
        'latitude': latest_geolocation.latitude if latest_geolocation else None,
        'longitude': latest_geolocation.longitude if latest_geolocation else None,
        'location_type': latest_geolocation.get_location_type_display() if latest_geolocation else None,
    }
    return render(request, 'panel/manager/manage_order/track_deliveries.html', context)



from .models import Delivery, Invoice, Vehicle

def view_deliveries(request):
    deliveries = Delivery.objects.all()
    return render(request, 'panel/manager/manage_order/view_deliveries.html', {'deliveries': deliveries})

def schedule_pickup(request):
    if request.method == 'POST':
        # Logic to schedule a pickup, e.g., save to the database
        pass
    return render(request, 'panel/manager/manage_order/schedule_pickup.html')

def view_invoices(request):
    invoices = Invoice.objects.all()
    return render(request, 'panel/manager/manage_order/view_invoices.html', {'invoices': invoices})

def track_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    return render(request, 'panel/manager/manage_order/track_vehicle.html', {'vehicle': vehicle})

@login_required
def chat_view(request):
    user = request.user
    messages = ChatMessage.objects.filter(receiver=user) | ChatMessage.objects.filter(sender=user)
    messages = messages.order_by('timestamp')

    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = user
            # Set the receiver dynamically or have a fixed role based receiver
            message.receiver = CustomUser.objects.filter(role='deliver').first()  # Example: Send to first Deliver user
            message.save()
            return redirect('chat')  # Replace 'chat' with your chat URL name
    else:
        form = ChatMessageForm()

    context = {
        'messages': messages,
        'form': form,
    }
    return render(request, 'panel/manager/chat/chat.html', context)








##admin panel


@login_required
def user_management(request):
    users = CustomUser.objects.all()
    return render(request, 'panel/admin/manage_user/user_management.html', {'users': users})

@login_required
def add_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_management')
    else:
        form = RegistrationForm()
    return render(request, 'panel/admin/manage_user/user_management.html', {'form': form})

@login_required
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = RegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_management')
    else:
        form = RegistrationForm(instance=user)
    return render(request, 'panel/admin/manage_user/edit_user.html', {'form': form})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_management')
    return render(request, 'panel/admin/manage_user/confirm_delete.html', {'user': user})

def about_us_dev(request):
    return render(request, 'panel/admin/about/about_us_dev.html')


from .models import PressingProfile, Photo, Video
from .forms import PromotionForm, SocialMediaForm

@login_required
def marketing_promotions(request):
    if request.method == 'POST':
        pressing_id = request.POST.get('pressing_id')
        pressing = get_object_or_404(PressingProfile, id=pressing_id)
        
        # Handle photo uploads
        photos = request.FILES.getlist('photos')
        for photo in photos:
            photo_instance = Photo.objects.create(image=photo)
            pressing.photos.add(photo_instance)

        # Handle video uploads
        videos = request.FILES.getlist('videos')
        for video in videos:
            video_instance = Video.objects.create(video_file=video)
            pressing.videos.add(video_instance)
        
        # Handle social media links
        if 'facebook' in request.POST:
            pressing.facebook_url = request.POST.get('facebook')
            pressing.instagram_url = request.POST.get('instagram')
            pressing.tiktok_url = request.POST.get('tiktok')
            pressing.youtube_url = request.POST.get('youtube')
            pressing.save()
        
        return redirect('marketing_promotions')

    pressings = PressingProfile.objects.all()
    return render(request, 'panel/admin/marketing/marketing_promotions.html', {'pressings': pressings})



@login_required
def add_pressing(request):
    if request.method == 'POST':
        profile_form = PressingProfileForm(request.POST, request.FILES)
        photo_form = PhotoForm(request.POST, request.FILES)
        video_form = VideoForm(request.POST, request.FILES)

        if profile_form.is_valid() and photo_form.is_valid() and video_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            profile.save()

            # Save photos
            photos = request.FILES.getlist('photos')
            for photo in photos:
                new_photo = Photo(image=photo)
                new_photo.save()
                profile.photos.add(new_photo)

            # Save videos
            videos = request.FILES.getlist('videos')
            for video in videos:
                new_video = Video(video_file=video)
                new_video.save()
                profile.videos.add(new_video)

            profile.save()

            messages.success(request, "Pressing added successfully!")
            return redirect('add_pressing')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        profile_form = PressingProfileForm()
        photo_form = PhotoForm()
        video_form = VideoForm()

    return render(request, 'panel/admin/platform_management/add_pressing.html', {
        'profile_form': profile_form,
        'photo_form': photo_form,
        'video_form': video_form,
    })




@login_required
def chat_view(request):
    users = CustomUser.objects.exclude(id=request.user.id)  # Get all users except the logged-in user
    return render(request, 'panel/admin/chat/chat_room.html', {'users': users})

@login_required
def send_message(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver_id')
        message_text = request.POST.get('message')

        receiver = get_object_or_404(CustomUser, id=receiver_id)
        message = ChatMessage.objects.create(sender=request.user, receiver=receiver, message=message_text)

        return JsonResponse({'status': 'success', 'message_id': message.id})

@login_required
def get_messages(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    messages = ChatMessage.objects.filter(
        (models.Q(sender=request.user) & models.Q(receiver=user)) |
        (models.Q(sender=user) & models.Q(receiver=request.user))
    ).order_by('timestamp')

    return JsonResponse({'messages': list(messages.values())})



from .models import CustomUser, Contact, PressingProfile, Receipt, ChatMessage

def analytics_view(request):
    user_count = CustomUser.objects.count()
    contact_count = Contact.objects.count()
    pressing_profile_count = PressingProfile.objects.count()
    receipt_count = Receipt.objects.count()
    chat_message_count = ChatMessage.objects.count()

    context = {
        'user_count': user_count,
        'contact_count': contact_count,
        'pressing_profile_count': pressing_profile_count,
        'receipt_count': receipt_count,
        'chat_message_count': chat_message_count,
    }
    return render(request, 'panel/admin/analytics/analytics.html', context)