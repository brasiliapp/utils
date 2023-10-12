from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def get_and_check_is_not_null(variable_name: str):
    value = os.getenv(variable_name)
    
    if value is None:
        raise ValueError(f"You should provide a value for {variable_name} in .env file!")
    
    return value
    

DEPUTY_DATA_ENDOINT = get_and_check_is_not_null('DEPUTY_DATA_ENDOINT')

LEGISLATURE_ID = int(get_and_check_is_not_null('LEGISLATURE_ID'))

DEPUTY_TO_SKIP_GABINET_DATA = int(get_and_check_is_not_null('DEPUTY_TO_SKIP_GABINET_DATA'))

DEPUTY_TO_SKIP_SPEECH_DATA = int(get_and_check_is_not_null('DEPUTY_TO_SKIP_SPEECH_DATA'))

INITIAL_DATE_DEPUTY_SPEECH_SEARCH = get_and_check_is_not_null('INITIAL_DATE_DEPUTY_SPEECH_SEARCH')

FINAL_DATE_DEPUTY_SPEECH_SEARCH = get_and_check_is_not_null('FINAL_DATE_DEPUTY_SPEECH_SEARCH')