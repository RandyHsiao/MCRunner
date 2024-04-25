using PowerLanguage;
using System;

namespace MCRunner.Orders
{
    public class OrderCreator : IOrderCreator, IOrderManaged
    {
        public event Action<OrderInfo> OrderSent;

        public IOrderPriced Limit(SOrderParameters orderParams)
        {
            var order = new LimitOrder(orderParams, true);
            order.OrderSent += OrderSent;
            return order;
        }

        public IOrderMarket MarketNextBar(SOrderParameters orderParams)
        {
            var order = new MarketOrder(orderParams, true);
            order.OrderSent += OrderSent;
            return order;
        }

        public IOrderMarket MarketThisBar(SOrderParameters orderParams)
        {
            var order = new MarketOrder(orderParams, false);
            order.OrderSent += OrderSent;
            return order;
        }

        public IOrderPriced Stop(SOrderParameters orderParams)
        {
            var order = new StopOrder(orderParams, true);
            order.OrderSent += OrderSent;
            return order;
        }

        public IOrderStopLimit StopLimit(SOrderParameters orderParams)
        {
            var order = new StopLimitOrder(orderParams, true);
            order.OrderSent += OnOrderSent;
            return order;
        }

        private void OnOrderSent(OrderInfo order)
        {
            OrderSent.SafeTrigger(order);
        }
    }
}
