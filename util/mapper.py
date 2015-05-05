from schemas.common import *

def upper_to_lower_camel(string):
    first_letter = string[0]
    return first_letter.lower() + string[1:]

def lower_to_upper_camel(string):
    first_letter = string[0]
    return first_letter.upper() + string[1:]

def convert_keys(d, convert):
    new_d = {}
    for k, v in d.items():
        new_d[convert(k)] = convert_keys(v,convert) if isinstance(v,dict) else v
    return new_d


if __name__ == '__main__':

    x = {
    "type": "object",
    "required": [],
    "properties": {
        "Login": string,
        "CampaignID": integer,
        "Name": string,
        "FIO": string,
        "StartDate": integer,
        "Strategy": {
            "type": "object",
            "required": ["StrategyName"],
            "properties": {
                "StrategyName": {
                    "type": "string",
                    "enum": []
                },
                "MaxPrice": float,
                "AveragePrice": float,
                "WeeklySumLimit": float,
                "ClicksPerWeek": integer
            }
        },
        "SmsNotification": {
            "type": "object",
            "required": [],
            "properties": {
                "MetricaSms": string,
                "ModerateResultSms": string,
                "MoneyInSms": string,
                "MoneyOutSms": string,
                "SmsTimeFrom": string,
                "SmsTimeTo": string
            }
        },
        "EmailNotification": {
            "type": "object",
            "required": ["Email", "WarnPlaceInterval", "MoneyWarningValue"],
            "properties": {
                "Email": string,
                "WarnPlaceInterval": integer,
                "MoneyWarningValue": integer,
                "SendAccNews": string,
                "SendWarn": string
            }
        },
        "StatusBehavior": string,
        "TimeTarget": {
            "type": "object",
            "required": ["DailyHours"],
            "properties": {
                "ShowOnHolidays": string,
                "HolidayShowFrom": integer,
                "HolidayShowTo": integer,
                "DaysHours": {
                    "type": "object",
                    "required": ["Hours", "Days"],
                    "properties": {
                        "Hours": {
                            "type": "array",
                            "items": integer
                        },
                        "Days": {
                            "type": "array",
                            "items": integer
                        }
                    }
                },
                "TimeZone": string
            }
        },
        "StatusContextStop": string,
        "ContextLimit": string,
        "ContextLimitSum": integer,
        "ContextPricePercent": integer,
        "AutoOptimization": string,
        "StatusMetricaControl": string,
        "DisabledDomains": string,
        "DisabledIps": string,
        "StatusOpenStat": string,
        "ConsiderTimeTarget": string,
        "MinusKeywords": {
            "type": "array",
            "items": string
        },
        "AddRelevantPhrases": string,
        "RelevantPhrasesBudgetLimit": integer,
    }
}

    print(convert_keys(x, upper_to_lower_camel))