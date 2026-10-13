# Lyco 软件图标

本目录是按 lyco-ip 指导规范生成的衍生软件图标；基准设计图未随软件重新分发。

- 源图：resources/icon-source.png（透明 PNG）
- 身份与精确 SHA-256：resources/icon-source.json
- 署名：Lyco © lilyco-42
- 图标许可：resources/ICON-LICENSE.md。软件代码许可和 IP 图标许可分开保留。

原始规范固定在 82f35f190129498f73ef7199075c3a1723adfe2d；保留黑上红下、黑色短 bob、灰色半垂眼、放松闭嘴、角色自身右侧（观众左侧）的单个哑光白 X 发夹。本图为有意裁切的头肩图标，以 L2 配色和 L3 发夹承受低分辨率裁切；不新增武器、徽章、边框或文字。

由内置 imagegen 生成并作定向修正；完整生成/修正提示词记录在 JSON。原 PNG 保持不变。下游 Actions 生成 16/24/32/48/64/128/256 多尺寸 ICO，保留透明度并核对固定来源哈希，再用于程序、安装器和快捷方式。转换、产品构建及验证只在 GitHub Actions。
