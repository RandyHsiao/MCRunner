using PowerLanguage;
using System;

namespace MCRunner.Instruments
{
    public interface IMonitoredInstrument : IInstrument
    {
        public event Action<Bar> Updated;
    }
}
