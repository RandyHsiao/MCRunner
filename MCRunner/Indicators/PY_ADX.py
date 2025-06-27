import clr
clr.AddReference("System")
clr.AddReference("System.Data")
clr.AddReference("System.Xml")
clr.AddReference("System.Drawing")
clr.AddReference("System.Windows.Forms")
clr.AddReference("System.Core")
clr.AddReference("Microsoft.CSharp")
clr.AddReference("PLTypes")
clr.AddReference("PLStudiesProxy")
clr.AddReference("PLBuiltInFunctions")
clr.AddReference("PLTradeManager")
clr.AddReference("ATCenterProxy.interop")
clr.AddReference("PLDataLoader")

from System import *
from System.Drawing import *
from System.Linq import *
from PowerLanguage import *
import PowerLanguage.Function as PLFunction
import PowerLanguage.Strategy as PLStrategy
import PowerLanguage.Indicator as PLIndicator

class PY_ADX:

    length = 14
    
    def GetInputs(self):
        return Array[InputInfo]([InputInfo('length', clr.GetClrType(Double))])
            
    def GetInputValue(self, name):
        if name == 'length':
            return Double(self.length)
            
    def SetInputValue(self, name, value):
        if name == 'length':
            self.length = value
            
    def Create(self, ctx):
        # create variable objects, function objects, plot objects etc.
        self.__ctx = ctx
        self.m_adx1 = PLFunction.ADX(ctx);
        self.m_adxvalue = VariableSeries[Double](ctx);
        self.plot1 = ctx.AddPlot(PlotAttributes("ADX", EPlotShapes.Line, Color.Cyan, Color.Empty, Int32(0), EPlotStyle.Solid, Boolean(True)))

    def StartCalc(self):
        # assign inputs 
        self.m_adx1.Length = Convert.ToInt32(self.length)
        self.m_adxvalue.DefaultValue = Double(0)

    def CalcBar(self):
        # indicator logic 
        self.m_adxvalue.Value = self.m_adx1[0];
        self.plot1.SetBarsAgoValue(0, self.m_adxvalue.Value)
        if PublicFunctions.DoubleGreater(self.m_adxvalue.Value, self.m_adxvalue[1]) and PublicFunctions.DoubleLessEquals(self.m_adxvalue[1], self.m_adxvalue[2]):
            self.__ctx.Alerts.Alert("Indicator turning up")
        else:
            if PublicFunctions.DoubleLess(self.m_adxvalue.Value, self.m_adxvalue[1]) and PublicFunctions.DoubleGreaterEquals(self.m_adxvalue[1], self.m_adxvalue[2]):
                self.__ctx.Alerts.Alert("Indicator turning down")
