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

class PY_Bollinger_Bands:

    numdevsdn = -2
    numdevsup = 2
    length = 20
    displace = 0
    
    def GetInputs(self):
        return Array[InputInfo]([InputInfo('length', clr.GetClrType(Double)), InputInfo('numdevsup', clr.GetClrType(Double)), InputInfo('numdevsdn', clr.GetClrType(Double)), InputInfo('displace', clr.GetClrType(Double))])
            
    def GetInputValue(self, name):
        if name == 'length':
            return Double(self.length)
        if name == 'numdevsup':
            return Double(self.numdevsup)
        if name == 'numdevsdn':
            return Double(self.numdevsdn)
        if name == 'displace':
            return Double(self.displace)
            
    def SetInputValue(self, name, value):
        if name == 'length':
            self.length = value
        if name == 'numdevsup':
            self.numdevsup = value
        if name == 'numdevsdn':
            self.numdevsdn = value
        if name == 'displace':
            self.displace = value
            
    def Create(self, ctx):
        # create variable objects, function objects, plot objects etc.
        self.__ctx = ctx
        self.m_averagefc1 = PLFunction.AverageFC(ctx)
        self.m_lowerband = VariableSeries[Double](ctx)
        self.m_upperband = VariableSeries[Double](ctx)
        self.Plot1 = ctx.AddPlot(PlotAttributes("UpperBand", EPlotShapes.Line, Color.Yellow, Color.Empty, Int32(0), EPlotStyle.Solid, Boolean(True)))
        self.Plot2 = ctx.AddPlot(PlotAttributes("LowerBand", EPlotShapes.Line, Color.Blue, Color.Empty, Int32(0), EPlotStyle.Solid, Boolean(True)))
        self.Plot3 = ctx.AddPlot(PlotAttributes("MidLine", EPlotShapes.Line, Color.Gray, Color.Empty, Int32(0), EPlotStyle.Solid, Boolean(True)))

    def StartCalc(self):
        # assign inputs 
        self.bollingerprice = self.__ctx.Bars.Close;
        self.testpriceuband = self.__ctx.Bars.Close;
        self.testpricelband = self.__ctx.Bars.Close;
        self.m_averagefc1.price = self.bollingerprice;
        self.m_averagefc1.length = Convert.ToInt32(self.length);

    def CalcBar(self):
        # indicator logic 
        m_avg = Double(0)
        m_avg = self.m_averagefc1[0]
        m_sdev = PublicFunctions.StandardDeviationCustom(self.bollingerprice, Convert.ToInt32(self.length), Convert.ToInt32(1))
        self.m_upperband.Value = (m_avg + (self.numdevsup*m_sdev))
        self.m_lowerband.Value = (m_avg + (self.numdevsdn*m_sdev))
        if (self.displace >= 0) or self.__ctx.Bars.CurrentBar > Math.Abs(self.displace):
            self.Plot1.SetBarsAgoValue(Convert.ToInt32(self.displace), self.m_upperband.Value)
            self.Plot2.SetBarsAgoValue(Convert.ToInt32(self.displace), self.m_lowerband.Value)
            self.Plot3.SetBarsAgoValue(Convert.ToInt32(self.displace), m_avg)
            if self.displace <= 0:
                if PublicFunctions.CrossesOver(self.__ctx, self.testpricelband, self.m_lowerband):
                    self.__ctx.Alerts.Alert("Price crossing over lower price band");
                else:
                    if PublicFunctions.CrossesUnder(self.__ctx, self.testpriceuband, self.m_upperband):
                        self.__ctx.Alerts.Alert("Price crossing under upper price band")
