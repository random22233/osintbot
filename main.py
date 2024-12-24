from flask import Flask  
# from app.routers import start, fullname, email, phone, skype  
from app.routers import email, username  

app = Flask(__name__)  

# Register all blueprints (routers)  
# app.register_blueprint(start.router)  
# app.register_blueprint(fullname.router)  
app.register_blueprint(email.router)  
app.register_blueprint(username.router)  
# app.register_blueprint(phone.router)  
# app.register_blueprint(skype.router)  

if __name__ == "__main__":  
    app.run(host='0.0.0.0', port=5000, debug=True)