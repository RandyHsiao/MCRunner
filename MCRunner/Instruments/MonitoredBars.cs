using System.Collections.Generic;
using System;

namespace MCRunner.Instruments
{
    public class MonitoredBars : LoadableBars, IMonitoredInstrument
    {
        public event Action<Bar> Updated;

        public override void AddBar(Bar bar)
        {
            base.AddBar(bar);
            Updated.SafeTrigger(bar);
        }

        public new IEnumerable<IMonitoredInstrument> ToSingleDataStream()
        {
            return new List<IMonitoredInstrument> { this };
        }
    }
}
