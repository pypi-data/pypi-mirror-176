# 获得持仓股票，以及对应的股数、持仓成本等信息
def get_holdings(accountid, datatype, func):
    holdinglist = {}
    resultlist = func(accountid, datatype, "POSITION")
    print("resultlist ", resultlist)
    for obj in resultlist:
        # print("obj ",obj)
        code = obj.m_strInstrumentID

        holdinglist[obj.m_strInstrumentID + "." + obj.m_strExchangeID] = {"m_nVolume": obj.m_nVolume,
                                                                          "avg_cost": obj.m_dOpenPrice,
                                                                          "market_value": obj.m_dMarketValue,
                                                                          "m_nCanUseVolume": obj.m_nCanUseVolume}
    return holdinglist
