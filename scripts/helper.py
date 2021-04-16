from datetime import datetime

def process_time(time):
    #time = datetime.strptime(time, '%a %b %d %H:%M:%S +0000 %Y')
    time = time.strftime('%Y-%m-%dT%H:%M:%S')
    return time

def convert_dict_to_string(message):
    "May not use this function as dictionary seems to be working fine."
    msg_str = ''
    for key, value in message.items():
        if value:
            msg_str += value + "cs631separator" #cs631separator because , or ; may be in the tweet itself.
        else:
            msg_str += "NAcs631separator"

    return msg_str
