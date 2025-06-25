
#AIzaSyALP0INRIK4O873yyJj5M92ehlj5qGbn6Q
import getpass
import os
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GOOGLE_API_KEY"] = "AIzaSyALP0INRIK4O873yyJj5M92ehlj5qGbn6Q"

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)