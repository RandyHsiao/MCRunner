using System;

namespace PowerLanguage.Function
{
    ///<summary>
    /// Simple function�s class that provides a way to use <see cref="PowerLanguage.PublicFunctions.StandardError"/>.
    ///</summary>
    public class StdError : FunctionSimple<Double>
    {
        public StdError(CStudyControl ctx) :
            base(ctx) {}

        public StdError(CStudyControl ctx, int data_stream) :
            base(ctx, data_stream) {}

        public ISeries<Double> price { get; set; }

        public Int32 length { get; set; }

        protected override double CalcBar(){
            return price.StandardError(length);
        }
    }
}