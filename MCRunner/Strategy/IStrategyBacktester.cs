using Bar = MCRunner.Instruments.Bar;
using MCRunner.Orders;
using PowerLanguage.Strategy;
using PowerLanguage;
using System;

namespace MCRunner.Strategy
{
    public interface IStrategyBacktester<T> : IOrderManaged where T : SignalObject
    {
        public T Strategy { get; }

        public IStrategyPerformance StrategyInfo { get; }

        public void Backtest();

        public void Backtest(Action action);

        public void Backtest(Action<Bar> action);
    }
}
