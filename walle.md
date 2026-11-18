Updated todo list

# WALL·E 自主化：从零到成品的施工手册

我按上一轮点评的修正版来写。凡是和原方案不同的地方，都标了 **【修正】**。所有固件和 Python 代码都还没有在实机上跑过，请当作起点，按各阶段的验收项逐步测试。

整个过程分 10 个阶段，每个阶段都有验收标准，验收不过不要进入下一阶段。

```
阶段 0  采购与准备
阶段 1  原版机体（已有可跳过）
阶段 2  电源改造
阶段 3  传感器、摄像头、麦克风装配
阶段 4  Arduino 固件
阶段 5  Pi 系统环境
阶段 6  实时进程（link + synth）        ← P0 里程碑
阶段 7  感知 + 注视 + 情绪              ← P1 "活起来"
阶段 8  语音 + 找物                      ← P2
阶段 9  记忆 + 好奇                      ← P3
阶段 10 GPU 开放词汇 + 靠近避障          ← P4/P5
```

---

## 阶段 0：采购与准备

### 0.1 物料清单

> **价格说明：** 以下为 2026 年 11 月淘宝 / 立创商城的散件零售行情，只作预算参考。同款不同店差价可达一倍，进口件（Pololu、Adafruit 原装、ReSpeaker）另计运费与关税。标"兼容"的是国产替代件，功能等价但寿命和一致性略差。

**机体部分（已有原版机体可跳过）**

| 件                        | 规格                              | 数量           | 主要作用                                                                 | 参考价（¥）                  | 渠道 / 备注                                      |
| ------------------------- | --------------------------------- | -------------- | ------------------------------------------------------------------------ | ---------------------------- | ------------------------------------------------ |
| 3D 打印件                 | walle-replica README 里链接的 STL | 全套           | 整机机械结构，共 316 件 / 65 个 STL，详见 `stl/parts-manifest.md`        | 代打 500–1200；自己打耗材 60–90 | 自己打（PLA 足够），或嘉立创三维猴、未来工场代打 |
| Arduino Uno R3            | 原装或兼容（CH340 也行）          | 1              | 整机主控：收串口指令、跑 20ms 控制循环、驱动电机、读电流与电池           | 兼容 25 / 原装 130           | 淘宝                                             |
| Arduino Motor Shield Rev3 | L298P                             | 1              | 叠在 Uno 上驱动左右履带电机，附带每路电流检测（就是堵转判断的数据源）；每路 2A，电机堵转 5.5A，正常行驶够用、别长时间顶墙 | 兼容 35 / 原装 210           | 淘宝                                             |
| PCA9685                   | 16 路舵机驱动板，I2C 地址 0x40    | 1              | 用 I2C 转 12 位 PWM 同时驱动 7 个舵机，比 Uno 自带 Servo 库抖动小得多    | 12–20                        | 淘宝                                             |
| MG90S 舵机                | 高扭矩微型舵机，金属齿，**180° 位置式** | 7（另备 2 个） | 7 个活动关节：头旋转 1、颈部 2、眼 2、手臂 2（原版 List of Parts 第 e1 项） | 8–15/个，9 个约 80–135       | **不要 360° 连续旋转版**；尽量原厂，批次间脉宽/舵盘花键有差异，必须重新标定 |
| 37D 12V 减速电机          | **Pololu #4745：100:1，100 RPM，6mm D 轴（16mm 长），偏心输出，无编码器** | 2              | 履带驱动，要的是低速大扭矩而不是高转速（原版 e2）；**买直流版，不买编码版** | 国产 40–75/个；Pololu 250–350/个 | 国产 JGB37-520 接口接近（6mm D/7mm 偏心/6×M3），但扭矩/寿命低于 4745；须核对轴长/孔距，编码版不做推荐 |

**国产 37D 替代选项（12V、无编码；6mm D 轴、7mm 偏心、6×M3 是硬条件）**

| 型号 | 转速/扭矩 | 接口 | 结论 | 参考价 |
|---|---|---|---|---|
| Pololu #4745 | 100 RPM / 34 kg·cm 堵转 | 6mm D×16mm，7mm 偏心，6×M3 | 原设计，零风险 | 约 ¥300 |
| 37GB-520 / JGB37-520 | 100 RPM / 标称 4.8 kg·cm | 6mm D×15mm，平面 11.5mm，7mm 偏心，6×M3 | **可直接替**，属降级；换后重调 `STALL_RAW` | ¥30–60 |
| 37GB-520 低速版 | 60–66 RPM / 扭矩更大 | 同上 | 可直接替，整车变慢，转弯/找物时序要重调 | ¥30–60 |
| 37GB-550 / JGB37-550 | 100 RPM / 约 40 kg·cm 级 | 37mm、6mm D，但本体更长 | **不 drop-in**：12V 启动约 6A，L298P 2A/路 + 1.6A 堵转阈值会误切 | ¥45–80 |
| 37GB-555 / DGB37-555 | 170 RPM / 30 kg·cm 堵转，连续 2.5A | 同上，更长 | **不 drop-in**：要换 BTS7960 并改轮架 | ¥50–90 |
| 37D 克隆 / 二手 4745 | 看实物 | 必须 6mm D×16mm、7mm 偏心、6×M3 | 对得上就是原设计 | ¥150–350 |

> 国产只认 **GB（偏心轴）**，不要 **GA（中心轴）**；不要带编码器的 520B/550B。下单前让卖家量：轴径、轴伸出、平面长度、偏心距、6 孔孔距（31mm 圆 / 相邻 15.5mm）、空载转速、堵转电流。先买一只试样，装 `wheel-gear-motor` 和 `wheel-frame` 试啮合，过了再买第二只。

**紧固件与五金（对应原版 List of Parts 的 h1–h4，不要照"按原项目 BOM"自己猜）**

| 件                | 规格                          | 数量 | 主要作用                                                     | 参考价（¥） |
| ----------------- | ----------------------------- | ---- | ------------------------------------------------------------ | ----------- |
| M3 螺栓（短）     | M3 × 6mm 内六角               | 2    | 网页正文清单有此项，PDF 清单未列；固定薄件                   | 1–2         |
| M3 螺栓（中）     | M3 × 10mm 内六角              | 14   | 主力紧固件，车体、手臂、轮架的大部分连接都靠它               | 3–5         |
| M3 螺栓（长）     | M3 × 20mm 内六角              | 12   | 穿过轴套的长连接，颈部、手臂铰链用                             | 3–5         |
| M3 螺母           | M3 标准螺母                   | 26   | 和上面 28 颗螺栓配对（多备几颗，打印件公差大时好找）          | 3–6         |
| 回形针（连杆）    | 普通大号回形针                | 3    | 颈部与手臂的柔性连杆，PDF 写 2、网页正文写 3，按 3 备          | 0–2         |
| 平凸透镜          | ⌀31.5–32.5 mm                 | 2    | **眼睛的镜片**——作者说这两片玻璃是 WALL·E "有灵魂"的关键；可从旧双筒望远镜拆 | 20–40（拆旧望远镜 0） |

**五金小计：约 30 元 ～ 60 元**（买整包更便宜，螺栓螺母一包 50 颗通常 10 元以内）

> **两点澄清（原文档的"按原项目 BOM"会误导）：**
> 1. **履带不需要采购**——履带板 `tread-plate`（70 件）和履带销 `tread-pin`（140 件）都是 3D 打印件，全机 316 件里它们占了 210 件。原始文件名为 `tread-plate-x70` / `tread-pin-x140`，交付包已去掉数量后缀，数量只写在 `数量表.csv` 里。
> 2. **原版 BOM 不含轴承**。轴承只出现在两个第三方 remix 的履带张紧系统里（Thingiverse 4285247 / 4832742），原版 `wheel-bracket` 用的是打印轴套，不要额外买。
>
> **件数口径（最终）：65 个文件 / 316 件。**
> 官方 2019 年的 List of Parts PDF 记 **310 件**；当前 STL 集（2022-12 导出）按原始文件名里的 `-xN` 展开是 **314 件**。差的 4 件是后来追加的 `body-front-power`、`missing-piston-insert`、`switch-holder`、`neck-bottom-linkage-longer`（各 1 件）。
> 另外 `eye-camera-replica` 与 `eye-camera-mount` **各打 2 件**（共 +2 件 → 316）：两者外径同为 ⌀40.9mm、中心孔 ⌀2.3 / ⌀12.0mm，是 **同一只眼的互换件**，不是两个不同零件。各打一对，是为了「假镜片」和「眼球内装摄像头」两种方案都能试错，坏一只也有备件。官方默认只打 replica ×2，这里是**有意偏离官方 BOM 的唯一一处**。

**小计：约 310 元（全兼容件 + 自己打印）～ 2400 元（原装件 + Pololu + 代打）**

**改造新增 + 装配漏项：P0 必买**

| 件                    | 规格                                           | 数量 | 主要作用                                                             | 参考价（¥）           | 说明                                   |
| --------------------- | ---------------------------------------------- | ---- | -------------------------------------------------------------------- | --------------------- | -------------------------------------- |
| Raspberry Pi 4        | 4GB 或 8GB                                     | 1    | 跑感知、决策、语音，把关节指令用 UDP 发给实时进程                     | 4GB 320–390；8GB 520–670 | 已有则跳过                             |
| 高耐久 TF 卡          | 32GB 以上，选 High Endurance 系列              | 1    | 系统盘。日志和数据库都在写，普通卡几个月就写坏                        | 40–60                 | 或 USB SSD                             |
| 降压模块 A            | 12V→5V **8A**（XL4016 或同类；XL4016 为非同步，够用） | 1    | 单独给 7 个舵机供电，防止舵机抢电流把 Pi 拉到重启                    | 15–28                 | 舵机轨；7×MG90S 堵转约 5A，5A 模块无余量 |
| 降压模块 B            | 12V→5.1V 5A，带 USB-C 或接线柱                 | 1    | 给 Pi 供电；接在急停之前，所以按下急停 Pi 仍在跑                     | 15–25                 | Pi 轨；Pi 4 需 5V/3A，USB-C 座要有 5.1k CC 电阻，否则用 A-to-C 线 |
| 急停开关              | 蘑菇头急停，**1 常闭 + 1 常闭**（双触点），10A | 1    | 一拍下去物理切断电机与舵机动力（NC1），同时给 Uno 一个中断（NC2）     | 15–30                 | 双触点；双电机同时堵转最坏约 16A > 10A，由 10A 保险丝先切断，属保护 |
| 保险丝座 + 10A 保险丝 | 刀片式                                         | 1    | 主回路过流保护，接反或短路时保住电池和线束                            | 5–10                  | 主回路                                 |
| 电解电容              | 1000µF/16V                                     | 3    | 吸收舵机启动瞬间的电流冲击，稳住电压                                  | 1–2/个                | 舵机轨 2 个、Pi 轨 1 个                |
| USB 麦克风            | 全向 USB 麦，或 ReSpeaker USB Mic Array        | 1    | 语音唤醒和识别的输入；装得离电机越远，误唤醒越少                      | 普通 50–100；ReSpeaker 400–600 |                                        |
| 散热                  | 铝壳或散热片 + 5V 3010 风扇                    | 1    | Pi 4 满载容易上 80°C 降频，直接表现为检测变卡                        | 20–40                 |                                        |
| XT60 公母头 + 硅胶线  | XT60 公母 2 对；14AWG 红黑各 1m；22AWG 红黑各 2m | 1 套 | 大电流主回路（电池→保险丝→急停→电机/Buck）和信号走线 | 30–50                 |                                        |
| 分压电阻              | 100kΩ + 47kΩ，1%                              | 各 1（备 2） | 电池电压检测：12.6V → A2 约 4.03V；**必装**，不装 A2 悬空会误触发欠压 | 1–2                   | 原清单漏项                             |
| 舵机延长线            | 3P 公对母，20–30cm                             | 7    | MG90S 线长仅约 17–25cm，头/臂到 PCA9685 不够                        | 10–20                 | 原清单漏项                             |
| 18AWG 硅胶线          | 红黑各 0.5m                                   | 1 套 | Buck A → PCA9685 V+ 的 5A 舵机电源；22AWG 只够信号                  | 8–15                  | 原清单漏项                             |
| 热熔铜螺母 + VHB      | M2.5/M3 铜螺母若干 + VHB 胶带                  | 1 套 | 机身无固定孔，Pi/双 Buck/PCA9685 靠它固定                            | 15–30                 | 原清单漏项                             |

**小计：约 550 元（4GB Pi + 普通 USB 麦）～ 1590 元（8GB Pi + ReSpeaker，含新增漏项）**

**P1/P2 推荐**

| 件                                | 规格                                  | 数量 | 主要作用                                                       | 参考价（¥）                        |
| --------------------------------- | ------------------------------------- | ---- | -------------------------------------------------------------- | ---------------------------------- |
| IMU                               | MPU6050 模块（GY-521）                | 1    | 角速度积分出航向角，让"转身 45°"这种动作能闭环                  | 8–15                               |
| ToF 测距                          | VL53L1X 模块                          | 1    | 正前方测距，靠到 25cm 就停、以及避障的减速依据                  | 25–40（VL53L0X 便宜但量程只有 2m） |
| 摄像头                            | Pi Camera Module 3（广角版更好）      | 1    | 人脸检测、视觉伺服盯人、找物；**板 25×24mm，装不进眼球，头壳安装需自制支架** | 标准 200–230；广角 250–300         |
| 电池                              | **3S 3000mAh** LiPo（2200–3300 均可；5000mAh 长 135mm+，机身底板 129×116，平放装不下，需实测/斜放） + 平衡充电器 + 防爆袋 | 1    | 整机动力，按这个负载大约能跑 1.5–2.5 小时                         | 电池 120–200 + 充电器 100–200 + 袋 20–30 |
| 杜邦线            | 母-母 20cm                    | 20 根 | 接 MPU6050 / VL53L1X 到 Pi 的 I2C，以及 PCA9685 到 Uno 的逻辑线 | 8–12        |
| 热缩管 + 扎带     | ⌀2/⌀3/⌀5 混装 + 尼龙扎带      | 1 套  | 焊点绝缘、线束收口，避免线在脖子转动时被扯断                    | 15–25       |
| 尼龙柱 + M2.5 螺丝 | M2.5×10mm 尼龙柱 ×4，M2.5×6 螺丝 ×8 | 1 套  | 固定 Pi 和摄像头转接板；打印件上没有 M3 孔位的地方用它           | 10–15       |
| 扬声器 + 功放      | 3W 小喇叭 + PAM8403，或 USB 声卡 + 小音箱 | 1 套 | P2 发声；原清单只有麦克风，没有输出                             | 20–40       |
| CSI 延长排线       | 30–50cm，15→15 pin                    | 1    | 摄像头在头部、Pi 在机身，标准 200mm 排线可能不够（先量）         | 10–20       |

**小计：约 535 元 ～ 900 元（含扬声器/功放、CSI 延长线）**

**可选：GPU 端**

屋里一台有 NVIDIA 显卡、显存 6GB 以上的电脑即可 —— 只用来跑 YOLO-World 开放词汇检测和中→英翻译。

| 件 | 规格 | 数量 | 主要作用 | 参考价（¥） |
| --- | --- | --- | --- | --- |
| GPU 主机 | NVIDIA 显卡，显存 6GB 以上 | 1 | 跑开放词汇检测（认"红色马克杯"这类词）+ 中文 prompt 翻译，Pi 只发图收框 | 已有 0；二手 RTX 3060 12G 约 1000–1300 |

**整机预算（不含 GPU、不含工具）：约 1430 元（全兼容件）～ 4950 元（原装件 + 代打 + ReSpeaker + 8GB Pi）。**
最常见的中配（兼容 Uno/Shield + Pi 4B 4GB + 国产电机 + 普通 USB 麦 + 打印件代打）落在 **2350 元上下**。
如果已经有 Pi、有打印机、手头有 Uno，实际现金支出通常在 **850–1250 元**——主要花在电机、电池、舵机和摄像头这四样上。

> **2026-11-18 硬件清单修订（对照原版仓库 378573d）**
>
> 1. **电机**：明确为 Pololu #4745（100:1 / 100 RPM / 6mm D 轴 / 16mm 轴长 / 偏心 / **无编码器**）。国产 JGB37-520 接口接近（6mm D / 7mm 偏心 / 6×M3），可作降级替代，但扭矩和寿命低于 4745，须核对轴长/孔距；**不推荐编码版**——Uno 的 D2/D3 已分别被急停和电机 PWM 占用，没有空闲外部中断，打印件是按无编码电机设计的，编码器尾部空间未验证。
> 2. **电池**：5000mAh → **3000mAh**（2200–3300 均可）。机身内舱底板实测 129×116mm，5000mAh 普遍 135mm 以上，平放装不进去；原版用 2200mAh。
> 3. **Buck A**：5A → **8A**。7×MG90S 堵转约 4.9–5.6A，5A 模块没有余量；XL4016 是**非同步** buck，原描述"同步整流"已删。
> 4. **补漏项**：100k/47k 分压电阻、7 根舵机延长线、18AWG 舵机电源线、热熔铜螺母 + VHB、扬声器 + 功放、CSI 延长排线。
> 5. **摄像头**：Pi Camera 3 是 25×24mm 板，装不进眼球；`eye-camera-mount` 的 ⌀12mm 孔是给微型摄像头的。头壳安装要自制支架，排线可能要加长。
> 6. **保留提醒**：L298P 每路 2A，而 4745 堵转 5.5A；正常行驶没问题，别长时间顶墙。10A 保险丝会在双电机同时堵转（最坏约 16A）时先熔断，急停触点负责断电，这是保护动作。MG90S 批次间脉宽范围/舵盘花键有差异，每批都要重新标定；**不要买 360° 连续旋转版**。Pi 4 用 USB-C 供电时注意 Buck 的 USB-C 座是否带 5.1k CC 电阻，否则用 A-to-C 线。
> 7. **安装结构**：机身没有给急停（22mm 孔）、保险丝座、XT60、双 Buck 预留位置，先规划开孔/支架再动手；电子件用热熔铜螺母或 VHB 固定。

### 0.2 工具

电烙铁、焊锡、万用表（必备）、热熔胶枪、剥线钳、斜口钳、小号螺丝刀套装。有一台可调电源最好，用来限流上电测试。

### 0.3 软件准备

- 电脑上安装：Arduino IDE 2.x、Raspberry Pi Imager、VS Code（含 Remote-SSH 插件）。
- 克隆原项目，从基线版本新建分支：

```bash
git clone https://github.com/chillibasket/walle-replica.git
cd walle-replica && git checkout 378573d -b autonomy
```

---

## 阶段 1：原版机体（已有可跳过）

1. 按项目 README 和 wiki 打印、组装机械结构。舵机先**不要装舵盘**。
2. 按原项目接线：Uno 叠 Motor Shield，PCA9685 接 A4/A5，7 个舵机接 PCA9685 的 0–6 通道。
3. 刷原版固件，用原版的 `calibrate` 流程把 `preset[7][2]` 标定好，**记下数值**。
4. 舵机转到中位后再装舵盘。

**验收：** 原版网页遥控能让所有关节和履带正常工作。

---

## 阶段 2：电源改造

### 2.1 目标拓扑

```
3S LiPo ──XT60──[10A 保险丝]──[急停 NC1]──┬── Motor Shield Vin（拔掉 Vin 跳线帽）→ 2× 电机
                                          └── Buck A (5.0V) ── PCA9685 V+ 端子 ── 7× 舵机
                                                     └─ 2× 1000µF 并在 V+ 端子
          └────────────(急停之前)────────────── Buck B (5.1V) ── Pi USB-C
                                                     └─ 1000µF
急停 NC2：D2 ──┤NC├── GND     （按下急停 → D2 变高电平 → 中断）
所有 GND 共地（星形接法，汇总在电池负极附近）
```

**为什么这样接：** 急停按下后，电机和舵机**在物理上断电**，Pi 不断电，可以继续记录日志，复位后能马上恢复。

### 2.2 操作步骤

1. **先调电压，再接负载。** 两个 Buck 先接可调电源输入 12V，空载调出电压：A 调到 5.0V，B 调到 5.15V。
2. **给 A 加假负载测试。** 接一个 5Ω 功率电阻，确认电压不低于 4.9V，模块不烫手。
3. **Motor Shield 断开 Vin 跳线**（板背面的 "Vin Connect" 焊盘要切开）。这样电机电源不会倒灌给 Uno，Uno 只靠 USB 由 Pi 供电。
4. **PCA9685 的 V+ 接 Buck A**，VCC 逻辑电源仍然从 Uno 取 5V。电容并联在 V+ 端子上，**注意极性**。
5. **焊急停开关**：NC1 串进主回路，NC2 接 D2 和 GND。
6. **共地检查。** 万用表蜂鸣档逐一测：电池负、Buck A 负、Buck B 负、Uno GND、PCA9685 GND、Pi GND，必须全部导通。
7. **电池分压**：100k/47k 电阻分压，中点接 A2；12.6V 输入时 A2 约 4.03V。

**验收：**

- 先接可调电源（12V 限流 2A）上电，再换电池。
- 7 个舵机同时打到极限位置时，用万用表测 Pi 的 5V 不低于 5.0V，Pi 不重启（`vcgencmd get_throttled` 返回 `0x0`）。
- 按下急停，电机和舵机立即没劲，Pi 不受影响。

---

## 阶段 3：传感器、摄像头、麦克风装配

### 3.1 Pi 的 I2C 接线【修正】

IMU 和 ToF 都接 Pi，不接 Uno。

| 设备    | VCC              | GND   | SDA            | SCL            | 地址 |
| ------- | ---------------- | ----- | -------------- | -------------- | ---- |
| MPU6050 | Pi 3.3V（pin 1） | pin 6 | GPIO2（pin 3） | GPIO3（pin 5） | 0x68 |
| VL53L1X | Pi 3.3V          | GND   | GPIO2          | GPIO3          | 0x29 |

- **MPU6050** 用热熔胶或双面胶**牢固固定在底盘中心**，Z 轴朝上。它测的是底盘转了多少度，要装在车体上，不能装在头上。
- **VL53L1X** 装在底盘前方正中，离地约 5–8cm，朝正前方，前面不要有遮挡。

### 3.2 摄像头【修正】

- 装在**头部壳体中间**（两眼之间下方），或者装在**眼眶外壳的固定部分**。**不要装在会倾斜的眼球上。**
- 做法：打印一个小转接板，用 M2 螺丝固定。CSI 排线从颈部空腔走线，留够头部转动的余量（转到两端各转一下，确认排线不被拉紧）。
- **注意：Pi Camera 3 是 25×24mm 的板，装不进眼球；`eye-camera-mount` 的 ⌀12mm 孔是给微型摄像头的。** 想保留"眼睛里有摄像头"的原版效果，只能用微型摄像头；用 Pi Camera 3 就按上面的头壳方案，并准备 30–50cm 的 CSI 延长排线。
- 镜头和舵盘之间加一小片黑色遮光，防止反光。

### 3.3 麦克风

- 装在**背部或顶部、离履带电机最远的位置**，用海绵减震。
- USB 线插 Pi。

### 3.4 Pi 安装

- Pi 装进机身，装散热片，风扇朝外排风。
- Uno 通过 USB 线连接 Pi（这根线同时是 Uno 的电源和串口）。

**验收：** 全部装配好后，头部、颈部转到极限位置，所有线缆都不受拉扯。

---

## 阶段 4：Arduino 固件

### 4.1 设计要点

- **【修正】流式直通模式。** 每帧目标只做**每帧最大变化量限幅**（安全保护），不做梯形规划。梯形规划保留给开机动画和降级时用。
- **【修正】关节分辨率 0–1000**，校验改成 **CRC-8**。
- **【修正】开机发 `B` 帧**，Pi 等收到 `B` 帧再开始发数据（解决打开串口时 Uno 复位的问题）。
- **不使用 `String` 类**，用定长缓冲解析。

### 4.2 协议（最终版）

```
Pi→MCU  J,seq,j0..j6,v,w*CC\n     关节 0..1000，v/w -100..100，CC = CRC-8 十六进制
        H,seq*CC\n                心跳
        R,seq*CC\n                解除急停闩锁
MCU→Pi  B*CC\n                    开机完成
        T,seq,batt_mv,curA,curB,flags*CC\n   遥测 20Hz；flags 各位：estop/undervolt/stallA/stallB/wdt
        E,code*CC\n               事件
CRC-8 校验范围：'*' 之前的全部字符，多项式 0x07，初值 0
```

### 4.3 新建 `firmware/walle_stream/walle_stream.ino`

先安装库：Adafruit PWM Servo Driver Library。

```cpp
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm(0x40);

// 换成你在阶段 1 标定得到的值：{min_pwm, max_pwm}
int preset[7][2] = {{410,120},{532,178},{120,310},{465,271},{278,479},{340,135},{150,360}};

const uint8_t PIN_DIR[2]={12,13}, PIN_PWM[2]={3,11}, PIN_BRK[2]={9,8};
const uint8_t PIN_ESTOP=2, PIN_OE=10, PIN_BAT=A2, PIN_CUR[2]={A0,A1};
const uint16_t WDT_MS=200, MAX_STEP=60;   // MAX_STEP：每帧最多变化多少（0..1000 量程）
const uint16_t UNDERVOLT_MV=10200, STALL_RAW=550, STALL_MS=500;

volatile bool estopFlag=false;
bool estopLatched=false, servosOn=true;
int cur[7], tgt[7], v=0, w=0, mot[2]={0,0};
uint32_t lastRx=0, lastTele=0, lastChange=0, stallT[2]={0,0};
uint16_t seqOut=0, battMv=0, battFilt=0;
uint8_t flags=0;
char buf[96]; uint8_t blen=0;

uint8_t crc8(const char* s, uint8_t n){
  uint8_t c=0;
  for(uint8_t i=0;i<n;i++){ c^=s[i]; for(uint8_t b=0;b<8;b++) c=(c&0x80)?(c<<1)^0x07:(c<<1); }
  return c;
}
void sendFrame(const char* body){
  char out[64]; uint8_t n=strlen(body);
  snprintf(out,sizeof(out),"%s*%02X\n",body,crc8(body,n));
  Serial.write(out);
}
void onEstop(){ estopFlag=true; }

void setServo(uint8_t i,int val){
  int p = map(val,0,1000,preset[i][0],preset[i][1]);
  pwm.setPWM(i,0,p);
}
void servosOff(){ for(uint8_t i=0;i<7;i++) pwm.setPWM(i,0,0); servosOn=false; }

void setMotor(uint8_t m,int spd){   // spd -255..255
  digitalWrite(PIN_DIR[m], spd>=0);
  digitalWrite(PIN_BRK[m], spd==0);
  analogWrite(PIN_PWM[m], abs(spd));
}

void handleLine(char* s,uint8_t n){
  char* star=strchr(s,'*'); if(!star) return;
  uint8_t body=star-s;
  if(crc8(s,body)!=(uint8_t)strtoul(star+1,NULL,16)){ sendFrame("E,CRC"); return; }
  *star=0;
  char type=s[0];
  lastRx=millis();
  if(type=='H') return;
  if(type=='R'){ if(digitalRead(PIN_ESTOP)==LOW){ estopLatched=false; estopFlag=false; } return; }
  if(type!='J') return;
  int vals[10]; uint8_t k=0;
  char* tok=strtok(s+2,",");   // 跳过 "J,"
  tok=strtok(NULL,",");        // 跳过 seq
  while(tok && k<10){ vals[k++]=atoi(tok); tok=strtok(NULL,","); }
  if(k!=9) return;
  for(uint8_t i=0;i<7;i++){
    if(vals[i]<0||vals[i]>1000){ sendFrame("E,RANGE"); return; }
  }
  bool changed=false;
  for(uint8_t i=0;i<7;i++){ if(tgt[i]!=vals[i]) changed=true; tgt[i]=vals[i]; }
  if(changed) lastChange=millis();
  v=constrain(vals[7],-100,100); w=constrain(vals[8],-100,100);
}

void setup(){
  Serial.begin(115200);
  pinMode(PIN_OE,OUTPUT); digitalWrite(PIN_OE,LOW);
  pinMode(PIN_ESTOP,INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(PIN_ESTOP),onEstop,RISING);
  for(uint8_t m=0;m<2;m++){ pinMode(PIN_DIR[m],OUTPUT); pinMode(PIN_BRK[m],OUTPUT); setMotor(m,0); }
  pwm.begin(); pwm.setPWMFreq(50);
  for(uint8_t i=0;i<7;i++){ cur[i]=tgt[i]=500; setServo(i,500); }
  lastRx=lastChange=millis();
  sendFrame("B");
}

void loop(){
  while(Serial.available()){
    char c=Serial.read();
    if(c=='\n'){ buf[blen]=0; handleLine(buf,blen); blen=0; }
    else if(blen<sizeof(buf)-1) buf[blen++]=c;
    else blen=0;
  }
  uint32_t now=millis();
  if(estopFlag){ estopLatched=true; estopFlag=false; sendFrame("E,ESTOP"); }

  uint16_t raw=analogRead(PIN_BAT);
  battMv=(uint32_t)raw*5000UL*147UL/47UL/1023UL;
  battFilt = battFilt ? (battFilt*15UL+battMv)/16 : battMv;
  bool under = battFilt<UNDERVOLT_MV;
  bool wdt = now-lastRx>WDT_MS;

  static uint32_t lastStep=0;
  if(now-lastStep>=20){
    lastStep=now;
    // 电机：看门狗/急停/欠压 → 线性刹停
    int target[2]={0,0};
    if(!wdt && !estopLatched && !under){
      target[0]=constrain((v+w)*255/100,-255,255);
      target[1]=constrain((v-w)*255/100,-255,255);
    }
    for(uint8_t m=0;m<2;m++){
      int d=target[m]-mot[m];
      mot[m]+=constrain(d,-25,25);
      if(analogRead(PIN_CUR[m])>STALL_RAW){
        if(!stallT[m]) stallT[m]=now;
        else if(now-stallT[m]>STALL_MS){ mot[m]=0; flags|=(4<<m); sendFrame(m?"E,STALLB":"E,STALLA"); }
      } else { stallT[m]=0; flags&=~(4<<m); }
      setMotor(m,mot[m]);
    }
    // 舵机：每帧限幅直通
    bool idleLong = now-lastChange>4000;
    bool cut = estopLatched || (wdt && now-lastRx>2000) || idleLong;
    if(cut){ if(servosOn) servosOff(); }
    else{
      servosOn=true;
      for(uint8_t i=0;i<7;i++){
        cur[i]+=constrain(tgt[i]-cur[i],-(int)MAX_STEP,(int)MAX_STEP);
        setServo(i,cur[i]);
      }
    }
  }

  if(now-lastTele>=50){
    lastTele=now;
    flags = (flags&0x0C) | (estopLatched?1:0) | (under?2:0) | (wdt?16:0);
    char b[48];
    snprintf(b,sizeof(b),"T,%u,%u,%u,%u,%u",seqOut++,battFilt,analogRead(A0),analogRead(A1),flags);
    sendFrame(b);
  }
}
```

**刷写前需要核对的参数：**

- `preset` 换成阶段 1 标定得到的值。
- `STALL_RAW`：官方 Motor Shield 的电流检测约 1.65V/A，550 大约对应 1.6A。按自己的电机实测后调整。
- `MAX_STEP=60`：相当于每 20ms 最多走量程的 6%，满量程大约 0.33 秒走完。这个值决定"最快的扫视"能有多快。

### 4.4 刷写与单测

用 Arduino IDE 打开、编译、上传，然后在电脑上用 Python 单测：

```python
# tools/fw_test.py
import serial, time
def crc8(s):
    c=0
    for ch in s.encode():
        c^=ch
        for _ in range(8): c=((c<<1)^0x07)&0xFF if c&0x80 else (c<<1)&0xFF
    return c
def frame(body): return f"{body}*{crc8(body):02X}\n".encode()
s=serial.Serial('/dev/ttyACM0',115200,timeout=0.1)
while b'B*' not in s.readline(): pass
for i in range(500):
    j=[500+int(200*__import__('math').sin(i/20))]+[500]*6
    s.write(frame("J,%d,%s,0,0"%(i,",".join(map(str,j)))))
    time.sleep(0.02)
    while s.in_waiting: print(s.readline())
```

**验收：**

1. 头部平滑地左右摆动，遥测 `T` 帧连续输出。
2. 脚本运行中按 Ctrl-C：200ms 内电机停止，2 秒后舵机断电，flags 中看门狗位为 1。
3. 按急停，收到 `E,ESTOP`；松开急停并发送 `R` 后恢复。
4. 跑 10 分钟，没有一条 `E,CRC`。

---

## 阶段 5：Pi 系统环境

```bash
# 用 Raspberry Pi Imager 刷 Raspberry Pi OS Bookworm 64-bit Lite，预设 SSH、WiFi、用户名
sudo raspi-config        # Interface → I2C 开启；Camera 默认已支持
sudo apt update && sudo apt install -y python3-venv python3-picamera2 python3-opencv \
     i2c-tools alsa-utils libatlas-base-dev git
sudo usermod -aG dialout,i2c,audio,video $USER
python3 -m venv --system-site-packages ~/walle-env
source ~/walle-env/bin/activate
pip install pyserial smbus2 numpy onnxruntime sounddevice sherpa-onnx \
            ultralytics ncnn vl53l1x fastapi uvicorn requests
```

**逐项检查硬件：**

```bash
i2cdetect -y 1                   # 应看到 0x29 和 0x68
libcamera-hello -t 2000          # 摄像头出画面（无屏幕可用 rpicam-still -o t.jpg）
arecord -l                       # 能看到 USB 麦克风
arecord -D plughw:1 -d 3 t.wav && aplay t.wav
ls /dev/ttyACM*                  # 能看到 Uno
vcgencmd measure_temp
```

**减少 TF 卡写入：** 日志写到 tmpfs，SQLite 打开 WAL 模式（后面代码里会做）。

---

## 阶段 6：实时进程（P0 里程碑）

### 6.1 进程架构【修正】

```
walle-rt.service    （nice -10，单独进程）
  ├─ link：串口收发、握手、遥测
  └─ synth：50Hz 合成
       ▲ UDP 127.0.0.1:9001，JSON 格式，约 10Hz
       │ {gaze:[pan,tilt], pose:"curious", mood:{...}, base:[v,w], reflex:...}
walle-brain.service （普通优先级）
  ├─ perception / imu / tof
  ├─ voice
  ├─ decision（attention、mood、behavior、search）
  └─ memory、ipc（Unix socket）
```

两个进程独立运行：brain 崩溃时，rt 继续保持 idle 动作；rt 崩溃时，固件看门狗负责停车。

### 6.2 目录结构

```
walle-brain/
  rt/      link.py  synth.py  rt_main.py
  brain/   main.py  imu.py  tof.py  perception.py  gaze.py  mood.py
           attention.py  behavior.py  search.py  novelty.py  memory.py
           voice.py  audio.py  detector.py  ipc.py  config.py
  gpu/     server.py
  sounds/  *.wav
  systemd/ walle-rt.service  walle-brain.service
```

### 6.3 `rt/link.py`

```python
import serial, threading, time

def crc8(s: str) -> int:
    c = 0
    for ch in s.encode():
        c ^= ch
        for _ in range(8):
            c = ((c << 1) ^ 0x07) & 0xFF if c & 0x80 else (c << 1) & 0xFF
    return c

class Link:
    def __init__(self, port="/dev/ttyACM0"):
        self.s = serial.Serial(port, 115200, timeout=0.05)
        self.seq = 0
        self.tele = {"batt": 0, "curA": 0, "curB": 0, "flags": 0, "t": 0}
        self.events = []
        self._wait_boot()
        threading.Thread(target=self._rx, daemon=True).start()

    def _wait_boot(self):
        # 打开串口会让 Uno 复位，必须等到 B 帧
        t0 = time.time()
        while time.time() - t0 < 5:
            if self.s.readline().startswith(b"B*"):
                return
        raise RuntimeError("Arduino not booted")

    def _send(self, body):
        self.s.write(f"{body}*{crc8(body):02X}\n".encode())

    def send_joints(self, joints, v=0, w=0):
        self.seq = (self.seq + 1) & 0xFFFF
        j = ",".join(str(int(max(0, min(1000, x)))) for x in joints)
        self._send(f"J,{self.seq},{j},{int(v)},{int(w)}")

    def reset_estop(self):
        self._send(f"R,{self.seq}")

    def _rx(self):
        while True:
            line = self.s.readline().decode(errors="ignore").strip()
            if "*" not in line:
                continue
            body, cc = line.rsplit("*", 1)
            try:
                if crc8(body) != int(cc, 16):
                    continue
            except ValueError:
                continue
            f = body.split(",")
            if f[0] == "T" and len(f) == 6:
                self.tele = {"batt": int(f[2]), "curA": int(f[3]), "curB": int(f[4]),
                             "flags": int(f[5]), "t": time.time()}
            elif f[0] == "E":
                self.events.append((time.time(), f[1]))
```

### 6.4 `rt/synth.py`（核心）

关节顺序与 PCA9685 通道一致：`0 head 旋转，1 neckTop，2 neckBot，3 eyeR，4 eyeL，5 armL，6 armR`（请按自己的实际接线核对）。

```python
import math, random

JOINTS = ["head", "neckT", "neckB", "eyeR", "eyeL", "armL", "armR"]

# 姿态词汇表：0..1000
POSES = {
    "neutral":  [500, 500, 500, 500, 500, 300, 300],
    "curious":  [500, 700, 350, 650, 650, 350, 350],
    "sad":      [500, 250, 600, 200, 200, 150, 150],
    "startled": [500, 800, 200, 800, 800, 600, 600],
    "point_L":  [500, 600, 450, 600, 600, 900, 300],
    "point_R":  [500, 600, 450, 600, 600, 300, 900],
    "rest":     [500, 300, 600, 400, 400, 200, 200],
}

class Spring:
    """二阶弹簧；zeta<1 会产生过冲。"""
    def __init__(self, x=500.0, k=60.0, zeta=0.75):
        self.x, self.v, self.k, self.c = x, 0.0, k, 2 * zeta * math.sqrt(k)
    def step(self, target, dt):
        a = self.k * (target - self.x) - self.c * self.v
        self.v += a * dt
        self.x += self.v * dt
        return self.x

class Noise1D:
    """平滑噪声：几个不同频率的正弦叠加，再加随机相位。"""
    def __init__(self):
        self.f = [random.uniform(0.05, 0.3) for _ in range(3)]
        self.p = [random.uniform(0, 6.28) for _ in range(3)]
    def __call__(self, t):
        return sum(math.sin(2 * math.pi * f * t + p) for f, p in zip(self.f, self.p)) / 3

class Synth:
    def __init__(self):
        # 头部旋转慢一点，颈部、眼睛快一点
        ks = [35, 50, 50, 90, 90, 40, 40]
        self.springs = [Spring(k=k) for k in ks]
        self.noise = [Noise1D() for _ in JOINTS]
        self.cmd = {"gaze": None, "pose": "neutral", "mood": {}, "base": [0, 0], "reflex": None}
        self.reflex_t = 0.0

    def update_cmd(self, cmd):
        self.cmd.update(cmd)
        if cmd.get("reflex"):
            self.reflex_t = 0.0

    def step(self, t, dt):
        m = self.cmd["mood"]
        energy = m.get("energy", 0.7)
        arousal = m.get("arousal", 0.3)
        base = list(POSES.get(self.cmd["pose"], POSES["neutral"]))

        # 注视：gaze=[pan, tilt]，取值 -1..1，pan 给头部，tilt 拆给两个颈部关节
        if self.cmd["gaze"]:
            pan, tilt = self.cmd["gaze"]
            base[0] = 500 + 400 * pan
            base[1] += 250 * tilt
            base[2] -= 120 * tilt

        # 情绪偏移：能量低 → 低头、手臂下垂
        base[1] -= (1 - energy) * 150
        base[5] -= (1 - energy) * 80
        base[6] -= (1 - energy) * 80

        # 惊吓反射：一个 0.6 秒的衰减冲量
        if self.cmd.get("reflex") == "startle" and self.reflex_t < 0.6:
            amp = math.exp(-self.reflex_t * 6)
            base[1] += 250 * amp
            base[3] += 250 * amp
            base[4] += 250 * amp
            self.reflex_t += dt

        out = []
        for i, sp in enumerate(self.springs):
            amp = (10 + 25 * arousal) * (0.5 + energy)   # 量程的 1–3%
            tgt = base[i] + amp * self.noise[i](t)
            sp.k = (30 + 70 * energy) * (1.5 if i in (3, 4) else 1.0)
            sp.c = 2 * 0.75 * math.sqrt(sp.k)
            out.append(max(0, min(1000, sp.step(tgt, dt))))
        v, w = self.cmd["base"]
        return out, v, w
```

### 6.5 `rt/rt_main.py`

```python
import socket, json, time, os
from link import Link
from synth import Synth

os.nice(-10) if os.geteuid() == 0 else None
link, syn = Link(), Synth()
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("127.0.0.1", 9001)); sock.setblocking(False)
tele_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

DT = 0.02
t0 = time.monotonic(); nxt = t0; last_cmd = 0
while True:
    try:
        while True:
            data, _ = sock.recvfrom(4096)
            syn.update_cmd(json.loads(data)); last_cmd = time.monotonic()
    except BlockingIOError:
        pass
    now = time.monotonic()
    if now - last_cmd > 1.0:
        syn.cmd["base"] = [0, 0]   # brain 失联：底盘停，但 idle 继续
    j, v, w = syn.step(now - t0, DT)
    link.send_joints(j, v, w)
    tele_out.sendto(json.dumps({"tele": link.tele, "events": link.events[-5:]}).encode(),
                    ("127.0.0.1", 9002))
    nxt += DT
    time.sleep(max(0, nxt - time.monotonic()))
```

### 6.6 systemd 服务

```ini
# systemd/walle-rt.service
[Unit]
Description=WALL-E realtime
After=dev-ttyACM0.device
[Service]
ExecStart=/home/pi/walle-env/bin/python /home/pi/walle-brain/rt/rt_main.py
WorkingDirectory=/home/pi/walle-brain/rt
Nice=-10
Restart=always
RestartSec=2
User=pi
[Install]
WantedBy=multi-user.target
```

```bash
sudo cp systemd/*.service /etc/systemd/system/ && sudo systemctl daemon-reload
sudo systemctl enable --now walle-rt
```

**P0 验收：**

1. 只启动 rt，机器人持续缓慢微动，10 分钟内动作看不出重复。
2. 用脚本把 `gaze` 在 -1 和 1 之间来回切换：头部转过去会有可见的小过冲，然后回稳。
3. 用 `kill -9` 杀掉 rt：200ms 内停车。
4. 微动幅度最小时，舵机**没有持续的嗡嗡声**。如果有，把 `amp` 的下限调大，或者把 `MAX_STEP` 调小。

---

## 阶段 7：感知 + 注视 + 情绪（P1 "活起来"）

### 7.1 `brain/imu.py`：航向

```python
import smbus2, time, threading

class IMU:
    def __init__(self, bus=1, addr=0x68):
        self.b, self.a = smbus2.SMBus(bus), addr
        self.b.write_byte_data(addr, 0x6B, 0)       # 唤醒
        self.b.write_byte_data(addr, 0x1B, 0x08)    # 陀螺仪量程 ±500dps
        self.yaw, self.bias, self.accel_mag = 0.0, 0.0, 1.0
        self._calib()
        threading.Thread(target=self._loop, daemon=True).start()

    def _gz(self):
        h, l = self.b.read_i2c_block_data(self.a, 0x47, 2)
        v = (h << 8) | l
        return (v - 65536 if v > 32767 else v) / 65.5

    def _acc(self):
        d = self.b.read_i2c_block_data(self.a, 0x3B, 6)
        r = [((d[i] << 8) | d[i+1]) for i in (0, 2, 4)]
        r = [(x - 65536 if x > 32767 else x) / 16384 for x in r]
        return sum(x*x for x in r) ** 0.5

    def _calib(self, n=300):
        # 校准期间机器人必须静止
        self.bias = sum(self._gz() for _ in range(n)) / n

    def _loop(self):
        t = time.monotonic()
        while True:
            now = time.monotonic(); dt = now - t; t = now
            gz = self._gz() - self.bias
            if abs(gz) > 0.5:
                self.yaw = (self.yaw + gz * dt) % 360
            self.accel_mag = self._acc()
            time.sleep(0.005)

    def bumped(self):
        return abs(self.accel_mag - 1.0) > 0.35
```

### 7.2 `brain/tof.py`

```python
import VL53L1X, threading, time

class ToF:
    def __init__(self):
        self.t = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
        self.t.open(); self.t.start_ranging(2)   # 中距离模式
        self.mm = 4000
        threading.Thread(target=self._loop, daemon=True).start()
    def _loop(self):
        while True:
            d = self.t.get_distance()
            if d > 0: self.mm = d
            time.sleep(0.05)
```

### 7.3 `brain/perception.py`：人脸 + 运动

先下载 OpenCV 的 YuNet 人脸模型 `face_detection_yunet_2023mar.onnx`（在 opencv_zoo 仓库里）。

```python
import cv2, numpy as np, threading, time
from picamera2 import Picamera2

class Perception:
    def __init__(self, w=640, h=480):
        self.cam = Picamera2()
        self.cam.configure(self.cam.create_video_configuration(main={"size": (w, h), "format": "RGB888"}))
        self.cam.start()
        self.face = cv2.FaceDetectorYN.create("models/face_detection_yunet_2023mar.onnx", "", (320, 240))
        self.W, self.H = w, h
        self.frame = None; self.faces = []; self.motion = None
        self._prev = None
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        while True:
            f = self.cam.capture_array()
            self.frame = f
            small = cv2.resize(f, (320, 240))
            _, det = self.face.detect(small)
            self.faces = [] if det is None else [
                ((d[0] + d[2]/2) / 320, (d[1] + d[3]/2) / 240, d[2] / 320) for d in det]
            g = cv2.GaussianBlur(cv2.cvtColor(small, cv2.COLOR_RGB2GRAY), (21, 21), 0)
            if self._prev is not None:
                diff = cv2.threshold(cv2.absdiff(g, self._prev), 25, 255, cv2.THRESH_BINARY)[1]
                ys, xs = np.nonzero(diff)
                self.motion = (xs.mean()/320, ys.mean()/240, len(xs)/(320*240)) if len(xs) > 400 else None
            self._prev = g
            time.sleep(1/15)
```

**注意：** 头在转动时整幅画面都在动，运动检测会误报。所以 brain 只在 rt 报告"头部基本静止"时才采信运动检测结果（见 7.5）。

### 7.4 `brain/gaze.py`：视觉伺服

```python
class Gaze:
    """把画面里的目标 (u,v)∈[0,1] 转换成 gaze 指令 [pan, tilt]∈[-1,1]。"""
    def __init__(self, kp=0.6, ki=0.05, dead=0.04, hfov=66):
        self.pan, self.tilt, self.ip, self.it = 0.0, 0.0, 0.0, 0.0
        self.kp, self.ki, self.dead = kp, ki, dead
    def update(self, u, v, dt):
        ex, ey = u - 0.5, 0.5 - v
        if abs(ex) < self.dead: ex = 0
        if abs(ey) < self.dead: ey = 0
        self.ip = max(-0.3, min(0.3, self.ip + ex * dt))
        self.it = max(-0.3, min(0.3, self.it + ey * dt))
        self.pan  = max(-1, min(1, self.pan  + (self.kp * ex + self.ki * self.ip) * dt * 3))
        self.tilt = max(-1, min(1, self.tilt + (self.kp * ey + self.ki * self.it) * dt * 3))
        return [self.pan, self.tilt]
    def head_saturated(self):
        return abs(self.pan) > 0.85
```

当头部转到接近极限（`head_saturated`）时，由 behavior 层让底盘朝同方向慢慢转，实现"头先动、底盘后跟"。

### 7.5 `brain/mood.py`、`attention.py`

```python
# mood.py
class Mood:
    def __init__(self):
        self.curiosity, self.arousal, self.energy, self.sociability = 0.5, 0.2, 0.8, 0.3
    def step(self, dt, novelty=0, stim=0, face=False, batt_mv=12000, moving=0):
        self.curiosity += dt * (novelty * 0.5 - 0.02 * self.curiosity)
        self.arousal += dt * (stim * 3 - 0.15 * self.arousal)
        batt = min(1, max(0, (batt_mv - 10500) / 2000))
        self.energy += dt * ((0.3 + 0.7 * batt) - self.energy) / 30 - dt * moving * 0.002
        self.sociability += dt * ((1 if face else 0) - self.sociability) / 20
        for k in ("curiosity", "arousal", "energy", "sociability"):
            setattr(self, k, max(0, min(1, getattr(self, k))))
    def d(self): return self.__dict__.copy()
```

```python
# attention.py
import math, random, time

class Attention:
    def __init__(self, temp=0.25, hold=0.8):
        self.temp, self.hold = temp, hold
        self.cur, self.since = None, 0
    def pick(self, cands):
        """cands: [(kind, u, v, score)]"""
        now = time.time()
        if self.cur and now - self.since < self.hold:
            best = [c for c in cands if c[0] == self.cur[0]]
            if best: return best[0]
        if not cands: return None
        ws = [math.exp(c[3] / self.temp) for c in cands]
        r = random.uniform(0, sum(ws))
        for c, wt in zip(cands, ws):
            r -= wt
            if r <= 0:
                if not self.cur or c[3] > self.cur[3] * 1.2 or now - self.since > self.hold:
                    self.cur, self.since = c, now
                return self.cur
        return self.cur
```

### 7.6 `brain/main.py`（P1 版本）

```python
import socket, json, time, random, threading
from perception import Perception
from imu import IMU
from gaze import Gaze
from mood import Mood
from attention import Attention

out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tele_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tele_in.bind(("127.0.0.1", 9002)); tele_in.setblocking(False)

per, imu, gz, mood, att = Perception(), IMU(), Gaze(), Mood(), Attention()
tele = {"batt": 12000}
scan_target = (0.5, 0.5); scan_t = 0

def send(**kw): out.sendto(json.dumps(kw).encode(), ("127.0.0.1", 9001))

dt = 0.1
while True:
    try:
        while True:
            tele = json.loads(tele_in.recvfrom(8192)[0])["tele"]
    except BlockingIOError:
        pass
    cands = [("face", u, v, 1.0) for u, v, _ in per.faces]
    if per.motion and abs(gz.pan) < 0.9:
        cands.append(("motion", per.motion[0], per.motion[1], 0.7))
    if time.time() > scan_t:
        scan_target = (random.uniform(0.2, 0.8), random.uniform(0.35, 0.65))
        scan_t = time.time() + random.uniform(1.5, 4)
    cands.append(("scan", *scan_target, 0.3))
    tgt = att.pick(cands)
    stim = 1 if imu.bumped() else 0
    mood.step(dt, stim=stim, face=bool(per.faces), batt_mv=tele.get("batt", 12000))
    gaze = gz.update(tgt[1], tgt[2], dt) if tgt else None
    pose = "startled" if stim else ("curious" if mood.curiosity > 0.6 else "neutral")
    base_w = 25 * (1 if gz.pan > 0 else -1) if gz.head_saturated() else 0
    send(gaze=gaze, pose=pose, mood=mood.d(), base=[0, base_w],
         reflex="startle" if stim else None)
    time.sleep(dt)
```

**P1 验收：**

1. 屋里没人时，机器人会到处"看"，有停顿，不像在待机。
2. 人走动时头会跟着；人站定后，人脸稳定在画面中心 ±10% 以内，没有来回振荡。
3. 拍一下机身，会出现惊吓反应。
4. 人走到侧面，头部转到极限后，底盘会跟着转过来。

**如果出现振荡：** 依次尝试调小 `kp`、调大 `dead`，或在 rt 里降低头部弹簧的 `k`。

---

## 阶段 8：语音 + 找物（P2）

### 8.1 唤醒与识别【修正】

使用 **sherpa-onnx**：

- **关键词检测（KWS）** 直接用中文拼音关键词，**不需要训练**。
- **SenseVoice** 做中文识别。

```bash
mkdir -p models && cd models
# 从 sherpa-onnx 的 GitHub releases 下载：
#   sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01   （中文 KWS）
#   sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17      （ASR，int8 版本）
```

关键词文件 `keywords.txt` 的写法参考 KWS 模型附带的示例。把"瓦力"转成模型要求的拼音 token 格式，可以用 sherpa-onnx 自带的 `text2token` 工具。

```python
# brain/voice.py
import sherpa_onnx, sounddevice as sd, numpy as np, re, queue, threading, time

PAT = re.compile(r"(?:找到|找找|找一下|帮我找|看看|去找)\s*(.+)")

class Voice:
    def __init__(self, on_command, is_noisy):
        self.on_command, self.is_noisy = on_command, is_noisy
        d = "models/sherpa-onnx-kws-zipformer-wenetspeech-3.3M-2024-01-01"
        self.kws = sherpa_onnx.KeywordSpotter(
            tokens=f"{d}/tokens.txt", encoder=f"{d}/encoder-epoch-12-avg-2-chunk-16-left-64.int8.onnx",
            decoder=f"{d}/decoder-epoch-12-avg-2-chunk-16-left-64.int8.onnx",
            joiner=f"{d}/joiner-epoch-12-avg-2-chunk-16-left-64.int8.onnx",
            keywords_file="models/keywords.txt", num_threads=1)
        a = "models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17"
        self.asr = sherpa_onnx.OfflineRecognizer.from_sense_voice(
            model=f"{a}/model.int8.onnx", tokens=f"{a}/tokens.txt", language="zh", use_itn=True, num_threads=2)
        self.q = queue.Queue()
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        sr = 16000
        stream = self.kws.create_stream()
        with sd.InputStream(samplerate=sr, channels=1, dtype="float32", blocksize=1600,
                            callback=lambda d, *_: self.q.put(d[:, 0].copy())):
            while True:
                chunk = self.q.get()
                if self.is_noisy():
                    continue        # 电机转动时不监听
                stream.accept_waveform(sr, chunk)
                while self.kws.is_ready(stream):
                    self.kws.decode_stream(stream)
                if self.kws.get_result(stream):
                    self.kws.reset_stream(stream)
                    self.on_command("__wake__")
                    audio = self._record(sr, 3.0)
                    s = self.asr.create_stream(); s.accept_waveform(sr, audio)
                    self.asr.decode_stream(s)
                    text = s.result.text
                    m = PAT.search(text)
                    self.on_command(m.group(1).strip("。，！？ ") if m else ("__heard__:" + text))

    def _record(self, sr, sec):
        buf, need = [], int(sr * sec)
        while sum(len(b) for b in buf) < need:
            buf.append(self.q.get())
        return np.concatenate(buf)[:need]
```

**调试：** 在 `keywords.txt` 里可以给每个关键词设置触发阈值，先用较低的阈值确认能唤醒，再逐步调高，减少误触发。

### 8.2 本地检测器（固定类别）

```bash
# 在电脑上导出，然后把模型目录拷到 Pi
yolo export model=yolov8n.pt format=ncnn imgsz=320
```

```python
# brain/detector.py
from ultralytics import YOLO
import requests, base64, cv2

ZH2EN = {"杯子": "cup", "瓶子": "bottle", "手机": "cell phone", "书": "book", "椅子": "chair",
         "球": "sports ball", "键盘": "keyboard", "鼠标": "mouse", "遥控器": "remote",
         "人": "person", "猫": "cat", "狗": "dog", "背包": "backpack", "碗": "bowl",
         "笔记本": "laptop", "电脑": "laptop", "剪刀": "scissors", "泰迪熊": "teddy bear",
         "玩偶": "teddy bear", "钟": "clock", "花瓶": "vase", "盆栽": "potted plant"}

class Detector:
    def __init__(self, gpu_url=None):
        self.local = YOLO("models/yolov8n_ncnn_model", task="detect")
        self.gpu_url = gpu_url
        self.offline = gpu_url is None

    def _local_class(self, zh):
        for k, v in ZH2EN.items():
            if k in zh: return v
        return None

    def detect(self, frame, target_zh):
        """返回 [(u, v, area, score)]，坐标已归一化。"""
        if self.gpu_url:
            try:
                ok, jpg = cv2.imencode(".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 80])
                r = requests.post(self.gpu_url + "/detect", timeout=1.0, json={
                    "image": base64.b64encode(jpg).decode(), "prompt": target_zh, "top_k": 5})
                self.offline = False
                return [self._norm(b["xyxy"], b["score"], frame) for b in r.json()["boxes"]]
            except Exception:
                self.offline = True
        cls = self._local_class(target_zh)
        if cls is None: return None   # 表示本地模型不认识这个词
        res = self.local(frame, imgsz=320, verbose=False)[0]
        names = res.names
        return [self._norm(b.xyxy[0].tolist(), float(b.conf), frame)
                for b in res.boxes if names[int(b.cls)] == cls and b.conf > 0.35]

    @staticmethod
    def _norm(xyxy, s, f):
        h, w = f.shape[:2]; x1, y1, x2, y2 = xyxy
        return ((x1+x2)/2/w, (y1+y2)/2/h, (x2-x1)*(y2-y1)/(w*h), s)
```

### 8.3 `brain/search.py`：状态机

```python
import time

class Search:
    """每次 tick 返回 rt 指令 dict；返回 None 表示搜索结束。"""
    def __init__(self, det, per, imu, tof, gaze, audio, memory=None, timeout=30):
        self.det, self.per, self.imu, self.tof, self.gz, self.au, self.mem = det, per, imu, tof, gaze, audio, memory
        self.timeout = timeout
        self.state = None

    def start(self, target):
        self.target, self.t0 = target, time.time()
        self.state, self.ts = "ACK", time.time()
        self.best = None                       # (score, yaw)
        self.sector, self.view = 0, 0
        self.yaw0 = self.imu.yaw
        self.au.play("curious")

    def _score(self, hits):
        return max(((s * min(1, a * 8) * (1 - abs(u - 0.5)), u, v) for u, v, a, s in hits), default=None)

    def tick(self, dt):
        st, now = self.state, time.time()
        if st is None: return None
        if now - self.t0 > self.timeout and st in ("SWEEP", "TURN"):
            self.state, self.ts = "GIVE_UP", now; self.au.play("sad")

        if st == "ACK":
            if now - self.ts > 0.6: self.state, self.ts = "SWEEP", now
            return {"pose": "curious", "gaze": [0, 0.3], "base": [0, 0]}

        if st == "SWEEP":
            views = [-0.7, 0, 0.7]
            pan = views[self.view]
            if now - self.ts < 0.5:            # 等转到位、画面稳定
                return {"pose": "curious", "gaze": [pan, 0.1], "base": [0, 0]}
            hits = self.det.detect(self.per.frame, self.target)
            if hits is None:
                self.state = "UNKNOWN"; self.au.play("confused")
                return {"pose": "sad", "gaze": [0, 0], "base": [0, 0]}
            sc = self._score(hits)
            if sc and sc[0] > 0.25:
                self.gz.pan = pan
                self.state, self.ts = "SERVO", now; self.au.play("found")
                return {"pose": "curious", "gaze": [pan, 0.1], "base": [0, 0]}
            if sc and (not self.best or sc[0] > self.best[0]):
                self.best = (sc[0], self.imu.yaw)
            self.view += 1; self.ts = now
            if self.view == 3:
                self.view = 0; self.sector += 1
                if self.sector >= 8:
                    self.state, self.ts = "GIVE_UP", now; self.au.play("sad")
                else:
                    self.state, self.turn_goal = "TURN", (self.yaw0 + 45 * self.sector) % 360
            return {"pose": "curious", "gaze": [pan, 0.1], "base": [0, 0]}

        if st == "TURN":
            err = ((self.turn_goal - self.imu.yaw + 540) % 360) - 180
            if abs(err) < 5:
                self.state, self.ts = "SWEEP", now
                return {"base": [0, 0]}
            return {"pose": "curious", "gaze": [0, 0.1], "base": [0, max(-35, min(35, err * 1.2))]}

        if st == "SERVO":
            hits = self.det.detect(self.per.frame, self.target) or []
            sc = self._score(hits)
            if not sc:
                if now - self.ts > 2: self.state, self.ts = "SWEEP", now
                return {"base": [0, 0]}
            self.ts = now
            g = self.gz.update(sc[1], sc[2], dt)
            w = 20 * g[0] if abs(g[0]) > 0.3 else 0
            if abs(sc[1] - 0.5) < 0.08 and abs(g[0]) < 0.3:
                self.state = "APPROACH"
            return {"pose": "curious", "gaze": g, "base": [0, w]}

        if st == "APPROACH":
            if self.tof.mm < 250 or now - self.ts > 8:
                self.state, self.ts = "CONFIRM", now
                return {"base": [0, 0]}
            hits = self.det.detect(self.per.frame, self.target) or []
            sc = self._score(hits)
            g = self.gz.update(sc[1], sc[2], dt) if sc else [self.gz.pan, self.gz.tilt]
            speed = min(40, max(15, (self.tof.mm - 250) / 15))
            return {"pose": "curious", "gaze": g, "base": [speed, 25 * g[0]]}

        if st == "CONFIRM":
            side = "point_R" if self.gz.pan > 0 else "point_L"
            if now - self.ts > 2.5:
                if self.mem: self.mem.log_command(self.target, True, now - self.t0, self.per.frame)
                self.state = None
                return {"pose": "neutral", "base": [0, 0]}
            return {"pose": side, "gaze": [self.gz.pan, self.gz.tilt], "base": [0, 0]}

        if st == "GIVE_UP":
            t = now - self.ts
            if t > 3:
                if self.mem: self.mem.log_command(self.target, False, now - self.t0, None)
                self.state = None
                return {"pose": "neutral", "base": [0, 0]}
            shake = 0.4 if int(t * 3) % 2 else -0.4
            return {"pose": "sad", "gaze": [shake if t < 1.5 else 0, -0.4], "base": [0, 0]}

        if st == "UNKNOWN":
            self.state = None
            return {"pose": "sad", "base": [0, 0]}
```

### 8.4 `brain/audio.py`

```python
import subprocess, os
class Audio:
    def __init__(self, d="sounds"): self.d = d
    def play(self, name):
        p = os.path.join(self.d, name + ".wav")
        if os.path.exists(p):
            subprocess.Popen(["aplay", "-q", p], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
```

准备 8 个音效文件 `found / curious / confused / startled / content / sad / hello / thinking.wav`，统一转成 16kHz 单声道。音效可以从原项目里裁剪，或用电子合成音效自己做。如果需要外放，给 Pi 加一个 USB 声卡和小音箱。

### 8.5 接入 `main.py`

在主循环里加入搜索逻辑：

```python
from voice import Voice
from detector import Detector
from search import Search
from tof import ToF
from audio import Audio

au, tof = Audio(), ToF()
det = Detector(gpu_url=None)        # 阶段 10 再填 GPU 地址
srch = Search(det, per, imu, tof, gz, au)
moving = lambda: abs(tele.get("curA", 0)) + abs(tele.get("curB", 0)) > 80

def on_cmd(t):
    if t == "__wake__": send(pose="curious", gaze=[0, 0.4], base=[0, 0]); au.play("hello")
    elif t.startswith("__heard__"): au.play("confused")
    else: srch.start(t)
Voice(on_cmd, moving)

# 主循环里，在 send() 之前：
cmd = srch.tick(dt)
if cmd is not None:
    send(mood=mood.d(), **cmd); time.sleep(dt); continue
```

**P2 验收：**

1. 说"瓦力"，机器人抬头并播放打招呼音效（1 秒内）。
2. 说"瓦力……找到杯子"：机器人开始转动搜索，30 秒内找到，靠近，停在约 25cm，转头盯住，抬手指向目标。
3. 杯子藏起来：转一圈后摇头、低头，播放沮丧音效。
4. 说"找到独角兽"（本地不认识的词）：播放困惑音效。
5. 原地转满 8 个扇区后，底盘朝向和起点相差小于 20°（IMU 航向有效）。

---

## 阶段 9：记忆 + 好奇（P3）

### 9.1 embedding 模型

在电脑上导出 MobileNetV3-Small，去掉分类头，输出 576 维特征：

```python
# 在电脑上运行
import torch, torchvision
m = torchvision.models.mobilenet_v3_small(weights="DEFAULT")
m.classifier = torch.nn.Identity(); m.eval()
torch.onnx.export(m, torch.randn(1, 3, 224, 224), "mnv3s_emb.onnx", opset_version=13)
```

### 9.2 `brain/memory.py`

```python
import sqlite3, numpy as np, time, cv2, onnxruntime as ort

class Memory:
    def __init__(self, path="/home/pi/walle-data/mem.db"):
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS objects(id INTEGER PRIMARY KEY, first_seen REAL, last_seen REAL,
            count INTEGER, emb BLOB, label TEXT, yaw_hint REAL);
        CREATE TABLE IF NOT EXISTS episodes(id INTEGER PRIMARY KEY, t REAL, event TEXT, target_id INTEGER, outcome TEXT);
        CREATE TABLE IF NOT EXISTS commands(id INTEGER PRIMARY KEY, t REAL, text TEXT, success INTEGER, duration_s REAL);
        """)
        self.sess = ort.InferenceSession("models/mnv3s_emb.onnx", providers=["CPUExecutionProvider"])
        self._load()

    def _load(self):
        rows = self.db.execute("SELECT id, emb FROM objects").fetchall()
        self.ids = [r[0] for r in rows]
        self.embs = np.stack([np.frombuffer(r[1], np.float32) for r in rows]) if rows else np.zeros((0, 576), np.float32)

    def embed(self, crop):
        x = cv2.resize(crop, (224, 224)).astype(np.float32) / 255
        x = ((x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]).transpose(2, 0, 1)[None].astype(np.float32)
        e = self.sess.run(None, {self.sess.get_inputs()[0].name: x})[0][0]
        return e / (np.linalg.norm(e) + 1e-8)

    def novelty(self, e):
        if len(self.embs) == 0: return 1.0, None
        sims = self.embs @ e
        i = int(np.argmax(sims))
        return float(1 - sims[i]), self.ids[i]

    def observe(self, crop, label=None, yaw=None, merge_thr=0.15):
        e = self.embed(crop)
        nov, oid = self.novelty(e)
        now = time.time()
        if oid is not None and nov < merge_thr:
            self.db.execute("UPDATE objects SET last_seen=?, count=count+1, yaw_hint=COALESCE(?,yaw_hint) WHERE id=?",
                            (now, yaw, oid))
        else:
            cur = self.db.execute("INSERT INTO objects(first_seen,last_seen,count,emb,label,yaw_hint) VALUES(?,?,?,?,?,?)",
                                  (now, now, 1, e.astype(np.float32).tobytes(), label, yaw))
            oid = cur.lastrowid; self._load()
        self.db.commit()
        return nov, oid

    def yaw_hint(self, label):
        r = self.db.execute("SELECT yaw_hint FROM objects WHERE label=? AND yaw_hint IS NOT NULL "
                            "ORDER BY last_seen DESC LIMIT 1", (label,)).fetchone()
        return r[0] if r else None

    def log_command(self, text, ok, dur, frame):
        self.db.execute("INSERT INTO commands(t,text,success,duration_s) VALUES(?,?,?,?)",
                        (time.time(), text, int(ok), dur))
        self.db.commit()
```

**【修正】关于"二次寻找更快"：** 只记录一个**相对航向提示 `yaw_hint`**，不记录坐标。下次搜索同一个词时，`Search.start` 先查 `yaw_hint`，**先转到那个方向搜**。IMU 航向在重启后会归零，所以这个提示只在同一次开机期间有效。验收标准也相应改成"**同一次开机内第二次寻找更快**"。

在 `Search.start` 里加入：

```python
hint = self.mem.yaw_hint(target) if self.mem else None
if hint is not None:
    self.state, self.turn_goal = "TURN", hint
```

在 `CONFIRM` 状态里，裁出目标框，调用 `mem.observe(crop, label=self.target, yaw=self.imu.yaw)`。

### 9.3 好奇驱动

在 brain 主循环里**每 2 秒做一次**：

1. 用本地 YOLOv8n 的全类别检测结果作为候选区域，或用显著性检测。
2. 取最大的框，裁剪出来，调用 `mem.observe` 得到 novelty。
3. 如果 novelty 高于"历史 novelty 的 80% 分位数"，就作为一个 `("novel", u, v, 0.9 * novelty)` 候选加入注意力，并把 novelty 喂给 `mood.curiosity`。
4. 如果 `curiosity > 0.75`，并且 ToF 距离大于 60cm，就慢速靠近（v=15），2 秒后停下观察。

**工具脚本：** 写一个 `tools/test_novelty.py`，对同一个物体连续拍 5 张照片，确认 novelty 逐张下降。这个测试不需要机器人，在电脑上就能跑。

**P3 验收：**

1. 拿一个新物体放到它面前：机器人凑过去看。第二次再拿出来，novelty 下降 50% 以上，反应明显变平淡。
2. 同一次开机内，第二次说"找到杯子"，用时不超过第一次的一半。

---

## 阶段 10：GPU 开放词汇 + 避障（P4/P5）

### 10.1 GPU 服务 `gpu/server.py`

```bash
pip install fastapi uvicorn ultralytics transformers sentencepiece opencv-python
```

```python
import base64, time, numpy as np, cv2
from fastapi import FastAPI
from pydantic import BaseModel
from ultralytics import YOLOWorld
from transformers import MarianMTModel, MarianTokenizer

app = FastAPI()
det = YOLOWorld("yolov8s-worldv2.pt")
tok = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-zh-en")
mt = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-zh-en").cuda()
_cache = {}

def zh2en(s):
    if s not in _cache:
        out = mt.generate(**tok([s], return_tensors="pt").to("cuda"), max_new_tokens=20)
        _cache[s] = tok.decode(out[0], skip_special_tokens=True).lower().strip(". ")
    return _cache[s]

class Req(BaseModel):
    image: str
    prompt: str
    top_k: int = 5

@app.post("/detect")
def detect(r: Req):
    t0 = time.time()
    img = cv2.imdecode(np.frombuffer(base64.b64decode(r.image), np.uint8), cv2.IMREAD_COLOR)
    en = zh2en(r.prompt)
    det.set_classes([en])
    res = det.predict(img, conf=0.15, verbose=False)[0]
    boxes = sorted([{"xyxy": b.xyxy[0].tolist(), "score": float(b.conf), "label": en} for b in res.boxes],
                   key=lambda b: -b["score"])[: r.top_k]
    return {"boxes": boxes, "en": en, "latency_ms": int((time.time() - t0) * 1000)}
```

启动：

```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

- **安全：** 这个服务只在局域网内监听，路由器上不要做端口映射。
- **接入：** 把 Pi 上的 `Detector(gpu_url="http://<GPU机IP>:8000")` 填好。连不上时会自动回落到本地模型，`det.offline` 为 True；可以在离线时播放 `thinking` 音效作为提示。

### 10.2 避障与脱困（P5）

在 `APPROACH` 状态以及好奇驱动的靠近过程中，统一套一层安全限速：

```python
def safe_v(v, tof_mm):
    if tof_mm < 200: return min(v, 0)
    if tof_mm < 500: return min(v, 15)
    return v
```

脱困逻辑：遥测里出现堵转标志，或者 IMU 检测到碰撞时：

1. 后退 0.6 秒（v=-25）。
2. 原地转 30°，用 IMU 闭环控制角度。
3. 播放 `startled` 音效。
4. 如果 1 分钟内脱困超过 3 次，放弃当前任务，进入 `sad` 姿态。

**P4/P5 验收：**

1. 说"找到红色的马克杯"，能在多个杯子里挑出红色的那个。
2. 拔掉 GPU 机网线：自动切回本地模型，"找到杯子"仍然可用。
3. 让机器人朝墙走：在 20–25cm 处停下，全程不撞。
4. 把它卡在椅子腿之间：能自己退出来。

---

## 附 A：标定与调参顺序

| 顺序 | 参数                    | 位置              | 方法                                                               |
| ---- | ----------------------- | ----------------- | ------------------------------------------------------------------ |
| 1    | `preset`                | 固件              | 原版标定流程                                                       |
| 2    | 姿态表 `POSES`          | synth             | 写一个 `tools/record_poses.py`：键盘逐关节微调，满意后打印当前数值 |
| 3    | 弹簧 `k`、阻尼比 `zeta` | synth             | 先单关节阶跃，用肉眼看过冲：过冲 3–8% 最自然                       |
| 4    | `MAX_STEP`              | 固件              | 最快扫视不卡顿、舵机不尖叫                                         |
| 5    | Gaze 的 `kp`、`dead`    | brain             | 人站定时头部不来回晃                                               |
| 6    | `STALL_RAW`             | 固件              | 用手按住履带，读遥测里的电流值                                     |
| 7    | KWS 阈值                | `keywords.txt`    | 一天内误唤醒次数少于 3 次                                          |
| 8    | 检测阈值（0.25 / 0.35） | search / detector | 用 20 张自家场景照片调                                             |

## 附 B：故障排查

| 现象             | 先查什么                                              |
| ---------------- | ----------------------------------------------------- |
| Pi 随机重启      | `vcgencmd get_throttled`；Buck B 电压；是否共地       |
| 串口出现 `E,CRC` | 共地；USB 线质量（换短线、带磁环的线）                |
| 舵机嗡嗡响       | 微动幅度太小；`MAX_STEP` 太小导致来回抖；舵机本身质量 |
| 头部抽搐         | 视觉伺服增益太高；运动检测在头部转动时没有屏蔽        |
| 转圈角度不准     | IMU 零偏校准时机器人没静止；IMU 没固定牢              |
| 一直唤醒失败     | 麦克风离电机太近；阈值太高；`arecord` 录音音量太小    |
| 检测很慢         | Pi 温度超过 80°C；YOLO 输入分辨率；是否重复加载了模型 |

## 附 C：总时间线（单人，业余时间）

| 阶段     | 内容                  | 预计                   |
| -------- | --------------------- | ---------------------- |
| 0–3      | 采购、电源、装配      | 1–2 周（主要是等快递） |
| 4–6      | 固件 + 实时进程（P0） | 3–5 天                 |
| 7        | 活起来（P1）          | 4–6 天                 |
| 8        | 语音 + 找物（P2）     | 1–2 周                 |
| 9        | 记忆（P3）            | 1 周                   |
| 10       | GPU + 避障（P4/P5）   | 1–2 周                 |
| **合计** |                       | **约 7–10 周**         |

**每个阶段都必须先通过验收，再进入下一阶段。** P0 和 P1 最重要，机器人"像活的"大部分靠这两步。

如果需要，我可以把这些代码整理成完整的 `walle-brain/` 工程，写进本地工作区。
