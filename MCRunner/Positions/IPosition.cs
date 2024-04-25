using MCRunner.Orders;
using System;

namespace MCRunner.Positions
{
    public class InvalidOrderException : SystemException
    {
        public InvalidOrderException(string message) : base(message)
        {
        }
    }

    public interface IPosition
    {
        public double Size { get; }

        public void ValidateOrder(OrderInfo order);

        public void UpdatePosition(OrderInfo order);
    }
}
