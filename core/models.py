from django.db import models
import datetime
from . import utils

class Task:
    id:int
    header:str
    text:str
    date_start:datetime
    date_end:datetime

    def __init__(self, header:str, text:str, date_start:datetime, date_end:datetime):
        self.id = utils.get_current_timestamp()
        self.header = header
        self.text = text
        self.date_start = date_start
        self.date_end = date_end
