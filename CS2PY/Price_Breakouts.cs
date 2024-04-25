using System;
using System.Drawing;
using System.Linq;
using PowerLanguage.Function;
using ATCenterProxy.interop;

namespace PowerLanguage.Strategy
{
    public class Price_Breakouts : SignalObject
    {
        // Create the inputs
        [Input]
        public int EMALength { get; set; }

        [Input]
        public int LookbackPeriod { get; set; }

        public Price_Breakouts(object _ctx) : base(_ctx) 
        {
            // Give the inputs a default value
            EMALength      = 50;
            LookbackPeriod = 10;
        }

        private IOrderMarket enterLong, enterShort, exitLong, exitShort;
        private XAverage EMA;
        private VariableSeries<double> lowestClose, highestClose, emaValues;

        protected override void Create()
        {
            // Create the orders
            enterLong = OrderCreator.MarketNextBar(new 
                SOrderParameters(Contracts.Default, EOrderAction.Buy));

            enterShort = OrderCreator.MarketNextBar(new 
                SOrderParameters(Contracts.Default, EOrderAction.SellShort));

            exitLong = OrderCreator.MarketNextBar(new 
                SOrderParameters(Contracts.Default, EOrderAction.Sell));

            exitShort = OrderCreator.MarketNextBar(new 
                SOrderParameters(Contracts.Default, EOrderAction.BuyToCover));

            // Create the variable series
            lowestClose  = new VariableSeries<double>(this);
            highestClose = new VariableSeries<double>(this);
            emaValues    = new VariableSeries<double>(this);

            // Create the EMA function
            EMA = new XAverage(this);
        }

        protected override void StartCalc()
        {
            // Specify the EMA settings
            EMA.Length = EMALength;
            EMA.Price = Bars.Close;
        }

        protected override void CalcBar()
        {
            lowestClose.Value  = Bars.Close.Lowest(LookbackPeriod, 1);
            highestClose.Value = Bars.Close.Highest(LookbackPeriod, 1);
            emaValues.Value    = EMA[0];

            // Look for entries
            if (StrategyInfo.MarketPosition == 0)
            {
                if ((Bars.Close[0] > highestClose[0]) && (Bars.Close[1] < highestClose[1]))
                {
                    enterLong.Send();
                }
                else if ((Bars.Close[0] < lowestClose[0]) && (Bars.Close[1] > lowestClose[1]))
                {
                    enterShort.Send();
                }
            }

            // Manage open long positions
            else if (StrategyInfo.MarketPosition > 0)
            {
                if ((Bars.Close[0] < emaValues[0]) && (Bars.Close[1] >= emaValues[1]))
                {
                    exitLong.Send();
                }
            }

            // Manage open short positions
            else if (StrategyInfo.MarketPosition < 0)
            {
                if ((Bars.Close[0] > emaValues[0]) && (Bars.Close[1] <= emaValues[1]))
                {
                    exitShort.Send();
                }
            }

            // Set the values for communicating with the indicator
            StrategyInfo.SetPlotValue(1, lowestClose[0]);
            StrategyInfo.SetPlotValue(2, highestClose[0]);
            StrategyInfo.SetPlotValue(3, emaValues[0]);
        }
    }
}