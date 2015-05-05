manual = {
    "HighestPosition": "«Наивысшая доступная позиция»",
    "LowestCost": "«Показ в блоке по минимальной цене»",
    "LowestCostPremium": "«Показ в блоке по минимальной цене», но объявления показываются только в спецразмещении»"
}

limited_manual = {
    "NoPremiumPosition": "«Показ под результатами поиска»",
    "IndependentControl": "«Независимое управление для разных типов площадок»"
}

automatic = {
    "WeeklyBudget": "«Недельный бюджет»",
    "WeeklyPacketOfClicks": "«Недельный пакет кликов»",
    "AverageClickPrice": "«Средняя цена клика»"
}

common = dict()
common.update(manual)
common.update(limited_manual)
common.update(automatic)
enum = [key for key in common]