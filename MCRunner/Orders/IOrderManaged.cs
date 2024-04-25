using System;

namespace MCRunner.Orders
{
    public interface IOrderManaged
    {
        public event Action<OrderInfo> OrderSent;
    }
}
