from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
import requests
from .models import EmailSettings
User = get_user_model()


# Create your views here.

coordinate_url = "http://api.openweathermap.org/geo/1.0/direct"
weather_url = "https://api.openweathermap.org/data/2.5/weather"


def index(request):
    return render(request, "index.html")


def create_user(request):
    first_name = request.POST.get("firstName", "")
    last_name = request.POST.get("lastName", "")
    username = request.POST.get("username", "")
    email = request.POST.get("email")
    password1 = request.POST.get("password1")
    password2 = request.POST.get("password2")
    can_send_mails = bool(request.POST.get("canSendMails"))

    if password1 != password2:
        messages.error(request, "Please Enter The same Password")
        return redirect("signup")
    if User.objects.filter(email=email).exists():
        messages.error(request, "Username or Email already exists.")
        return False
    else:
        User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password1,
            can_send_email=can_send_mails,
        )
        messages.success(request, "Account Created Successfully.")
        return True
    return False


def signup(request):
    if request.method == "POST":
        res = create_user(request)
        if res:
            return redirect("login")
        return redirect("signup")
    return render(request, "signup.html")


def loginUser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        messages.error(request, "Invalid Credientals")
        return redirect("login")
    return render(request, "login.html")

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    messages.success(request, "User Logged out successfully")
    return redirect('login')


@login_required(login_url='login')
def deleteUser(request):
    user = request.user
    logout(request)
    User.delete(user)
    messages.success(request, "User Deleted successfully")
    return redirect('signup')



# views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

from .models import EmailSettings


@login_required(login_url='login')
def update_email_settings(request):

    if request.method == "POST":

        settings, created = EmailSettings.objects.get_or_create(
            user=request.user
        )

        settings.weather_alerts = "weather_alerts" in request.POST
        settings.daily_forecast = "daily_forecast" in request.POST
        settings.weekly_summary = "weekly_summary" in request.POST

        settings.email_frequency = request.POST.get(
            "email_frequency",
            "daily"
        )

        settings.save()

        messages.success(request, "Email settings updated successfully.")

    return redirect("home")



def get_coordinates(request, city):

    if not city:
        messages.error(request, "Please enter a city name.")
        return None, None

    params = {
        "q": city,
        "limit": 1,
        "appid": "66e6c2e542cf345f5d7c5ceb6e43ee5a",
    }

    response = requests.get(coordinate_url, params=params)

    if response.status_code != 200:
        return None, None

    data = response.json()

    if not data:
        return None, None

    lat = data[0]["lat"]
    lon = data[0]["lon"]

    return lat, lon


def get_weather_data(loc):
    """Return a dictionary of current weather and none if data not found"""
    parameters = {
        "appid": "66e6c2e542cf345f5d7c5ceb6e43ee5a",
        "q": loc,
        "units": "metric",
    }
    response = requests.get(weather_url, params=parameters)
    data = response.json()
    if data:
        response = response.json()

        current_weather = {
            "city": response["name"],
            "country": response["sys"]["country"],
            "temperature": response["main"]["temp"],
            "feels_like": response["main"]["feels_like"],
            "temp_min": response["main"]["temp_min"],
            "temp_max": response["main"]["temp_max"],
            "condition": response["weather"][0]["main"],
            "description": response["weather"][0]["description"],
            "icon": response["weather"][0]["icon"],
            "icon_url": f"https://openweathermap.org/img/wn/{response['weather'][0]['icon']}@2x.png",
            "humidity": response["main"]["humidity"],
            "pressure": response["main"]["pressure"],
            "wind_speed": response["wind"]["speed"],
            "wind_direction": response["wind"]["deg"],
            "wind_gust": response["wind"].get("gust"),
            "visibility": response["visibility"],
            "clouds": response["clouds"]["all"],
            "latitude": response["coord"]["lat"],
            "longitude": response["coord"]["lon"],
            "sunrise": response["sys"]["sunrise"],
            "sunset": response["sys"]["sunset"],
            "timezone": response["timezone"],
        }
        return current_weather
    return None


@login_required(login_url="login")
def home(request):
    context, weather_data = None, None
    if request.method == "POST":
        city = request.POST.get("city")
        lat, lon = get_coordinates(request, city)
        if lat is None or lon is None:
            messages.error(request, "Invalid City Name.")
            return redirect("home")
        weather_data = get_weather_data(city)
        if weather_data is None:
            messages.error(request, "Unable to fetch weather data.")
            return redirect("home")

    user_settings, created = EmailSettings.objects.get_or_create(
        user=request.user
    )

    context = { "user_settings": user_settings, "weather": weather_data }
    return render(request, "home.html", context)
