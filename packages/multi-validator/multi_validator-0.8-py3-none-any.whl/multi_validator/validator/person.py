import re


def validate_name(name):
    if name.replace(" ", "").isalpha():
        return True
    else:
        return False

def validate_height_in_cm(height):
    if height < 300 and height > 10:
        return True
    else:
        return False

def validate_weigth_in_kg(weight):
    if weight < 200 and weight > 0:
        return True
    else:
        return False

def validate_gender(gender):
    genders = ['Male', 'Female', 'Other']
    if gender in genders:
        return True
    else:
        return False

def validate_blood_group(blood_group):
    blood_groups = ['AB+' , 'AB-', 'A+', 'A-', 'B+', 'B-', 'O+' , 'O-']
    if blood_group in blood_groups:
        return True
    else:
        return False