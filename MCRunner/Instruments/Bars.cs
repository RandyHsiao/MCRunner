﻿using PowerLanguage;
using System;
using System.Collections.Immutable;

namespace MCRunner.Instruments
{
    public class Bars : IInstrument
    {
        public int CurrentBar
        {
            get
            {
                var index = bars.Count - 1;
                if (index < 0)
                {
                    throw new IndexOutOfRangeException();
                }

                return index;
            }
        }

        public IInstrumentSettings Info => throw new NotImplementedException();
        public IStatusLine StatusLine => throw new NotImplementedException();

        public double HighValue
        {
            get
            {
                return bars[CurrentBar].High;
            }
        }

        public double LowValue
        {
            get
            {
                return bars[CurrentBar].Low;
            }
        }

        public double OpenValue
        {
            get
            {
                return bars[CurrentBar].Open;
            }
        }

        public double CloseValue
        {
            get
            {
                return bars[CurrentBar].Close;
            }
        }

        public double VolumeValue
        {
            get
            {
                return bars[CurrentBar].Volume;
            }
        }

        public double TicksValue => throw new NotImplementedException();
        public double UpTicksValue => throw new NotImplementedException();
        public double DownTicksValue => throw new NotImplementedException();
        public double OpenIntValue => throw new NotImplementedException();

        public DateTime TimeValue
        {
            get
            {
                return bars[CurrentBar].Time;
            }
        }

        public DateTime LastBarTime
        {
            get
            {
                var lastBar = CurrentBar - 1;
                if (lastBar < 0)
                {
                    throw new IndexOutOfRangeException();
                }

                return bars[lastBar].Time;
            }
        }

        public bool LastBarOnChart => throw new NotImplementedException();
        public bool LastBarInSession => throw new NotImplementedException();
        public double Point => throw new NotImplementedException();
        public EBarState Status => throw new NotImplementedException();
        public IROList<SessionObject> Sessions => throw new NotImplementedException();
        public ISeriesSymbolDataRand FullSymbolData => throw new NotImplementedException();
        public IDOMData DOM => throw new NotImplementedException();
        public InstrumentDataRequest Request => throw new NotImplementedException();
        public DateTime BarUpdateTime => throw new NotImplementedException();
        public uint TickIDValue => throw new NotImplementedException();

        public ISeries<DateTime> Time { get; protected set; }
        public ISeries<double> High { get; protected set; }
        public ISeries<double> Low { get; protected set; }
        public ISeries<double> Open { get; protected set; }
        public ISeries<double> Close { get; protected set; }
        public ISeries<double> Volume { get; protected set; }
        public ISeries<double> Ticks => throw new NotImplementedException();
        public ISeries<double> UpTicks => throw new NotImplementedException();
        public ISeries<double> DownTicks => throw new NotImplementedException();
        public ISeries<double> OpenInt => throw new NotImplementedException();

        protected ImmutableList<Bar> bars = ImmutableList<Bar>.Empty;

        public Bars()
        {
            ReloadBarSeries();
        }

        public ImmutableList<IInstrument> ToSingleDataStream()
        {
            return ImmutableList<IInstrument>.Empty.Add(this);
        }

        protected void ReloadBarSeries()
        {
            Close = new BarSeries<double>(bars, "Close");
            High = new BarSeries<double>(bars, "High");
            Low = new BarSeries<double>(bars, "Low");
            Open = new BarSeries<double>(bars, "Open");
            Time = new BarSeries<DateTime>(bars, "Time");
            Volume = new BarSeries<double>(bars, "Volume");
        }
    }
}