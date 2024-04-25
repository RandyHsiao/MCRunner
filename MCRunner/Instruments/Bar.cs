using System;

namespace MCRunner.Instruments
{
    public enum BarType
    {
        Live,
        Historic
    }

    public struct Bar
    {
        public DateTime Time;
        public double High;
        public double Low;
        public double Open;
        public double Close;
        public double Volume;
        public BarType BarType;
    }
}
