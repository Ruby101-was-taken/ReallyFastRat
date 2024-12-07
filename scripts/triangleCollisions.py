import pygame
from pygame.math import Vector2

def point_in_triangle(pt, v1, v2, v3):
    """Check if a point is inside a triangle using barycentric coordinates."""
    d1 = (pt[0] - v2[0]) * (v1[1] - v2[1]) - (v1[0] - v2[0]) * (pt[1] - v2[1])
    d2 = (pt[0] - v3[0]) * (v2[1] - v3[1]) - (v2[0] - v3[0]) * (pt[1] - v3[1])
    d3 = (pt[0] - v1[0]) * (v3[1] - v1[1]) - (v3[0] - v1[0]) * (pt[1] - v1[1])
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    return not (has_neg and has_pos)

def line_intersects_line(p1, p2, q1, q2):
    """Check if two lines (p1, p2) and (q1, q2) intersect."""
    def ccw(a, b, c):
        return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])
    return ccw(p1, q1, q2) != ccw(p2, q1, q2) and ccw(p1, p2, q1) != ccw(p1, p2, q2)

def rectTriangleCollision(rect, triangle_points):
    """Check for collision between a rectangle and a triangle."""
    # 1. Check if any triangle points are inside the rectangle
    for point in triangle_points:
        if rect.collidepoint(point):
            return True
    
    # 2. Check if any rectangle points are inside the triangle
    rect_points = [
        (rect.left, rect.top),
        (rect.right, rect.top),
        (rect.left, rect.bottom),
        (rect.right, rect.bottom)
    ]
    for point in rect_points:
        if point_in_triangle(point, *triangle_points):
            return True

    # 3. Check if any edges intersect
    triangle_edges = [
        (triangle_points[0], triangle_points[1]),
        (triangle_points[1], triangle_points[2]),
        (triangle_points[2], triangle_points[0])
    ]
    rect_edges = [
        (rect_points[0], rect_points[1]),
        (rect_points[1], rect_points[3]),
        (rect_points[3], rect_points[2]),
        (rect_points[2], rect_points[0])
    ]
    for tri_edge in triangle_edges:
        for rect_edge in rect_edges:
            if line_intersects_line(tri_edge[0], tri_edge[1], rect_edge[0], rect_edge[1]):
                return True

    return False