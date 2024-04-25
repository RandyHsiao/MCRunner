using System;
using System.Collections.Generic;

namespace MCRunner.Instruments
{
    public class PlayableBars : Bars
    {
        private IEnumerable<Bar> BarsToPlay { get; set; }

        public PlayableBars(IEnumerable<Bar> barsToPlay)
        {
            BarsToPlay = new List<Bar>(barsToPlay);
        }

        public void Play(Action action)
        {
            Play(bar => action());
        }

        public void Play(Action<Bar> action)
        {
            bars.Clear();

            foreach (var bar in BarsToPlay)
            {
                bars = bars.Add(bar);
                ReloadBarSeries();
                action(bar);
            }

            BarsToPlay = null;
        }
    }
}
