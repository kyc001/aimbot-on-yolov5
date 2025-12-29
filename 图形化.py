import os
import sys

import cv2
import torch
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QImage, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)


class DetectionThread(QThread):
    """检测线程，避免界面卡顿."""

    finished = pyqtSignal(object)
    progress = pyqtSignal(int)

    def __init__(self, model, image_path, conf_threshold, iou_threshold):
        super().__init__()
        self.model = model
        self.image_path = image_path
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold

    def run(self):
        try:
            # 设置模型参数
            self.model.conf = self.conf_threshold
            self.model.iou = self.iou_threshold

            # 执行检测
            results = self.model(self.image_path)

            # 返回结果
            self.finished.emit(results)
        except Exception as e:
            self.finished.emit(str(e))


class YOLOv5Detector(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置中文字体
        font = QFont()
        font.setFamily("SimHei")
        self.setFont(font)

        # 模型相关变量
        self.model = None
        self.model_path = None  # 本地模型路径
        self.image_path = None
        self.results = None

        # 初始化UI
        self.initUI()

        # 默认不加载模型，等待用户选择
        self.statusBar().showMessage("请选择本地训练的模型文件 (.pt)")

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle("YOLOv5 图像检测工具")
        self.setGeometry(100, 100, 1200, 800)

        # 创建主布局
        main_layout = QHBoxLayout()

        # 左侧控制面板
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        control_panel.setMaximumWidth(350)

        # 模型选择
        model_group = QGroupBox("模型设置")
        model_layout = QVBoxLayout()

        self.model_path_label = QLabel("未选择模型")
        self.model_path_label.setWordWrap(True)
        self.model_path_label.setStyleSheet("color: #666; font-size: 12px;")

        self.select_model_button = QPushButton("选择模型文件")
        self.select_model_button.clicked.connect(self.select_model)

        self.load_model_button = QPushButton("加载模型")
        self.load_model_button.clicked.connect(self.load_model)
        self.load_model_button.setEnabled(False)

        model_layout.addWidget(self.model_path_label)
        model_layout.addWidget(self.select_model_button)
        model_layout.addWidget(self.load_model_button)
        model_group.setLayout(model_layout)

        # 参数调整
        params_group = QGroupBox("检测参数")
        params_layout = QVBoxLayout()

        # 置信度阈值
        conf_layout = QHBoxLayout()
        self.conf_label = QLabel("置信度阈值: 0.5")
        self.conf_slider = QSlider(Qt.Horizontal)
        self.conf_slider.setMinimum(0)
        self.conf_slider.setMaximum(100)
        self.conf_slider.setValue(50)
        self.conf_slider.valueChanged.connect(self.on_conf_changed)

        conf_layout.addWidget(self.conf_label)
        conf_layout.addWidget(self.conf_slider)

        # IoU阈值
        iou_layout = QHBoxLayout()
        self.iou_label = QLabel("IoU阈值: 0.45")
        self.iou_slider = QSlider(Qt.Horizontal)
        self.iou_slider.setMinimum(0)
        self.iou_slider.setMaximum(100)
        self.iou_slider.setValue(45)
        self.iou_slider.valueChanged.connect(self.on_iou_changed)

        iou_layout.addWidget(self.iou_label)
        iou_layout.addWidget(self.iou_slider)

        params_layout.addLayout(conf_layout)
        params_layout.addLayout(iou_layout)
        params_group.setLayout(params_layout)

        # 按钮区域
        button_layout = QHBoxLayout()

        self.load_button = QPushButton("加载图片")
        self.load_button.clicked.connect(self.load_image)
        self.load_button.setEnabled(False)  # 未加载模型前禁用

        self.detect_button = QPushButton("开始检测")
        self.detect_button.clicked.connect(self.detect)
        self.detect_button.setEnabled(False)

        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.detect_button)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)

        # 统计信息
        self.stats_group = QGroupBox("检测统计")
        self.stats_layout = QVBoxLayout()

        self.total_objects = QLabel("目标总数: 0")
        self.total_classes = QLabel("类别数: 0")
        self.avg_confidence = QLabel("平均置信度: 0%")

        self.stats_layout.addWidget(self.total_objects)
        self.stats_layout.addWidget(self.total_classes)
        self.stats_layout.addWidget(self.avg_confidence)

        self.stats_group.setLayout(self.stats_layout)
        self.stats_group.setVisible(False)

        # 添加所有控件到左侧面板
        control_layout.addWidget(model_group)
        control_layout.addWidget(params_group)
        control_layout.addLayout(button_layout)
        control_layout.addWidget(self.progress_bar)
        control_layout.addWidget(self.stats_group)
        control_layout.addStretch()

        # 右侧图像显示区域
        self.image_display = QLabel("请加载一张图片")
        self.image_display.setAlignment(Qt.AlignCenter)
        self.image_display.setMinimumSize(800, 600)
        self.image_display.setStyleSheet("border: 1px solid #cccccc;")

        # 添加到主布局
        main_layout.addWidget(control_panel)
        main_layout.addWidget(self.image_display)

        # 设置中央窗口
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def select_model(self):
        """选择本地模型文件."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择模型文件", "", "PyTorch 模型 (*.pt);;所有文件 (*)", options=options
        )

        if file_path:
            self.model_path = file_path
            self.model_path_label.setText(f"已选择模型: {os.path.basename(file_path)}")
            self.load_model_button.setEnabled(True)
            self.statusBar().showMessage(f"已选择模型: {file_path}")

    def load_model(self):
        """加载本地YOLOv5模型."""
        if not self.model_path:
            QMessageBox.warning(self, "警告", "请先选择模型文件")
            return

        try:
            self.statusBar().showMessage(f"正在加载模型: {os.path.basename(self.model_path)}...")
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(50)

            # 加载自定义模型
            self.model = torch.hub.load("ultralytics/yolov5", "custom", path=self.model_path)

            self.progress_bar.setValue(100)
            self.progress_bar.setVisible(False)
            self.statusBar().showMessage(f"模型加载成功: {os.path.basename(self.model_path)}")

            # 启用加载图片按钮
            self.load_button.setEnabled(True)

            QMessageBox.information(self, "成功", "模型加载成功！")
        except Exception as e:
            self.progress_bar.setVisible(False)
            self.statusBar().showMessage(f"模型加载失败: {e!s}")
            QMessageBox.critical(self, "错误", f"模型加载失败: {e!s}")

    def load_image(self):
        """加载图片."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择图片", "", "图像文件 (*.png *.jpg *.jpeg *.bmp *.webp);;所有文件 (*)", options=options
        )

        if file_path:
            self.image_path = file_path
            self.display_image(file_path)
            self.detect_button.setEnabled(True)
            self.stats_group.setVisible(False)

    def display_image(self, image_path):
        """显示图片."""
        pixmap = QPixmap(image_path)

        # 调整图片大小以适应显示区域
        if pixmap.width() > self.image_display.width() or pixmap.height() > self.image_display.height():
            pixmap = pixmap.scaled(
                self.image_display.width(), self.image_display.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )

        self.image_display.setPixmap(pixmap)

    def display_result(self, results):
        """显示检测结果."""
        # 获取检测结果图像
        result_img = results.render()[0]

        # 转换为Qt格式
        result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
        h, w, ch = result_img.shape
        bytes_per_line = ch * w
        q_img = QImage(result_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)

        # 调整大小以适应显示区域
        if pixmap.width() > self.image_display.width() or pixmap.height() > self.image_display.height():
            pixmap = pixmap.scaled(
                self.image_display.width(), self.image_display.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )

        self.image_display.setPixmap(pixmap)

        # 更新统计信息
        self.update_stats(results)

    def update_stats(self, results):
        """更新统计信息."""
        if results is None:
            return

        # 获取检测结果
        detections = results.pandas().xyxy[0]

        if not detections.empty:
            # 计算统计信息
            total_objects = len(detections)
            total_classes = len(detections["name"].unique())
            avg_confidence = detections["confidence"].mean() * 100

            # 更新UI
            self.total_objects.setText(f"目标总数: {total_objects}")
            self.total_classes.setText(f"类别数: {total_classes}")
            self.avg_confidence.setText(f"平均置信度: {avg_confidence:.2f}%")

            # 显示统计信息面板
            self.stats_group.setVisible(True)

    def detect(self):
        """执行检测."""
        if self.model is None or self.image_path is None:
            return

        # 获取当前参数
        conf_threshold = self.conf_slider.value() / 100.0
        iou_threshold = self.iou_slider.value() / 100.0

        # 禁用按钮并显示进度条
        self.detect_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.statusBar().showMessage("正在检测...")

        # 创建并启动检测线程
        self.detection_thread = DetectionThread(self.model, self.image_path, conf_threshold, iou_threshold)
        self.detection_thread.finished.connect(self.on_detection_finished)
        self.detection_thread.progress.connect(self.progress_bar.setValue)
        self.detection_thread.start()

    def on_detection_finished(self, results):
        """检测完成回调."""
        # 恢复UI状态
        self.detect_button.setEnabled(True)
        self.progress_bar.setVisible(False)

        if isinstance(results, str):
            # 处理错误
            self.statusBar().showMessage(f"检测失败: {results}")
            QMessageBox.critical(self, "错误", f"检测失败: {results}")
        else:
            # 保存结果
            self.results = results

            # 显示结果
            self.display_result(results)
            self.statusBar().showMessage("检测完成")

    def on_conf_changed(self, value):
        """置信度阈值变化."""
        conf_value = value / 100.0
        self.conf_label.setText(f"置信度阈值: {conf_value:.2f}")

    def on_iou_changed(self, value):
        """IoU阈值变化."""
        iou_value = value / 100.0
        self.iou_label.setText(f"IoU阈值: {iou_value:.2f}")


if __name__ == "__main__":
    # 设置PyQt5的异常处理
    def excepthook(exc_type, exc_value, traceback_obj):
        """处理未捕获的异常."""
        error_msg = f"错误类型: {exc_type.__name__}\n错误信息: {exc_value!s}"
        QMessageBox.critical(None, "应用程序错误", error_msg)
        sys.__excepthook__(exc_type, exc_value, traceback_obj)

    sys.excepthook = excepthook

    app = QApplication(sys.argv)
    window = YOLOv5Detector()
    window.show()
    sys.exit(app.exec_())
