using PowerLanguage;

namespace MCRunner.Orders
{
    public struct OrderInfo
    {
        public double ConditionPrice;
        public double Price;
        public double Size;
        public EOrderAction OrderAction;
        public IOrderObject Order;
        public OrderExit OrderExit;
    }
}
