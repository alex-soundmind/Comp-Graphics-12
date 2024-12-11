import matplotlib.pyplot as plt
import numpy as np

class WarnockAlgorithm:
    def __init__(self, polygons):
        self.polygons = polygons[:8]

    def get_visible_segments(self, polygons):
        visible_segments = []
        intersecting_segments = []
        for i, poly in enumerate(polygons):
            for j in range(len(poly)):
                v1 = poly[j]
                v2 = poly[(j + 1) % len(poly)]
                segment = [v1, v2]
                visible_part, intersecting_part = self.get_visible_part_of_segment(segment, polygons[:i] + polygons[i + 1:])
                if visible_part:
                    visible_segments.extend(visible_part)
                if intersecting_part:
                    intersecting_segments.extend(intersecting_part)
        return visible_segments, intersecting_segments

    def get_visible_part_of_segment(self, segment, polygons):
        v1, v2 = segment
        intersections = [v1, v2]
        intersecting_parts = []

        for poly in polygons:
            for i in range(len(poly)):
                p1 = poly[i]
                p2 = poly[(i + 1) % len(poly)]
                intersection = self.calculate_intersection(v1, v2, p1, p2)
                if intersection:
                    intersections.append(intersection)

        intersections = sorted(intersections)
        visible_parts = []

        for i in range(len(intersections) - 1):
            mid_point = ((intersections[i][0] + intersections[i + 1][0]) / 2, (intersections[i][1] + intersections[i + 1][1]) / 2)
            if not self.point_in_any_polygon(mid_point, polygons):
                visible_parts.append((intersections[i], intersections[i + 1]))
            else:
                intersecting_parts.append((intersections[i], intersections[i + 1]))

        return visible_parts, intersecting_parts

    def calculate_intersection(self, v1, v2, p1, p2):
        x1, y1 = v1
        x2, y2 = v2
        x3, y3 = p1
        x4, y4 = p2

        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if denominator == 0:
            return None

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator

        if 0 <= t <= 1 and 0 <= u <= 1:
            return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))
        return None

    def point_in_any_polygon(self, point, polygons):
        x, y = point
        for poly in polygons:
            if self.point_in_polygon(x, y, poly):
                return True
        return False

    def point_in_polygon(self, x, y, poly):
        n = len(poly)
        inside = False
        p1x, p1y = poly[0]
        for i in range(n + 1):
            p2x, p2y = poly[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def render(self, ax):
        visible_segments, intersecting_segments = self.get_visible_segments(self.polygons)
        for segment in visible_segments:
            x, y = zip(*segment)
            ax.plot(x, y, color='black')
        for segment in intersecting_segments:
            x, y = zip(*segment)
            ax.plot(x, y, color='red', linestyle='--')
        for poly in self.polygons:
            x, y = zip(*poly)
            ax.plot(x, y, color='black')

def draw_axes(ax):
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)

def draw_grid(ax, scale=1):
    ax.set_xticks(np.arange(-3, 10, scale))
    ax.set_yticks(np.arange(-1, 10, scale))
    ax.grid(color='gray', linestyle='--', linewidth=0.5)

if __name__ == "__main__":
    polygons = [
        [(3, 3), (7, 3), (5, 7)],
        [(1, 5), (5, 5), (3, 9)]
    ]

    fig, ax = plt.subplots()
    ax.set_xlim(-3, 10)
    ax.set_ylim(-1, 10)

    draw_axes(ax)
    draw_grid(ax)

    warnock = WarnockAlgorithm(polygons)
    warnock.render(ax)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
