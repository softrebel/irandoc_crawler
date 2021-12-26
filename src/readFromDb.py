import json
from src.Models.tmuModels import *
from src.tmuRepository import *
import os
# import pandas as pd


_repository = TmuRepository()

row=_repository.get_all_tags()
# df = pd.Daframe