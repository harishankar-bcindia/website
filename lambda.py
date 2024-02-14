import logging
import json
from main import insert_credentials_into_database

if len(logging.getLogger().handlers) > 0:
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(level=logging.INFO)

def lambda_handler(event, context):
    # TODO implement
    logging.info(event)
    # Get the header
    try:
        username = event.get('headers', {}).get('username')
        password = event.get('headers', {}).get('password')
        email_id = event.get('headers', {}).get('email_id')
        logging.info(f'username:{username} password: {password} email_id: {email_id}')
        if username!=None and password!=None and email_id!=None:
            first_name,last_name,gender,contact_no = '','','',''
            try:
                first_name = event.get('headers', {}).get('first_name')
                last_name = event.get('headers', {}).get('last_name')
                gender = event.get('headers', {}).get('gender')
                contact_no = event.get('headers', {}).get('contact_no')
            except Exception as e:
                logging.exception(f'Non-mandatory fields are not provided: {e}')
            finally:
                data = {
                        'username' : str(username),
                        'password' : str(password),
                        'email_id' : str(email_id),
                        'first_name' : str(first_name),
                        'last_name' : str(last_name),
                        'gender' : str(gender),
                        'contact_no' : str(contact_no)
                    }
                try:
                    result = insert_credentials_into_database(data)
                    if result is not None:
                        logging.info(f'Request processed successfully:\n{result}')
                        return {
                                'statusCode': 200,
                                'body': json.dumps(result)
                            }
                    else:
                        logging.info(f'Got None response in result from create.py file')
                        return {
                                'statusCode': 500,
                                'body': json.dumps('We apologize for the inconvenience. Our server encountered an unexpected issue that prevented us from fulfilling your request. Please try again later')
                            }
                except Exception as e:
                    logging.info(f'Unexpected error in calling result(create.py) file: {e}')
                    return {
                            'statusCode': 500,
                            'body': json.dumps('We apologize for the inconvenience. Our server encountered an unexpected issue that prevented us from fulfilling your request. Please try again later')
                        }

        else:
            logging.info(f'username,password and email_id are mandatory :(')
            return {
                    'statusCode': 400,
                    'body': json.dumps('username,password and email_id are mandatory :(')
                }
    except Exception as e:
        logging.info(f'Provide username,password and email_id in headers! :( {e}')
        return {
            'statusCode': 400,
            'body': json.dumps('Provide username,password and email_id in headers!')
        }
