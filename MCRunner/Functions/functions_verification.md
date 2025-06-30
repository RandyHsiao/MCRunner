```
📄 檔名：python/mcrunner/Functions/functions_verification.md
```

````markdown
# Function Verification Structure

本資料夾為 MultiCharts 所使用的技術指標運算 Function 實作與對照區。目標為：

- 建立 PowerLanguage、MultiCharts.NET、Python 間的 Function 對照表
- 支援指標與策略層級運作的 Python 架構（模仿 MultiCharts.NET 風格）
- 提供重構指標程式的依據：將 `PY_*.py` 中內嵌的 Function 拆分出來，改為呼叫共用模組

---

## 🔧 命名與結構原則

| 類別            | 格式說明                           | 副檔名 | 範例             |
|-----------------|------------------------------------|--------|------------------|
| PowerLanguage    | 原始 `.txt` 程式（由 MC 匯出）         | `.txt` | `XAverage.txt`   |
| MultiCharts .NET | C# 撰寫之 .NET 函式實作               | `.cs`  | `XAverage.cs`    |
| Python 重構版    | 依照 MCRunner 架構重寫（預期放入 `functions/` 資料夾） | `.py`  | `xaverage.py`    |

**目前的 Functions 還在轉寫中，`functions/` 資料夾尚未建立，但重構方向與架構如下說明。**

---

## 📚 Function 對照表（目前已收錄）

| 功能名稱            | PowerLanguage        | MultiCharts.NET         | 備註或用途                                      |
|---------------------|----------------------|--------------------------|-------------------------------------------------|
| ADX                 | `ADX.txt`            | `ADX.cs`                | `Indicator.ADX` 會呼叫 `Function.ADX`         |
| AverageFC           | `AverageFC.txt`      | `AverageFC.cs`          | 提供給 Bollinger Bands 中心線用               |
| XAverage            | `XAverage.txt`       | `XAverage.cs`           | 指數加權移動平均 (Wilder EMA), 給 RSI/MACD 用 |
| SummationFC         | `SummationFC.txt`    | `SummationFC.cs`        | 用於 MACD 中的基礎計算                          |
| RSI                 | `RSI.txt`            | `RSI.cs`                | 有用到 `XAverage`                               |
| MACD                | `MACD.txt`           | `MACD.cs`               | 用到 `SummationFC`, `XAverage`, `AverageFC`     |
| StandardDev         | `StandardDev.txt`    | （對應為 `StdError.cs`） | 無直接命名對應，推測使用 .NET 內建實作         |
| VariancePS          | `VariancePS.txt`     | 無明確對應               | 可能為 PowerLanguage 專用                      |

---

## 🧪 Python 架構重構原則

1. **所有 Function 運算邏輯應獨立於 indicators 檔案之外**，統一放入 `functions/*.py` 中。
2. 每個 Function 的 Python 實作格式應如下：

```python
# 例如：xaverage.py
def xaverage(close: Sequence[float], length: int = 14) -> List[float]:
    ...
````

3. `indicators/PY_*.py` 中應只保留：

   * `Create(ctx)`、`StartCalc()`、`CalcBar()` 架構
   * 對應 `ctx.AddPlot(...)` 及 `Alerts.Alert(...)` 的調用邏輯
   * 其餘技術運算呼叫 `from mcrunner.functions import xaverage` 等

---

## 📌 關於 `ctx` 的補充說明

MultiCharts.NET 與 MCRunner 的指標架構皆使用：

```csharp
public class SomeIndicator : IndicatorObject {
    ...
    protected override void Create() {
        plot1 = AddPlot(...);
    }

    protected override void CalcBar() {
        ...
    }
}
```

對應 Python 中，`ctx` 通常作為 context 傳入，用於呼叫：

* `ctx.AddPlot(...)`
* `ctx.Alerts.Alert(...)`

初版的 `.py` 多數 **未明確傳入 ctx**，導致無法呼叫這些內建功能。後續應：

* 加入 `def Create(self, ctx)` 並保存 `self.ctx = ctx`
* 修改 `self.ctx.AddPlot(...)` 與 `self.ctx.Alerts.Alert(...)`

---

## 🧭 建議修正方向

* 檢查 `PY_*.py` 中是否仍內嵌了運算邏輯（如 ADX, RSI 等）
* 若是，應將其拆出至 `functions/` 資料夾，並調整 import 呼叫
* 若 ctx 未使用，應補上 `Create(self, ctx)` 與相關內容
* 確保所有指標遵守 `Create → StartCalc → CalcBar` 流程設計（與 `StrategyRunner` 呼叫邏輯一致）

---

## 🔁 後續驗證建議

* 對照 `.csv` 指標輸出結果與 `functions/*.py` 結果是否一致
* 檢查是否仍有任何 Function 重複實作在指標內
* 撰寫 `test_functions_accuracy.py` 進行函數單元測試

```

