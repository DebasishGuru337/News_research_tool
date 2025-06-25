FROM python:3-alpine3.15

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any need packages specified in requirements.text
RUN  pip install -r requirements.txt

# Make port 30001 available to the word outside for this container
EXPOSE 30001


# Install streamlit
RUN pip install streamlit

# Run app.py when the container lunches
CMD [ "python","app.py" ]



