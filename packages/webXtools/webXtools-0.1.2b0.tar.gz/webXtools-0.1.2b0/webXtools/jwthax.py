from webXtools.bf import bruteforce, bruteforceFile, bruteforceList
from webXtools.helper import splitFile
import hmac, base64, hashlib, string

genToken = lambda secret, content: (base64.b64encode(hmac.new(secret.encode(), content.encode(), digestmod = hashlib.sha256).digest()).decode('ascii')).replace("=", "").replace("+", "-").replace("/", "_")


def jwtBrute(token:str, minLength=1, maxLength=4, charSet=string.ascii_letters+string.digits, stringFile="", stringList=[], noOfThreads=1):
    """Crack a JWT either using a blind string bruteforce or a file of words or a list of words

    Args:
        token (str): The JWT
        minLength (int, optional): Minimum length of string to bruteforce. Defaults to 1.
        maxLength (int, optional): Maximum length of string to bruteforce. Defaults to 4.
        charSet (string, optional): The character set. Defaults to string.ascii_letters+string.digits.
        file (str, optional): Use the words present in the file. Takes higher precedence than charSet if defined. Defaults to "".
        stringList (list, optional): Use the words present in the file. Takes higher precedence than stringFile if defined. Defaults to [].
        noOfThreads (int, optional): Number of threads to use. Defaults to 1.
    Returns:
        str or None: Returns the secret key if it was bruteforced or returns None
    """
    

    header, data, sign = token.split(".")
    content = f"{header}.{data}"

    def checker(secret):
        currHash = genToken(secret, content)
        if currHash == sign:
            return True
        else:
            return False
    
    if stringList != []:
        return(bruteforceList(stringList, noOfThreads, checker))

    if stringFile != "":
        return(bruteforceFile(stringFile, noOfThreads, checker))
        
    return(bruteforce(minLength, maxLength, charSet, noOfThreads, checker))