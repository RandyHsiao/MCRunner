using OrderCreator = MCRunner.Orders.OrderCreator;
using PowerLanguage.Strategy;
using PowerLanguage;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Reflection;
using System;

namespace MCRunner.Strategy
{
    public class StrategyRunner<T> where T : SignalObject
    {
        public T Strategy { get; private set; }

        private readonly Type type = typeof(T);

        public StrategyRunner(
            IEnumerable<IInstrument> barsData = null,
            IOrderCreator orderCreator = null,
            IOutput output = null,
            IStrategyPerformance strategyInfo = null)
        {
            Strategy = (T)Activator.CreateInstance(type, "");

            if (barsData is null)
            {
                SetProtectedProperty("BarsData", new List<IInstrument>());
            }
            else
            {
                SetProtectedProperty("BarsData", new List<IInstrument>(barsData));
            }

            if (orderCreator is null)
            {
                orderCreator = new OrderCreator();
            }

            if (output is null)
            {
                output = new ConsoleOutput();
            }

            if (strategyInfo is null)
            {
                strategyInfo = new StrategyPerformance();
            }

            SetProtectedProperty("OrderCreator", orderCreator);
            SetProtectedProperty("Output", output);
            SetProtectedProperty("StrategyInfo", strategyInfo);
        }

        public void Create()
        {
            CallProtectedMethod("Create");
        }

        public void StartCalc()
        {
            CallProtectedMethod("StartCalc");
        }

        public void CalcBar()
        {
            CallProtectedMethod("CalcBar");
        }

        protected void CallProtectedMethod(string name)
        {
            MethodInfo method = Strategy.GetType().GetMethod(
                name, BindingFlags.NonPublic | BindingFlags.Instance);
            method.Invoke(Strategy, null);
        }

        protected void SetProtectedProperty(string name, object value)
        {
            PropertyInfo property = Strategy.GetType().GetProperty(
                name, BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
            property.SetValue(Strategy, value);
        }
    }
}
