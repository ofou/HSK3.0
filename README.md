# HSK official Query System
Word, character and grammar lists for the new HSK, as CSV. Current syllabus: 《HSK 考试大纲》 (2025-11, in force 2026-07). The previous standard, 《国际中文教育中文水平等级标准》 *Chinese Proficiency Grading Standards for International Chinese Language Education* (New HSK Levels 2021), is kept alongside it.

Data sources: https://www.chinesetest.cn/syllabus and https://www.blcup.com/CW110?id=1065

## Syllabus — HSK 3.0 (2025)

《HSK 考试大纲》 *Syllabus for the Chinese Proficiency Test*, released 2025-11 by 中外语言交流合作中心, in force from 2026-07.

<table>
  <thead>
    <tr>
      <th rowspan="2">Level</th><th rowspan="2">Band</th>
      <th colspan="2">Words</th>
      <th colspan="2">Characters<br>(recognition)</th>
      <th colspan="2">Characters<br>(writing)</th>
      <th colspan="2">Grammar points</th>
    </tr>
    <tr>
      <th>introduced</th><th>cumulative</th>
      <th>introduced</th><th>cumulative</th>
      <th>introduced</th><th>cumulative</th>
      <th>introduced</th><th>cumulative</th>
    </tr>
  </thead>
  <tbody>
    <tr><td rowspan="3">Beginner</td><td>1</td><td>300</td><td>300</td><td>246</td><td>246</td><td>0</td><td>0</td><td>70</td><td>70</td></tr>
    <tr><td>2</td><td>200</td><td>500</td><td>125</td><td>371</td><td>100</td><td>100</td><td>78</td><td>148</td></tr>
    <tr><td>3</td><td>500</td><td>1000</td><td>284</td><td>655</td><td>150</td><td>250</td><td>96</td><td>244</td></tr>
    <tr><td rowspan="3">Intermediate</td><td>4</td><td>1000</td><td>2000</td><td>441</td><td>1096</td><td>150</td><td>400</td><td>95</td><td>339</td></tr>
    <tr><td>5</td><td>1600</td><td>3600</td><td>431</td><td>1527</td><td>150</td><td>550</td><td>70</td><td>409</td></tr>
    <tr><td>6</td><td>1800</td><td>5400</td><td>413</td><td>1940</td><td>150</td><td>700</td><td>50</td><td>459</td></tr>
    <tr><td>Advanced</td><td>7–9</td><td>5600</td><td>11000</td><td>1148</td><td>3088</td><td>500</td><td>1200</td><td>134</td><td>593</td></tr>
    <tr><td colspan="2"><b>Total</b></td><td colspan="2"><b>11000</b></td><td colspan="2"><b>3088</b></td><td colspan="2"><b>1200</b></td><td colspan="2"><b>593</b></td></tr>
  </tbody>
</table>

## Files

UTF-8, CRLF, Chinese header row, one entry per row. Row counts are the syllabus totals above.

| file | rows | columns |
|---|---|---|
| `词汇 2025.csv` | 11000 | `No., 级别, 词语, 拼音, 词性` — vocabulary: level, word, pinyin, part of speech |
| `汉字 2025.csv` | 3088 | `No., 级别, 汉字` — characters for recognition |
| `手写汉字 2025.csv` | 1200 | `No., 级别, 汉字` — characters for writing |
| `语法 2025.csv` | 593 | `No., 级别, 类别, 类别名称, 细目, 语法内容, 例句` — grammar, with example sentences |

`级别` is `一级`…`六级`, `七-九级`. In `词汇 2025.csv` a word that returns at a higher band with another sense carries both, e.g. `四级（五级）`; the band it counts against is the first one. Writing characters start at band 2: bands 1–2 share one list of 100.

The 2021 standard is still here for comparison — `词汇.csv` (11092), `词汇 2022.csv`, `汉字.csv` (3000 characters over 3149 character/reading rows), `手写汉字 2023.csv` (1200), `音节 2022.csv` (1110 syllables, dropped in 2025) and `语法.csv` (572).

## Sources

Every figure above was checked against both official sources, band by band:

- [新版HSK考试大纲1219.pdf](https://hsk.cn-bj.ufileos.com/3.0/%E6%96%B0%E7%89%88HSK%E8%80%83%E8%AF%95%E5%A4%A7%E7%BA%B21219.pdf) — the 406-page syllabus. Vocabulary 序号 runs 1–11000 with band breaks at 300/500/1000/2000/3600/5400; the 认读字 lists end at 246/125/284/441/431/413/1148.
- [chinesetest.cn/syllabus](https://www.chinesetest.cn/syllabus) — the official query system, `POST /api/hsk/outline/{glossaryPage,hanziPage,languagePage}`, which is where the CSVs above come from. Its `total` fields report the same 11000 / 3088 / 1200 / 593.

One correction was applied while building `词汇 2025.csv`: the query system omits band-5 entry 序号 2472 `好 hào 动`, returning 10999 words. That entry is present in the PDF and has been restored, so the file holds all 11000.

## Updates

25-05-2021: fixed all of typos.
6-6-2021: Change encoding 汉字.csv to UTF8

2022-04-22：fixed 音节 file, and release 2.1 version include csv files and excel sheets file.
2023-11-27 fixed 语法 file.

2023-11-27 added 汉字表 2023（only 3000) and 手写汉字Handwriting 2023.

2026-08-19 restored the 语法 file: converted the GB2312 upload to UTF-8 and recovered the 590 “……” its export had dropped. Its 572 items and 48/81/81/76/71/67/148 split are the 2021 standard, so it is filed as 语法.csv next to 词汇.csv and 汉字.csv, leaving the name 语法 2025.csv free for the 593-item 2025 list.

2026-08-19 added the 2025 syllabus: 词汇 2025.csv (11000), 汉字 2025.csv (3088 认读字), 手写汉字 2025.csv (1200 书写字) and 语法 2025.csv (593 grammar points, with example sentences), built from chinesetest.cn's official query API and checked band by band against 《HSK 考试大纲》. README now documents the 2025 syllabus in English.
