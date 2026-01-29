import json
import os
from utils.embedding import CVEmbeddingStore
from typing import List
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def prompt(context:List[str], questions:str) -> str:
    pass

