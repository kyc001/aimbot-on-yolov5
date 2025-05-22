# YOLOv5 图形化目标检测工具  
基于 PyQt5 和 YOLOv5 的图像目标检测程序，提供直观的图形化界面，支持加载本地训练模型、实时显示检测结果及参数调整。适用于快速验证模型效果、部署轻量级检测任务。


## 🚀 项目特点  
1. **图形化交互**：  
   - 支持图片导入与预览，检测结果实时渲染在原图上。  
   - 可视化调整检测参数（置信度阈值、NMS IoU 阈值）。  
2. **模型兼容性**：  
   - 无缝加载 YOLOv5 官方预训练模型及自定义训练模型（`.pt` 文件）。  
3. **多平台支持**：  
   - 基于 PyQt5 开发，支持 Windows/macOS/Linux 系统。  
4. **性能监控**：  
   - 显示检测目标总数、类别数、平均置信度等统计信息。  


## 📦 安装指南  
### **环境要求**  
- **Python**：3.8+  
- **依赖库**：  
  ```  
  PyQt5>=5.15.9       # 图形界面  
  torch>=2.0.0        # 深度学习框架（需支持 CUDA/CPU）  
  torchvision>=0.15.0 # 计算机视觉工具  
  opencv-python>=4.8.0# 图像处理  
  numpy>=1.26.0       # 数值计算  
  Pillow>=10.0.1      # 图像加载  
  ```  

### **安装步骤**  
1. **克隆项目**：  
   ```bash  
   git clone https://github.com/your-username/your-repo.git  
   cd your-repo  
   ```  
2. **创建虚拟环境（可选）**：  
   ```bash  
   python -m venv venv  
   source venv/bin/activate  # Linux/macOS  
   venv\Scripts\activate     # Windows  
   ```  
3. **安装依赖**：  
   ```bash  
   pip install -r requirements.txt  
   ```  


## 🎮 使用说明  
### **1. 启动程序**  
```bash  
python main.py  
```  

### **2. 加载自定义模型**  
- 点击 **选择模型文件**，选中训练好的 YOLOv5 模型（如 `runs/train/exp1/weights/best.pt`）。  
- 点击 **加载模型**，等待模型初始化完成。  

### **3. 检测图像**  
- 点击 **加载图片**，选择待检测的图像文件（支持 JPG/PNG/BMP 等格式）。  
- 调整 **置信度阈值**（建议 0.25-0.7）和 **IoU 阈值**（建议 0.4-0.6）。  
- 点击 **开始检测**，结果将显示在右侧窗口，统计信息同步更新。  

### **4. 结果保存**  
- 检测结果图像自动保存到程序根目录的 `runs/detect/` 文件夹。  


## 📷 界面截图  
![主界面](https://raw.githubusercontent.com/your-username/your-repo/main/screenshot.png)  
*左：参数控制面板；右：图像预览与检测结果*  


## 🛠️ 参数说明  
| 参数名称   | 功能描述                                                | 范围 | 默认值 |
| ---------- | ------------------------------------------------------- | ---- | ------ |
| 置信度阈值 | 过滤低置信度检测结果（值越高，检测越严格）              | 0-1  | 0.5    |
| IoU 阈值   | 非极大值抑制（NMS）的交并比阈值（值越高，保留的框越少） | 0-1  | 0.45   |


## 📚 模型训练建议  
1. **数据准备**：  
   使用 [Roboflow](https://roboflow.com/) 或 [LabelImg](https://github.com/tzutalin/labelImg) 标注数据集，格式为 YOLO 标签（`.txt`）。  
2. **训练流程**：  
   ```bash  
   # 使用 YOLOv5 官方仓库训练  
   git clone https://github.com/ultralytics/yolov5  
   python train.py --data coco128.yaml --weights yolov5s.pt --epochs 100  
   ```  
3. **导出模型**：  
   训练完成后，将 `runs/train/exp/weights/best.pt` 复制到本项目目录中使用。  


## 🤝 贡献与反馈  
- **问题反馈**：请在 GitHub 仓库的 [Issues](https://github.com/your-username/your-repo/issues) 中提交 Bug 或功能请求。  
- **代码贡献**：欢迎提交 Pull Request，但需先创建 Issue 说明改动内容。  
- **联系方式**：邮箱 `your-email@example.com`，或 GitHub 私信。  


## 📜 开源协议  
本项目采用 **MIT 开源协议**，允许商业使用、修改和再发布，但需保留原作者声明。具体见 [LICENSE](https://github.com/your-username/your-repo/blob/main/LICENSE) 文件。  


## 🌟 鸣谢  
- [Ultralytics YOLOv5](https://github.com/ultralytics/yolov5)：目标检测模型基础。  
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt)：图形界面框架。  
- [TorchHub](https://pytorch.org/hub/)：模型加载与推理支持。  

如果本项目对您有帮助，欢迎在 GitHub 上点亮 ⭐，感谢支持！