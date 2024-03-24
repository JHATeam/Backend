from urllib.parse import urlparse

def is_url(input_string):
    try:
        result = urlparse(input_string)
        return all([result.scheme, result.netloc])  # Checking if both scheme and netloc are present
    except ValueError:
        return False
    

print(is_url('http://localhost:8080/'))