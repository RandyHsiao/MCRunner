# Indicator Verification Structure

本資料夾用於收錄 MultiCharts 指標的三種版本實作（PowerLanguage / C# / Python），並建立對應關係以利後續自動化比對與驗證。

## 🔧 命名與副檔名規則

| 語言版本        | 檔名格式說明                    | 副檔名 |
|-----------------|---------------------------------|--------|
| PowerLanguage    | 與指標名稱一致（如 `ADX.txt`）     | `.txt` |
| MultiCharts .NET | 與指標名稱一致（如 `ADX.cs`）      | `.cs`  |
| MC x Python      | 加上 `PY_` 前綴（如 `PY_ADX.py`） | `.py`  |

這些檔案皆放在 `indicators/` 資料夾中，無需再分子資料夾，藉由檔案名稱與副檔名即可自動判別語言版本與對應指標。

---

## 📚 指標對應表

| 指標名稱           | PowerLanguage       | C# (.NET)          | Python (MC.NET)      |
|--------------------|---------------------|--------------------|----------------------|
| ADX                | `ADX.txt`           | `ADX.cs`           | `PY_ADX.py`          |
| Bollinger Bands    | `Bollinger_Bands.txt` | `Bollinger_Bands.cs` | `PY_Bollinger_Bands.py` |
| MACD               | `MACD.txt`          | `MACD.cs`          | `PY_MACD.py`         |
| Mov Avg 1 Line     | `Mov_Avg_1_Line.txt`| `Mov_Avg_1_Line.cs`| `PY_Mov_Avg_1_Line.py` |
| RSI                | `RSI.txt`           | `RSI.cs`           | `PY_RSI.py`          |

---

## 📁 資料夾說明

所有對應檔案請放置於：

project-root/
└── indicators/
├── ADX.txt
├── ADX.cs
├── PY_ADX.py
├── ...
└── indicator_verification.md ← 本說明文件

---

## 🧪 驗證資料與 Python 運算行為說明

已匯出一份指標驗證資料檔案：

2330_1_Day_With_Indicators.csv

此檔案為以 MultiCharts 執行五個指標（ADX、Bollinger Bands、MACD、Mov Avg 1 Line、RSI）後，透過於每個指標中加入 `Print` 指令所輸出。內容包含：

- 原始歷史資料（Open, High, Low, Close, Volume...）  
- 所有指標內部運算過程中輸出的中間值與最終值  
- 每個指標可能輸出多個欄位（例如 Bollinger Bands 同時輸出中軌、上軌、下軌）

其對應的原始歷史資料為：

instruments/data/2330 1 Day.txt

`.csv` 可視為該 `.txt` 資料集的擴充版本，用於比對驗證各個 Python 指標實作與 MultiCharts 結果是否一致。因檔案放置於 `indicators/` 資料夾下，故改以 `.csv` 儲存以避免與 `.txt` 混淆。


## 📌 Python 指標驗證邏輯

目標是：

> 在不開啟 MultiCharts 的情況下，僅使用 `PY_*.py` 的官方 Python 版本指標程式碼，直接在本地執行，並比對 `.csv` 的結果。

若能驗證一致，則可採用此程式碼為運算邏輯基底，改寫成 MCRunner 版本以進行回測。

---

## ⚠️ 注意事項

- `PY_*.py` 中多數使用 MultiCharts 提供的內建 `Function`（如 `PLFunction.ADX`），官方未公開其 Python 原始碼，推測是共用 .NET API 實作。
- 在無法使用完整 MultiCharts 執行環境的情況下：
  - 可**移除繪圖、Alerts 等 UI 功能**
  - 僅保留運算邏輯
  - 避免依賴 `ctx.AddPlot` 等無法執行的部分
- 在 MCRunner 的 Python 架構中，建議**模擬 Function 行為並對照 `.csv` 值進行一致性驗證**

---

## 🔁 後續驗證建議

- 撰寫 `test_indicator_accuracy.py` 腳本
  - 讀取 `.csv` 的欄位與輸出
  - 執行 `PY_*.py` 計算結果
  - 比對每一行差異
- 若有缺失的 Function，可在 MCRunner 寫 mock 模擬函式進行補齊


## 🧭 後續驗證建議

未來可基於本結構：
- 匯出 MultiCharts 的指標輸出數據
- 以 Python 模擬對照
- 撰寫比對測試用的 `test_*.py` 腳本
- 更新驗證結果與進度於另一份 `indicator_results.md` 文件
