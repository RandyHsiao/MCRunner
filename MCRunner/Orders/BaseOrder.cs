using PowerLanguage;
using System;

namespace MCRunner.Orders
{
    public abstract class BaseOrder : IOrderObject, IOrderManaged
    {
        public event Action<OrderInfo> OrderSent;

        public SOrderParameters OrderParams { get; private set; }

        public Order Info { get; private set; }

        public int ID { get; private set; }

        public BaseOrder(
            SOrderParameters orderParams, OrderCategory orderCategory, bool openNext)
        {
            OrderParams = orderParams;
            Info = new Order(
                orderParams.Name,
                orderParams.Action,
                orderCategory,
                orderParams.Lots,
                openNext,
                orderParams.ExitTypeInfo);
            ID = GetHashCode();
        }

        public override bool Equals(object obj)
        {
            var equals = false;

            if (obj is object && obj.GetType() == GetType())
            {
                var order = (BaseOrder)obj;
                if (order.OrderParams.Name == OrderParams.Name
                    && order.OrderParams.Action == OrderParams.Action
                    && order.OrderParams.ExitTypeInfo == OrderParams.ExitTypeInfo
                    && order.OrderParams.Lots.Contract == OrderParams.Lots.Contract
                    && order.OrderParams.Lots.Type == OrderParams.Lots.Type
                    && order.Info.Category == Info.Category
                    && order.Info.OnClose == Info.OnClose)
                {
                    equals = true;
                }
            }

            return equals;
        }

        public override int GetHashCode()
        {
            return HashCode.Combine(OrderParams, Info.Category, Info.OnClose);
        }

        protected virtual void TriggerOrderSent(OrderInfo orderInfo)
        {
            OrderSent.SafeTrigger(orderInfo);
        }
    }
}
