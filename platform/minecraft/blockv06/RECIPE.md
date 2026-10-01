# BLOCKv0.6 · Lyco 皮肤生成配方（可复现）

> 这份文档记录**怎么把 Lyco 的 3D 预览图变成 64×64 Minecraft 皮肤**的完整配方。
> 所有参数都是实测出来的，不是猜的。产物见 [`seeds/`](seeds/)，可复现的 notebook 见 [`notebook/`](notebook/)。

---

## 完整管线

```
① lyco-ip 三视图 (design/three-view/lyco_three_view.png)
        │
        │  codex / gpt-image-2，用 prompts/minecraft-skin.md 的「路线 A1」提示词
        ▼
② 3D 方块人预览图（正/背双联斜视角）        → preview_stage1_input.png
        │
        │  上传成【公开】HF 数据集
        ▼
③ Kaggle T4 跑 BLOCKv0.6（Flux2KleinPipeline）
        │
        │  NEAREST 降到 64×64  +  清掉第二层白底
        ▼
④ 64×64 RGBA 皮肤                            → seeds/lyco_kaggle_v6_seed*.png
```

---

## 阶段一 · 出 3D 预览图

| 项目 | 值 |
|---|---|
| 模型 | `gpt-image-2`（codex） |
| 尺寸 | 1024×1024 |
| 参考图 | `design/three-view/lyco_three_view.png` |
| 提示词 | [`prompts/minecraft-skin.md`](../../../prompts/minecraft-skin.md) 路线 A1 |

**最关键的一句**（不加这句，模型会给你画一张「皮肤图集」而不是 3D 预览）：

```
ALSO NO: skin texture atlas, UV layout, unwrapped texture sheet, flat texture
map, or any 2D texture diagram. This must be a 3D RENDERED PREVIEW, not a
texture sheet.
```

---

## 阶段二 · Kaggle 跑 BLOCKv0.6

### 环境

| 项目 | 实测值 |
|---|---|
| GPU | **Tesla T4, 15.6 GB**（Kaggle 免费层） |
| torch | 2.10.0+cu128 |
| diffusers | 0.37.1 |
| 模型加载 | 125 秒 |
| 单张生成 | **79–89 秒** |
| 全程 | 约 8.5 分钟 |

### ★ 五个必须遵守的参数

```python
MODEL_ID = "AliceKJ/BLOCKv0.6"

# ① T4 是 Turing 架构，不支持 bfloat16 → 必须 float16
pipe = Flux2KleinPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.float16)

# ② 15 GB 模型塞不进 15.6 GB 显存 → 必须开 CPU offload
pipe.enable_model_cpu_offload()

result = pipe(
    prompt=PROMPT,
    # ③ 必须 resize 到 512。不 resize 会按 1024 推理：慢 4 倍（355s vs 80s）且输出尺寸不对
    image=preview.convert("RGB").resize((512, 512)),
    num_inference_steps=30,   # ④ 不是 20
    guidance_scale=4.0,       # ⑤★ 最关键 —— 设成 1.0 会输出【纯白空图】，且不报错
    generator=torch.Generator("cpu").manual_seed(seed),
).images[0]
```

### PROMPT（直接用模型卡的原文）

```
Image-to-image translation using the reference image. The reference shows the same
3D Minecraft character with front and back views in a single image. Generate the
corresponding Minecraft skin UV atlas in 64x64 pixel-art UV layout. High-quality
anime-style. Flat shading, sharp pixel edges, no blur, no anti-aliasing. Keep
consistent UV placement and mapping; match the same character design from the
reference. Model type: classic (auto-detected Minecraft player model).
```

---

## 阶段三 · 后处理（两件必做）

### ① NEAREST 降到 64×64

模型输出 **512×512**。实测它的像素网格正好是 **8× 整数倍**
（强边缘间隔中位数 = 8px），所以 **NEAREST 降采样是无损的**。

```python
skin = result.convert("RGBA").resize((64, 64), Image.NEAREST)
```

> ⚠️ **绝对不要用 LANCZOS / BOX** —— 会把像素风糊掉。

### ② 清掉第二层的白底 ★

**这是最容易漏、后果最严重的一步。**

模型输出 **RGB，没有 alpha 通道**，它把「应该透明」的第二层（外套层）
填成了白色。而 Minecraft 的第二层是**盖在第一层上面渲染**的 →
**不清的话，角色在游戏里就是一坨白块。**

实测对照：

| | hat | jacket | 四肢 | 结果 |
|---|---|---|---|---|
| **未清** | 100% | 100% | 100% | ❌ 白块 |
| 已清 | 12% | 16% | 0% | ✅ 正常 |

第二层的六个区域：

```python
OVERLAY_RECTS = {
    "hat":     (32, 0, 64, 16),
    "jacket":  (16, 32, 40, 48),
    "rSleeve": (40, 32, 56, 48),
    "lSleeve": (48, 48, 64, 64),
    "rPant":   (0, 32, 16, 48),
    "lPant":   (0, 48, 16, 64),
}
```

把其中的近白像素（三通道 > 235）置为透明；清完剩余不足 12% 就整层清空。

> 注意：**第一层绝不能动**。第一层是身体本体，有透明像素就是破洞。
> 左臂主层是 `(32,48)-(48,64)`，**不是**到 64 —— 写错会误判。

---

## 实测产物

| seed | 耗时 | 输出 | 均值 | 标准差 |
|---|---|---|---|---|
| 42 | 79.3s | 512×512 | 179.0 | 96.5 |
| 123 | 86.9s | 512×512 | 187.4 | 93.4 |
| 2024 | 88.7s | 512×512 | 172.0 | 98.6 |
| 7 | 87.7s | 512×512 | 182.8 | 95.9 |

**4/4 全部有内容**，皮肤校验通过（64×64 RGBA、第一层 36 面全不透明）。

---

## ★ 一张「空图检测」救回来的教训

**v4 那次失败值得单独记一笔**：脚本输出了 `All done!`，
三张 64×64 皮肤却全是**纯白空图**（均值 254.1、标准差 0.3、只有 6 种颜色）。

原因是 `guidance_scale=1.0` + 空提示词 —— FLUX 关掉 CFG 会直接塌成空白，
**而且它不报错**。

所以必须自己加检测：

```python
blank = (arr.std() < 3.0) or (len(np.unique(arr.reshape(-1,3), axis=0)) < 8)
```

**静默失败比报错危险得多。** 同一轮里还有两个同类问题：
预览图 URL 是 404（静默回退到模型自带示例，生成的根本不是 Lyco）、
漏了 `resize((512,512))`（慢 4 倍但"看起来正常"）。

---

## 怎么复现

### 用现成的 notebook

[`notebook/blockv0-6-lyco-skin-generator-v6.ipynb`](notebook/blockv0-6-lyco-skin-generator-v6.ipynb)
+ [`kernel-metadata.json`](notebook/kernel-metadata.json)

```bash
kaggle kernels push          # 在该目录下执行
kaggle kernels status lilyco4242/blockv0-6-lyco-skin-generator-v6
kaggle kernels output lilyco4242/blockv0-6-lyco-skin-generator-v6 -p ./out
```

> **注意**：Kaggle 免费 GPU 有排队，实测**排队 8 小时后才开始跑**，
> 实际执行只要 8.5 分钟。别误以为卡死了。

### 依赖的公开数据集

预览图放在 `lyco42/lyco-preview`（**必须公开**，否则 notebook 里会 401 并静默回退）。

> 踩过的坑：HF 账号是 **`lyco42`**，Kaggle 账号是 **`lilyco4242`**，两个不同的账号。
> 早期引用的 `lilyco4242/lyco-preview` 其实**不存在（404）**。

---

## 已知局限

| 局限 | 说明 |
|---|---|
| **脸偏糊** | 8×8 像素是物理上限，模型输出的脸是中间色、缺结构 |
| **随机性大** | 换 seed 差别明显，只能多跑几个挑 |
| **细节丢失** | X 发夹、银扣、O 环、靴扣基本糊掉 |
| **排队久** | Kaggle 免费层排队可达 8 小时 |

**结论**：AI 负责「好看」，代码负责「准确」。
要精确的发夹/纽扣/O 环，仍然得看 [`tools/build_mc_skin_v3.py`](../../../tools/)。
