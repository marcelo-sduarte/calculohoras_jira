"""
Contem todas as bibliotecas usadas na automação
"""
import boto3
import codecs
import calendar
from collections import Counter
from datetime import date, timedelta, datetime
import datetime
from enum import Enum
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import glob
import json
from jira import JIRA
from jira.resources import Issue
import logging, os
import locale
import libs
from libs import lib_logging,lib_spreadsheet, lib_json, lib_process, lib_calendar,lib_email, lib_jira
import numpy as np
import math
import pandas as pd
import random
import re
import requests
import shutil
import subprocess
import smtplib
import traceback
import time
from typing import Union
import win32cred
from unidecode import unidecode 
import unicodedata











