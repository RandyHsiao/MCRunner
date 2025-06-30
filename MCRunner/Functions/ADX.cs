namespace PowerLanguage.Function
{
        public sealed class ADX : FunctionSimple<double>
        {
            private DirMovement m_dir_mov;

            public int Length{
                get { return m_dir_mov.Length; }
                set { m_dir_mov.Length = value; }
            }

            public ADX(CStudyControl _master) : this(_master, 0) {}

            public ADX(CStudyControl _master, int _data_stream)
                : base(_master, _data_stream) {}

            protected override void Create() {
                m_dir_mov = new DirMovement(this);
            }

            protected override void StartCalc() {
                m_dir_mov.PriceH = Bars.High;
                m_dir_mov.PriceL = Bars.Low;
                m_dir_mov.PriceC = Bars.Close;
            }

            protected override double CalcBar(){
                m_dir_mov.Call();
                return m_dir_mov.ADX[0];
            }
        }
}