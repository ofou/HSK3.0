# HSK official Query System
Word, character, grammar, task and topic lists for the new HSK, as CSV — a mirror of the official query system, checked against the published table on every sync. Current syllabus: 《HSK 考试大纲》, released 2025-11, in force from 2026-07.

Data source: https://www.chinesetest.cn/syllabus

## Syllabus — HSK 3.0 (2025)

《HSK 考试大纲》 *Syllabus for the Chinese Proficiency Test*, released 2025-11 by 中外语言交流合作中心, in force from 2026-07.

Every number below is verified against the API on each run — [the workflow](.github/workflows/sync.yml) fails if this table and the data disagree, and [`大纲.csv`](大纲.csv) is the same table as data.

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

UTF-8, CRLF, Chinese header row, one entry per row, `No.` contiguous from 1. Every data-bearing endpoint of the official query system is mirrored here — 17217 rows in total.

| file | rows | columns | upstream |
|---|---|---|---|
| [`词汇.csv`](词汇.csv) | 11000 | `No., 级别, 词语, 拼音, 词性` — vocabulary: level, word, pinyin, part of speech | `glossaryPage`, `type=1` |
| [`汉字.csv`](汉字.csv) | 3088 | `No., 级别, 汉字` — characters for recognition | `hanziPage`, `type=1` |
| [`手写汉字.csv`](手写汉字.csv) | 1200 | `No., 级别, 汉字` — characters for writing | `hanziPage`, `type=2` |
| [`语法.csv`](语法.csv) | 593 | `No., 级别, 类别, 类别名称, 细目, 语法内容, 例句` — grammar, with example sentences | `languagePage` |
| [`任务.csv`](任务.csv) | 678 | `No., 级别, 任务类型, 任务示例` — 任务大纲: what a candidate must be able to do | `taskPage` |
| [`话题.csv`](话题.csv) | 427 | `No., 级别, 一级话题, 二级话题, 三级话题` — 话题大纲: topic areas and their items | `topicPage` |
| [`专有名词.csv`](专有名词.csv) | 231 | `No., 等次, 词语, 类别` — proper nouns by category | `glossaryPage`, `type=2` |
| [`大纲.csv`](大纲.csv) | 7 | `级别` + introduced and cumulative counts per dimension — the table above as data | derived |

`级别` is `一级`…`六级`, `七-九级`. In [`词汇.csv`](词汇.csv) a word that returns at a higher band with another sense carries both, e.g. `四级（五级）`; the band it counts against is the first one. Writing characters start at band 2: bands 1–2 share one list of 100. The 2025 syllabus has no syllable list, so there is no 音节 file; the 2021 lists are in the git history, up to tag [`3.0`](https://github.com/ofou/hsk/tree/3.0).

[`专有名词.csv`](专有名词.csv) is the odd one out: the API serves it from the vocabulary table but it is graded 初等/中等/高等 rather than by band, has no pinyin, and its 231 entries are **not** part of the 11000 — it is the 2021 standard's proper-noun appendix, 34 categories from 省级行政区域简称 and 节气 to 名胜古迹 and 朝代.

## Releases

A [monthly workflow](.github/workflows/sync.yml) rebuilds all eight files from the API and, when anything changed, publishes them as an **English-headed build**: identical Chinese data, English column names, ASCII filenames.

```sh
curl -LO https://github.com/ofou/hsk/releases/latest/download/vocabulary.csv   # 词汇.csv
curl -LO https://github.com/ofou/hsk/releases/latest/download/characters.csv   # 汉字.csv
curl -LO https://github.com/ofou/hsk/releases/latest/download/handwriting.csv  # 手写汉字.csv
curl -LO https://github.com/ofou/hsk/releases/latest/download/grammar.csv      # 语法.csv
curl -LO https://github.com/ofou/hsk/releases/latest/download/tasks.csv        # 任务.csv
curl -LO https://github.com/ofou/hsk/releases/latest/download/topics.csv       # 话题.csv
curl -LO https://github.com/ofou/hsk/releases/latest/download/propernouns.csv  # 专有名词.csv
curl -LO https://github.com/ofou/hsk/releases/latest/download/syllabus.csv     # 大纲.csv
```

Headers become `No., Level, Word, Pinyin, PartOfSpeech`, `No., Level, Character`, `No., Level, Category, Subcategory, Detail, Content, Examples`, `No., Level, TaskType, TaskExample`, `No., Level, Topic, Subtopic, Items` and `No., Tier, Word, Category`. Each release also carries `SHA256SUMS.txt` and a per-band count table.

The job is a full rebuild, never a patch. It fails instead of writing when the API answers with something unexpected: a page count that disagrees with the reported total, a row count more than 5% below what is on disk, a hole in `No.`, an unknown band, a blank entry, or a record type it does not know how to store. It also asserts coverage — rows written must equal rows served — so a new section appearing upstream breaks the build instead of going unnoticed.

Most importantly it asserts the **mirror** itself: per-band counts must equal the published 2025 table, and the table in this README must equal what the API returned. Either disagreement fails the run and prints the offending cells. A genuine new edition of the syllabus is therefore a deliberate act — dispatch with `allow_table_drift`, then update the table here — rather than something that lands silently.

`upstream: derived` in the table above means computed from the other files, not fetched.

## Sources

Every row and every figure above was checked against both official sources:

- [新版HSK考试大纲1219.pdf](https://hsk.cn-bj.ufileos.com/3.0/%E6%96%B0%E7%89%88HSK%E8%80%83%E8%AF%95%E5%A4%A7%E7%BA%B21219.pdf) — the 406-page syllabus. Vocabulary 序号 runs 1–11000 with band breaks at 300/500/1000/2000/3600/5400; the 认读字 lists end at 246/125/284/441/431/413/1148.
- [chinesetest.cn/syllabus](https://www.chinesetest.cn/syllabus) — the official query system, `POST /api/hsk/outline/{glossaryPage,hanziPage,languagePage}` with `current` and `size`, which is where these files come from. Per-band `total` with `examLevelId=HSK1…HSK7-9`: grammar 70/78/96/95/70/50/134, 认读字 246/125/284/441/431/413/1148, 书写字 0/100/150/150/150/150/500. Endpoint totals are 593 for `languagePage`, 4288 for `hanziPage` (3088 + 1200) and 11230 for `glossaryPage` — the latter being 10999 words plus a 231-entry proper-noun appendix (`type=2`, tiers 初等/中等/高等) that is not part of the 11000.

[`词汇.csv`](词汇.csv) carries one repair: the query system omits band-5 entry 序号 2472 `好 hào 动` and so returns 10999 words. That entry is in the PDF and has been restored, giving all 11000. Every other row matches the API exactly — [`汉字.csv`](汉字.csv), [`手写汉字.csv`](手写汉字.csv) and [`语法.csv`](语法.csv) are identical to it including row order.

## Updates

25-05-2021: fixed all of typos.
6-6-2021: Change encoding 汉字.csv to UTF8

2022-04-22：fixed 音节 file, and release 2.1 version include csv files and excel sheets file.
2023-11-27 fixed 语法 file.

2023-11-27 added 汉字表 2023（only 3000) and 手写汉字Handwriting 2023.

2026-08-19 fixed the 语法 file that had been uploaded as a GB2312 export: converted it to UTF-8 and recovered the 590 “……” the export had dropped. It turned out to be the 2021 grammar list (572 items, 48/81/81/76/71/67/148), superseded below.

2026-08-19 replaced the data with the 2025 syllabus and dropped the 2021 files: 词汇.csv (11000), 汉字.csv (3088 认读字), 手写汉字.csv (1200 书写字), 语法.csv (593 grammar points, now with 例句). Built from chinesetest.cn's official query API, verified row by row against it and band by band against 《HSK 考试大纲》. 音节 has no 2025 counterpart. The 2021 lists remain in the git history, up to tag 3.0.
