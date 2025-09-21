
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException



app = FastAPI() 


class EmailService: 
    def send_email(self, recipient: str, message: str): 
        print(f"Sending email to {recipient}: {message}")

def get_email_service(): 
    return EmailService() 


email_service_dependency = Annotated[EmailService, Depends(get_email_service)]


def send_email(recipient: str, message: str, 
               email_service: email_service_dependency): 
    email_service.send_email(recipient, message)

    

class AuthService: 
    def authenticate(self, token:str): 
        if token == 'valid-token': 
            return True 
        else: 
            raise HTTPException(status_code=401, detail='Unauthorized')
        

def get_auth_service():
    return AuthService() 

auth_service_dependency = Annotated[AuthService, Depends(get_auth_service)]


@app.get("/secure-data/")
def get_secure_data(token:str, auth_service: auth_service_dependency): 
    if auth_service.authenticate(token): 
        return {"data": "this is secure data"}