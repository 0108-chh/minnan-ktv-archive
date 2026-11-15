# 闽南语老歌 KTV 库 🎤

从小米电视 ikTV 点歌机里完整导出的 **120 首闽南语老歌 KTV MV**，全部是原盘文件（无转码、无重压），
并且每首都是**原唱 / 伴奏双音轨**——放进任何支持 MKV 的点歌机或播放器，就能切原唱、切伴唱。

这是第一批。希望大家一起把它补成一份完整的闽南语老歌库。

## 下载

视频走 GitHub Releases（单文件超过仓库 100MB 限制）：

**→ [前往 Releases 页面下载](https://github.com/0108-chh/minnan-ktv-archive/releases/latest)**

| 文件 | 内容 |
|---|---|
| `minnan-ktv-120.zip.part-aa ~ part-ad` | 120 首 MKV 的分卷压缩包（用 `cat` / `copy /b` 合并后解压） |
| `manifest.csv` | 全部 120 首的技术清单（时长、大小、编码、音轨） |

合并与解压：

```bash
# Linux / macOS / Git Bash
cat minnan-ktv-120.zip.part-* > minnan-ktv-120.zip && unzip minnan-ktv-120.zip
```

```bat
:: Windows CMD
copy /b minnan-ktv-120.zip.part-aa+minnan-ktv-120.zip.part-ab+minnan-ktv-120.zip.part-ac+minnan-ktv-120.zip.part-ad minnan-ktv-120.zip
```

## 文件说明

- 编码：H.264 + AAC（每首 2 条音轨：原唱、伴奏）
- 容器：Matroska（`.mkv`），4K 电视上直接播没问题
- 单首 20~80MB，总大小约 5.7GB
- 完整技术参数见 [`manifest.csv`](manifest.csv)

## 歌名认领 🙏

电视导出时文件名只有歌曲 ID（如 `60007073.mkv`），歌名存在点歌机的私有数据库里拿不到。
**听过闽南老歌的朋友，帮帮忙认领一下**：打开 [`songs.csv`](songs.csv)，
把「歌名」和「演唱者」两列填上，直接提 Pull Request，一行就好。

认领小技巧：MKV 直接拖进 VLC / PotPlayer 播放就能看到画面，
用「时长 + 大小」对号入座，认领几首算几首，不用全填。

## 如何贡献新歌

想把手里更多的闽南语老歌 KTV MV 加进来？两种方式：

### 方式一：有 ikTV / 点歌机原盘（推荐，质量最高）

1. 参照 [CleanYourTV](https://github.com/Gathin23/cleanyourtv) 的方法用 ADB 从电视导出
   （文件在 `/sdcard/KTVSong/song<N>/` 下，无扩展名，实际是 MKV）
2. 按 `60007073.mkv` 这种「原始 ID.mkv」命名，不要转码
3. 提 PR 上传（或先放网盘开 issue 附链接，由维护者合并进 Release）

### 方式二：手头有视频文件

1. 保持原始画质，MKV 优先；有双音轨（原唱/伴奏）务必保留
2. 文件名写成 `歌名 - 演唱者.mkv`
3. 提 PR 或 [开 issue](https://github.com/0108-chh/minnan-ktv-archive/issues) 附上链接

### 点歌机导入

导入 ikTV 点歌机时把文件改回「原始 ID」无扩展名格式放回 `/sdcard/KTVSong/` 即可；
歌名映射依赖 App 私有数据库，换机后需要重新匹配（这也是认领歌名的价值）。

## 目录结构

```
├── README.md         本文件
├── songs.csv         歌单 + 歌名认领表（持续更新，欢迎 PR）
├── manifest.csv      技术清单（时长/大小/编码/音轨）
└── CONTRIBUTING.md   贡献指南
```

## 免责声明

本仓库仅用于闽南语老歌的**个人学习、研究与怀旧交流**。所有歌曲的版权归各自的
唱片公司、词曲作者及权利人所有。如你的权利受到侵害，请开 issue 联系，我们会立即处理下架。
