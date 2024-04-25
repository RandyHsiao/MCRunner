using PowerLanguage;
using System;
using System.Collections.Generic;
using System.Reflection;

namespace MCRunner.Instruments
{
    public class BarSeries<T> : ISeries<T>
    {
        private IList<Bar> Bars { get; }
        private FieldInfo Field { get; }

        private readonly Type type = typeof(T);

        public T this[int barsAgo]
        {
            get
            {
                if (barsAgo < 0)
                {
                    throw new IndexOutOfRangeException("Can't look into the future!");
                }

                var count = Bars.Count;
                var index = count - 1 - barsAgo;
                
                if (index < 0)
                {
                    throw new IndexOutOfRangeException(
                        String.Format("{0} is too far back! There are only {1} bars",
                        index, count));
                }

                var bar = Bars[index];
                var value = Field.GetValue(bar);
                return (T)Convert.ChangeType(value, type);
            }
        }

        public T Value
        {
            get
            {
                return this[0];
            }
        }

        public BarSeries(IList<Bar> bars, string fieldName)
        {
            if (bars is null)
            {
                throw new ArgumentNullException("bars must not be null");
            }

            Bars = bars;
            Field = typeof(Bar).GetField(
                fieldName, BindingFlags.Public | BindingFlags.Instance);

            if (Field is null)
            {
                throw new ArgumentException(
                    string.Format("{0} is not a valid Bar field", fieldName));
            }
            
            if (Field.FieldType != type)
            {
                throw new ArgumentException(
                    string.Format("{0} is not the same type as {1}", fieldName, type));
            }
        }
    }
}
