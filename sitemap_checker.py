import os

import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import schedule
import time

# Replace with the URL of your sitemap.xml file
sitemap_url = os.environ.get('SITEMAP_URL')
webhook_url = os.environ.get('WEBHOOK_URL')
print(sitemap_url)
print(webhook_url)


def check_urls():
    try:
        # Send a GET request to the sitemap.xml file
        response = requests.get(sitemap_url)

        # Parse the XML response using ElementTree
        root = ET.fromstring(response.content)
        success = True
        print(f'Starting sitemap checker at {datetime.utcnow().strftime("%Y-%m-%d %H:%M")}.')
        # Iterate through all <url> elements in the sitemap
        for url in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
            loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text

            # Send a GET request to the URL and check the response status code
            try:
                response = requests.get(loc)
                if response.status_code != 200:
                    print(f'{loc} is not accessible (status code: {response.status_code}).')
                    success = False
                    # Send a notification to Microsoft Teams
                    message = {
                        'text': f'URL {loc} is not accessible (status code: {response.status_code}).'
                    }
                    response = requests.post(webhook_url, json=message)
                    response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f'{loc} is not accessible.')
                success = False
                # Send a notification to Microsoft Teams
                message = {
                    'text': f'URL {loc} is not accessible: {str(e)}'
                }
                response = requests.post(webhook_url, json=message)
                response.raise_for_status()
        print(
            f'Sitemap checker {"succeed" if success else "failed"} at {datetime.utcnow().strftime("%Y-%m-%d %H:%M")}.')
    except Exception as e:
        print(e)
        message = {
            'text': e
        }
        requests.post(webhook_url, json=message)


check_urls()
schedule.every(5).minutes.do(check_urls)

while 1:
    schedule.run_pending()
    time.sleep(1)
