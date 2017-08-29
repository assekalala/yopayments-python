try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

from dicttoxml import dicttoxml
import xmltodict


class YoPayments(object):

    def __init__(self, username, password, enviroment='production'):
        self.api_username = username
        self.api_password = password
        if enviroment == 'production':
            self.api_url = 'https://paymentsapi2.yo.co.ug/ybs/task.php'
        else:
            self.api_url = 'https://41.220.12.206/services/yopaymentsdev/task.php'

    def _request(self, xml):
        headers = {
            'Content-Type': 'application/xml',
            'Content-Transfer-Encoding': 'text/plain'
        }
        request = urllib2.Request(self.api_url, data=xml, headers=headers)
        connection = urllib2.urlopen(request)
        response = connection.read()
        connection.close()

        response_dict = xmltodict.parse(response)
        return response_dict['AutoCreate']

    def check_balance(self):
        request = {
            'Request': {
                'APIUsername': self.api_username,
                'APIPassword': self.api_password,
                'Method': 'acacctbalance'
            }
        }
        xml = dicttoxml(request, custom_root='AutoCreate', attr_type=False)
        return self._request(xml)

    def send_money(self, amount, account, reason=None):
        request = {
            'Request': {
                'APIUsername': self.api_username,
                'APIPassword': self.api_password,
                'Method': 'acwithdrawfunds',
                'Amount': amount,
                'Account': account,
                'Narrative': reason if not None else 'Payment'
            }
        }
        xml = dicttoxml(request, custom_root='AutoCreate', attr_type=False)
        return self._request(xml)

    def pull_money(self, from_, amount, reason):
        request = {
            'Request': {
                'APIUsername': self.api_username,
                'APIPassword': self.api_password,
                'Method': 'acwithdepostfunds',
                'Amount': amount,
                'Account': from_,
                'Narrative': reason if not None else 'Withdraw'
            }
        }
        xml = dicttoxml(request, custom_root='AutoCreate', attr_type=False)
        return self._request(xml)

    def transfer(self, to, amount, reason):
        request = {
            'Request': {
                'APIUsername': self.api_username,
                'APIPassword': self.api_password,
                'Method': 'acwithdepostfunds',
                'Amount': amount,
                'Account': to,
                'Narrative': reason if not None else 'Transfer'
            }
        }
        xml = dicttoxml(request, custom_root='AutoCreate', attr_type=False)
        return self._request(xml)

    def mini_statement(self, start_date=None, end_date=None):
        request = {
            'Request': {
                'APIUsername': self.api_username,
                'APIPassword': self.api_password,
                'Method': 'acgetministatement',
                'StartDate': start_date,
                'EndDate': end_date,
            }
        }
        xml = dicttoxml(request, custom_root='AutoCreate', attr_type=False)
        return self._request(xml)

    def send_airtime(self, to, amount, reason=None):
        request = {
            'Request': {
                'APIUsername': self.api_username,
                'APIPassword': self.api_password,
                'Method': 'acsendairtimemobile',
                'Amount': amount,
                'Account': to,
                'Narrative': reason if not None else 'Airtime Purchase'
            }
        }
        xml = dicttoxml(request, custom_root='AutoCreate', attr_type=False)
        return self._request(xml)

def main():
    """ A simple demo to be used from command line. """
    import sys

    def log(message):
        print(message)

    def print_usage():
        log('usage: %s <api username> <api password> pay <customber_mobile> <amount> <reason>' % sys.argv[0])
        log('usage: %s <api username> <api password> transfer <customber_mobile> <amount> <reason>' % sys.argv[0])
        log('       %s <api username> <api password> balance ' % sys.argv[0])

    if len(sys.argv) > 4 and sys.argv[3] == 'transfer':
        username, password, account, amount = sys.argv[1], sys.argv[2], sys.argv[4], sys.argv[5]
        yo = YoPayments(username, password)

        if len(sys.argv) > 6:
            reason = sys.argv[6]
            log(yo.transfer(amount, account, reason))
        else:
            log(yo.transfer(amount, account))
    elif len(sys.argv) > 4 and sys.argv[3] == 'pay':
        username, password, account, amount = sys.argv[1], sys.argv[2], sys.argv[4], sys.argv[5]
        yo = YoPayments(username, password)

        if len(sys.argv) > 6:
            reason = sys.argv[6]
            log(yo.send_money(amount, account, reason))
        else:
            log(yo.send_money(amount, account))
    elif len(sys.argv) > 3 and sys.argv[3] == 'balance':
        username, password = sys.argv[1], sys.argv[2]
        yo_payments = YoPayments(username, password)
        log(yo_payments.check_balance())
    else:
        print_usage()
        sys.exit(1)

    sys.exit(0)

if __name__ == '__main__':
    main()