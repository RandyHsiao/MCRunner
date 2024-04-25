using Bar = MCRunner.Instruments.Bar;
using MCRunner.Orders;
using MCRunner.Positions;
using PowerLanguage;
using System.Collections.Immutable;
using System;

namespace MCRunner.Strategy
{
    public class StrategyManager
    {
        public event Action<OrderInfo> OrderValidated;

        public event Action<OrderInfo> OrderCanceled;

        private ImmutableHashSet<OrderInfo> previousSubmittedOrders =
            ImmutableHashSet<OrderInfo>.Empty;
        private ImmutableHashSet<OrderInfo> untriggeredOrders =
            ImmutableHashSet<OrderInfo>.Empty;
        private ImmutableHashSet<OrderInfo> validatedOrders =
            ImmutableHashSet<OrderInfo>.Empty;
        private readonly IPosition longPosition = new LongPosition();
        private readonly IPosition shortPosition = new ShortPosition();
        private readonly StrategyPerformance strategyInfo = new StrategyPerformance();

        private int Size
        {
            get
            {
                return (int)(longPosition.Size - shortPosition.Size);
            }
        }

        public IStrategyPerformance StrategyInfo
        {
            get
            {
                return strategyInfo;
            }
        }

        public StrategyManager(IOrderManaged orderCreator)
        {
            orderCreator.OrderSent += OnOrderSent;
        }

        public void UpdateMarketPositionAtBroker(double positionChange)
        {
            strategyInfo.UpdateMarketPositionAtBroker(positionChange);
        }

        public void TriggerOrders(Bar bar)
        {
            foreach (var order in untriggeredOrders)
            {
                if (order.Order is IOrderPriced)
                {
                    var price = order.ConditionPrice;
                    if (price <= 0)
                    {
                        price = order.Price;
                    }

                    switch (order.OrderAction)
                    {
                        case EOrderAction.Buy:
                        case EOrderAction.BuyToCover:
                            if (price >= bar.Low)
                            {
                                OnOrderTriggered(order);
                            }
                            break;

                        case EOrderAction.Sell:
                        case EOrderAction.SellShort:
                            if (price <= bar.High)
                            {
                                OnOrderTriggered(order);
                            }
                            break;

                        default:
                            throw new ArgumentException("Unknown OrderAction");
                    }
                }
                else
                {
                    throw new ArgumentException("Unknown order type");
                }
            }

            foreach (var order in previousSubmittedOrders)
            {
                if (!untriggeredOrders.Contains(order))
                {
                    OrderCanceled.SafeTrigger(order);
                }
            }

            previousSubmittedOrders = untriggeredOrders;
            untriggeredOrders = untriggeredOrders.Clear();
        }

        private void OnOrderSent(OrderInfo order)
        {
            ValidateOrder(order);

            if (!validatedOrders.Contains(order))
            {
                validatedOrders = validatedOrders.Add(order);
                OrderValidated.SafeTrigger(order);
            }

            CheckIfOrderTriggered(order);
        }

        private void OnOrderTriggered(OrderInfo order)
        {
            switch (order.OrderAction)
            {
                case EOrderAction.Buy:
                case EOrderAction.Sell:
                    longPosition.UpdatePosition(order);
                    break;

                case EOrderAction.SellShort:
                case EOrderAction.BuyToCover:
                    shortPosition.UpdatePosition(order);
                    break;

                default:
                    throw new ArgumentException("Invalid OrderAction");
            }

            strategyInfo.MarketPosition = Size;

            validatedOrders = validatedOrders.Remove(order);
            untriggeredOrders = untriggeredOrders.Remove(order);
            previousSubmittedOrders = previousSubmittedOrders.Remove(order);
        }

        private void ValidateOrder(OrderInfo order)
        {
            switch (order.OrderAction)
            {
                case EOrderAction.Buy:
                case EOrderAction.Sell:
                    longPosition.ValidateOrder(order);
                    break;

                case EOrderAction.SellShort:
                case EOrderAction.BuyToCover:
                    shortPosition.ValidateOrder(order);
                    break;

                default:
                    throw new InvalidOrderException("Unknown OrderAction");
            }
        }

        private void CheckIfOrderTriggered(OrderInfo order)
        {
            if (order.Order is IOrderMarket)
            {
                OnOrderTriggered(order);
            }
            else
            {
                untriggeredOrders = untriggeredOrders.Add(order);
            }
        }
    }
}
