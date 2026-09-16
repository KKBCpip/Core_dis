# geometry_utils.py

from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps


class GeometryAnalyzer:
    """几何属性分析器，封装测量逻辑"""

    @staticmethod
    def get_edge_length(edge_shape):
        """计算单条边(Edge)的长度"""
        try:
            props = GProp_GProps()
            brepgprop.LinearProperties(edge_shape, props)
            return props.Mass()
        except Exception as e:
            print(f"计算边长出错: {e}")
            return 0.0

    @staticmethod
    def get_shape_volume(shape):
        """计算实体(Solid)的体积"""
        props = GProp_GProps()
        # 注意：这里假设传入的是 TopoDS_Solid 或者是 BRep_Builder 合并后的 Shape
        brepgprop.VolumeProperties(shape, props)
        volume = props.Mass()
        return volume