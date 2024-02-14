import json
import uuid
import gspread
import logging
import numpy as np
import pandas as pd
import oauth2client as oauth2client
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
# import smtplib
# from email.mime.text import MIMEText

if len(logging.getLogger().handlers) > 0:
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)

def get_database():
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('./credentials.json', scope)
    # authorize the clientsheet
    client = gspread.authorize(creds)
    # get the instance of the Spreadsheet
    sheet = client.open('database').sheet1
    data_instance = sheet.get_all_records()
    df = pd.DataFrame.from_dict(data_instance)
    return df,sheet

def check_availability(username,email_id,dataframe):
    username_row_index = np.where(dataframe["username"] == str(username).lower())
    email_row_index = np.where(dataframe["email_id"] == str(email_id).lower())
    username_flag = np.array_equal(username_row_index[0], np.array([])) if username_row_index and len(username_row_index) > 0 else True
    email_id_flag = np.array_equal(email_row_index[0], np.array([])) if email_row_index and len(email_row_index) > 0 else True
    return username_flag,email_id_flag

def insert_credentials_into_database(data):
    try:
        spreadsheet = get_database()
        dataframe = spreadsheet[0]
        sheet = spreadsheet[1]
        date_time_stamp = str(datetime.now())
        sr_no = len(dataframe)+1
        new_uuid = str(uuid.uuid4())
        username = data['username'].lower()
        password = data['password']
        email_id = data['email_id'].lower()
        first_name = data['first_name']
        last_name = data['last_name']
        gender = data['gender']
        contact_no = data['contact_no']
        list = [date_time_stamp,sr_no,new_uuid,username,password,email_id,first_name,last_name,gender,contact_no]
    except Exception as e:
        logging.exception(f"Unexpected error in get_database(): {e}")
        return None
    try:
        availability_flags = check_availability(username,email_id,dataframe)
        username_availability = availability_flags[0]
        email_id_availability = availability_flags[1]
        try:
            if username_availability and email_id_availability:
                sheet.insert_row(list,2)
                response_string = f'username is : {username} and password is : {password}'
                logging.info(f'Account created successfully! You can now proceed :) {response_string}')
                return f'Account created successfully! You can now proceed :) {response_string}'
            elif not username_availability:
                logging.info(f'Failed to create account! Username already exists :(')
                return f'Failed to create account! Username already exists :('
            elif not email_id_availability:
                logging.info(f'Failed to create account! Email id already exists :(')
                return f'Failed to create account! Email id already exists :('
            elif not username_availability and not email_id_availability:
                logging.info(f'Failed to create account! Both Username and Email id already exists :(')
                return f'Failed to create account! Both Username and Email id already exists :('
            else:
                logging.info(f'Unexpected error: Failed to create account!')
                return f'Unexpected error: Failed to create account! :('
        except Exception as e:
            logging.exception(f"Unexpected error in inserting row: {e}")
            return None
    except Exception as e:
        logging.exception(f"Unexpected error in check_availability(): {e}")
        return None
