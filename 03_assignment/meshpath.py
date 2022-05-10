import networkx as nx
import rhino3dm as rg
import meshutils as mu

def SimpleGraphFromMesh(mesh):

    # Create graph
    G=nx.Graph()

    #Get the full graph
    for i in range(mesh.Faces.Count):
        
        # Add node to graph and get its neighbours
        G.add_node(i)
        neighbours = mu.getAdjancentFaces(mesh ,i)
        
        # Add edges to graph
        for n in neighbours:
            if n > i:
                G.add_edge(i,n)

    return G


def shortestPath(g, f1, f2):

    sp = nx.shortest_path(g, f1, f2, weight = "weight")
    
    return sp

