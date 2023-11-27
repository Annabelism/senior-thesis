import csv
import random
import requests


header = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"

class WebRequester:
    def __init__(self):
        self.session = requests.Session()
        # A comprehensive set of headers to mimic a real browser
        self.headers = {
            'User-Agent': header,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',  # Do Not Track Request Header
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }

    def get(self, url):
        response = self.session.get(url, headers=self.headers)
        return response

def test_access(url):
    web_requester = WebRequester()
    try:
        response = web_requester.get(url)
        if response.status_code == 200:
            # text = response.text
            # print(len(text)
            return True
        else:
            # print(f'Request failed with status code: {response.status_code}')
            return False
    except Exception as e:
        # print(f'An error occurred: {e}')
        return False

def read_data(filename):
    l = []
    with open(filename, mode='r', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            l.append(row)
    return l

def clean(data):
    cleand_data = []
    for site in data:
        url = site["url"]
        if test_access(url):
            cleand_data.append(site)
    return cleand_data
        

def save_and_write(data):
    # sampled_dicts = random.sample(data, 100)

    output_python_file = 'MBFC.py'

    with open(output_python_file, mode='w', encoding='utf-8') as pyfile:
        pyfile.write('data = [\n')  
        for d in data:
            dict_string = repr(d)
            pyfile.write('    ' + dict_string + ',\n')
        pyfile.write(']\n')  # End the list


def main():
    input_csv_file = 'media-bias-scrubbed-results.csv'
    MBFC_DATA = read_data(input_csv_file)
    MBFC_DATA = clean(MBFC_DATA)
    save_and_write(MBFC_DATA)


main()

