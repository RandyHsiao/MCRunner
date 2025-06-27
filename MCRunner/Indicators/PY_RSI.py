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

class PY_RSI:
    
    overbcolor = Color.Red
    overscolor = Color.Cyan
    overbought = 70
    oversold = 30
    length = 14
    
    def GetInputs(self):
        return Array[InputInfo]([InputInfo('overbcolor', clr.GetClrType(Color)), InputInfo('overscolor', clr.GetClrType(Color)), InputInfo('overbought', clr.GetClrType(Double)), InputInfo('oversold', clr.GetClrType(Double)), InputInfo('length', clr.GetClrType(Double))])
            
    def GetInputValue(self, name):
        if name == 'overbcolor':
            return self.overbcolor
        if name == 'overscolor':
            return self.overscolor
        if name == 'overbought':
            return Double(self.overbought)
        if name == 'oversold':
            return Double(self.oversold)
        if name == 'length':
            return Double(self.length)
            
    def SetInputValue(self, name, value):
        if name == 'overbcolor':
            self.overbcolor = value
        if name == 'overscolor':
            self.overscolor = value
        if name == 'overbought':
            self.overbought = value
        if name == 'oversold':
            self.oversold = value
        if name == 'length':
            self.length = value
            
    def Create(self, ctx):
        # create variable objects, function objects, plot objects etc.
        self.__ctx = ctx
        self.m_rsi1 = PLFunction.RSI(ctx)
        self.m_myrsi = VariableSeries[Double](ctx)
        self.Plot1 = ctx.AddPlot(PlotAttributes("RSI", EPlotShapes.Line, Color.Silver, Color.Empty, Int32(0), EPlotStyle.Solid, Boolean(True)))
        self.Plot2 = ctx.AddPlot(PlotAttributes("OverBot", EPlotShapes.Line, Color.Green, Color.Empty, Int32(0), EPlotStyle.Solid, Boolean(True)))
        self.Plot3 = ctx.AddPlot(PlotAttributes("OverSld", EPlotShapes.Line, Color.Green, Color.Empty, Int32(0), EPlotStyle.Solid, Boolean(True)))
        
    def StartCalc(self):
        # assign inputs 
        self.m_rsi1.price = self.__ctx.Bars.Close
        self.m_rsi1.length = Convert.ToInt32(self.length)

    def CalcBar(self):
        # indicator logic 
        self.m_myrsi.Value = self.m_rsi1[0]
        self.Plot1.SetValue(self.m_myrsi.Value)
        self.Plot2.SetValue(self.overbought)
        self.Plot3.SetValue(self.oversold)
        if PublicFunctions.DoubleGreater(self.m_myrsi.Value, self.overbought):
            self.Plot1.Colors[0] = self.overbcolor
        else:
            if PublicFunctions.DoubleLess(self.m_myrsi.Value, self.oversold):
                self.Plot1.Colors[0] = self.overscolor
        if PublicFunctions.CrossesOver(self.__ctx, self.m_myrsi, self.oversold):
            self.__ctx.Alerts.Alert("Indicator exiting oversold zone")
        else:
            if PublicFunctions.CrossesUnder(self.__ctx, self.m_myrsi, self.overbought):
                self.__ctx.Alerts.Alert("Indicator exiting overbought zone")
            
