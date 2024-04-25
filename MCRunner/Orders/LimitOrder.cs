using PowerLanguage;
using System;

namespace MCRunner.Orders
{
    public class LimitOrder : BaseOrder, IOrderPriced
    {
        public LimitOrder(SOrderParameters orderParams, bool openNext = false)
            : base(orderParams, OrderCategory.Limit, openNext)
        {
        }

        public void Send(double price)
        {
            if (price <= 0)
            {
                throw new ArgumentOutOfRangeException("price must be larger than 0");
            }

            TriggerOrderSent(new OrderInfo()
            {
                Order = this,
                OrderAction = OrderParams.Action,
                OrderExit = OrderParams.ExitTypeInfo,
                Price = price,
                Size = OrderParams.Lots.GetSize()
            });
        }

        public void Send(double price, int numLots)
        {
            if (price <= 0)
            {
                throw new ArgumentOutOfRangeException("price must be larger than 0");
            }

            if (numLots < 0)
            {
                throw new ArgumentOutOfRangeException("numLots must be larger than 0");
            }
            else if (numLots == 0)
            {
                Send(price);
            }
            else
            {
                TriggerOrderSent(new OrderInfo()
                {
                    Order = this,
                    OrderAction = OrderParams.Action,
                    OrderExit = OrderParams.ExitTypeInfo,
                    Price = price,
                    Size = OrderParams.Lots.GetSize(numLots)
                });
            }
        }

        public void Send(string new_name, double price)
        {
            throw new NotImplementedException();
        }

        public void Send(string new_name, double price, int numLots)
        {
            throw new NotImplementedException();
        }

        public void SendFromEntry(double price, string fromName)
        {
            throw new NotImplementedException();
        }

        public void SendFromEntry(double price, int numLots, string fromName)
        {
            throw new NotImplementedException();
        }

        public void SendFromEntry(string new_name, double price, string fromName)
        {
            throw new NotImplementedException();
        }

        public void SendFromEntry(string new_name, double price, int numLots, string fromName)
        {
            throw new NotImplementedException();
        }
    }
}
