# Back End API 
This repo is for the Phyton Flask Based API with full deployment of docker registry and azure devops

# Installation
```bash
# Please install python 3.4+ in your system minimum
# Install pipenv
pip install pipenv

# Install requirements
pipenv install -r requirements.txt

# Run the pipenv shell
pipenv shell

# create a .env that contains following information for dev/staging/prod:
# SENDGRID_API_KEY
# HASH_KEY
# BOILERPLATE_ENV
# AZURE_B2C_CLIENT_ID 
# AZURE_B2C_SECRET 
# AZURE_B2C_SCOPE 
# AZURE_B2C_TENENT
# DATABASE_NAME

# or update the value itself in config.py

# Please update mongo_uri in config.py and use localhost (MONGO_URI = "mongodb://localhost:27017/") for backend testing purposes to reduce server consumption

# Run the application from backendirectory
python wsgi.py

# Use mongocompass to check localhost database
```
# Build and Test
Docker Build 
```bash
docker build -t api:1.0 -f Dockerfile .
```

Docker Run
```bash
docker run -p 5000:5000 -e SENDGRID_API_KEY=<your send grid key> -e HASH_KEY=<your hash key> -e BOILERPLATE_ENV=<dev/prod/test> magic-ats-backend-api:1.0
```

Test 
```bash
python -m manage.py test  
```

