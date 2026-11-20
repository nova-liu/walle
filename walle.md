# WALL·E 自主化：从零到成品的施工手册

基于chillibasket 的WALL·E： https://wired.chillibasket.com/3d-printed-wall-e/
进行改造，让他能够看到东西，听懂说话，自主决策行为。

需要打印的 61 个文件在 [stl/print](stl/print),文件名已去掉 `-xN` 后缀。每个 STL 只含 1 份,打印份数见下表。

## 打印清单

| 组 | 文件(去掉 .STL) | 打印份数 |
|---|---|---|
| 身体 | body-bottom | 1 |
| 身体 | body-back | 1 |
| 身体 | body-front | 1 |
| 身体 | body-front-door | 1 |
| 身体 | body-front-pins | 2 |
| 身体 | body-left | 1 |
| 身体 | body-right | 1 |
| 身体 | body-top | 1 |
| 身体 | body-neck-servo-holder | 1 |
| 手臂 | arm-servo-bracket-left | 1 |
| 手臂 | arm-servo-bracket-right | 1 |
| 手臂 | arm-hinge-inner | 2 |
| 手臂 | arm-hinge-outer | 2 |
| 手臂 | arm-hinge-axle | 2 |
| 手臂 | arm-barrel | 2 |
| 手臂 | arm-barrel-end | 2 |
| 手臂 | arm-piston | 2 |
| 手臂 | hand-bracket | 2 |
| 手臂 | hand-axle | 2 |
| 手臂 | hand-finger-left | 2 |
| 手臂 | hand-finger-right | 2 |
| 手臂 | hand-finger-middle | 2 |
| 头 | head-center | 1 |
| 头 | head-axle | 1 |
| 头 | eye-back-left | 1 |
| 头 | eye-back-right | 1 |
| 头 | eye-middle-left | 1 |
| 头 | eye-middle-right | 1 |
| 头 | eye-front-left | 1 |
| 头 | eye-front-right | 1 |
| 头 | eye-camera-replica | 2 |
| 头 | eye-camera-mount | 2 |
| 颈 | neck-bottom-axle | 1 |
| 颈 | neck-bottom-left | 1 |
| 颈 | neck-bottom-right | 1 |
| 颈 | neck-bottom-linkage | 1 |
| 颈 | neck-middle-axle | 1 |
| 颈 | neck-top | 1 |
| 颈 | neck-round-bottom | 1 |
| 颈 | neck-round-top-left | 1 |
| 颈 | neck-round-top-right | 1 |
| 颈 | neck-wire-guide-left | 1 |
| 颈 | neck-wire-guide-right | 1 |
| 颈 | neck-top-linkage | 1 |
| 轮子 | wheel-back | 4 |
| 轮子 | wheel-front | 4 |
| 轮子 | wheel-top | 8 |
| 轮子 | wheel-gear-driven | 2 |
| 轮子 | wheel-gear-motor | 2 |
| 轮子 | wheel-axle-notched | 6 |
| 轮子 | wheel-axle-back | 2 |
| 轮子 | wheel-axle-spacer | 8 |
| 轮子 | wheel-frame-left | 1 |
| 轮子 | wheel-frame-right | 1 |
| 轮子 | wheel-frame-addon | 2 |
| 轮子 | wheel-bracket-inner-left | 1 |
| 轮子 | wheel-bracket-inner-right | 1 |
| 轮子 | wheel-bracket-outer-left | 1 |
| 轮子 | wheel-bracket-outer-right | 1 |
| 履带 | tread-plate | 70 |
| 履带 | tread-pin | 140 |
| **合计** | | **312** |

作者 Google Drive 的 STL 文件夹里还有 14 个文件,不在 PDF 清单里,用途我没核实,已单独放进 [stl/not-in-pdf](stl/not-in-pdf),先不打印:`body-front-power`、`switch-holder`、`missing-piston-insert`、`neck-bottom-linkage-longer`、`wheel-top-larger`、`wheel-bracket-inner-left-2`、`wheel-bracket-inner-left-3`、`wheel-bracket-inner-right-2`、`wheel-bracket-inner-right-3`、`wheel-bracket-outer-left-2`、`wheel-bracket-outer-left-3`、`wheel-bracket-outer-right-2`、`wheel-bracket-outer-right-3`、`Wall-E_Assembly_NotForPrinting`(仅供查看装配)。

## 分两次打印

文件是 [stl/print](stl/print) 里对应文件的副本。第一次打完试装没问题,再打第二次。两次都用同样的工艺、层高和摆放方向。

### 第一次打:[stl/batch-1](stl/batch-1)

| 文件(去掉 .STL) | 打印份数 |
|---|---|
| arm-hinge-axle | 1 |
| arm-hinge-outer | 1 |
| arm-hinge-inner | 1 |
| wheel-axle-back | 1 |
| wheel-top | 1 |
| tread-plate | 6 |
| tread-pin | 12 |
| body-neck-servo-holder | 1 |
| arm-servo-bracket-left | 1 |
| **合计** | **25** |

### 第二次打:[stl/batch-2](stl/batch-2)

| 组 | 文件(去掉 .STL) | 整机总数 | 第一次已打 | 第二次打 |
|---|---|---|---|---|
| 身体 | body-bottom | 1 | 0 | 1 |
| 身体 | body-back | 1 | 0 | 1 |
| 身体 | body-front | 1 | 0 | 1 |
| 身体 | body-front-door | 1 | 0 | 1 |
| 身体 | body-front-pins | 2 | 0 | 2 |
| 身体 | body-left | 1 | 0 | 1 |
| 身体 | body-right | 1 | 0 | 1 |
| 身体 | body-top | 1 | 0 | 1 |
| 手臂 | arm-servo-bracket-right | 1 | 0 | 1 |
| 手臂 | arm-hinge-inner | 2 | 1 | 1 |
| 手臂 | arm-hinge-outer | 2 | 1 | 1 |
| 手臂 | arm-hinge-axle | 2 | 1 | 1 |
| 手臂 | arm-barrel | 2 | 0 | 2 |
| 手臂 | arm-barrel-end | 2 | 0 | 2 |
| 手臂 | arm-piston | 2 | 0 | 2 |
| 手臂 | hand-bracket | 2 | 0 | 2 |
| 手臂 | hand-axle | 2 | 0 | 2 |
| 手臂 | hand-finger-left | 2 | 0 | 2 |
| 手臂 | hand-finger-right | 2 | 0 | 2 |
| 手臂 | hand-finger-middle | 2 | 0 | 2 |
| 头 | head-center | 1 | 0 | 1 |
| 头 | head-axle | 1 | 0 | 1 |
| 头 | eye-back-left | 1 | 0 | 1 |
| 头 | eye-back-right | 1 | 0 | 1 |
| 头 | eye-middle-left | 1 | 0 | 1 |
| 头 | eye-middle-right | 1 | 0 | 1 |
| 头 | eye-front-left | 1 | 0 | 1 |
| 头 | eye-front-right | 1 | 0 | 1 |
| 头 | eye-camera-replica | 2 | 0 | 2 |
| 头 | eye-camera-mount | 2 | 0 | 2 |
| 颈 | neck-bottom-axle | 1 | 0 | 1 |
| 颈 | neck-bottom-left | 1 | 0 | 1 |
| 颈 | neck-bottom-right | 1 | 0 | 1 |
| 颈 | neck-bottom-linkage | 1 | 0 | 1 |
| 颈 | neck-middle-axle | 1 | 0 | 1 |
| 颈 | neck-top | 1 | 0 | 1 |
| 颈 | neck-round-bottom | 1 | 0 | 1 |
| 颈 | neck-round-top-left | 1 | 0 | 1 |
| 颈 | neck-round-top-right | 1 | 0 | 1 |
| 颈 | neck-wire-guide-left | 1 | 0 | 1 |
| 颈 | neck-wire-guide-right | 1 | 0 | 1 |
| 颈 | neck-top-linkage | 1 | 0 | 1 |
| 轮子 | wheel-back | 4 | 0 | 4 |
| 轮子 | wheel-front | 4 | 0 | 4 |
| 轮子 | wheel-top | 8 | 1 | 7 |
| 轮子 | wheel-gear-driven | 2 | 0 | 2 |
| 轮子 | wheel-gear-motor | 2 | 0 | 2 |
| 轮子 | wheel-axle-notched | 6 | 0 | 6 |
| 轮子 | wheel-axle-back | 2 | 1 | 1 |
| 轮子 | wheel-axle-spacer | 8 | 0 | 8 |
| 轮子 | wheel-frame-left | 1 | 0 | 1 |
| 轮子 | wheel-frame-right | 1 | 0 | 1 |
| 轮子 | wheel-frame-addon | 2 | 0 | 2 |
| 轮子 | wheel-bracket-inner-left | 1 | 0 | 1 |
| 轮子 | wheel-bracket-inner-right | 1 | 0 | 1 |
| 轮子 | wheel-bracket-outer-left | 1 | 0 | 1 |
| 轮子 | wheel-bracket-outer-right | 1 | 0 | 1 |
| 履带 | tread-plate | 70 | 6 | 64 |
| 履带 | tread-pin | 140 | 12 | 128 |
| **合计** | | **312** | **25** | **287** |

## 表 1:第一阶段(复现原版,可遥控)

| # | 零件 | 规格 / 搜索关键词 | 数量 | 用途与备注 |
|---|---|---|---|---|
| 1 | 3D 打印件 | PLA 或 PETG,约 2–3 kg(估算,以切片为准)。按上面的打印清单打印,共 312 件(PDF 的 310 件加 2 个 `eye-camera-mount`) | 1 套 | 机身、头、颈、手臂、轮子、履带 |
| 2 | TPU 耗材(可选) | 履带用,配合 ZDC 的回形针销 remix | 1 卷 | 提高履带抓地力 |
| 3 | M3 螺栓 10mm | 不锈钢 | 14(买 30) | 固定外壳 |
| 4 | M3 螺栓 20mm | 不锈钢 | 12(买 20) | 固定外壳 |
| 5 | M3 螺栓 6mm | 不锈钢 | 2(买 10) | 网页清单列出,PDF 未列 |
| 6 | M3 螺母 | 不锈钢 | 26(买 40) | 配合螺栓 |
| 7 | 回形针 | 普通金属回形针 | 3 | 颈部连杆 |
| 8 | 平凸透镜 | ⌀31.5–32.5mm,或拆旧双筒望远镜 | 2 | 眼睛镜片 |
| 9 | 微型舵机 | TowerPro MG90S | 7(买 9) | 头、颈上、颈下、左右眼、左右臂 |
| 10 | 12V 减速直流电机 | Pololu 37D,100–150RPM,⌀37mm,偏心输出轴,参考 pololu.com/product/4745,下单前核对规格（JGB37-520 110rpm 国产替代） | 2 | 履带驱动 |
| 11 | Arduino Uno R3 | 或兼容板 | 1 | 实时控制电机和舵机 |
| 12 | Arduino Motor Shield Rev3 | 或同类 L298P 电机扩展板 | 1 | 驱动 2 个直流电机 |
| 13 | 16 路 I²C 舵机驱动板 | Adafruit PCA9685(产品号 815) | 1 | 驱动 7 个舵机 |
| 14 | 树莓派 5 8GB + 官方 Active Cooler | | 1 | 作者用 Pi 4。提前买 Pi 5,第二阶段要接 NPU。我没验证作者软件在 Pi 5 上直接可用 |
| 15 | microSD 卡 | 64GB,A2 高耐久 | 1 | 系统盘 |
| 16 | 降压模块 12V→5V | 5V 8–10A,如 Pololu D24V90F5 | 1 | 给树莓派供电。Pi 5 接 GPIO 5V 引脚,并在 config.txt 设 `usb_max_current_enable=1` |
| 17 | 锂电池 | 3S 11.1V 2200mAh 30C,XT60 接口 | 1 | 主电源 |
| 18 | LiPo 平衡充电器 + 防爆袋 | 支持 3S | 1 套 | 充电和存放 |
| 19 | XT60 连接器 | 公母各 5 对一包 | 1 包 | 电池接口 |
| 20 | 总电源开关 | 10A 以上,船型或拨动 | 1 | |
| 21 | 保险丝或保险管座 | 10A | 1 | 保护电池线 |
| 22 | USB-A 转 USB-B 线 | 短线 | 1 | Uno 连树莓派 |
| 23 | I²S 功放模块 | MAX98357A | 1 | Pi 5 没有 3.5mm 耳机口,不能直接接作者的喇叭 |
| 24 | 小喇叭 | 3W,4Ω,直径 28–40mm | 1 | 播放音效 |
| 25 | 电阻 | 100kΩ、47kΩ | 各 1(买 5) | 电池电压检测分压 |
| 26 | OLED 显示屏(可选) | 1.3 寸 SH1106 I²C | 1 | 装进太阳能面板位置显示电量 |
| 27 | 导线 | 22–24AWG 硅胶线多色,眼睛线要长 | 1 套 | 眼睛舵机线要穿颈部 |
| 28 | 杜邦线或 JST 接头、热缩管 | | 1 套 | 接线 |
| 29 | 瞬间胶 | | 1 | 作者说有几个小件要粘 |
| 30 | 太阳能面板贴纸 | 光面相纸 + 作者提供的 PDF | 1 | 填补空位 |
| 31 | 涂装用品(可选) | 填补底漆、黄/白/浅灰/深灰/黑/红喷漆,黑和棕色丙烯颜料,砂纸 | 1 套 | 作者的外观做法 |

第一阶段不含摄像头:作者的网页只支持 CSI 摄像头,不支持 USB 摄像头。第二阶段会用自己的软件接 USB 摄像头。

## 表 2:第二阶段(看、听、自主决策,在表 1 基础上追加)

| # | 零件 | 规格 / 搜索关键词 | 数量 | 用途与备注 |
|---|---|---|---|---|
| 1 | AI 加速板 | Raspberry Pi AI HAT+ 2(Hailo-10H,40 TOPS INT4,板载 8GB),含排针和间隔柱 | 1 | 取代原先的 13 TOPS 版本(Hailo-8L 不支持 LLM/VLM),占同一个 PCIe 插槽,两块不能同时装。同时跑视觉模型(人脸、目标检测、姿态)和 VLM 决策(见下方软件架构)。语音识别仍在 Pi 5 的 CPU 上跑。**待验证**:① 这块板上能跑的 VLM 清单(官方发布时列的是 Qwen2.5-VL-3B)和实测速度;② VLM 与视觉检测能否同时在这块芯片上跑;③ 价格,我看到的零售价在 130–200 美元之间,各家不一致 |
| 2 | 机内小风扇 | 30mm 5V | 1 | 外壳封闭,需要在壳体开进出风口 |
| 3 | 麦克风阵列 | Seeed ReSpeaker XVF3800 4 麦 USB;空间不够就换 ReSpeaker Lite | 1 | 本地识别比云端更怕噪声,需要硬件降噪和波束成形。XVF3800 还带声源方向,可以让头转向说话的人。先量好空间,XVF3800 直径约 9cm |
| 4 | USB 摄像头模块 | UVC,广角约 100°,尺寸要能放进眼睛(⌀约 30mm 以内) | 1 | 视觉输入,装进 `eye-camera-mount` |
| 5 | 细软 USB 线 | 硅胶线,0.5–1m | 1–2 | 摄像头线走颈部,耐反复弯折 |
| 6 | 舵机独立降压模块 | 输出 6V,5A | 1 | 舵机和树莓派分电源轨,防止电流尖峰重启树莓派 |
| 7 | 电解电容 | 1000µF,25V | 2 | 舵机电源轨滤波 |
| 8 | 多区 ToF 测距 | VL53L5CX 模块 | 1 | 前方障碍 |
| 9 | ToF 测距 | VL53L1X 模块 | 2 | 朝下防跌落 |
| 10 | IMU | BNO055 或 BNO085 模块 | 1 | 检测被抬起、碰撞、航向 |
| 11 | Qwiic/STEMMA QT 线 | 100–200mm | 若干 | 传感器接树莓派 I²C |
| 12 | 大容量电池 | 3S 11.1V 5000mAh,XT60 | 1 | 续航提高到 2–3 小时。机身放不下就放进 cooler box 背包,表 1 的 2200mAh 留作备用 |
| 13 | cooler box 背包(打印) | Thingiverse thing:4160072 | 1 | 装大电池 |
| 14 | 内部电子件安装盒(打印) | Thingiverse thing:5227296 | 1 | 固定树莓派和电路板 |
| 15 | 编码器版 Pololu 37D 电机 | 同系列带编码器版本 | 2 | **必需**(原为可选)。自主决策会下达"靠近""后退""绕开"这类位移意图,没有编码器和里程计就是开环乱走。速度闭环和里程计需要改固件 |

## 第二阶段软件架构(VLM 决策,全部本地运行,不用云端模型)

目标:动作不是预先定义好的套路,而是根据看到、听到的内容由模型自主选择和生成。不需要买东西,但需要自己写下面几层。

### 分层

```
感知层(10–30Hz)     人脸/人体/姿态检测、ToF、IMU、声源方向、VAD + 语音识别(Pi 5 CPU)
   ↓ 汇总成"世界状态"文字 + 一帧画面
反射层(<50ms,不用模型)   人脸跟随、防跌落急停、被抬起/碰撞反应、巨响一惊。可随时打断下面的层
内在状态            好奇、精力、社交欲、无聊,由规则随时间和事件更新
   ↓
决策层(秒级,VLM)    输入:一帧画面 + 世界状态 + 内在状态 + 最近动作及结果
                    输出:受约束的 JSON(意图 + 带时间的动作函数序列)
   ↓
动作生成层          把函数调用渲染成平滑轨迹:最小加加速度插值、预备动作与过冲、待机微动
   ↓
安全层              关节限位、速度限幅、手臂与机身碰撞检查、履带限速 → PCA9685 / 电机
```

### 决策层怎么工作

- **模型不会训练,也不直接控制舵机。** 它只看一份"身体说明书"(系统提示词)和一组高层动作函数,写出该调用哪些函数。真实舵机角度由配置文件和安全层负责,换舵机或重新标定只改配置。
- **动作函数(控制在 5–8 个,参数用 0–1 或 -1–1 的归一化值和枚举):**

| 函数 | 作用 |
|---|---|
| `look_at(target, speed)` | 头和眼睛转向目标(人脸、声源、物体) |
| `express(valence, arousal)` | 情绪,由动作层展开为眼睛、脖子、手臂的组合 |
| `raise_arm(side, height, speed)` | 抬手臂 |
| `neck(extend, tilt)` | 脖子伸缩和倾斜 |
| `move(direction, speed, duration)` | 履带移动:forward / back / turn_left / turn_right |
| `stop()` | 立即停车 |
| `chirp(pitch, duration, contour)` | 叫声 |

- **一次输出一段带时间偏移的调用序列,** 例如 `[{t:0, fn:look_at}, {t:0.5, fn:raise_arm}, {t:1.0, fn:chirp}]`。函数调用**立即返回**,只把动作放进队列,由动作生成层按时间执行,不等动作做完。这样模型慢也不会让机器人僵住。
- **用事件触发决策,不按固定时钟:** 新人出现或离开、一句话说完、声源突变、长时间无事(无聊计时)、被抬起再放下、一段动作序列执行完。
- **决策有时效:** 模型返回时如果世界已经变化很大(比如人已经走了),丢弃这次决策并重新触发。
- **输出格式用语法约束解码(JSON schema / GBNF),** 保证一定合法,不依赖模型自觉。

### 其他约定

- **叫声:** `chirp` 默认用小型参数合成器(音高曲线、时长)生成电子音,用表 1 的 I²S 功放和喇叭播放;预录 wav 作为备选。播放叫声时暂停识别,所以不需要回声消除。
- **听的时候先停车:** 履带电机和舵机噪声会明显降低识别率,需要听人说话时先停车,这是一个明确的行为状态。
- **安全层的限位表要靠装配后实测:** MG90S 没有位置反馈,自由生成的动作更容易撞到机身或堵转。ToF 防跌落和急停优先于一切决策。
- **语音识别的语言(中文/英文)和唤醒词方案还没定,** 先选定模型再测 CPU 占用。

### 买板子之前先验证(这些我都没有验证过)

1. 在 Pi 5 + AI HAT+ 2 上实测:带一帧图像的单次 VLM 决策要多久;
2. VLM 和视觉检测能否同时在这块芯片上运行;
3. 加上语法约束后,输出 JSON 的合规率和行为是否合理;
4. 持续推理时 CPU 占用和温度(机身是封闭的);
5. 电机运转和停止两种状态下的语音识别率。

**降级方案:** 如果 VLM 太慢或理解太差,把检测结果转成文字,改用纯文本小模型(1.5B 左右,在 Pi 5 CPU 上跑)做决策。动作函数和接口不变,只换模型。

### 本阶段不做的

- **VLA:** 它只负责"动作怎么做",不决定"做什么",而且需要自己机器人的示教数据。
- **RL 和微调:** 以后可以挑有明确目标的技能(避障跟随、风格化动作)单独做,前提是先建好仿真模型。若要微调模型,注意 AI HAT+ 2 只能跑厂商编译好的模型,微调后的权重不一定能直接用。
