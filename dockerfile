# 1. Use an official Python base image
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /code

# 3. Copy the requirements file first (better for caching)
COPY ./requirements.txt /code/requirements.txt

# 4. Install the dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 5. Copy the 'app' folder into the container
COPY ./app /code/app    

# 6. Command to run the FastAPI app using Uvicorn
# We use 0.0.0.0 so it's accessible from outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]