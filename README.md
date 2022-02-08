# SecureFileTransfer

A django application that allows you transfer files securely by generating a secure link and password.

## Running the Application on your local machine (make sure you already have pyton3 and pip installed)

1. Using the template provided in the '.env.dev.example file', create a .env file with local inputing all the configurations.
2. Go back one directory and create a virtual environment by running **python3 -m venv 'whatever name you decide'**
3. Activate the virtual environment by running **source bin/activate** while in the venv directory.
4. Navigate back into the project root directory and run **pip install -r requirements.txt**
5. Migrate your tables to the database by running **python3 manage.py makemigrations** && **python3 manage.py migrate**
6. Run the app by typing **python3 manage.py runserver**
