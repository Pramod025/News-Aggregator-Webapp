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

# def home(request):
#     global parsing_data
#     # Assuming your data retrieval logic remains the same
#     try:
#         # new_data = parsing_data
#         # new_data = {"totalArticles": 98201, "articles": [{"title": "'Rashtra-neeti over rajneeti': PM Modi tells why his govt didn't bring 'White Paper' in 2014", "description": "Prime Minister Narendra Modi said on Friday, \u201cI could have bring the White paper in 2014\u2026 If I had to fulfil my political aspirations\u2026\u201d", "content": "Prime Minister Narendra Modi said on Friday, \u201cI could have bring the White Paper in 2014\u2026 If I had to fulfil my political aspirations, I would have presented those numbers before India (in 2014)\u2026It would have suited me politically, but national polic... [4258 chars]", "url": "https://www.livemint.com/news/india/pm-modi-says-could-have-brought-white-paper-in-2014-but-national-policy-new-initiatives-roadmap-10-points-11707492293948.html", "image": "https://www.livemint.com/lm-img/img/2024/02/09/1600x900/Prime-Minister-Narendra-Modi--PTI-_1707492671134_1707492684245.jpg", "publishedAt": "2024-02-09T15:27:26Z", "source": {"name": "Mint", "url": "https://www.livemint.com"}}, {"title": "Paytm fiasco: One97 Communication forms advisory panel headed by former SEBI chairman M Damodaran", "description": "The advisory panel to help Paytm address compliance and regulatory issues.", "content": "The owner of fintech firm Paytm, One 97 Communications Limited, on Friday announced the formation of an advisory committee chaired by former Securities and Exchange Board of India (SEBI) chairman M Damodaran. The committee will work closely with the ... [2244 chars]", "url": "https://www.livemint.com/companies/news/paytm-fiasco-one-97-communication-forms-group-advisory-committee-to-address-regulatory-matters-11707485708651.html", "image": "https://www.livemint.com/lm-img/img/2024/02/09/1600x900/Paytm_1707485993523_1707485993757.jpg", "publishedAt": "2024-02-09T13:44:55Z", "source": {"name": "Mint", "url": "https://www.livemint.com"}}, {"title": "Jiten Ram Manjhi, a man for all alliances", "description": "Manjhi spoke out against his son getting charge of the SC/ST welfare department. Are we not capable of looking after other departments, he asked | Latest News India", "content": "Former Bihar chief minister and Hindustani Awam Morcha (Secular) leader Jitan Ram Manjhi, who has been predicting the return of Nitish Kumar to the National Democratic Alliance (NDA) fold once again for the past six months, are giving sleepless night... [4417 chars]", "url": "https://www.hindustantimes.com/india-news/jiten-ram-manjhi-a-man-for-all-alliances-101707484505978.html", "image": "https://www.hindustantimes.com/ht-img/img/2024/02/09/1600x900/Jitan-Ram-Manjhi-in-Patna--PTI-_1700669262484_1707485039125.jpg", "publishedAt": "2024-02-09T13:27:25Z", "source": {"name": "Hindustan Times", "url": "https://www.hindustantimes.com"}}, {"title": "Pranab Mukherjee's daughter says attacked on internet for questioning Gandhis", "description": "Sharmistha Mukherjee claimed a supporter followed by senior Congress leaders said nasty things about her on social media. | Latest News India", "content": "New Delhi: Sharmistha Mukherjee, the daughter of former president Pranab Mukherjee, on Friday accused Congress supporters of viciously trolling her on social media for questioning the role of the Gandhi family in an interview last week. She said the ... [2405 chars]", "url": "https://www.hindustantimes.com/india-news/pranab-mukherjees-daughter-sharmistha-mukherjee-says-attacked-on-internet-for-questioning-gandhis-101707480959924.html", "image": "https://www.hindustantimes.com/ht-img/img/2024/02/09/1600x900/PTI12-05-2023-000223B-0_1701933722734_1707481152180.jpg", "publishedAt": "2024-02-09T12:24:48Z", "source": {"name": "Hindustan Times", "url": "https://www.hindustantimes.com"}}, {"title": "Lal Salaam audience review: Check out how social media reacts to Rajinikanth film; it's time for Thalaivar, say netizens", "description": "Rajinikanth's Lal Salaam, directed by Aishwarya Rajinikanth, is a social drama with a message that revolves around cricket and religion in a village.", "content": "Rajinikanth starrer \u2018Lal Salaam\u2019, coupled with the directorial skills of daughter Aishwarya Rajinikanth, is set to be a mega hit at the Box Office, whose story revolves around cricket and religion and how people in a village politicise a popular spor... [523 chars]", "url": "https://www.livemint.com/news/lal-salaam-audience-review-check-out-how-social-media-reacts-to-rajinikanth-starrer-it-s-a-wrap-say-netizens-11707468047926.html", "image": "https://www.livemint.com/lm-img/img/2024/02/09/1600x900/ls_1707471207656_1707471226456.jpg", "publishedAt": "2024-02-09T12:05:53Z", "source": {"name": "Mint", "url": "https://www.livemint.com"}}, {"title": "Google Rebrands Its Chatbot, Bard, As Gemini", "description": "Google, under Alphabet, advances in AI, rebranding its chatbot. This positions Google in direct rivalry with OpenAI, marking a pivotal moment in the AI competition.", "content": "Alphabet\u2019s Google has made significant strides in the realm of artificial intelligence (AI), recently rebranding its chatbot and introducing a new subscription plan. This move places Google in direct competition with its rival OpenAI, signaling a piv... [1394 chars]", "url": "https://currentaffairs.adda247.com/google-rebrands-its-chatbot-bard-as-gemini/", "image": "https://wpassets.adda247.com/wp-content/uploads/multisite/sites/5/2024/02/09165137/India-ranks-38th-out-of-139-countries-in-the-World-Banks-LPI-Report-202310.png", "publishedAt": "2024-02-09T11:24:52Z", "source": {"name": "Adda247", "url": "https://currentaffairs.adda247.com"}}, {"title": "Best phones under Rs 40,000 (Feb 2024): OnePlus 12R, Nothing Phone (2) to Samsung Galaxy S22 5G", "description": "We don\u2019t remember seeing most of these smartphones under Rs 40,000 in India ever before", "content": "Looking to buy a new smartphone under Rs 40,000? Drop everything you are doing and check this out right now! Never before do we remember seeing such a fine collection of phones at one time in this budget. And it\u2019s not even a festive season, unless yo... [7104 chars]", "url": "https://www.firstpost.com/tech/best-phones-under-rs-40000-feb-2024-oneplus-12r-nothing-phone-2-to-samsung-galaxy-s22-5g-13709022.html", "image": "https://images.firstpost.com/wp-content/uploads/2024/02/Nothing-Phone-2.jpg", "publishedAt": "2024-02-09T11:22:26Z", "source": {"name": "Firstpost", "url": "https://www.firstpost.com"}}, {"title": "Vaccination against cervical cancer; pilot project to be launched in Wayanad and Alappuzha", "description": "Plus one and plus two girl students to be vaccinated in both districts.kerala cervical cancer projects. kerala government hpv vaccination. cervical cancer. HPV tests. AIIMS-Delhi and the Indian Council of Medical Research. National Cancer Screening Programme. Visual Inspection with Acetic Acid", "content": "Alappuzha: In a major step aimed at eradicating cervical cancer, Kerala will launch a vaccination programme for plus one and plus two girl students in Alappuzha and Wayanad. The Health Department has issued an order approving the road map for the era... [1608 chars]", "url": "https://www.onmanorama.com/lifestyle/health/2024/02/09/kerala-cervical-cancer-alappuzha-wayanad-hpv-vaccine.html", "image": "https://img.onmanorama.com/content/dam/mm/en/lifestyle/health/images/2024/2/9/cervical-cancer-1.jpg", "publishedAt": "2024-02-09T11:13:19Z", "source": {"name": "Onmanorama", "url": "https://www.onmanorama.com"}}]}

#         # Append the new data to existing data
#         # Append the new articles to existing articles
#         # parsing_data["articles"] += new_data["articles"]

#         # request.session['parsing_data'] = parsing_data

#         # Return JsonResponse to inform the client about the success
#         articles = request.session.get('parsing_data',{})
#         if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#             data = {'articles': articles}

#             return JsonResponse(data)
        
#         else:

#             return render(request, "home.html", articles)
#     except Exception as e:
#         return JsonResponse({'error': str(e)})

# def home(request):
#    return redirect('view_article')


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

        # with open('api_response.json', 'w') as file:
        #     json.dump(Api_data, file)
    else:
        print(f"Error: {response.status_code}")
    
    # for item in headlines.get('articles', []):
    #     link = item.get("url", "")
    #     title = item.get("title", "")
    #     imgx = item.get("image", "")
    #     published_at = item.get("publishedAt")

    #     new_headline = Headline()
    #     new_headline.title = title
    #     new_headline.url = link
    #     new_headline.image = imgx
    #     new_headline.save()

    # Store parsing_data in the session
    request.session['parsing_data'] = parsing_data
    # Api_data = {"totalArticles": 98201, "articles": [{"title": "'Rashtra-neeti over rajneeti': PM Modi tells why his govt didn't bring 'White Paper' in 2014", "description": "Prime Minister Narendra Modi said on Friday, \u201cI could have bring the White paper in 2014\u2026 If I had to fulfil my political aspirations\u2026\u201d", "content": "Prime Minister Narendra Modi said on Friday, \u201cI could have bring the White Paper in 2014\u2026 If I had to fulfil my political aspirations, I would have presented those numbers before India (in 2014)\u2026It would have suited me politically, but national polic... [4258 chars]", "url": "https://www.livemint.com/news/india/pm-modi-says-could-have-brought-white-paper-in-2014-but-national-policy-new-initiatives-roadmap-10-points-11707492293948.html", "image": "https://www.livemint.com/lm-img/img/2024/02/09/1600x900/Prime-Minister-Narendra-Modi--PTI-_1707492671134_1707492684245.jpg", "publishedAt": "2024-02-09T15:27:26Z", "source": {"name": "Mint", "url": "https://www.livemint.com"}}, {"title": "Paytm fiasco: One97 Communication forms advisory panel headed by former SEBI chairman M Damodaran", "description": "The advisory panel to help Paytm address compliance and regulatory issues.", "content": "The owner of fintech firm Paytm, One 97 Communications Limited, on Friday announced the formation of an advisory committee chaired by former Securities and Exchange Board of India (SEBI) chairman M Damodaran. The committee will work closely with the ... [2244 chars]", "url": "https://www.livemint.com/companies/news/paytm-fiasco-one-97-communication-forms-group-advisory-committee-to-address-regulatory-matters-11707485708651.html", "image": "https://www.livemint.com/lm-img/img/2024/02/09/1600x900/Paytm_1707485993523_1707485993757.jpg", "publishedAt": "2024-02-09T13:44:55Z", "source": {"name": "Mint", "url": "https://www.livemint.com"}}, {"title": "Jiten Ram Manjhi, a man for all alliances", "description": "Manjhi spoke out against his son getting charge of the SC/ST welfare department. Are we not capable of looking after other departments, he asked | Latest News India", "content": "Former Bihar chief minister and Hindustani Awam Morcha (Secular) leader Jitan Ram Manjhi, who has been predicting the return of Nitish Kumar to the National Democratic Alliance (NDA) fold once again for the past six months, are giving sleepless night... [4417 chars]", "url": "https://www.hindustantimes.com/india-news/jiten-ram-manjhi-a-man-for-all-alliances-101707484505978.html", "image": "https://www.hindustantimes.com/ht-img/img/2024/02/09/1600x900/Jitan-Ram-Manjhi-in-Patna--PTI-_1700669262484_1707485039125.jpg", "publishedAt": "2024-02-09T13:27:25Z", "source": {"name": "Hindustan Times", "url": "https://www.hindustantimes.com"}}, {"title": "Pranab Mukherjee's daughter says attacked on internet for questioning Gandhis", "description": "Sharmistha Mukherjee claimed a supporter followed by senior Congress leaders said nasty things about her on social media. | Latest News India", "content": "New Delhi: Sharmistha Mukherjee, the daughter of former president Pranab Mukherjee, on Friday accused Congress supporters of viciously trolling her on social media for questioning the role of the Gandhi family in an interview last week. She said the ... [2405 chars]", "url": "https://www.hindustantimes.com/india-news/pranab-mukherjees-daughter-sharmistha-mukherjee-says-attacked-on-internet-for-questioning-gandhis-101707480959924.html", "image": "https://www.hindustantimes.com/ht-img/img/2024/02/09/1600x900/PTI12-05-2023-000223B-0_1701933722734_1707481152180.jpg", "publishedAt": "2024-02-09T12:24:48Z", "source": {"name": "Hindustan Times", "url": "https://www.hindustantimes.com"}}, {"title": "Lal Salaam audience review: Check out how social media reacts to Rajinikanth film; it's time for Thalaivar, say netizens", "description": "Rajinikanth's Lal Salaam, directed by Aishwarya Rajinikanth, is a social drama with a message that revolves around cricket and religion in a village.", "content": "Rajinikanth starrer \u2018Lal Salaam\u2019, coupled with the directorial skills of daughter Aishwarya Rajinikanth, is set to be a mega hit at the Box Office, whose story revolves around cricket and religion and how people in a village politicise a popular spor... [523 chars]", "url": "https://www.livemint.com/news/lal-salaam-audience-review-check-out-how-social-media-reacts-to-rajinikanth-starrer-it-s-a-wrap-say-netizens-11707468047926.html", "image": "https://www.livemint.com/lm-img/img/2024/02/09/1600x900/ls_1707471207656_1707471226456.jpg", "publishedAt": "2024-02-09T12:05:53Z", "source": {"name": "Mint", "url": "https://www.livemint.com"}}, {"title": "Google Rebrands Its Chatbot, Bard, As Gemini", "description": "Google, under Alphabet, advances in AI, rebranding its chatbot. This positions Google in direct rivalry with OpenAI, marking a pivotal moment in the AI competition.", "content": "Alphabet\u2019s Google has made significant strides in the realm of artificial intelligence (AI), recently rebranding its chatbot and introducing a new subscription plan. This move places Google in direct competition with its rival OpenAI, signaling a piv... [1394 chars]", "url": "https://currentaffairs.adda247.com/google-rebrands-its-chatbot-bard-as-gemini/", "image": "https://wpassets.adda247.com/wp-content/uploads/multisite/sites/5/2024/02/09165137/India-ranks-38th-out-of-139-countries-in-the-World-Banks-LPI-Report-202310.png", "publishedAt": "2024-02-09T11:24:52Z", "source": {"name": "Adda247", "url": "https://currentaffairs.adda247.com"}}, {"title": "Best phones under Rs 40,000 (Feb 2024): OnePlus 12R, Nothing Phone (2) to Samsung Galaxy S22 5G", "description": "We don\u2019t remember seeing most of these smartphones under Rs 40,000 in India ever before", "content": "Looking to buy a new smartphone under Rs 40,000? Drop everything you are doing and check this out right now! Never before do we remember seeing such a fine collection of phones at one time in this budget. And it\u2019s not even a festive season, unless yo... [7104 chars]", "url": "https://www.firstpost.com/tech/best-phones-under-rs-40000-feb-2024-oneplus-12r-nothing-phone-2-to-samsung-galaxy-s22-5g-13709022.html", "image": "https://images.firstpost.com/wp-content/uploads/2024/02/Nothing-Phone-2.jpg", "publishedAt": "2024-02-09T11:22:26Z", "source": {"name": "Firstpost", "url": "https://www.firstpost.com"}}, {"title": "Vaccination against cervical cancer; pilot project to be launched in Wayanad and Alappuzha", "description": "Plus one and plus two girl students to be vaccinated in both districts.kerala cervical cancer projects. kerala government hpv vaccination. cervical cancer. HPV tests. AIIMS-Delhi and the Indian Council of Medical Research. National Cancer Screening Programme. Visual Inspection with Acetic Acid", "content": "Alappuzha: In a major step aimed at eradicating cervical cancer, Kerala will launch a vaccination programme for plus one and plus two girl students in Alappuzha and Wayanad. The Health Department has issued an order approving the road map for the era... [1608 chars]", "url": "https://www.onmanorama.com/lifestyle/health/2024/02/09/kerala-cervical-cancer-alappuzha-wayanad-hpv-vaccine.html", "image": "https://img.onmanorama.com/content/dam/mm/en/lifestyle/health/images/2024/2/9/cervical-cancer-1.jpg", "publishedAt": "2024-02-09T11:13:19Z", "source": {"name": "Onmanorama", "url": "https://www.onmanorama.com"}}]}
    
    # request.session['parsing_data'] = headlines
    # return redirect("../")
    # context = {
    # "articles": '',
    # "headlines": headlines,
    # }
    # print(context["object_list"])
    # return render(request, "home.html", context)
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


