from fastapi import FastAPI, Request, Response 
from starlette.middleware.base import BaseHTTPMiddleware 
import time 
from collections import defaultdict 
from typing import Dict 


app = FastAPI() 



class AdvancedMiddleware(BaseHTTPMiddleware): 
    def __init__(self, app): 
        super().__init__(app) 
        self.rate_limit_records: Dict[str, float] = defaultdict(float) 


    async def log_message(self, message:str): 
        print(message) 

    async def dispatch(self, request, call_next):
        clientip = request.client.host
        current_time = time.time() 
        if current_time - self.rate_limit_records[clientip] < 1: # 1 request per record limit 
            return Response(content="rate limit exceeded", status_code=429)
        
        self.rate_limit_records[clientip] = current_time 
        path = request.url.path 
        await self.log_message(f"Request to {path}")


        # Process the requst 
        start_time = time.time() 
        response = await call_next(request) 
        process_time = time.time() - start_time


        # add custom headerswithout modifying the original headers object 
        custom_headers = {"X-Process-Time": str(process_time)}
        for header, value in custom_headers.items(): 
            response.headers.append(header, value) 
        

        # asynchronous logging for processi0ng time 
        await self.log_message(f"Response for {path} took {process_time} seconds")
        return response 
    

app.add_middleware(AdvancedMiddleware) 


@app.get("/")
async def main(): 
    return {"message": "hello, world"}