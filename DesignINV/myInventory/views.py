# Dashboard View
def dashboard(request):
    return render(request, 'dashboard.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Site, Inventory
import pandas as pd

def upload_inventory(request):
    excel_data = None
    columns = None
    site_name = None
    user_name = None

    if request.method == 'POST' and 'file' in request.FILES:
        file = request.FILES['file']
        site_name = request.POST.get('site_name')
        user_name = request.POST.get('user_name')

        # Only admin can upload for another user
        if not request.user.is_staff and user_name != request.user.username:
            messages.error(request, "You can only upload inventory for yourself.")
            return redirect('upload_inventory')

        if file.name.endswith('.xlsx') or file.name.endswith('.xls'):
            try:
                # Read the Excel file
                df = pd.read_excel(file, header=2)  # Skipping the first 2 rows

                # Cleaning the data: drop rows with missing 'Material Description'
                df_cleaned = df.dropna(subset=['Material Description'])
                columns = df_cleaned.columns.tolist()

                # Get or create the site
                site, created = Site.objects.get_or_create(name=site_name)

                # Get the user based on user_name (either admin selecting a user or the current user)
                user = User.objects.get(username=user_name)

                # Save inventory data to the database, linking to the site and user
                for _, row in df_cleaned.iterrows():
                    Inventory.objects.create(
                        site=site,
                        material_code=row['Material Code'],
                        material_desc=row['Material Description'],
                        owner=row['Owner'],
                        type=row['Type'],
                        category=row['Category'],
                        opening_stock=row['Opening Stock \n(FY-2024-25)'],
                        user=user  # Link the data to the specific user
                    )

                messages.success(request, 'Inventory data loaded and saved successfully.')
            except Exception as e:
                messages.error(request, f"Error reading the file: {e}")
        else:
            messages.error(request, 'Please upload a valid Excel file.')

    return render(request, 'upload_inventory.html', {'excel_data': excel_data, 'columns': columns, 'site_name': site_name})




def view_notifications(request):
    return render(request, 'view_notifications.html')


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Inventory, Site, Notification
from django.utils import timezone

def edit_inventory(request, site_name):
    # Fetch the site based on the site_name passed in the URL
    site = Site.objects.get(name=site_name)
    
    # Fetch inventory data for the specific site
    inventory_items = Inventory.objects.filter(site=site, user=request.user)

    if request.method == 'POST':
        # Iterate over each inventory item and update the consumption value
        for inventory in inventory_items:
            consumption = request.POST.get(f'consumption_{inventory.id}')
            if consumption and int(consumption) != 0:
                consumption = int(consumption)  # Parse consumption value
                # Calculate closing stock
                closing_stock = inventory.opening_stock - consumption
                
                # Create a Notification for the updated row
                Notification.objects.create(
                    site=site,
                    material_code=inventory.material_code,
                    opening_stock=inventory.opening_stock,
                    consumption=consumption,
                    closing_stock=closing_stock,
                    timestamp=timezone.now()
                )
                
                # Update inventory with new closing stock (and set opening stock to the new closing stock)
                inventory.opening_stock = closing_stock
                inventory.save()  # Save the updated inventory record

        messages.success(request, 'Inventory updated successfully.')
        return redirect('inventory_history', site_name=site_name)  # Redirect to inventory history page after update

    return render(request, 'edit_inventory.html', {'site': site, 'inventory_items': inventory_items})


def inventory_history(request, site_name):
    # Fetch the site and updated inventory data
    site = Site.objects.get(name=site_name)
    inventory_items = Inventory.objects.filter(site=site, user=request.user)
    
    # Fetch notifications to display changes
    notifications = Notification.objects.filter(site=site).order_by('-timestamp')

    return render(request, 'inventory_history.html', {'site': site, 'inventory_items': inventory_items, 'notifications': notifications})



from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect

def home_page(request):
    return render(request, 'home_page.html')

def redirect_to_home(request):
    return redirect('home')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user')  # Redirect to the success page
        else:
            return render(request, 'user_login.html', {'error_message': 'Invalid credentials'})
    return render(request, 'user_login.html')

FIXED_USERNAME = 'Solonindia'
FIXED_PASSWORD = 'Sipl$2024'

def login1_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the provided username and password match the fixed ones
        if username == FIXED_USERNAME and password == FIXED_PASSWORD:
            # Redirect to the admin page or any other page you want
            return redirect('admin')  # Adjust this to the correct URL name for the admin page
        else:
            # If credentials do not match
            return render(request, 'admin_login.html', {'error_message': 'Invalid credentials'})
    return render(request, 'admin_login.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'register.html', {'success_message': 'User created successfully'})
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def admin_page(request):
    return render(request,'admin.html')



def user_page(request):
    # Get the sites related to the logged-in user
    sites = Site.objects.filter(inventory__user=request.user).distinct()  # Only fetch sites the user has access to

    # If you want to pass the first site's name as a default or show all available sites
    # If there's at least one site, pass the first one as a default
    site_name = sites.first().name if sites.exists() else None

    return render(request, 'user.html', {'sites': sites, 'site_name': site_name})


def notification_list(request):
    # Retrieve all notifications from the Notification model
    notifications = Notification.objects.all().order_by('-timestamp')  # Optional: ordering by timestamp (latest first)

    # Passing notifications to the template
    context = {
        'notifications': notifications
    }
    
    return render(request, 'notification_list.html', context)