# Plotly ODF function for structure the ODF
import xarrayuvecs.uvecs as uvecs
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def ODF_template(res=400,xlabel='x',ylabel='y'):
    '''
    Create an circle with
    :param res: resolution of the image
    :type res: int
    :param xlabel: name of the x axis
    :type xlabel: string
    :param ylabel: name of the y axis
    :type ylabel: string
    '''

    fig=make_subplots(rows=1, cols=1)

    fig.add_shape(type="circle",
    xref='x', yref='y',
    x0=0, y0=0, x1=res, y1=res,
    line=dict(
        color="Black",
        width=5,
        )
    )
    fig.update_layout(height=600,width=700,paper_bgcolor="White")
    fig.update_layout(showlegend=False)
    #x axis
    fig.update_xaxes(visible=False)
    fig.add_trace(go.Scatter(
        x=np.array([res]),
        y=np.array([res/2]),
        mode="markers+text",
        text=xlabel,
        textposition="middle right"
    ))

    #y axis    
    fig.update_yaxes(visible=False)
    

    fig.add_trace(go.Scatter(
        x=np.array([res/2]),
        y=np.array([res]),
        mode="markers+text",
        text=ylabel,
        textposition="top center"
    ))

    fig.update_yaxes(scaleanchor = "x",scaleratio = 1)
    
    return fig

def add_orientation(proj_ori,fig=None,name=None,text=None,size=10,color='Black'):
    '''
    Add orientations on a pole figure
    :param proj_ori: projected point in the plane of projection dim=(n,2)
    :type proj_ori: np.array
    :param fig:
    :type fig: plotly.graph_objs._figure.Figure
    :param name: name of the point
    :type name: string
    :param text: text to print next to the point
    :type text: string
    :param size: marker size
    :type size: int
    :param color: marker color
    :type color: int
    '''
    if fig is None:
        res=400
        fig=ODF_template(res=res)
    else:
        res=float(fig.data[0].x)
    
    fig.add_trace(go.Scatter(
                    x=res/2+proj_ori[:,0]/(2**0.5)*res/2, 
                    y=res/2+proj_ori[:,1]/(2**0.5)*res/2,
                    mode="markers+text",
                    name=name,
                    text=text,
                    textposition="top center",
                    marker=dict(
                        color=color,
                        size=size,
                    )
                ))

    return fig

def vector2plane(xa_uvecs,xoz_plane=False):
    '''
    Project a 3D vector uvecs to the plane of the pole figure
    :param xa_uvecs: uvecs vector object
    :type xa_uvecs: uvecs
    :param xoz_plane: project in xoz plane
    :type xoz_plane: bool
    '''
    xyz_vec=xa_uvecs.uvecs.xyz()
    if xoz_plane:
        xyz_vec2=np.copy(xyz_vec)
        xyz_vec2[...,1]=xyz_vec[...,2]
        xyz_vec2[...,2]=xyz_vec[...,1]
        xyz_vec=xyz_vec2
        del xyz_vec2
        id0,id1=np.where(xyz_vec[...,2]<0)
        xyz_vec[id0,id1,:]=-xyz_vec[id0,id1,:]
        
    phiee=np.arccos(xyz_vec[...,2])
    thetaee=np.arctan2(xyz_vec[...,1],xyz_vec[...,0])
    xxv = np.multiply(2*np.sin(phiee/2),np.cos(thetaee))
    yyv = np.multiply(2*np.sin(phiee/2),np.sin(thetaee))

    proj_xy=np.dstack([xxv,yyv])

    return proj_xy


