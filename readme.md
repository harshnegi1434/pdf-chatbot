# PDF Chatbot

This is a simple Streamlit app that allows users to ask questions from PDF documents using a chatbot interface. The chatbot leverages Langchain for natural language processing tasks.

## Setup and Dependencies

### Environment Setup
1. Ensure you have Python installed on your system.
2. Clone this repository to your local machine.

### Installationv
1. Install the required Python packages by running `pip install -r requirements.txt`.

### Dependencies
- Python 3.11
- Streamlit
- PyPDF2
- Dotenv
- Langchain
- Langchain Community
- Langchain OpenAI

## Usage
1. Place your PDF files in the `pdfs` directory within the project folder.
2. Obtain an API key from OpenAI.
3. Create a `.env` file in the project directory and provide your OpenAI API key in the following format: OPENAI_API_KEY = your_openai_api_key_here
1. Run the Streamlit app by executing `streamlit run app.py` in your terminal.
2. The app will open in your default web browser.
3. Choose the desired PDF from the sidebar dropdown menu.
4. Type your questions related to the selected PDF in the chat window.
5. The chatbot will provide answers based on the content of the PDF.

## Files
- `app.py`: Contains the main Streamlit app code.
- `requirements.txt`: Lists all Python dependencies required to run the app.
- `README.md`: This file, providing information about the app.
- `dockerfile`: For creating dockerimage

## Credits
- This app utilizes Streamlit, PyPDF2, Dotenv, Langchain, and Langchain Community libraries for its functionality.

## Note
- Ensure that the PDF files are placed in the `pdfs` directory.
- The app creates and uses pickled files to store processed data and vector stores for efficiency.
- Adjustments may be needed based on specific PDF formats and contents.

## Docker Setup

### Dockerfile
1. Create a Dockerfile in the project directory with the following content:

```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port number the app runs on
EXPOSE 8501

# Run app.py when the container launches
CMD ["streamlit", "run", "app.py"]