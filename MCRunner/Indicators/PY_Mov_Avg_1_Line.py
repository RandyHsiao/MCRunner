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
clr.AddReference("PLStudiesProxyPython")
clr.AddReference("PLBuiltInFunctions")
clr.AddReference("PLTradeManager")
clr.AddReference("ATCenterProxy.interop")
clr.AddReference("PLDataLoader")

from System import *
from System.Diagnostics import *
from System.Drawing import *
from System.Linq import *
from PowerLanguage import *
import PowerLanguage.Function as PLFunction
import PowerLanguage.Strategy as PLStrategy
import PowerLanguage.Indicator as PLIndicator

class PY_Mov_Avg_1_Line:
    
    length = 9
    displace = 0
    
    def GetInputs(self):
        return Array[InputInfo]([InputInfo('length', clr.GetClrType(Double)), InputInfo('displace', clr.GetClrType(Double))])
            
    def GetInputValue(self, name):
        if name == 'length':
            return Double(self.length)
        if name == 'displace':
            return Double(self.displace)
            
    def SetInputValue(self, name, value):
        if name == 'length':
            self.length = value
        if name == 'displace':
            self.displace = value
        
    def Create(self, ctx):
        # create variable objects, function objects, plot objects etc.
        self.__ctx = ctx
        self.m_averagefc1 = PLFunction.AverageFC(ctx)
        self.m_avg = VariableSeries[Double](ctx)
        self.Plot1 = ctx.AddPlot(PlotAttributes("Avg", EPlotShapes.Line, Color.Yellow, Color.Empty, Int32(0), EPlotStyle.Solid, Boolean(True)))

    def StartCalc(self):
        # assign inputs 
        self.price = self.__ctx.Bars.Close
        self.m_averagefc1.price = self.price
        self.m_averagefc1.length = Convert.ToInt32(self.length)
    
    def CalcBar(self):
        # indicator logic 
        self.m_avg.Value = self.m_averagefc1[0];
        if self.displace >= 0 or self.__ctx.Bars.CurrentBar > Math.Abs(Convert.ToInt32(self.displace)):
            self.Plot1.SetBarsAgoValue(Convert.ToInt32(self.displace), Double(self.m_avg.Value))
            if self.displace <= 0:
                if PublicFunctions.CrossesOver(self.__ctx, self.price, self.m_avg):
                    self.__ctx.Alerts.Alert("Price crossing over average")
                else:
                    if PublicFunctions.CrossesUnder(self.__ctx, self.price, self.m_avg):
                        self.__ctx.Alerts.Alert("Price crossing under average")
        