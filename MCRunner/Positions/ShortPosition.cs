using MCRunner.Orders;
using PowerLanguage;
using System.Collections.Immutable;
using System.Linq;
using System;

namespace MCRunner.Positions
{
    public class ShortPosition : IPosition
    {
        public double Size
        {
            get
            {
                return positions.Sum(position => position.Size);
            }
        }

        private ImmutableList<PositionInfo> positions = ImmutableList<PositionInfo>.Empty;

        public void ValidateOrder(OrderInfo order)
        {
            switch (order.OrderAction)
            {
                case EOrderAction.SellShort:
                    break;

                case EOrderAction.BuyToCover:
                    if (positions.Count == 0)
                    {
                        throw new InvalidOrderException("Can't close position before opening one!");
                    }

                    if (order.OrderExit.ExitType != OrderExit.EExitType.All)
                    {
                        throw new InvalidOrderException("Only OrderExit.EExitType.All is currently supported");
                    }
                    break;

                default:
                    throw new InvalidOrderException("Short orders only!");
            }
        }

        public void UpdatePosition(OrderInfo order)
        {
            if (order.OrderAction == EOrderAction.SellShort)
            {
                OpenPosition(order);
            }
            else if (order.OrderAction == EOrderAction.BuyToCover)
            {
                ClosePosition(order);
            }
            else
            {
                throw new ArgumentException(string.Format("Unsupported OrderAction {0}", order.OrderAction));
            }
        }

        private void OpenPosition(OrderInfo order)
        {
            positions = positions.Add(new PositionInfo() { Size = order.Size });
        }

        private void ClosePosition(OrderInfo order)
        {
            if (positions.Count == 0)
            {
                throw new InvalidOperationException("Can't close position before opening one!");
            }

            if (order.OrderExit.ExitType == OrderExit.EExitType.All)
            {
                positions = positions.Clear();
            }
            else
            {
                throw new NotImplementedException("Other OrderExit types not currently supported");
            }
        }
    }
}
