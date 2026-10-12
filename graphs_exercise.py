def build_adjacency_list(edges, directed=False):
    graph = {}
    for u, v in edges:
        graph.setdefault(u, [])
        graph.setdefault(v, [])
        graph[u].append(v)
        if not directed:
            graph[v].append(u)
    return graph


def degrees(graph):
    return {v: len(neighbours) for v, neighbours in graph.items()}

def in_out_degree(graph):
    out_degree = {v: len(neighbours) for v, neighbours in graph.items()}
    in_degree = {v: 0 for v in graph}
    for neighbours in graph.values():
        for w in neighbours:
            in_degree[w] = in_degree.get(w, 0) + 1

    for v in in_degree:
        out_degree.setdefault(v, 0)
    return in_degree, out_degree


# ---------------- Task 3 ----------------

def dfs(graph, start):
    """Vertices reachable from start, in order of first visit.
    Unvisited neighbours are visited in sorted (alphabetical) order."""
    visited = set()
    order = []
    stack = [start]
    while stack:
        v = stack.pop()
        if v in visited:
            continue
        visited.add(v)
        order.append(v)
        # push in reverse order so the smallest neighbour is popped first
        for w in sorted(graph.get(v, []), reverse=True):
            if w not in visited:
                stack.append(w)
    return order


def connected_components(graph):
    components = []
    seen = set()
    for v in sorted(graph):
        if v not in seen:
            comp = set(dfs(graph, v))
            components.append(comp)
            seen |= comp
    return components


def is_weakly_connected(graph):
    # undirected "shadow": for every edge u -> v add both directions
    shadow = {v: [] for v in graph}
    for u, neighbours in graph.items():
        for v in neighbours:
            shadow.setdefault(v, [])
            shadow[u].append(v)
            shadow[v].append(u)
    return len(connected_components(shadow)) == 1


# ---------------- Task 4 ----------------

def eulerian_type(graph, directed=False):
    """Returns "circuit", "path" or "none"."""
    if not directed:
        # --- undirected branch ---
        deg = degrees(graph)
        # connectivity: only vertices that have edges matter
        with_edges = {v: nb for v, nb in graph.items() if nb}
        if len(connected_components(with_edges)) > 1:
            return "none"
        odd = sum(1 for d_ in deg.values() if d_ % 2 == 1)
        if odd == 0:
            return "circuit"
        if odd == 2:
            return "path"
        return "none"

    # --- directed branch ---
    in_deg, out_deg = in_out_degree(graph)
    # weak connectivity: only vertices that have edges matter
    with_edges = {v: nb for v, nb in graph.items() if nb or in_deg[v] > 0}
    if with_edges and not is_weakly_connected(with_edges):
        return "none"
    excess = [out_deg[v] - in_deg[v] for v in graph]
    if any(e not in (-1, 0, 1) for e in excess):
        return "none"
    plus = excess.count(1)
    minus = excess.count(-1)
    if plus == 0 and minus == 0:
        return "circuit"
    if plus == 1 and minus == 1:
        return "path"
    return "none"


# ---------------- Tests: Task 1 ----------------

edges = [("P1", "P2"), ("P1", "P3"), ("P2", "P3"), ("P3", "P4"), ("P4", "P5")]
g = build_adjacency_list(edges)
print("Adjacency list:", g)
print("Degrees:", degrees(g))
assert sum(degrees(g).values()) == 2 * len(edges)

d = build_adjacency_list(edges, directed=True)
print("_________________________________")
print("Directed adjacency list.:", d)
indeg, outdeg = in_out_degree(d)
print("Incoming edges: ", indeg)
print("Outcoming edges:", outdeg)
assert sum(indeg.values()) == sum(outdeg.values()) == len(edges)

# ---------------- Tests: Task 3 (graph G1 from the handout) ----------------

print("_________________________________")
print("Task 3")

V1 = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
E1 = [("A", "D"), ("A", "I"), ("B", "D"), ("B", "F"), ("B", "G"),
      ("B", "I"), ("C", "E"), ("C", "H"), ("C", "J"), ("C", "K"),
      ("D", "F"), ("D", "G"), ("E", "J"), ("H", "J"), ("J", "K")]
G1 = build_adjacency_list(E1)

print("DFS from A:", dfs(G1, "A"))
print("DFS from C:", dfs(G1, "C"))

comps = connected_components(G1)
print("Components:", comps)

assert set().union(*comps) == set(G1) == set(V1)
assert sum(len(c) for c in comps) == len(G1)
assert all(a.isdisjoint(b) for i, a in enumerate(comps) for b in comps[i + 1:])

d1 = build_adjacency_list([("P1", "P2"), ("P3", "P2")], directed=True)
d2 = build_adjacency_list([("P1", "P2"), ("P3", "P4")], directed=True)
print("d1 weakly connected:", is_weakly_connected(d1))
print("d2 weakly connected:", is_weakly_connected(d2))

# ---------------- Tests: Task 3 (graph G2) ----------------

print("_________________________________")
print("Task 3, graph G2")

E2 = [("P", "Q"), ("Q", "R"), ("R", "P"), ("R", "S"), ("T", "S")]
G2 = build_adjacency_list(E2, directed=True)

print("G2 adjacency list:", G2)
print("DFS from P:", dfs(G2, "P"))
print("DFS from S:", dfs(G2, "S"))
print("DFS from T:", dfs(G2, "T"))
print("G2 weakly connected:", is_weakly_connected(G2))
# NOTE: connected_components is NOT meaningful for directed graphs,
# use is_weakly_connected for them.

# ---------------- Tests: Task 4 (graphs G1, G3, G4, G5A G5B, Konigsberg) ----------------

print("_________________________________")
print("Task 4")

E3 = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"),
      ("D", "E"), ("E", "F"), ("F", "G"), ("G", "D")]
E4 = [e for e in E3 if e != ("F", "G")]                 # G3 without {F, G}
E5a = [("1", "2"), ("2", "3"), ("3", "1"), ("1", "4"), ("4", "1")]
E5b = [e for e in E5a if e != ("4", "1")]               # G5a without (4, 1)
EK = [("A", "B"), ("A", "B"), ("A", "C"), ("A", "C"),
      ("A", "D"), ("B", "D"), ("C", "D")]

# (name, edges, directed)
cases = [
    ("G1",         E1,  False),
    ("G3",         E3,  False),
    ("G4",         E4,  False),
    ("G5a",        E5a, True),
    ("G5b",        E5b, True),
    ("Konigsberg", EK,  False),
]


results = {}
for name, es, directed in cases:
    graph = build_adjacency_list(es, directed)
    results[name] = eulerian_type(graph, directed)
    print(f"{name:11s} -> {results[name]}")

# Self-check 1
for name, es, directed in cases:
    if results[name] != "circuit":
        continue
    after = []
    for i in range(len(es)):
        rest = es[:i] + es[i + 1:]
        res = eulerian_type(build_adjacency_list(rest, directed), directed)
        assert res != "circuit"
        after.append(res)
    print(f"Self-check 1, {name}: removed each of {len(es)} edges ->", sorted(set(after)))

# Self-check 2"
for name, es, directed in cases:
    graph = build_adjacency_list(es, directed)
    if not directed:
        odd = sum(x % 2 for x in degrees(graph).values())
        if odd not in (0, 2):
            assert results[name] == "none"
        print(f"Self-check 2, {name}: odd vertices = {odd}")
    else:
        i_, o_ = in_out_degree(graph)
        exc = {v: o_[v] - i_[v] for v in graph}
        if any(e not in (-1, 0, 1) for e in exc.values()):
            assert results[name] == "none"
        print(f"Self-check 2, {name}: excess = {exc}")

# Self-check 3
assert all(x % 2 == 0 for x in degrees(G1).values())
assert eulerian_type(G1) == "none"
print("Self-check 3: G1 all degrees even, but verdict is", eulerian_type(G1))

# Self-check 4
for name, es, directed in cases:
    if directed and results[name] == "circuit":
        rev = [(v, u) for u, v in es]
        res = eulerian_type(build_adjacency_list(rev, True), True)
        assert res == "circuit"
        print(f"Self-check 4, {name} reversed ->", res)


