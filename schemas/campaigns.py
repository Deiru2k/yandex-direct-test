from yandex import strategies
from schemas.common import *

create_required = ["login", "campaignID", "name", "fIO", "strategy", "emailNotification"]

campaign = {
    "type": "object",
    "required": create_required,
    "properties": {
        "login": string,
        "campaignID": integer,
        "name": string,
        "fIO": string,
        "startDate": string,
        "strategy": {
            "type": "object",
            "required": ["strategyName"],
            "properties": {
                "strategyName": {
                    "type": "string",
                    "enum": strategies.enum
                },
                "maxPrice": float,
                "averagePrice": float,
                "weeklySumLimit": float,
                "clicksPerWeek": integer
            }
        },
        "smsNotification": {
            "type": "object",
            "required": [],
            "properties": {
                "metricaSms": string,
                "moderateResultSms": string,
                "moneyInSms": string,
                "moneyOutSms": string,
                "smsTimeFrom": string,
                "smsTimeTo": string
            }
        },
        "emailNotification": {
            "type": "object",
            "required": ["email", "warnPlaceInterval", "moneyWarningValue"],
            "properties": {
                "email": string,
                "warnPlaceInterval": integer,
                "moneyWarningValue": integer,
                "sendAccNews": string,
                "sendWarn": string
            }
        },
        "statusBehavior": string,
        "timeTarget": {
            "type": "object",
            "required": ["daysHours"],
            "properties": {
                "showOnHolidays": string,
                "holidayShowFrom": integer,
                "holidayShowTo": integer,
                "daysHours": {
                    "type": "array",
                    "items": {
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
                    }
                },
                "timeZone": string
            }
        },
        "statusContextStop": string,
        "contextLimit": string,
        "contextLimitSum": integer,
        "contextPricePercent": integer,
        "autoOptimization": string,
        "statusMetricaControl": string,
        "disabledDomains": string,
        "disabledIps": string,
        "statusOpenStat": string,
        "considerTimeTarget": string,
        "minusKeywords": {
            "type": "array",
            "items": string
        },
        "addRelevantPhrases": string,
        "relevantPhrasesBudgetLimit": integer,
    }
}

campaign_lists = {
    "type": "array",
    "items": campaign
}