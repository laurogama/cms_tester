import requests
from xml.dom import minidom

from private_settings import URL_HOST, URL_PORT, URL_ENDPOINT, SLACK_HOOK_URL, REQUEST_NOTIFICATION_XML

CMS_URL = "http://{}:{}{}".format(URL_HOST, str(URL_PORT), URL_ENDPOINT)


def parse_payload(data):
    if data:
        xmldoc = minidom.parseString(data)
        itemlist = xmldoc.getElementsByTagName('status')
        for s in itemlist:
            response_code = s.childNodes[0].nodeValue
            if response_code is not 200:
                print "deu merda"
                return response_code
    return 200


def alert_slack(status_code=None, message=None):
    print status_code
    if status_code is not 200:
        response = requests.post(url=SLACK_HOOK_URL,
                                 json={'text': "Erro ao contatar cms: http code={}, msg=>{}".format(status_code,
                                                                                                    message)})
        print response


def test_cms(XML_PAYLOAD=None):
    headers = {'Content-Type': 'text/xml'}
    try:
        response = requests.post(CMS_URL, data=XML_PAYLOAD, headers=headers)
        alert_slack(response.status_code)
        clean_string = response.text.strip()
        print clean_string
        alert_slack(parse_payload(response.text))
    except requests.exceptions.ConnectionError as e:
        alert_slack(e.errno, e.message)
    except Exception as e:
        alert_slack(None, e.message)


if __name__ == "__main__":
    payload = REQUEST_NOTIFICATION_XML
    test_cms(payload)
