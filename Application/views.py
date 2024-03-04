from django.shortcuts import render,render, redirect
import requests,json
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from Application.models import Article
from django.shortcuts import render, get_object_or_404
from .forms import ArticleForm
from Application.models import Headline

# Create your views here.

parsing_data={"articles":[]}
current_request = "Home"
global_category =  "general"

def Parsing(request, category_name):
    # parsing_data = {}
    global current_request
    global global_category 
    url = "https://gnews.io/api/v4/top-headlines"
    # Retrieve user language from the session, default to 'en'
    user_language = request.session.get('language', 'en')
    user_category = request.session.get('category', 'general')

    params = {
        "category": user_category,
        "max": 8,  # Limiting to 5 article
        "country":"in",
        "lang" : user_language,
        "apikey": "35f0b3e6beb8601f4db1d9e6a901e2b4"
    }
    params["category"] = category_name

    response = requests.get(url, params=params)

    if response.status_code == 200:
        Api_data = response.json()
        # print(headlines)
        parsing_data["articles"] = Api_data.get('articles', [])
    else:
        print(f"Error: {response.status_code}")

    # Store parsing_data in the session
    request.session['parsing_data'] = parsing_data
    current_request = "Parsing"
    global_category = params["category"]
    return render(request, "home.html", Api_data)
    

def home(request):
    global current_request
    Headline.objects.all().delete()
    url = "https://gnews.io/api/v4/top-headlines"
    # Retrieve user language from the session, default to 'en'
    user_language = request.session.get('language', 'en')

    params = {
        "category": 'general',
        "max": 8,  # Limiting to 1 article
        "country":"in",
        "lang" : user_language,
        "apikey": "35f0b3e6beb8601f4db1d9e6a901e2b4"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        News = response.json()
    else:
        print(f"Error: {response.status_code}")


    for item in News.get('articles', []):
        link = item.get("url", "")
        title = item.get("title", "")
        imgx = item.get("image", "")
        published_at = item.get("publishedAt")

        new_headline = Headline()
        new_headline.title = title
        new_headline.url = link
        new_headline.image = imgx
        new_headline.publishedAt = published_at
        new_headline.save()
    
    current_request = "Home"
    return redirect("news_list")

def news_list(request):
    article = Article.objects.all()[::-1]
    headlines = Headline.objects.all()[::-1]
    context = {
    "articles": article,
    "headlines": headlines,
    }
    # print(context["object_list"])
    return render(request, "home.html", context)


def view_article(request,title):
    article = get_object_or_404(Article, title=title)
    # print(article)
    context = {
        "article": article,
    }
    return render(request, "view_article.html", context)


def set_language(request, lang_code):
    # Set the user's language preference in the session
    request.session['language'] = lang_code
    if current_request == "Home":
        return redirect('home')
    elif current_request == "Parsing":
        return redirect('Parsing',category_name = global_category)

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!!")
   
        
        return redirect('signin')
    
    return render(request, "signup.html")


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(username=username, password=pass1)
        # print(user)
        if user is not None:
            login(request, user)
            # name = user.username
            # messages.success(request, "Logged In Sucessfully!!")
            return redirect("home")
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('signin')
    
    return render(request, "signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')


def publish(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)  # Use the form that includes FileField for image
        if form.is_valid():
            # Process form data, including the uploaded image
            form.save()
            return redirect('home')
    else:
        form = ArticleForm()

    return render(request, 'article.html')


