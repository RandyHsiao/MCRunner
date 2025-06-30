using System;

namespace PowerLanguage.Function
{
    public static class AvgTrueRange
    {
        public static double AverageTrueRange(this IStudy _this, int length){
            return AverageTrueRange(_this, length, 0);
        }

        public static ISeries<double> AverageTrueRangeSeries(this IStudy _this, int length){
            return new Lambda<double>(_bb => AverageTrueRange(_this, length, _bb));
        }

        public static double AverageTrueRange(this IStudy _this, int length, int bb)
        {
            return _this.TrueRangeSeries(bb).Average(length);
        }

        public static double AverageTrueRange(this IStudy _this, int length, int bb, int datastream)
        {
            return _this.TrueRangeSeries(bb, datastream).Average(length);
        }
    }
}