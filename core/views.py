from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from .models import Task
from .serializers import TaskSerializer
import json
from django.urls import reverse

tasks = []

def get_tasks(request:HttpRequest):
    return JsonResponse(tasks, TaskSerializer, safe=False)

def delete_task(request:HttpRequest, id):
    if id is None:
        return JsonResponse({"message": "Bad Request", "status_code": 400})
    if len(tasks) == 0:
        return JsonResponse({"message": "Tasks not found", "status_code": 404})
    
    for task in tasks:
        if(task.id == id):
            del task
            return JsonResponse({"message": "Tasks deleted", "status_code": 200})
        
    return JsonResponse({"message": "Task not found", "status_code": 404})

@csrf_exempt
def add_task(request:HttpRequest):
    if request.method == "POST":
        header = request.POST.get("header", None)
        text = request.POST.get("text", None)
        date_start = request.POST.get("date_start", None)
        date_end = request.POST.get("date_end", None)

        if header is not None and text is not None and date_start is not None and date_end is not None:
            tasks.append(Task(header,text,date_start,date_end))
            return JsonResponse({"message": "Task added", "status_code": 200})
    return JsonResponse({"message": "Bad Request", "status_code": 400})

cache = {}
items = []

def getItemById(request:HttpRequest, id):
    if len(items) < 0:
        return JsonResponse({"message":"Items is empty"})
    
    if(id in cache):
        print("From cache")
        return JsonResponse(cache[id])
    
    item = filter(lambda x: x.id == id, items)

    if len(item) < 1:
        return JsonResponse({"message":"Item not found"})
    
    cache[id] = item[0]

    return JsonResponse(item[0])

@csrf_exempt
def postBookJson(request:HttpRequest):
    
    if(request.method == "POST"):

        data = json.loads(request.body.decode('utf-8'))

        title = data.get("title")
        description = data.get("description")
        year = data.get("year")

        if( not isinstance(title, str) or not isinstance(description, str) or not str(year).isdigit()):
             return JsonResponse({"error": "Invalid data"})

        normalized = {
            "title": title.capitalize(),
            "description": description.capitalize(),
            "year": int(year)
        }

        return JsonResponse(normalized)
    
    return JsonResponse({"error": "Only POST allowed"})

def redirectUserAgent(request:HttpRequest):
    header = request.META["HTTP_USER_AGENT"]

    if("Windows" in header or "Linux" in header or "Mac" in header):
        return HttpResponseRedirect(reverse("pcPage"))
    elif("iPhone" in header or "Android" in header):
        return HttpResponseRedirect(reverse("mobilePage"))
    
def pcPage(request:HttpRequest):
    return HttpResponse("<h1>Добро пожаловать на компьютерную версию</h1>")

def mobilePage(request:HttpRequest):
    return HttpResponse("<h1>Добро пожаловать на мобильную версию</h1>")

data_dict = {}

def getData(request:HttpRequest, key):
    if(key in data_dict):
        return JsonResponse({"data":data_dict[key]})
    
    return JsonResponse({"status":404})

@csrf_exempt
def postData(request:HttpRequest):

    if(request.method == "POST"):
        key = request.POST.get('key',None)
        data = request.POST.get('data',None)

        data_dict[key] = data
        return JsonResponse({"message":"Added data" ,'status':200}) 
    
    return JsonResponse({"message":"Only POST allowed"})