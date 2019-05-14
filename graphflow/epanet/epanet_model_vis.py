from matplotlib import animation
from matplotlib import pyplot as plt
import wntr
from graphflow.epanet.epanet_model import EpanetFlowNetwork


def get_animation(epanet_flow_network: EpanetFlowNetwork, frames: int, fps: int):
    fig = plt.figure(figsize=(12, 10), facecolor='w')
    axis = plt.gca()
    values = epanet_flow_network.results.node[epanet_flow_network.simulation_type.value]
    initial_values = values.loc[0, :]
    wntr.graphics.plot_network(epanet_flow_network.water_network_model,
                               node_attribute=initial_values,
                               ax=axis,
                               node_range=[0, 100],
                               node_size=40,
                               title="{} at 0 hours".format(epanet_flow_network.simulation_type.value))

    anim = animation.FuncAnimation(fig,
                                   __update,
                                   interval=50,
                                   frames=frames,
                                   blit=False,
                                   repeat=False,
                                   fargs=(epanet_flow_network, values, fig))

    animation_file_name = "{}.mp4".format(epanet_flow_network.simulation_type.value)
    anim.save(animation_file_name, fps=fps, extra_args=['-vcodec', 'libx264'])


def __update(frame_number, epanet_flow_network: EpanetFlowNetwork, values, fig):
    node_values = values.loc[frame_number * 3600, :]
    fig.clf()
    nodes, edges = wntr.graphics.plot_network(epanet_flow_network.water_network_model,
                                              node_attribute=node_values,
                                              ax=plt.gca(),
                                              node_range=[0, 100],
                                              node_size=40,
                                              title="{} at {} hours".format(epanet_flow_network.simulation_type.value,
                                                                            str(frame_number)))
    return nodes, edges
