using Bar = MCRunner.Instruments.Bar;
using MCRunner.Instruments;
using MCRunner.Orders;
using OrderCreator = MCRunner.Orders.OrderCreator;
using PowerLanguage.Strategy;
using PowerLanguage;
using System.Collections.Generic;
using System;

namespace MCRunner.Strategy
{
    public class StrategyBacktester<T> : IStrategyBacktester<T> where T : SignalObject
    {
        public T Strategy { get; private set; }
        public IStrategyPerformance StrategyInfo { get; private set; }
        public event Action<OrderInfo> OrderSent;
        private readonly StrategyRunner<T> runner;
        private readonly PlayableBars playableBars;

        public StrategyBacktester(IEnumerable<Bar> bars)
        {
            var orderCreator = new OrderCreator();
            orderCreator.OrderSent += (order) => OrderSent.SafeTrigger(order);

            var manager = new StrategyManager(orderCreator);
            StrategyInfo = manager.StrategyInfo;

            playableBars = new PlayableBars(bars);

            runner = new StrategyRunner<T>(
                playableBars.ToSingleDataStream(),
                orderCreator: orderCreator,
                strategyInfo: StrategyInfo);
            Strategy = runner.Strategy;
        }

        public void Backtest()
        {
            Backtest((bar) => { });
        }

        public void Backtest(Action action)
        {
            Backtest((bar) => action());
        }

        public void Backtest(Action<Bar> action)
        {
            runner.Create();
            runner.StartCalc();
            playableBars.Play((bar) =>
            {
                runner.CalcBar();
                action(bar);
            });
        }
    }
}
