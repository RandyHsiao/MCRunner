using System;

namespace PowerLanguage.Function
{
    public class SummationFC : FunctionSeries<Double>
    {
        
        private VariableSeries<Double> m_sum;

        public SummationFC(CStudyControl ctx) :
            base(ctx) {}

        public SummationFC(CStudyControl ctx, int data_stream) :
            base(ctx, data_stream) {}

        public ISeries<Double> price { get; set; }

        public Int32 length { get; set; }

        protected override void Create(){
            m_sum = new VariableSeries<Double>(this);
        }

        protected override void StartCalc(){
        }

        private void on_first_bar(){
            m_sum.Value = 0;
            for (var i = 0; i < length; ++i)
                m_sum.Value += price[i];
        }


        protected override double CalcBar(){
            if (Bars.CurrentBar == 1)
                on_first_bar();
            else
                m_sum.Value = m_sum[1] + price.Value- price[length];
            return m_sum.Value;
        }
    }
}