namespace PowerLanguage.Function
{
        public sealed class XAverage : FunctionSeries<double>
        {
            public XAverage(CStudyControl _master) : base(_master) {}
            public XAverage(CStudyControl _master, int _ds) : base(_master, _ds) {}

            public ISeries<double> Price { get; set; }
            public int Length { get; set; }

            protected override double CalcBar(){
                if (1 == Bars.CurrentBar)
                    return Price[0];
                double prev = this[1];
                return prev + 2.0 / (Length + 1) * (Price[0] - prev);
            }
        }
}