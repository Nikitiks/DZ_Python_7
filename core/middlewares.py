from django.http import HttpRequest, HttpResponse
import time

class LimitedQueriesMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.paths = {}
        self.limit:int = 3
        self.time_limit = 60

    def __call__(self, request:HttpRequest):
        query = request.path_info
        now = time.time()

        if(query not in self.paths):
            self.paths[query] = {"first_visit": now, "count": 1}

        else:
            record = self.paths[query]

            if(now - record["first_visit"] > self.time_limit):
                self.paths[query] = {"first_visit": now, "count": 1}
            else:
                record["count"] += 1
                if(record["count"] > self.limit):
                    return HttpResponse("<h1>This query has reached its limit</h1>")
            
        return self.get_response(request)
        
