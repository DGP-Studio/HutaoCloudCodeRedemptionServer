import uuid
import os
from db_connection import db
from datetime import datetime


def generate_redemption_code():
    # Generate a 16-character redemption code
    return str(uuid.uuid4())[:18].upper()


def validate_redemption_code(code: str):
    # Check if the code is valid
    # Return True if valid, False if invalid
    sql_select = r"SELECT code FROM exchangeable WHERE code = '%s' LIMIT 1" % code
    result = db.fetch_one(sql=sql_select)
    if result is None:
        return False
    else:
        return True


def get_code_value(code: str) -> int:
    # Get the value of the code
    sql_select = r"SELECT value FROM exchangeable WHERE code = '%s' LIMIT 1" % code
    result = db.fetch_one(sql=sql_select)
    if result is None:
        return 0
    else:
        return int(result[0])


def reset_code(code: str) -> bool:
    # Reset the code
    sql_update = r"UPDATE exchangeable SET used = '0', used_by = NULL, used_datetime = NULL WHERE code = '%s'" % code
    result = db.execute(sql=sql_update)
    if result[0]:
        print("Reset code %s" % code)
        return True
    else:
        print("Failed to reset code %s" % code)
        return False


def generate_redemption_code_list_txt(list_of_code: list):
    # Generate a txt file containing the list of codes
    os.makedirs("generated_codes", exist_ok=True)
    file_name = "generated_codes/list_of_codes_%s.txt" % datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(file_name, "w", encoding='utf-8') as file:
        for code in list_of_code:
            if type(code) is str:
                file.write(code + "\n")
            elif type(code) is tuple or type(code) is list:
                file.write(",".join(str(i) for i in code) + "\n")
            else:
                print("Invalid code type: %s" % type(code))
    return file_name


def add_redemption_code_to_database(code: str, value: int, description: str, added_by: str):
    # Add the code to the database
    # Return True if success, False if failed
    if validate_redemption_code(code):
        # Code already exists
        return False
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql_insert = (r"INSERT INTO exchangeable (code, value, description, created_by, used, create_datetime) "
                  r"VALUES ('%s', '%s', '%s', '%s', '%s', '%s')") % (code, str(value), description,
                                                                     added_by, "0", current_datetime)
    result = db.execute(sql=sql_insert)
    if result[0]:
        print("Added code %s to database" % code)
        return True
    else:
        print("Failed to add code %s to database" % code)
        return False


def use_redemption_code(code: str, used_by_email: str) -> int:
    # Use the code
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql_update = (r"UPDATE exchangeable SET used_by = '%s', used = '1', used_datetime = '%s' "
                  r"WHERE code = '%s' AND used = '0'") % (used_by_email, current_datetime, code)
    result = db.execute(sql=sql_update)
    if result[0]:
        # Executed successfully
        if result[1] == 0:
            return 0
        elif result[1] == 1:
            return 1
        else:
            print("Unknown result: %s" % result[1])
            return 2


def get_all_unused_redemption_code():
    # Get all unused codes
    sql_select = r"SELECT code, value, description FROM exchangeable WHERE used = 0"
    result = db.fetch_all(sql=sql_select)
    return result
