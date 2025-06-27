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

class PY_MACD:
    
    macdlength = 9
    slowlength = 26
    fastlength = 12
    
    def GetInputs(self):
        return Array[InputInfo]([InputInfo('fastlength', clr.GetClrType(Double)), InputInfo('slowlength', clr.GetClrType(Double)), InputInfo('macdlength', clr.GetClrType(Double))])
            
    def GetInputValue(self, name):
        if name == 'fastlength':
            return Double(self.fastlength)
        if name == 'slowlength':
            return Double(self.slowlength)
        if name == 'macdlength':
            return Double(self.macdlength)
            
    def SetInputValue(self, name, value):
        if name == 'fastlength':
            self.fastlength = value
        if name == 'slowlength':
            self.slowlength = value
        if name == 'macdlength':
            self.macdlength = value
            
    def Create(self, ctx):
        # create variable objects, function objects, plot objects etc.
        self.__ctx = ctx
        self.m_macd1 = PLFunction.MACD(ctx)
        self.m_xaverage1 = PLFunction.XAverage(ctx)
        self.m_mymacd = VariableSeries[Double](ctx)
        self.m_macddiff = VariableSeries[Double](ctx)
        self.Plot1 = ctx.AddPlot(PlotAttributes("MACD", EPlotShapes.Line, Color.Cyan, Color.Empty, Int32(0), EPlotStyle.Solid, Boolean(True)))
        self.Plot2 = ctx.AddPlot(PlotAttributes("MACDAvg", EPlotShapes.Line, Color.Yellow, Color.Empty, Int32(0), EPlotStyle.Solid, Boolean(True)))
        self.Plot3 = ctx.AddPlot(PlotAttributes("MACDDiff", EPlotShapes.Histogram, Color.Blue, Color.Empty, Int32(0), EPlotStyle.Solid, Boolean(True)))
        self.Plot4 = ctx.AddPlot(PlotAttributes("ZeroLine", EPlotShapes.Line, Color.Green, Color.Empty, Int32(0), EPlotStyle.Solid, Boolean(True)))
        
    def StartCalc(self):
        # assign inputs 
        self.m_macd1.Price = self.__ctx.Bars.Close
        self.m_macd1.FastLength = Convert.ToInt32(self.fastlength)
        self.m_macd1.SlowLength = Convert.ToInt32(self.slowlength)
        self.m_xaverage1.Price = self.m_mymacd
        self.m_xaverage1.Length = Convert.ToInt32(self.macdlength)
        self.m_mymacd.DefaultValue = Double(0)
        self.m_macddiff.DefaultValue = Double(0)

    def CalcBar(self):
        # indicator logic 
        self.m_mymacd.Value = self.m_macd1[0]
        m_macdavg = self.m_xaverage1[0]
        self.m_macddiff.Value = self.m_mymacd.Value - m_macdavg
        self.Plot1.SetValue(self.m_mymacd.Value)
        self.Plot2.SetValue(m_macdavg)
        self.Plot3.SetValue(self.m_macddiff.Value)
        self.Plot4.SetValue(0)
        if PublicFunctions.CrossesOver(self.__ctx, self.m_macddiff, 0):
            self.__ctx.Alerts.Alert("Bullish alert")
        else:
            if PublicFunctions.CrossesUnder(self.__ctx, self.m_macddiff, 0):
                self.__ctx.Alerts.Alert("Bearish alert")
            
