namespace PowerLanguage.Function
{
    public sealed class MACD : FunctionSimple<double>
    {
        public MACD(CStudyControl _master) : base(_master) {}
        public MACD(CStudyControl _master, int _ds) : base(_master, _ds) {}

        public ISeries<double> Price { get; set; }
        public int FastLength { get; set; }
        public int SlowLength { get; set; }
        private XAverage XFastAvg, XSlowAvg;

        protected override void Create() {
            XFastAvg = new XAverage(this);
            XSlowAvg = new XAverage(this);
        }

        protected override void StartCalc() {
            XFastAvg.Price = Price;
            XFastAvg.Length = FastLength;
            XSlowAvg.Price = Price;
            XSlowAvg.Length = SlowLength;
        }

        protected override double CalcBar(){
            return XFastAvg.Value - XSlowAvg.Value;
        }
    }
}