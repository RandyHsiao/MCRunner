using System;
namespace PowerLanguage.Function
{
        public sealed class DirMovement : FunctionSeries<bool>
        {
            public DirMovement(CStudyControl _master) : this(_master, 0) {}
            public DirMovement(CStudyControl _master, int _data_stream) : base(_master, _data_stream) { }

            private Cum m_cumm;

            private VariableSeries<double> m_avg_plus_dm;
            private VariableSeries<double> m_avg_minus_dm;

            private VariableSeries<double> m_oDMI;
            private VariableSeries<double> m_oADX;
            private VariableSeries<double> m_oADXR;
            private VariableSeries<double> m_oVolty;
            private VariableSeries<double> m_oDMIPlus;
            private VariableSeries<double> m_oDMIMinus;

            private VariableObject<double> m_sum_plus_dm;
            private VariableObject<double> m_sum_minus_dm;
            private VariableObject<double> m_sum_tr;

            public ISeries<double> PriceH { get; set; }
            public ISeries<double> PriceL { get; set; }
            public ISeries<double> PriceC { get; set; }

            private int m_length = 1;

            public int Length{
                get { return m_length; }
                set { m_length = Math.Max(1, value); }
            }

            public ISeries<double> DMIPlus{get { return m_oDMIPlus; }}

            public ISeries<double> DMIMinus { get { return m_oDMIMinus; } }

            public ISeries<double> DMI{
                get { return m_oDMI; }
            }

            public ISeries<double> ADX{
                get { return m_oADX; }
            }

            public ISeries<double> ADXR { get { return m_oADXR; } }

            public ISeries<double> Volty{
                get { return m_oVolty; }
            }

            private double SmoothFactor{
                get { return 1.0/Length; }
            }

            protected override void Create() {
                m_oDMI = new VariableSeries<double>(this);
                m_oADX = new VariableSeries<double>(this);
                m_oADXR = new VariableSeries<double>(this);
                m_oVolty = new VariableSeries<double>(this);
                m_oDMIPlus = new VariableSeries<double>(this);
                m_oDMIMinus = new VariableSeries<double>(this);

                m_cumm = new Cum(this);

                m_avg_plus_dm = new VariableSeries<double>(this);
                m_avg_minus_dm = new VariableSeries<double>(this);

                m_sum_plus_dm = new VariableObject<double>(this);
                m_sum_minus_dm = new VariableObject<double>(this);
                m_sum_tr = new VariableObject<double>(this);
            }

            protected override void StartCalc() {
                m_cumm.price = m_oDMI;
            }

            protected override bool CalcBar(){
                var _current_bar = Bars.CurrentBar;
                if (1 == _current_bar){
                    for (var i = 0; i < Length; i++){
                        double _plus_dm = 0, _minus_dm = 0;
                        var _upper_move = PriceH[i] - PriceH[i + 1];
                        var _lower_move = PriceL[i + 1] - PriceL[i];

                        if (PublicFunctions.DoubleGreater(_upper_move, _lower_move) && PublicFunctions.DoubleGreater(_upper_move, 0))
                            _plus_dm = _upper_move;
                        else if (PublicFunctions.DoubleGreater(_lower_move, _upper_move) && PublicFunctions.DoubleGreater(_lower_move, 0))
                            _minus_dm = _lower_move;

                        m_sum_plus_dm.Value += _plus_dm;
                        m_sum_minus_dm.Value += _minus_dm;
                        m_sum_tr.Value += PriceH.TrueRangeCustom(PriceL, PriceC, i);
                    }
                    m_avg_plus_dm.Value = m_sum_plus_dm.Value/Length;
                    m_avg_minus_dm.Value = m_sum_minus_dm.Value/Length;
                    m_oVolty.Value = m_sum_tr.Value/Length;
                }
                else{
                    double _plus_dm = 0, _minus_dm = 0;
                    var _upper_move = PriceH[0] - PriceH[1];
                    var _lower_move = PriceL[1] - PriceL[0];

                    if (PublicFunctions.DoubleGreater(_upper_move, _lower_move) && PublicFunctions.DoubleGreater(_upper_move, 0))
                        _plus_dm = _upper_move;
                    else if (PublicFunctions.DoubleGreater(_lower_move, _upper_move) && PublicFunctions.DoubleGreater(_lower_move, 0))
                        _minus_dm = _lower_move;

                    m_avg_plus_dm.Value = m_avg_plus_dm[1] + SmoothFactor*(_plus_dm - m_avg_plus_dm[1]);
                    m_avg_minus_dm.Value = m_avg_minus_dm[1] + SmoothFactor*(_minus_dm - m_avg_minus_dm[1]);
                    m_oVolty.Value = Volty[1] +
                                     SmoothFactor*(PriceH.TrueRangeCustom(PriceL, PriceC) - Volty[1]);
                }

                var _oVoltyVal = m_oVolty.Value;
                
                var dmiPlus = .0;
                var dmiMinus = .0;

                if (PublicFunctions.DoubleGreater(_oVoltyVal, 0)){
                    dmiPlus = 100*m_avg_plus_dm[0]/_oVoltyVal;
                    dmiMinus = 100*m_avg_minus_dm[0]/_oVoltyVal;
                }

                m_oDMIPlus.Value = dmiPlus;
                m_oDMIMinus.Value = dmiMinus;

                var _divisor = dmiPlus + dmiMinus;
                if (PublicFunctions.DoubleGreater(_divisor, 0))
                    m_oDMI.Value = 100*Math.Abs(dmiPlus - dmiMinus)/_divisor;
                else
                    m_oDMI.Value = 0;

                if (_current_bar <= Length && _current_bar > 0){
                    m_oADX.Value = m_cumm.Value/_current_bar;
                    m_oADXR.Value = (ADX[0] + ADX[_current_bar - 1]) / 2;
                }
                else{
                    m_oADX.Value = ADX[1] + SmoothFactor*(DMI[0] - ADX[1]);
                    m_oADXR.Value = (ADX[0] + ADX[Length - 1]) / 2;
                }

                return true;
            }
        }
}