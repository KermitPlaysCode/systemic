import graphviz

x = 'x'
y = 'y'
z = 'z'
t = 't'
u = 'u'
v = 'v'
w = 'w'

first_d = [
    (x,y),
    (x,z),
    (x,t),
    (y,t)
]
first = graphviz.Digraph(name="cluster I")
first.edges(first_d)

second_d = [
    (v,w),
    (v,u)
]
second = graphviz.Digraph(name="cluster II")
second.edges(second_d)

g = graphviz.Digraph()
g1 = g.subgraph(first)
g2 = g.subgraph(second)
g.edge(x,w)
g.render(outfile='test.png')
