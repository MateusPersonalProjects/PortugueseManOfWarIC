import datetime

def parseDate(date_str):
    formats = [
        "%m-%d-%Y",  # MM-DD-YYYY
        "%Y-%m-%d",  # YYYY-MM-DD
        "%B/%d/%Y",  # MONTH/DAY/YEAR
        "%b/%d/%Y",  # Mon/Day/Year
        "%m/%d/%Y",  # MM/DD/YYYY
        "%d-%m-%Y",  # DD-MM-YYYY
        "%d/%m/%Y"   # DD/MM/YYYY
    ]
    
    for fmt in formats:
        try:
            parsed_date = datetime.datetime.strptime(date_str, fmt)
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            continue
    
    raise ValueError(f"Date format not recognized: {date_str}")


