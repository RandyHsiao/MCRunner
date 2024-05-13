using System;
using PowerLanguage.Function;

namespace MCRunner.Indicators
{
    [SameAsSymbol(true)]
    public class XAverage : IndicatorObject
    {
        private VariableSeries<double> values;

        [Input]
        public int Length { get; set; }

        [Input]
        public ISeries<double> Price { get; set; }

        protected override void Create()
        {
            values = new VariableSeries<double>(this);
        }

        protected override void CalcBar()
        {
            if (Bars.CurrentBar < Length)
            {
                return;
            }

            // 計算 EMA 值
            double alpha = 2.0 / (Length + 1);

            if (values.Count == 0)
            {
                values.Value = Price[0];
            }
            else
            {
                values.Value = values[1] + alpha * (Price[0] - values[1]);
            }
        }

        public double this[int barsAgo]
        {
            get
            {
                return values[barsAgo];
            }
        }

        public double Value
        {
            get { return values[0]; }
        }
    }
}