from flask import Flask
import ghhops_server as hs
import rhino3dm 
import meshpath as mp

app = Flask(__name__)
hops = hs.Hops(app)

@hops.component(
    "/gridMesh",
    name = "gridMesh",
    inputs=[
        hs.HopsInteger("U","U","U"),
        hs.HopsInteger("V","V","V")
    ],
    outputs=[
        hs.HopsMesh("Mesh","M","A simple rhino3dm mesh"),

    ]
)
def gridMesh(U,V):

    #creating a simple mesh from a grid of points
    grid = []
    mesh = rhino3dm.Mesh()
    
    for i in range(U):
        for j in range(V):
            p = rhino3dm.Point3d(i,j,0)
            grid.append(p)
            mesh.Vertices.Add(p.X, p.Y, p.Z) 
            
    for i in range(len(grid)-(V)):
        if ( i % V != V -1 ):
            mesh.Faces.AddFace(i,i+1, i+V+1,i+V)

    print(mesh.Faces.Count)

    for i in range(mesh.Faces.Count):
        print(mesh.Faces[i])

    return mesh

@hops.component(
    "/shortestpath",
    name = "shortestpath",
    inputs=[
        hs.HopsMesh("Input Mesh", "M", "Mesh"),
        hs.HopsInteger("face Index 1","f1","Face index one"),
        hs.HopsInteger("face Index 2","f2","Face index two")

    ],
    outputs=[
        hs.HopsInteger("SP","SP","Shortest path nodes", hs.HopsParamAccess.LIST),
        hs.HopsMesh("M","M","Stripe")

    ]
)
def shortestPath(mesh, f1, f2):

    G = mp.SimpleGraphFromMesh(mesh)
    SP = mp.shortestPath(G, f1, f2)
    M = mesh.MeshFaceList()
    
    return M


if __name__== "__main__":
    app.run(debug=True)
