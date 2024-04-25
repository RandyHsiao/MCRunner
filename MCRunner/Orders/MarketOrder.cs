using PowerLanguage;
using System;

namespace MCRunner.Orders
{
    public class MarketOrder : BaseOrder, IOrderMarket
    {
        public MarketOrder(SOrderParameters orderParams, bool openNext = false)
            : base(orderParams, OrderCategory.Market, openNext)
        {
        }

        public void Send()
        {
            TriggerOrderSent(new OrderInfo()
            {
                Order = this,
                OrderAction = OrderParams.Action,
                OrderExit = OrderParams.ExitTypeInfo,
                Size = OrderParams.Lots.GetSize()
            });
        }

        public void Send(int numLots)
        {
            if (numLots < 0)
            {
                throw new ArgumentOutOfRangeException("numLots must be larger than 0");
            }
            else if (numLots == 0)
            {
                Send();
            }
            else
            {
                TriggerOrderSent(new OrderInfo()
                {
                    Order = this,
                    OrderAction = OrderParams.Action,
                    OrderExit = OrderParams.ExitTypeInfo,
                    Size = OrderParams.Lots.GetSize(numLots)
                });
            }
        }

        public void Send(string new_name)
        {
            throw new NotImplementedException();
        }

        public void Send(string new_name, int numLots)
        {
            throw new NotImplementedException();
        }

        public void SendFromEntry(string fromName)
        {
            throw new NotImplementedException();
        }

        public void SendFromEntry(int numLots, string fromName)
        {
            throw new NotImplementedException();
        }

        public void SendFromEntry(string new_name, string fromName)
        {
            throw new NotImplementedException();
        }

        public void SendFromEntry(string new_name, int numLots, string fromName)
        {
            throw new NotImplementedException();
        }
    }
}
