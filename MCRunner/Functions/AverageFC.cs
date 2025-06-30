using System;

namespace PowerLanguage.Function
{
    public class AverageFC : FunctionSimple<Double>
    {
        private SummationFC m_summationfc1;

        public AverageFC(CStudyControl ctx) :
            base(ctx) {}

        public AverageFC(CStudyControl ctx, int data_stream) :
            base(ctx, data_stream) {}

        public ISeries<Double> price { get; set; }

        public Int32 length { get; set; }

        protected override void Create(){
            m_summationfc1 = new SummationFC(this);
        }

        protected override void StartCalc(){
            m_summationfc1.price = price;
            m_summationfc1.length = length;
        }


        protected override double CalcBar(){
            return m_summationfc1[0] / length;
        }
    }
}