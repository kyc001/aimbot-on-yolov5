# YOLOv5 图形化目标检测工具

基于 PyQt5 和 YOLOv5 的图像目标检测程序，提供直观的图形化界面，支持加载本地训练模型、实时显示检测结果及参数调整。适用于快速验证模型效果、目标检测任务（如人脸识别、物体检测等）。

## 🚀 项目特点

1. **图形化交互**：
   - 支持图片导入与预览，检测结果实时渲染在原图上
   - 可视化调整检测参数（置信度阈值、NMS IoU 阈值）

2. **模型兼容性**：
   - 无缝加载 YOLOv5 官方预训练模型及自定义训练模型（`.pt` 文件）

3. **多平台支持**：
   - 基于 PyQt5 开发，支持 Windows/macOS/Linux 系统

4. **性能监控**：
   - 显示检测目标总数、类别数、平均置信度等统计信息

## 📦 安装指南

### 环境要求

- **Python**：3.8+
- **推荐使用 micromamba 管理环境**

### 安装步骤

1. **克隆项目**：
   ```bash
   git clone https://github.com/kyc001/aimbot-on-yolov5.git
   cd aimbot-on-yolov5
   ```

2. **创建并激活环境**：
   ```bash
   # 使用 micromamba（推荐）
   micromamba create -n yolo python=3.11
   micromamba activate yolo
   
   # 或使用 conda
   conda create -n yolo python=3.11
   conda activate yolo
   ```

3. **安装依赖**：
   ```bash
   pip install -r requirements.txt
   
   # GUI 工具需要额外安装 PyQt5
   pip install PyQt5>=5.15.9
   ```

## 🎮 使用说明

### 方式一：图形化界面（推荐）

```bash
python 图形化.py
```

**操作步骤**：
1. 点击 **选择模型文件**，选中训练好的模型（如 `runs/train/exp1/weights/best.pt`）
2. 点击 **加载模型**，等待模型初始化完成
3. 点击 **加载图片**，选择待检测的图像文件
4. 调整 **置信度阈值** 和 **IoU 阈值**
5. 点击 **开始检测**，查看检测结果

### 方式二：命令行检测

```bash
# 使用预训练模型检测
python detect.py --weights yolov5s.pt --source data/images/bus.jpg

# 使用自定义训练模型检测
python detect.py --weights runs/train/exp1/weights/best.pt --source your_image.jpg

# 指定输出目录
python detect.py --weights yolov5s.pt --source data/images/ --project runs/detect --name exp1
```

### 方式三：训练自定义模型

```bash
# 使用 COCO128 数据集训练
python train.py --data coco128.yaml --weights yolov5s.pt --batch-size 16 --epochs 50

# 训练完成后模型保存在 runs/train/exp/weights/
```

## 🛠️ 参数说明

| 参数名称   | 功能描述                                                | 范围 | 默认值 |
| ---------- | ------------------------------------------------------- | ---- | ------ |
| 置信度阈值 | 过滤低置信度检测结果（值越高，检测越严格）              | 0-1  | 0.5    |
| IoU 阈值   | 非极大值抑制（NMS）的交并比阈值（值越高，保留的框越少） | 0-1  | 0.45   |

## ⚠️ 注意事项

1. **模型文件**：
   - 项目已包含预训练模型 `yolov5s.pt`
   - 自定义训练模型位于 `runs/train/exp1/weights/best.pt`

2. **运行环境**：
   - 推荐使用 GPU 加速推理（需安装 CUDA 版本的 PyTorch）
   - CPU 模式下可正常运行，但速度较慢

3. **中文显示**：
   - GUI 界面使用 SimHei 字体，确保系统已安装该字体
   - Linux 系统可能需要手动安装：`apt install fonts-wqy-zenhei`

4. **文件路径**：
   - 中文文件名在某些系统上可能导致问题，建议使用英文路径

## 📚 项目结构

```
aimbot/
├── 图形化.py          # GUI 检测工具
├── detect.py          # 命令行检测脚本
├── train.py           # 模型训练脚本
├── val.py             # 模型验证脚本
├── export.py          # 模型导出脚本
├── requirements.txt   # 依赖列表
├── yolov5s.pt         # 预训练模型
├── data/              # 数据集配置
├── models/            # 模型定义
├── runs/              # 训练/检测结果
│   ├── train/exp1/    # 训练结果（含模型权重）
│   └── detect/        # 检测结果输出
└── utils/             # 工具函数
```

## 🤝 贡献与反馈

- **问题反馈**：请在 GitHub 仓库的 [Issues](https://github.com/kyc001/aimbot-on-yolov5/issues) 中提交
- **代码贡献**：欢迎提交 Pull Request

## 📜 开源协议

本项目采用 **AGPL-3.0** 开源协议，详见 [LICENSE](LICENSE) 文件。

## 🌟 鸣谢

- [Ultralytics YOLOv5](https://github.com/ultralytics/yolov5)：目标检测模型基础
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt)：图形界面框架
- [PyTorch](https://pytorch.org/)：深度学习框架