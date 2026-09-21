import sys
import traceback
from OCC.Display.SimpleGui import init_display
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from geometry_utils import GeometryAnalyzer

class CADViewerApp:
    def __init__(self):
        try:
            # 1. 初始化显示后端
            self.display, self.start_display, self.add_menu, self.add_function = init_display()
            
            # 2. 创建测试模型
            self.test_shape = BRepPrimAPI_MakeBox(50.0, 50.0, 50.0).Shape()
            
            # 3. 将模型加入场景
            self.display.DisplayShape(self.test_shape, update=True)
            
            # 4. 注册鼠标选择回调函数
            self.display.register_select_callback(self.on_shape_click)
           
            # 5. 添加自定义菜单
            self.setup_menu()
            
            print("[System] 3D查看器已启动。请在模型上点击边以测量长度。")
            
        except Exception as e:
            # 捕获初始化过程中的所有异常并打印
            print("\n[Error] 初始化阶段发生严重错误：")
            traceback.print_exc()
            input("按回车键退出...")
            sys.exit(1)
        
    def setup_menu(self):
        """配置顶部菜单栏"""
        try:
            # 必须先添加菜单容器
            self.add_menu('测量工具')
            # 必须使用 add_function_to_menu，并且需要传入两个参数：
            # 1. 菜单名 ('测量工具')
            # 2. 绑定的功能函数 (self.measure_volume)
            self.add_function('测量工具', self.measure_volume)
        except Exception as e:
            print(f"[Error] 菜单创建失败: {e}")

    def on_shape_click(self, shape_list, *kwargs):
        """鼠标点击回调函数"""
        try:
            if not shape_list:
                return

            result = GeometryAnalyzer.measure(shape_list[0])
            if result is None:
                print("[Info] 当前选择不支持测量，请选择边、面或实体。")
                return

            measure_name, value, unit = result
            print(f"[Measure] {measure_name}: {value:.4f} {unit}")
        except Exception as e:
            print(f"[Error] 点击回调出错: {e}")

    def measure_volume(self):
        """计算并打印体积"""
        try:
            vol = GeometryAnalyzer.get_shape_volume(self.test_shape)
            print(f"[Measure] 模型总体积: {vol:.4f} mm^3")
        except Exception as e:
            traceback.print_exc()
            print(f"[Error] 计算体积出错: {e}")

    def run(self):
        """启动主事件循环"""
        try:
            print("[System] 正在启动显示主循环...")
            self.start_display()
        except Exception as e:
            print("\n[Error] 显示主循环崩溃：")
            traceback.print_exc()
            input("按回车键退出...")

if __name__ == "__main__":
    try:
        app = CADViewerApp()
        app.run()
    except Exception as e:
        print("\n[Error] 程序发生未捕获的异常：")
        traceback.print_exc()
        input("按回车键退出...")