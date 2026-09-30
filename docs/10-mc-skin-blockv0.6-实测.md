# MC 皮肤生成 · BLOCKv0.6 实测记录

> 2026-09-30 实测。**结论：模型可用，但质量上限不如手绘。**

---

## 一、模型可用性：已验证 ✅

| 项目 | 实测值 |
|---|---|
| 模型 | [AliceKJ/BLOCKv0.6](https://huggingface.co/AliceKJ/BLOCKv0.6) · apache-2.0 · 14.88 GB |
| 基座 | FLUX.2-klein-base-4B，官方 `Flux2KleinPipeline` |
| 单次推理 | **13–17 秒**（ZeroGPU，30 步，guidance 4.0） |
| 模型输出 | **512×512** |
| **输出像素网格** | **8× 整数倍**（强边缘间隔中位数 = 8px，实测） |
| 正确降采样 | `NEAREST` → 64×64，**无损** |
| 错误降采样 | LANCZOS / BOX —— 会把像素风糊掉 |

**产出了 3 张结构合法的 64×64 皮肤**：黑发红内层、黑军装红点缀、灰裤腿、红靴底，全部 4096 不透明像素。

---

## 二、阶段一提示词：已验证 ✅

不要让生图模型**直接**输出皮肤图集 —— 它不产出固定几何。

用 [prompts/minecraft-skin.md](https://github.com/lilyco-42/lyco-ip/blob/main/prompts/minecraft-skin.md)
里的**路线 A1** 提示词，让 codex 出「正/背双联斜视角 3D 预览」，**一次成功**：

- 方块人模型、立方头、方柱四肢
- 黑发红内层、白 X 发夹、双排扣红滚边、O 环腰带、不对称红内衬裙、灰裤袜、红底靴
- 纯白底、无文字、无徽章

**关键措辞**（不加这句，模型会给你画图集）：
```
ALSO NO: skin texture atlas, UV layout, unwrapped texture sheet, flat texture
map, or any 2D texture diagram. This must be a 3D RENDERED PREVIEW, not a
texture sheet.
```

---

## 三、翻车记录（按时间顺序，都是真金白银的教训）

### 3.1 `duration` 过度供给 —— 一次调用吃掉一整天配额

复用的公开 Space [HoletAI/block-minecraft-skin-generator](https://huggingface.co/spaces/HoletAI/block-minecraft-skin-generator)
把 `@spaces.GPU(duration=270)` 写死了。

免费用户每天 ZeroGPU 配额约 **300 秒** → **跑一次就几乎用光**。

```
AppError: You have exceeded your free ZeroGPU quota (270s requested vs. 268s left).
          Try again in 23:51:17.
```

**教训**：官方规范说 `duration = round(measured_max × 1.4)`，
**不要留"舒适余量"** —— 配额比较是 `requested vs remaining`，不是 `actual vs remaining`。
实测单次只要 **13–17 秒**，写 30–45 秒就够，写 270 秒等于把别人的额度也一起堵死。

### 3.2 匿名访客会被 duration 挡住

未登录时调用同一个 Space：
```
AppError: The requested GPU duration (270s) is larger than the maximum allowed
```

**登录后**（用自己的免费配额）才能跑通。

### 3.3 自建 Space：新账号托管不了

`lyco42` 账号实测免费额度的三个门槛：

| 尝试 | 结果 |
|---|---|
| 建 Gradio Space（默认 cpu-basic） | `402 Payment Required` —— 需要 PRO |
| 建 Gradio Space + 显式 `hardware: zero-a10g` | `402` —— **"You must be subscribed to PRO to host Spaces with ZeroGPU. If you recently created your account, please wait 30 days or request a community grant."** |
| 建 **Static** Space | 创建成功、`stage=RUNNING`、文件全部上传 —— 但 **`domains: None`，所有路径 404**（HF 主站的通用 404，`x-request-id` 来自 huggingface.co 而非容器） |

**结论**：账号不满 30 天时，**Static 也起不来**。已删除该半成品 Space。

**可行的三条路**（按代价排序）：
1. **直接用现成的公开 Space** —— 已验证可用，无需任何账号动作
2. **等账号满 30 天** —— 之后可免费托管 2 个 ZeroGPU Space
3. **申请社区 GPU grant** 或订阅 PRO

### 3.4 踩到的环境坑（与本机有关，非通用）

| 坑 | 现象 | 解法 |
|---|---|---|
| `NO_PROXY` 含裸 `::1` | `hf` CLI 抛 `httpx.InvalidURL: Invalid port: ':1]'` | 在 **Python 进程内**删除重建 `os.environ`；PowerShell 层改会被 profile 覆盖 |
| `hf.exe` 是 uv shim | 会重读系统环境，进程内改动无效 | 绕开 CLI，直接用 `huggingface_hub` Python API |
| `HF_TOKEN` 在用户级持久变量里 | 子进程没继承 | `winreg` 读 `HKEY_CURRENT_USER\Environment` |

---

## 四、质量评价：诚实版

### 能用的部分
- **结构合法**：输出的 64×64 是真正的 Minecraft 皮肤 UV 布局，可直接导入
- **整体配色对**：黑 + 红 + 灰 + 肤，符合人设
- **轮廓可读**：黑发、黑军装、灰腿、红靴底，远看能认出是同一个角色

### 不行的部分
- **脸**：64×64 里脸只有 **8×8 像素**，模型输出偏白块，眼睛/嘴几乎不可辨
- **细节丢失**：X 发夹、双排扣、O 环腰带基本糊掉
- **随机性大**：换 seed 出来差别明显，没有稳定收敛

### 和手绘对比

| | BLOCKv0.6 | 手绘 [`LYCO_mc_skin_v2_slim.png`](../../platform/minecraft/) |
|---|---|---|
| 速度 | 13–17 秒 | 需要人工画 |
| 结构合法性 | ✅ | ✅ |
| **脸** | ❌ 偏白块 | ✅ 半垂灰眼 + 白高光 + 深色上眼睑 |
| 细节特征 | 基本丢失 | ✅ X 发夹、银扣、O 环、靴扣 |
| 可复现 | 靠 seed 碰运气 | ✅ 完全可复现 |

**结论：AI 生成目前打不过手绘，原因不在模型，在 8×8 这个物理分辨率上限。**

---

## 五、正确的用法（推荐）

```
① 生图出概念 / 出 3D 预览      ← GPT，快，用来定方向
② BLOCKv0.6 出皮肤草稿         ← 13–17 秒，用来试配色和整体感觉
③ ★ 代码逐像素手绘最终皮肤      ← tools/build_mc_skin_v2.py，唯一能落地细节的路
```

**AI 负责「好看」，代码负责「准确」。** 这条在本项目里已经被验证三次了
（武器图集带、ChatGPT 高分图、BLOCK 皮肤）。

---

## 六、复现命令

```bash
# 阶段一：出 3D 预览（提示词见 prompts/minecraft-skin.md 路线 A1）
oma image generate --vendor codex --size 1024x1024 \
    --out ./preview -y -r design/three-view/lyco_three_view.png "<A1 提示词>"

# 阶段二：调现成 Space 出皮肤
python tools/block_skin_client.py ./preview/xxx.png ./out
```

脚本：`tools/block_skin_client.py`、`tools/seed_sweep.py`
