using ATCenterProxy.interop;
using PowerLanguage;
using System;

namespace MCRunner.Strategy
{
    public class StrategyPerformance : IStrategyPerformance
    {
        public double AvgEntryPrice => throw new NotImplementedException();

        public double OpenEquity => throw new NotImplementedException();

        public double ClosedEquity => throw new NotImplementedException();

        public int MarketPosition { get; set; }

        public int MarketPositionAtBroker
        {
            get
            {
                return (int)marketPositionAtBroker;
            }
        }

        public int MarketPositionAtBrokerForTheStrategy => throw new NotImplementedException();

        public double AvgEntryPriceAtBroker => throw new NotImplementedException();

        public double AvgEntryPriceAtBrokerForTheStrategy => throw new NotImplementedException();

        public IStrategy[] Signals => throw new NotImplementedException();

        private double marketPositionAtBroker = 0;

        public void UpdateMarketPositionAtBroker(double positionChange)
        {
            marketPositionAtBroker += positionChange;
        }

        public double ConvertCurrency(DateTime when, MTPA_MCSymbolCurrency from, MTPA_MCSymbolCurrency to, double value)
        {
            throw new NotImplementedException();
        }

        public double GetPlotValue(int plot_num)
        {
            throw new NotImplementedException();
        }

        public void SetPlotValue(int plot_num, double value)
        {
            throw new NotImplementedException();
        }
    }
}
