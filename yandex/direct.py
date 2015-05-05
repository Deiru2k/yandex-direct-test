import requests
import json


class YandexDirectError(Exception):

    def __init__(self, code, error, message):
        self.code = code
        self.error = error
        self.message = message

    def __str__(self):
        if self.message:
            message = "[%s] %s: %s" % (self.code, self.error, self.message)
        else:
            message = "[%s] %s" % (self.code, self.error)
        return message


class YandexDirectProxy:

    url_simple = "https://%s.direct.yandex.ru/v%s/json/"
    url_live = "https://%s.direct.yandex.ru/live/v%s/json/"

    _model = dict()

    def __init__(self, token: str, sandbox: bool=False, live: bool=False, version: int=4, locale: str="en"):
        env = "api-sandbox" if sandbox else "api"
        if not live:
            self.url = self.url_simple % (env, str(version))
        else:
            self.url = self.url_live % (env, str(version))
        self.token = token
        self.locale = locale
        self._model['token'] = self.token
        self._model['locale'] = self.locale

    def request(self, method: str, data=None):
        request_data = self._model
        request_data['method'] = method
        if data:
            request_data['param'] = data
        request_data = json.dumps(request_data)
        response = requests.post(url=self.url, data=request_data)
        response_data = json.loads(response.text)
        if "error_code" in response_data:
            print(response_data)
            raise YandexDirectError(
                response_data['error_code'],
                response_data['error_str'],
                response_data['error_detail']
            )
        return response_data['data']


class YandexDirect(YandexDirectProxy):

    def list_campaigns(self, logins=list()):
        if isinstance(logins, str):
            logins = [logins]
        campaigns = self.request("GetCampaignsList", logins)
        return campaigns

    def create_campaign(self, campaign_info: dict):
        return self.request("CreateOrUpdateCampaign", campaign_info)

    def update_campaign(self, campaign_info: dict):
        return self.create_campaign(campaign_info)

    def archive_campaign(self, campaign_id: int):
        data = {
            "CampaignID": campaign_id
        }
        return self.request("ArchiveCampaign", data)

    def unarchive_campaign(self, campaign_id: int):
        data = {
            "CampaignID": campaign_id
        }
        return self.request("UnArchiveCampaign", data)

    def stop_campaign(self, campaign_id: int):
        data = {
            "CampaignID": campaign_id
        }
        return self.request("StopCampaign", data)

    def resume_campaign(self, campaign_id: int):
        data = {
            "CampaignID": campaign_id
        }
        return self.request("ResumeCampaign", data)

    def delete_campaign(self, campaign_id: int):
        data = {
            "CampaignID": campaign_id,
        }
        return self.request("DeleteCampaign", data)

    def list_clients(self):
        return self.request("GetClientsList")

    def create_client(self, username, first_name, last_name):
        data = {
            "Login": username,
            "Name": first_name,
            "Surname": last_name
        }
        return self.request("CreateNewSubclient", data)


if __name__ == "__main__":

    yandex = YandexDirect(token=api_token, sandbox=True, locale="ru")
    campaign_data = {
        "Name":"Promotion of home appliances",
        "FIO":"Alex Gromov",
        "Strategy":{
            "StrategyName":"WeeklyBudget",
            "WeeklySumLimit":400,
            "MaxPrice":8
        },
        "TimeTarget":{
            "TimeZone":"Europe/Moscow",
            "DaysHours":[
                {
                    "Hours":[1,2,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
                    "Days":[1,2,3,4,5]
                },
                {
                    "Hours":[10,11,12,13,14,15,16,17,18,19,20],
                    "Days":[6,7]
                }
            ],
            "ShowOnHolidays":"Yes"
        },
        "StatusBehavior":"Yes",
        "StatusContextStop":"No",
        "ContextLimit":"Default",
        "ContextLimitSum":30,
        "ContextPricePercent":100,
        "AutoOptimization":"Yes",
        "StatusMetricaControl":"Yes",
        "DisabledDomains": "domain1.ru,domain2.ru",
        "DisabledIps": "64.234.23.21",
        "StatusOpenStat":"No",
        "ConsiderTimeTarget":"Yes",
        "AddRelevantPhrases":"No",
        "RelevantPhrasesBudgetLimit":100,
        "MinusKeywords":[],
        "SmsNotification":{
            "SmsTimeFrom":"09:00",
            "MoneyInSms":"Yes",
            "SmsTimeTo":"21:00",
            "MoneyOutSms":"Yes",
            "ModerateResultSms":"Yes",
            "MetricaSms":"Yes"
        },
        "EmailNotification":{
            "MoneyWarningValue":20,
            "SendAccNews":"Yes",
            "WarnPlaceInterval":60,
            "SendWarn":"Yes",
            "Email":"agrom@yandex.ru"
        }
    }
    # try:
    #    r = yandex.create_campaign(campaign_data)
    #    print(r)
    # except YandexDirectError as yaerror:
    #    print(yaerror)
    # yandex.delete_campaign(89357)
    # yandex.stop_campaign(89356)
    # yandex.archive_campaign(89356)
    # r = yandex.list_campaigns()
    # yandex.create_client("Misaka42", "Misaka", "Mikoto")
    r = yandex.list_clients()
    for client in r:
        print("%s: %s - %s" % (client['Login'], client['FIO'], client['Role']))
        client_campaigns = yandex.list_campaigns(client['Login'])
        for campaign in client_campaigns:
            print("\t%s: %s - %s" % (campaign['CampaignID'], campaign['Name'], campaign['Status']))
