from django.shortcuts import render,HttpResponse,redirect
import pymongo
from django.http import JsonResponse
from django.contrib.auth import logout
from django.urls import reverse
from .forms import FeedbackForm
from .models import UserProfile
from django.contrib.messages import info
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
import subprocess
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .forms import AvatarUploadForm
from .forms import SignUpForm, LoginForm
import uuid
from pymongo import MongoClient
from .models import User
import  google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import pandas as pd
import ast 
genai.configure(api_key="AIzaSyBNOgQu4Lu8lFuZbj3rs3Cn09n3bXddNyg")
model = genai.GenerativeModel('gemini-pro')
from .forms import MyForm
from .forms import FeedbackForm
# Create your views here.student
def index(request):
    context={
        "variable1":"this is sentence of yash",
        "variable2":"this is second sentence"
    }
    return render(request,'index.html')

# def searchcompanies(request):
#     return render(request,'searchcompanies.html')

def sendemail(request):
    return render(request,'sendemail.html')

def contact(request):
    return render(request,'feedback.html')

@login_required
def yourimprovement(request):
    return render(request,'yourimprovement.html')

@login_required
def my_view(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            location = cleaned_data['location']
            domain = cleaned_data['domain']
            search_uqid = cleaned_data['search_id']
            print("unique search id", search_uqid)
            print(location, domain)
            aimodel(domain, location, search_uqid)
            # Redirect to company_list view with search_uqid as URL parameter
            return redirect('company_list', search_uqid=search_uqid)
    else:
        form = MyForm()  # Create an empty form for GET requests

    context = {'form': form}
    return render(request, 'searchcompanies.html', context)


def connect_to_mongodb(uri="mongodb+srv://yashchindalia77:careernest9872@cluster1.8zgliyq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1"):

  try:
    client = pymongo.MongoClient(uri)
    print("Connection established successfully!")
    return client
  except pymongo.errors.ConnectionFailure as err:
    print("Error connecting to MongoDB:", err)
    raise

# Example usage (replace URI with your actual connection details)
client = connect_to_mongodb("mongodb+srv://yashchindalia77:careernest9872@cluster1.8zgliyq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1")  
def aimodel(domain,location,search_uqid):
    format_ofdata = ["",""]
    prompt = f"""
    You need to do these tasks:
    1) Strictly give 60 small and mid-level companies data that works in this domain {domain} and near to this city {location}.
    2) Strictly if you are unable to find some companies then give the companies name from another city that is near to that city.
    3) Strictly make sure to prioritize more to involve mid-level,startups and mncs companies also in the companies.
    4) Strictly give me just names. Don't give brief about the companies and extra titles like large company, small company, just give me names of all companies.
    5) Strictly make sure to end the response in the python list for example in this format {format_ofdata}
    6) strictly make sure the data is correct and accurate .
    7) Strictly give the details in this format {format_ofdata} .
    8) strictly if response is not complete then remove one company and close that with proper list [].
    """

        
    completion = model.generate_content(contents=prompt)
    response = completion.text
    print("response",response)
    cleaned_string = response.replace("```","")
    cleaned_string = response.replace("```","")
    print("cleaned string",cleaned_string)

    # print("type of the response",type(response),response)
    dictionary = ast.literal_eval(cleaned_string)
    print("dictionary is actual response",dictionary)
    # print("dictionary output",type(dictionary),dictionary)
    # Access the database and collections
    database = client["djongo_test"]
    collection = database["testing"]
    # print("collection",collection)
    # Use the collection object to interact with your MongoDB database (insert, find, etc.)
    data={"job_title":domain,"location":location}
    # Remember to close the connection after you're done (if using a client object)
    # client.close()

    for company in dictionary:
        data["_id"]=str(uuid.uuid4())
        data['searchunique_id']=search_uqid
        data['companyname']=company
        # data['linkdin_link']=company["linkdin_link"]
        # data['hr_name']=company["hr_name"]
        # data['hr_email_id']=company["hr_email_id"]
        # data['_id']=str(uuid.uuid4()),
        # data['_id']=str(uuid.uuid4()),
        print("data",data)
        insert=collection.insert_one(data)
        print("insert done",insert)
        client.close()
    return search_uqid

@login_required
def company_list(request, search_uqid):
    client = MongoClient('mongodb+srv://yashchindalia77:careernest9872@cluster1.8zgliyq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1', 27017)
    db = client['djongo_test']
    collection = db['testing']
    
    # Query MongoDB with the searchunique_id
    selection = {"searchunique_id": search_uqid}
    filtered_documents = collection.find(selection)
    documents_list = list(filtered_documents)
    
    print("Filtered documents:", documents_list)
    document_count = collection.count_documents(selection)
    print("Number of documents:", document_count)
    
    client.close()
    
    return render(request, 'company_list.html', {
        'companies': documents_list,
        'search_uqid': search_uqid 
    })
    
@login_required
def export_to_excel(request, search_uqid):
    client = MongoClient('mongodb+srv://yashchindalia77:careernest9872@cluster1.8zgliyq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1', 27017)
    db = client['djongo_test']
    collection = db['testing']
    
    # Query MongoDB with the searchunique_id
    selection = {"searchunique_id": search_uqid}
    filtered_documents = list(collection.find(selection))
    
    # Create a DataFrame from the MongoDB query
    df = pd.DataFrame(filtered_documents)
    
    # Drop the MongoDB ObjectId as it's not serializable
    df.drop(columns=['_id'], inplace=True)
    
    # Create a HttpResponse object with the appropriate header for an Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=companies_{search_uqid}.xlsx'
    
    # Use pandas to write the DataFrame to an Excel file
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Companies')
    
    return response



########################################chatbot##########################################
def chat_with_gemini(user_input):
    # Configure Gemini
    genai.configure(api_key="AIzaSyBNOgQu4Lu8lFuZbj3rs3Cn09n3bXddNyg")

    # Define generation configuration
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    # Define safety settings
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    }
    firstquestion=f"Hi , i am your interviewer and i will take your mock interview . first tell me in which domain you want to take mock interview"
    # Define initial chat settings
    system_instruction = f"""you are a technical interviewer. take the interview of the candidate.
    1)ask the domain of the candidate and then ask questions to the candidate .
    2)make sure to do the counter question on the user response.
    3)strictly ask questions one by one for example ask one question then wait for the user response and then ask the counter question.
    """,
    model_name = "gemini-1.5-pro"

    # Initialize the Gemini model
    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config,
        system_instruction=system_instruction,
        safety_settings=safety_settings,
    )

    # Start the chat session with initial history
    chat_session = model.start_chat(history=[{"role": "user", "parts": [user_input]}])

    # Interact with the chat session and get the response
    response = chat_session.send_message(user_input)
    bot_response = response.text

    return bot_response

conversation={"conversation_unique_id":str(uuid.uuid4())[:24]}
client = connect_to_mongodb("mongodb+srv://yashchindalia77:careernest9872@cluster1.8zgliyq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1")  
db = client['djongo_test']
collection = db['conversation']
# Django view to handle chatbot interaction
# Django view to handle chatbot interaction
# @login_required
# def chatbot_interaction(request):
#     if request.method == 'POST':
#         user_input = request.POST.get('user_input', '').strip()
#         if user_input:
#             conversation = {
#                 "_id": str(uuid.uuid4()),
#                 "user_input": user_input,
#                 "conversation_unique_id": str(uuid.uuid4())[:24]
#             }

#             # Chat with Gemini
#             bot_response = chat_with_gemini(user_input)
#             format_of_improved={"improved_response":""}
#             conversation['ai_response'] = bot_response
#             prompt = f"""you have given the {bot_response} question.
#                 1)you need to give  more technical way to give the response.
#                 2)strictly in this format {format_of_improved}
#                 3)strictly end the response in dictionary like {format_of_improved}
#                 """

#             # Generate response using Gemini
#             completion = model.generate_content(prompt)
#             response = completion.text

#             # Clean response and insert into MongoDB
#             cleaned_string = response.replace("```", "")
#             response_dict = ast.literal_eval(cleaned_string)
#             response_dictt=response_dict['improved_response']
#             # print("improved response",type(response_dict),response_dict)
#             conversation['improved_response']=response_dictt
#             print("conversation",type(conversation['improved_response']),conversation['improved_response'])
#             # Insert conversation into MongoDB
#             insert_result = collection.insert_one(conversation)
#             # print("insert result",insert_result)
#             return JsonResponse({'response': bot_response})
#         else:
#             return JsonResponse({'response': 'Please provide a non-empty input'})
#     else:
#         return JsonResponse({'response': 'Invalid request method'})


# def get_collection():
#     client = connect_to_mongodb("mongodb+srv://yashchindalia77:careernest9872@cluster1.8zgliyq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1") 
#     db = client['djongo_test']  # Replace with your database name
#     collection = db['conversation']  # Replace with your collection name
#     return collection

# @login_required
# def show_data(request):
#     collection = get_collection()
#     # Fetch only the required fields
#     data = collection.find({}, {'_id': 0, 'user_input': 1, 'ai_response': 1, 'improved_response': 1})
    
#     # Convert the cursor to a list
#     data_list = list(data)
#     # print("data ",data_list)
#     return render(request, 'show_data.html', {'data': data_list})

@login_required
def chatbot_interaction(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '').strip()
        if user_input:
            conversation = {
                "_id": str(uuid.uuid4()),
                "user_input": user_input,
                "conversation_unique_id": str(uuid.uuid4())[:24],
                "user_id": request.user.id  # Add user_id to the conversation
            }

            # Chat with Gemini
            bot_response = chat_with_gemini(user_input)
            format_of_improved = {"improved_response": ""}
            conversation['ai_response'] = bot_response
            prompt = f"""you have given the {bot_response} question.
                1)you need to give more technical way to give the response.
                2)strictly in this format {format_of_improved}
                3)strictly end the response in dictionary like {format_of_improved}
                4)stricltly end the response with proper {format_of_improved} closer of the dictionary .
                """

            # Generate response using Gemini
            completion = model.generate_content(prompt)
            response = completion.text

            # Clean response and insert into MongoDB
            cleaned_string = response.replace("```", "")
            response_dict = ast.literal_eval(cleaned_string)
            response_dictt = response_dict['improved_response']
            conversation['improved_response'] = response_dictt

            # Insert conversation into MongoDB
            insert_result = get_collection().insert_one(conversation)

            return JsonResponse({'response': bot_response})
        else:
            return JsonResponse({'response': 'Please provide a non-empty input'})
    else:
        return JsonResponse({'response': 'Invalid request method'})

def get_collection():
    client = connect_to_mongodb("mongodb+srv://yashchindalia77:careernest9872@cluster1.8zgliyq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1")
    db = client['djongo_test']  # Replace with your database name
    collection = db['conversation']  # Replace with your collection name
    return collection

@login_required
def show_data(request):
    collection = get_collection()
    user_id = request.user.id  # Get the current user's ID
    # Fetch only the required fields for the current user
    data = collection.find({"user_id": user_id}, {'_id': 0, 'user_input': 1, 'ai_response': 1, 'improved_response': 1})

    # Convert the cursor to a list
    data_list = list(data)

    return render(request, 'show_data.html', {'data': data_list})

def feedback_view(request):
    print("inside the feedback")
    if request.method == 'POST':
        print("inside the feedback post")
        form = FeedbackForm(request.POST)
        print("inside the form in the feedback")
        if form.is_valid():
            print("inside the form valid")
            form.save()
            print("Feedback saved successfully")  # Add for debugging
            return redirect('feedback_success')  # Ensure this URL name matches your URLconf
        else:
            print("Form errors:", form.errors)  # Add for debugging
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})

def feedback_success(request):
    print("printfeedback successs")
    return render(request, 'feedback_success.html')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            print("Form errors:", form.errors)  # Add this to print form errors
    else:
        form = SignUpForm()
        print("else of the signup")
    return render(request, 'signup.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a home page after successful login
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

@login_required
def account_section(request):
    return render(request, 'account_section.html')

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(reverse('login'))

@login_required
def upload_avatar(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = AvatarUploadForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account_section')  # Redirect to the profile page after upload
    else:
        form = AvatarUploadForm(instance=profile)

    return render(request, 'upload_avatar.html', {'form': form})
def profile_view(request):
    # Your logic to fetch and display user profile
    return render(request, 'account_profile.html', {'user': request.user})