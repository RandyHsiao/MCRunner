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

yaml
複製
編輯

---

## 🧭 後續驗證建議

未來可基於本結構：
- 匯出 MultiCharts 的指標輸出數據
- 以 Python 模擬對照
- 撰寫比對測試用的 `test_*.py` 腳本
- 更新驗證結果與進度於另一份 `indicator_results.md` 文件
