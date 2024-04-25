namespace MCRunner.Instruments
{
    public class LoadableBars : Bars
    {
        public virtual void AddBar(Bar bar)
        {
            bars = bars.Add(bar);
            ReloadBarSeries();
        }
    }
}
