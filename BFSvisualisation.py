import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.animation import FuncAnimation
import matplotlib.gridspec as gridspec
import random
from collections import deque
import numpy as np
import time

NUM_NODES = 15
EDGE_PROBABILITY = 0.18

fig = plt.figure(figsize=(14, 7))
fig.patch.set_facecolor("#0d1117")
gs = gridspec.GridSpec(1, 2, width_ratios=[2.2, 1], figure=fig)
gs.update(wspace=0.04)

ax      = fig.add_subplot(gs[0])
ax_code = fig.add_subplot(gs[1])

for a in (ax, ax_code):
    a.set_facecolor("#0d1117")

start_node = None
end_node   = None
G          = None
pos        = None
layers     = []
edge_layers= []
shortest_path = []
anim       = None

anim_start_time      = None
# ── Slowed down BFS phases so pseudocode is easier to follow ─────────────────
LAYER_DURATION       = 2.2   # was 0.7 — each BFS wave layer takes longer
NODE_SPRING_DURATION = 0.7
EDGE_SPRING_DURATION = 0.5
PATH_DURATION        = 1.4   # unchanged — final path anim stays the same

node_progress   = {}
edge_progress   = {}
path_progress   = 0.0
path_node_order = []
active_line     = -1
phase_timeline  = []

# ── Pseudocode ───────────────────────────────────────────────────────────────
CODE_LINES = [
    ("BFS(graph, start, goal):", False),
    ("  queue ← [start]",        True),
    ("  visited ← {start}",      True),
    ("  parent ← {start: None}", True),
    ("",                          False),
    ("  while queue not empty:",  True),
    ("    node ← queue.popleft()",True),
    ("    for neighbour in node:", True),
    ("      if neighbour not visited:", True),
    ("        visited.add(neighbour)",  True),
    ("        parent[neighbour] = node",True),
    ("        queue.append(neighbour)", True),
    ("        if neighbour == goal: break", True),
    ("",                          False),
    ("  return reconstruct_path(parent)", True),
]

PHASE_LINE = {
    "init_queue":   1,
    "init_visited": 2,
    "init_parent":  3,
    "while":        5,
    "dequeue":      6,
    "neighbour":    7,
    "mark_visited": 9,
    "mark_parent":  10,
    "enqueue":      11,
    "found":        12,
    "path":         14,
}


def ease_out_cubic(t):
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def ease_out_elastic(t):
    t = max(0.0, min(1.0, t))
    if t == 0 or t == 1:
        return t
    return (2 ** (-10 * t)) * np.sin((t * 10 - 0.75) * (2 * np.pi) / 3) + 1


def generate_graph():
    global G, pos, start_node, end_node, layers, edge_layers, shortest_path
    global node_progress, edge_progress, path_progress, path_node_order
    global anim_start_time, active_line, phase_timeline

    start_node = end_node = None
    layers = []; edge_layers = []; shortest_path = []
    node_progress = {}; edge_progress = {}
    path_progress = 0.0; path_node_order = []
    anim_start_time = None; active_line = -1; phase_timeline = []

    while True:
        G = nx.gnp_random_graph(NUM_NODES, EDGE_PROBABILITY)
        if nx.is_connected(G):
            break

    mapping = {i: chr(65 + i) for i in range(NUM_NODES)}
    G = nx.relabel_nodes(G, mapping)
    pos = nx.spring_layout(G, seed=random.randint(0, 1000))


def bfs_wave(start, goal):
    queue   = deque([start])
    visited = {start}
    parent  = {start: None}
    layers_out = []; edge_layers_out = []

    while queue:
        size = len(queue)
        current_layer = []; current_edges = []; found = False

        for _ in range(size):
            node = queue.popleft()
            for n in G.neighbors(node):
                if n not in visited:
                    visited.add(n); parent[n] = node
                    current_layer.append(n); current_edges.append((node, n))
                    if n == goal: found = True
                    else: queue.append(n)

        if current_layer:
            layers_out.append(current_layer)
            edge_layers_out.append(current_edges)
        if found:
            break

    path = []
    if goal in parent:
        cur = goal
        while cur is not None:
            path.append(cur); cur = parent[cur]
        path.reverse()

    return layers_out, edge_layers_out, path


def build_phase_timeline(total_bfs_time):
    """
    Spread pseudocode phase events evenly across each layer's longer duration
    so each highlighted line is visible for roughly equal time.
    """
    tl = []
    # Init lines shown briefly at the start
    tl.append((0.00, "init_queue"))
    tl.append((0.45, "init_visited"))
    tl.append((0.90, "init_parent"))

    for i in range(len(layers)):
        t0 = i * LAYER_DURATION
        # Spread the 6 per-layer phases evenly across LAYER_DURATION
        # so each gets ~(LAYER_DURATION / 6) ≈ 0.37 s of screen time
        step = LAYER_DURATION / 7.0
        tl.append((t0 + step * 0, "while"))
        tl.append((t0 + step * 1, "dequeue"))
        tl.append((t0 + step * 2, "neighbour"))
        tl.append((t0 + step * 3, "mark_visited"))
        tl.append((t0 + step * 4, "mark_parent"))
        tl.append((t0 + step * 5, "enqueue"))

    tl.append((total_bfs_time - 0.30, "found"))
    tl.append((total_bfs_time + 0.5,  "path"))
    tl.sort(key=lambda x: x[0])
    return tl


def lerp_color(c1, c2, t):
    t = max(0.0, min(1.0, t))
    return tuple((1 - t) * a + t * b for a, b in zip(c1, c2))


def get_node_color(node):
    unvisited = np.array([0.15, 0.22, 0.35, 1.0])
    start_c   = np.array([0.0,  0.85, 0.5,  1.0])
    end_c     = np.array([1.0,  0.25, 0.35, 1.0])
    wave_c    = np.array([0.2,  0.6,  1.0,  1.0])
    path_c    = np.array([0.4,  1.0,  0.55, 1.0])

    if path_progress > 0 and path_node_order and node in path_node_order:
        idx     = path_node_order.index(node)
        t_start = (idx / max(len(path_node_order) - 1, 1)) * 0.6
        local_t = max(0.0, (path_progress - t_start) / 0.4)
        p       = ease_out_elastic(local_t)
        base    = wave_c if node in node_progress else unvisited
        return tuple(lerp_color(base, path_c, p))

    if node == start_node: return tuple(start_c)
    if node == end_node:   return tuple(end_c)
    if node not in node_progress: return tuple(unvisited)

    p = min(node_progress[node], 1.0)
    return tuple(lerp_color(unvisited, wave_c, p))


def draw_code_panel():
    ax_code.clear()
    ax_code.set_facecolor("#0d1117")
    ax_code.axis("off")

    n      = len(CODE_LINES)
    line_h = 0.90 / n

    # Card background
    ax_code.add_patch(mpatches.FancyBboxPatch(
        (0.02, 0.01), 0.96, 0.97,
        boxstyle="round,pad=0.01",
        linewidth=1, edgecolor="#1e3050",
        facecolor="#0b1120",
        transform=ax_code.transAxes, zorder=0
    ))

    # Header
    ax_code.text(0.5, 0.975, "BFS  Pseudocode",
                 transform=ax_code.transAxes,
                 ha="center", va="top",
                 fontsize=9.5, fontweight="bold",
                 fontfamily="monospace", color="#8ab4f8")

    for i, (line_text, is_code) in enumerate(CODE_LINES):
        y          = 0.935 - i * line_h
        is_active  = (i == active_line)

        if is_active:
            # Glow highlight bar
            ax_code.add_patch(mpatches.FancyBboxPatch(
                (0.03, y - line_h * 0.48), 0.94, line_h * 0.92,
                boxstyle="round,pad=0.005",
                linewidth=0, facecolor="#162d50",
                transform=ax_code.transAxes, zorder=1
            ))
            # Accent stripe on left
            ax_code.add_patch(plt.Rectangle(
                (0.03, y - line_h * 0.48), 0.016, line_h * 0.92,
                facecolor="#4da6ff",
                transform=ax_code.transAxes, zorder=2
            ))
            color = "#e8f4ff"
        elif not is_code or not line_text:
            color = "#0b1120"
        else:
            color = "#3d5575"

        if line_text:
            ax_code.text(0.08, y, line_text,
                         transform=ax_code.transAxes,
                         ha="left", va="center",
                         fontsize=7.8, fontfamily="monospace",
                         color=color, zorder=3)


def draw_smooth(elapsed=0.0):
    ax.clear()
    ax.set_facecolor("#0d1117")
    ax.set_aspect("equal")

    all_edges  = list(G.edges())
    path_edges = []
    if path_node_order and len(path_node_order) > 1:
        path_edges = [(min(a, b), max(a, b))
                      for a, b in zip(path_node_order, path_node_order[1:])]

    edge_colors = []; edge_widths = []

    for u, v in all_edges:
        key = (min(u, v), max(u, v))

        if path_progress > 0 and key in path_edges:
            pidx    = path_edges.index(key)
            t_start = (pidx / max(len(path_edges), 1)) * 0.5
            local_t = max(0.0, (path_progress - t_start) / 0.5)
            p       = ease_out_cubic(local_t)
            r, g, b, a = lerp_color((0.15, 0.22, 0.35, 0.3), (0.4, 1.0, 0.55, 1.0), p)
            edge_colors.append((r, g, b, a)); edge_widths.append(1.0 + p * 3.5)

        elif key in edge_progress:
            p = min(edge_progress[key], 1.0)
            r, g, b, a = lerp_color((0.4, 0.5, 0.7, 0.5), (0.4, 0.75, 1.0, 1.0), p)
            edge_colors.append((r, g, b, a)); edge_widths.append(1.2 + p * 2.8)
        else:
            edge_colors.append((0.35, 0.45, 0.65, 0.55)); edge_widths.append(1.2)

    node_colors = [get_node_color(n) for n in G.nodes()]
    node_sizes  = []

    for node in G.nodes():
        if path_progress > 0 and path_node_order and node in path_node_order:
            idx     = path_node_order.index(node)
            t_start = (idx / max(len(path_node_order) - 1, 1)) * 0.6
            local_t = max(0.0, (path_progress - t_start) / 0.4)
            p       = ease_out_elastic(local_t)
            node_sizes.append(600 + p * 400)
        elif node in (start_node, end_node):
            node_sizes.append(900)
        else:
            p = min(node_progress.get(node, 0.0), 1.0)
            node_sizes.append(400 + ease_out_cubic(p) * 350)

    for (u, v), color, width in zip(all_edges, edge_colors, edge_widths):
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=[(u, v)],
                               edge_color=[color], width=width, alpha=None)

    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=node_sizes)
    nx.draw_networkx_labels(G, pos, ax=ax, font_color="white", font_size=9, font_weight="bold")

    if not start_node:
        title = "Click start node · Click end node · Press R to reset"
    elif not end_node:
        title = f"Start: {start_node}  ·  Now click the end node"
    else:
        title = f"BFS  {start_node} → {end_node}"
        if shortest_path:
            title += f"  ·  Path length: {len(shortest_path) - 1}"

    ax.set_title(title, color="#8ab4f8", fontsize=12, fontfamily="monospace", pad=12)
    ax.axis("off")

    draw_code_panel()


def animate_bfs():
    global anim, anim_start_time, node_progress, edge_progress
    global path_progress, path_node_order, active_line, phase_timeline

    node_progress   = {start_node: 1.0}
    edge_progress   = {}
    path_progress   = 0.0
    path_node_order = []
    active_line     = PHASE_LINE["init_queue"]
    anim_start_time = time.time()

    node_times = {}; edge_times = {}

    for i, (layer_nodes, layer_edges) in enumerate(zip(layers, edge_layers)):
        t0 = i * LAYER_DURATION
        for n in layer_nodes:
            node_times[n] = (t0, NODE_SPRING_DURATION)
        for e in layer_edges:
            key = (min(e[0], e[1]), max(e[0], e[1]))
            edge_times[key] = (t0, EDGE_SPRING_DURATION)

    total_bfs_time  = len(layers) * LAYER_DURATION + NODE_SPRING_DURATION
    total_anim_time = total_bfs_time + PATH_DURATION + 1.2

    if shortest_path:
        path_node_order = shortest_path

    phase_timeline = build_phase_timeline(total_bfs_time)

    def update(frame):
        global path_progress, active_line
        elapsed = time.time() - anim_start_time

        for node, (t0, dur) in node_times.items():
            node_progress[node] = ease_out_cubic(max(0.0, (elapsed - t0) / dur))
        for key, (t0, dur) in edge_times.items():
            edge_progress[key] = ease_out_cubic(max(0.0, (elapsed - t0) / dur))

        if elapsed > total_bfs_time:
            path_progress = min(1.0, (elapsed - total_bfs_time) / PATH_DURATION)

        # Walk the timeline to find the current active phase
        for t, phase in phase_timeline:
            if elapsed >= t:
                active_line = PHASE_LINE.get(phase, active_line)
            else:
                break

        draw_smooth(elapsed)

    interval_ms = 16
    n_frames    = int(total_anim_time * 1000 / interval_ms) + 30
    anim = FuncAnimation(fig, update, frames=n_frames, interval=interval_ms, repeat=False)
    plt.draw()


def get_closest_node(x, y):
    closest, min_dist = None, float("inf")
    for node, (nx_, ny_) in pos.items():
        d = (x - nx_) ** 2 + (y - ny_) ** 2
        if d < min_dist:
            min_dist = d; closest = node
    return closest


def on_click(event):
    global start_node, end_node, layers, edge_layers, shortest_path
    if event.inaxes != ax:
        return
    node = get_closest_node(event.xdata, event.ydata)
    if not start_node:
        start_node = node
        draw_smooth(); fig.canvas.draw()
    elif not end_node and node != start_node:
        end_node = node
        layers, edge_layers, shortest_path = bfs_wave(start_node, end_node)
        animate_bfs()


def on_key(event):
    global start_node, end_node, layers, edge_layers, shortest_path
    global node_progress, edge_progress, path_progress, path_node_order, anim, active_line
    if event.key.lower() == "r":
        if anim:
            anim.event_source.stop(); anim = None
        active_line = -1
        generate_graph()
        draw_smooth(); fig.canvas.draw()


generate_graph()
draw_smooth()

fig.canvas.mpl_connect("button_press_event", on_click)
fig.canvas.mpl_connect("key_press_event", on_key)

plt.tight_layout()
plt.show()