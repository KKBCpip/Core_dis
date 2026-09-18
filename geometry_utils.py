from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_FACE, TopAbs_SOLID, TopAbs_COMPSOLID, TopAbs_COMPOUND
from OCC.Core.BRepGProp import brepgprop
from OCC.Core.GProp import GProp_GProps


class GeometryAnalyzer:
    """几何属性分析器，封装测量逻辑"""

    @staticmethod
    def measure(shape):
        """根据拓扑类型测量形状，返回 (类型, 数值, 单位)。"""
        if shape is None or shape.IsNull():
            return None

        shape_type = shape.ShapeType()
        if shape_type == TopAbs_EDGE:
            return "边长", GeometryAnalyzer.get_edge_length(shape), "mm"
        if shape_type == TopAbs_FACE:
            return "面积", GeometryAnalyzer.get_face_area(shape), "mm^2"
        if shape_type in (TopAbs_SOLID, TopAbs_COMPSOLID, TopAbs_COMPOUND):
            return "体积", GeometryAnalyzer.get_shape_volume(shape), "mm^3"
        return None

    @staticmethod
    def get_edge_length(edge_shape):
        """计算单条边(Edge)的长度"""
        props = GProp_GProps()
        brepgprop.LinearProperties(edge_shape, props)
        return props.Mass()

    @staticmethod
    def get_face_area(face_shape):
        """计算单个面的面积"""
        props = GProp_GProps()
        brepgprop.SurfaceProperties(face_shape, props)
        return props.Mass()

    @staticmethod
    def get_shape_volume(shape):
        """计算实体(Solid)的体积"""
        props = GProp_GProps()
        brepgprop.VolumeProperties(shape, props)
        return props.Mass()