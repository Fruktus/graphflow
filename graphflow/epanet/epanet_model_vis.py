from matplotlib import animation
from matplotlib import pyplot as plt
import wntr
from graphflow.epanet.epanet_model import EpanetFlowNetwork


def save_animation(epanet_flow_network: EpanetFlowNetwork, frames: int, fps: int):
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


def draw_epicenter_plot(epanet_flow_network: EpanetFlowNetwork):
    wntr.graphics.plot_network(epanet_flow_network.water_network_model, node_size=0)
    plt.scatter(epanet_flow_network.epicenter[0], epanet_flow_network.epicenter[1], s=500, c='r', marker='*', zorder=2)


def draw_fragility_curve_plot(epanet_flow_network: EpanetFlowNetwork):
    wntr.graphics.plot_fragility_curve(epanet_flow_network.pipe_fc, xlabel='Rate of repair * pipe length')


def draw_distance_to_epicenter_plot(epanet_flow_network: EpanetFlowNetwork):
    wntr.graphics.plot_network(epanet_flow_network.water_network_model,
                               link_attribute=epanet_flow_network.distance_to_epicenter, node_size=0,
                               title='Distance to Epicenter')


def draw_peak_ground_acceleration_plot(epanet_flow_network: EpanetFlowNetwork):
    wntr.graphics.plot_network(epanet_flow_network.water_network_model, link_attribute=epanet_flow_network.pga,
                               node_size=0, link_width=1.5,
                               title='Peak ground acceleration')


def draw_peak_ground_velocity_plot(epanet_flow_network: EpanetFlowNetwork):
    wntr.graphics.plot_network(epanet_flow_network.water_network_model, link_attribute=epanet_flow_network.pgv,
                               node_size=0, link_width=1.5, title='Peak ground velocity')


def draw_repair_rate_plot(epanet_flow_network: EpanetFlowNetwork):
    wntr.graphics.plot_network(epanet_flow_network.water_network_model, link_attribute=epanet_flow_network.repair_rate,
                               node_size=0, link_width=1.5, title='Repair rate')


def draw_repair_rate_x_pipe_length(epanet_flow_network: EpanetFlowNetwork):
    wntr.graphics.plot_network(epanet_flow_network.water_network_model,
                               link_attribute=(epanet_flow_network.repair_rate * epanet_flow_network.length),
                               node_size=0, link_width=1.5, title='Repair rate*Pipe length')


def draw_probability_of_minor_leak(epanet_flow_network: EpanetFlowNetwork):
    wntr.graphics.plot_network(epanet_flow_network.water_network_model,
                               link_attribute=epanet_flow_network.pipe_pr['Minor leak'],
                               node_size=0, link_range=[0, 1], link_width=1.5, title='Probability of a minor leak')


def draw_probability_of_major_leak(epanet_flow_network: EpanetFlowNetwork):
    wntr.graphics.plot_network(epanet_flow_network.water_network_model,
                               link_attribute=epanet_flow_network.pipe_pr['Major leak'],
                               node_size=0, link_range=[0, 1], link_width=1.5, title='Probability of a major leak')


def draw_damage_states_plot(epanet_flow_network: EpanetFlowNetwork):
    gray_red_colormap = wntr.graphics.custom_colormap(3, colors=['0.75', 'blue', 'red'])
    wntr.graphics.plot_network(epanet_flow_network.water_network_model,
                               link_attribute=epanet_flow_network.pipe_damage_val,
                               node_size=0, link_width=1.5, link_cmap=gray_red_colormap,
                               title='Damage States (Blue = Minor, Red = Major)',
                               add_colorbar=False)


def show_plots():
    plt.show()
