import inspect

import requests


class JournalizeClient(object):
    BASE_URL = "https://api.journalize.io"
    USER_AGENT = "journalize.io python 0.0.4"

    def _frame_details(self):
        try:
            current_frame = inspect.currentframe()

            # We call f_back twice. One to unwind the caller of this function,
            # and again to unwind the caller of the python client
            previous_frame = current_frame.f_back.f_back

            frame_info = inspect.getframeinfo(previous_frame)
            (filename, line_number, function_name, lines, index) = frame_info
            return "%s:%s:%s %s" % (filename, line_number, function_name, lines[index])
        except:
            pass

        return None

    def __init__(self, api_key, base_url=None):
        self.api_key = api_key

        if base_url is not None:
            self.BASE_URL = base_url

    def me(self):
        headers = {"User-Agent": self.USER_AGENT, "X-API-KEY": self.api_key}
        rc = requests.get(self.BASE_URL + "/me", headers=headers)
        return rc.json()

    def record_event(self, amount: float, date=None, tags=None):
        if tags is None:
            tags = {}

        frame_details = self._frame_details()
        if frame_details is not None:
            tags["_journalize_code"] = frame_details

        headers = {"User-Agent": self.USER_AGENT, "X-API-KEY": self.api_key}
        payload = {"amount": amount, "date": date, "tags": tags}
        rc = requests.post(
            self.BASE_URL + "/events/record",
            json=payload,
            headers=headers,
        )
        return rc.json()

    def create_account(self, account_id, name, normal):
        headers = {"User-Agent": self.USER_AGENT, "X-API-KEY": self.api_key}
        payload = {"id": account_id, "name": name, "normal": normal}

        rc = requests.post(
            self.BASE_URL + "/ledger/accounts",
            json=payload,
            headers=headers,
        )
        return rc.json()

    def create_transaction(self, entries, date=None, tags=None):
        if tags is None:
            tags = {}

        frame_details = self._frame_details()
        if frame_details is not None:
            tags["_journalize_code"] = frame_details

        headers = {"User-Agent": self.USER_AGENT, "X-API-KEY": self.api_key}
        payload = {"date": date, "entries": entries, "tags": [tags]}

        rc = requests.post(
            self.BASE_URL + "/ledger/transaction",
            json=payload,
            headers=headers,
        )
        return rc.json()
