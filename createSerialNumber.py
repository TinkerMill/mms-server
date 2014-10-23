import random

def createSerialNumber():
    """Create a serial number for the badge  

    Returns:
       String with 8 random characters of 0-9 and A-Z
          
    """
    
    r = ""
    for i in range(4):
        r = r + chr(random.randrange(48,57))
        r = r + chr(random.randrange(65,90))

    return r