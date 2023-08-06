from finam.events.event import EventClient
from finam.order.order import OrderClient
from finam.portfolio.portfolio import PortfolioClient
from finam.securities.securities import SecurityClient


class Client:
    def __init__(self, token: str):
        self.portfolio = PortfolioClient(token)
        self.securities = SecurityClient(token)
        self.orders = OrderClient(token)
        self.event = EventClient(token)


if __name__ == "__main__":
    import asyncio

    from finam.order.model import (
        BoardType,
        Condition,
        ConditionType,
        CreateOrderRequestModel,
        DelOrderModel,
        OrdersRequestModel,
        OrderType,
        PropertyType,
        ValidateBefore,
        ValidBeforeType,
    )
    from finam.portfolio.model import PortfolioRequestModel

    client_id = "613395R9A27"
    code = "SiZ2"
    client = Client("CAEQzRYaGAGgZoXjzsERyBBOommi+wP3ltLSIPXWBw==")

    # print(asyncio.run(client.securities.get_data(code="Siz2")))

    # смотрим портфель
    params = PortfolioRequestModel(clientId=client_id)
    print(asyncio.run(client.portfolio.get_portfolio(params)))

    # выставляем заявку
    # payload = CreateOrderRequestModel(
    #     clientId=client_id,
    #     board="FUT",
    #     securityCode=code,
    #     buySell=OrderType.Buy,
    #     quantity=1,
    #     price=61111,
    #     property=PropertyType.PutInQueue,
    #     condition=None,
    #     validateBefore=None,
    # )
    # r = asyncio.run(client.orders.create_order(payload))
    # print(r)
    # transaction_id = r.data.transactionId
    # print(transaction_id)
    #
    # # # смотрим заявки
    # params = OrdersRequestModel(clientId=client_id)
    # print(asyncio.run(client.orders.get_orders(params)))
    #
    # # # выставляем СЛ
    # payload = CreateOrderRequestModel(
    #     clientId=client_id,
    #     board="FUT",
    #     securityCode=code,
    #     buySell=OrderType.Sell,
    #     quantity=1,
    #     price=61090,
    #     property=PropertyType.PutInQueue,
    #     condition=Condition(
    #         price=61090,
    #         type=ConditionType.AskOrLast
    #     ),
    #     validateBefore=ValidateBefore(
    #         type=ValidBeforeType.TillCancelled
    #     ),
    # )
    # r = asyncio.run(client.orders.create_order(payload))
    # print(r)
    # transaction_id = r.data.transactionId
    # print(transaction_id)
    #
    # # выставляем ТП
    # payload = CreateOrderRequestModel(
    #     clientId=client_id,
    #     board=BoardType.Futures,
    #     securityCode=code,
    #     buySell=OrderType.Sell,
    #     quantity=1,
    #     price=None,
    #     property=PropertyType.PutInQueue,
    #     condition=Condition(
    #         price=61150,
    #         type=ConditionType.LastUp
    #     ),
    #     validateBefore=ValidateBefore(
    #         type=ValidBeforeType.TillCancelled
    #     ),
    # )
    # r = asyncio.run(client.orders.create_order(payload))
    # print(r)
    # transaction_id = r.data.transactionId
    # print(transaction_id)
    #
    # # смотрим портфель
    # params = PortfolioRequestModel(clientId=client_id)
    # print(asyncio.run(client.portfolio.get_portfolio(params)))
    #
    # # смотрим заявки
    # params = OrdersRequestModel(clientId=client_id)
    # print(asyncio.run(client.orders.get_orders(params)))
    #
    # # смотрим заявки
    # params = OrdersRequestModel(clientId=client_id)
    # print(asyncio.run(client.orders.get_stop_orders(params)))

    # params = DelOrderModel(clientId=client_id, transactionId=transaction_id)
    # print(asyncio.run(client.orders.del_order(params)))
