using System;

namespace PowerLanguage.Function
{
    public class RSI : FunctionSeries<Double>
    {
        private VariableSeries<Double> m_netchgavg;

        private VariableSeries<Double> m_totchgavg;


        private double m_sf;

        public RSI(CStudyControl ctx) :
            base(ctx) {}

        public RSI(CStudyControl ctx, int data_stream) :
            base(ctx, data_stream) {}

        public ISeries<Double> price { get; set; }

        public Int32 length { get; set; }

        protected override void Create(){
            m_netchgavg = new VariableSeries<Double>(this);
            m_totchgavg = new VariableSeries<Double>(this);
            
        }

        protected override void StartCalc(){
            m_sf = 1.0/length;
        }


        protected override double CalcBar()
        {
            if (Bars.CurrentBar == 1)
            {
                m_netchgavg.Value = (price.Value - price[length]) / length;
                m_totchgavg.Value = new Lambda<Double>(_bb => Math.Abs(price[_bb] - price[1 + _bb])).Average(length);
            }
            else
            {
                double m_change = price.Value - price[1];
                m_netchgavg.Value = m_netchgavg[1] + m_sf*(m_change - m_netchgavg[1]);
                m_totchgavg.Value = m_totchgavg[1] + m_sf*(Math.Abs(m_change) - m_totchgavg[1]);
            }
            Double chgratio = 0.0;
            if (!PublicFunctions.DoubleEquals(m_totchgavg.Value , 0.0))
            {
                chgratio = m_netchgavg.Value/m_totchgavg.Value;
            }

            return 50*(chgratio + 1);
        }
    }
}