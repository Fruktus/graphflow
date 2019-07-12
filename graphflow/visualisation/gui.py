# pylint: skip-file
from tkinter import Tk, ttk, filedialog, Button, messagebox, Entry, Label
import tkinter as tk
import re

from graphflow.epanet.epanet_model import EpanetFlowNetwork, SimulationType
from graphflow.simple.simple_model_utils import from_json
from graphflow.extended.extended_model_utils import from_json as extended_from_json
from graphflow.epidemic.epidemic_simulation import Simulation
from graphflow.epidemic.epidemic_runner import Parser
from graphflow.epanet.epanet_model_vis import draw_epicenter_plot, draw_fragility_curve_plot,\
    draw_distance_to_epicenter_plot, save_animation, draw_peak_ground_acceleration_plot,\
    draw_peak_ground_velocity_plot, draw_repair_rate_plot, draw_repair_rate_x_pipe_length,\
    draw_probability_of_minor_leak, draw_probability_of_major_leak, draw_damage_states_plot, show_plots

from graphflow.visualisation.generic_vis import visualize_holoviews, visualize_epidemic
import graphflow.analysis.metrics as mtr
from graphflow.analysis.metric_utils import calculate_metric_array
from graphflow.analysis.network_utils import export_csv


class ChecklistBox(tk.Frame):
    def __init__(self, parent, choices, **kwargs):
        tk.Frame.__init__(self, parent, **kwargs)

        self.vars = []
        bg = self.cget("background")
        for choice in choices:
            var = tk.StringVar(value=choice)
            self.vars.append(var)
            cb = tk.Checkbutton(self, var=var, text=choice,
                                onvalue=choice, offvalue="",
                                anchor="w", width=20, background=bg,
                                relief="flat", highlightthickness=0)
            cb.deselect()
            cb.pack(side="top", fill="x", anchor="w")

    def get_checked_items(self):
        values = []
        for var in self.vars:
            value = var.get()
            if value:
                values.append(value)
        return values


class Gui:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("400x550")
        self.root.title("GraphFlow")
        self.root.style = ttk.Style()
        self.root.style.theme_use("default")
        self.nb = ttk.Notebook(self.root)

        self._add_simple_nb()
        self._add_extended_nb()
        self._add_epanet_nb()
        self._add_epidemic_nb()

        self.nb.pack(expand=1, fill="both")

    def _add_simple_nb(self):
        frame = ttk.Frame(self.nb)
        self.nb.add(frame, text='Simple')

        button_frame = ttk.Frame(frame, relief=tk.SUNKEN)
        load_button = Button(button_frame, text='load network',
                             command=lambda: self._load_file(self.root, filetypes=(("json files", "*.json"),
                                                                                   ("all files", "*.*"))))
        load_button.pack(side=tk.LEFT, padx=5, pady=5)
        calculate_button = Button(button_frame, text='calculate',
                                  command=lambda: self._calculate_simple(metrics=cb.get_checked_items()))
        calculate_button.pack(side=tk.LEFT, padx=5, pady=5)
        export_button = Button(button_frame, text='export', command=lambda: self._export_data())
        export_button.pack(side=tk.LEFT, padx=5, pady=5)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, expand=True)

        cb = self._generate_metrics_checklist(frame)
        cb.pack(side=tk.LEFT, padx=5, pady=5)

    def _add_extended_nb(self):
        frame = ttk.Frame(self.nb)
        self.nb.add(frame, text='Extended')

        buttonframe = ttk.Frame(frame, relief=tk.SUNKEN)
        load_button = Button(buttonframe, text='load network',
                             command=lambda: self._load_file(self.root, filetypes=(("json files", "*.json"),
                                                                                   ("all files", "*.*"))))
        load_button.pack(side=tk.LEFT, padx=5, pady=5)
        calculate_button = Button(buttonframe, text='calculate',
                                  command=lambda: self._calculate_extended(metrics=cb.get_checked_items()))
        calculate_button.pack(side=tk.LEFT, padx=5, pady=5)
        export_button = Button(buttonframe, text='export', command=lambda: self._export_data())
        export_button.pack(side=tk.LEFT, padx=5, pady=5)
        buttonframe.pack(side=tk.BOTTOM, fill=tk.X, expand=True)

        cb = self._generate_metrics_checklist(frame)
        cb.pack(side=tk.LEFT, padx=5, pady=5)

    def _add_epanet_nb(self):
        frame = ttk.Frame(self.nb)
        self.nb.add(frame, text='Epanet')

        # buttons #
        buttonframe = ttk.Frame(frame, relief=tk.SUNKEN)
        load_button = Button(buttonframe, text='load network',
                             command=lambda: self._load_file(self.root, filetypes=(("epanet files", "*.inp"),
                                                                                   ("all files", "*.*"))))
        load_button.pack(side=tk.LEFT, padx=5, pady=5)

        export_button = Button(buttonframe, text='export', command=lambda: self._export_data())
        export_button.pack(side=tk.LEFT, padx=5, pady=5)

        buttonframe.pack(side=tk.BOTTOM, fill=tk.X, expand=True)

        # checklist #
        cb = self._generate_metrics_checklist(frame)
        cb.pack(side=tk.LEFT, padx=5, pady=5)

        # earthquake #
        eq_frame = ttk.Frame(frame, relief=tk.SUNKEN)
        Label(eq_frame, text='Earthquake').pack(padx=5, pady=5)

        epicx_box_frame = ttk.Frame(eq_frame, relief=tk.FLAT)
        epicx_box = Entry(epicx_box_frame, width=8)
        epicx_box.pack(side=tk.RIGHT, padx=5, pady=5)
        Label(epicx_box_frame, text='epicenter x').pack(side=tk.RIGHT, padx=5, pady=5)
        epicx_box_frame.pack(fill=tk.X, expand=True, padx=5, pady=5)

        epicy_box_frame = ttk.Frame(eq_frame, relief=tk.FLAT)
        epicy_box = Entry(epicy_box_frame, width=8)
        epicy_box.pack(side=tk.RIGHT, padx=5, pady=5)
        Label(epicy_box_frame, text='epicenter y').pack(side=tk.RIGHT, padx=5, pady=5)
        epicy_box_frame.pack(fill=tk.X, expand=True, padx=5, pady=5)

        magni_box_frame = ttk.Frame(eq_frame, relief=tk.FLAT)
        magni_box = Entry(magni_box_frame, width=8)
        magni_box.pack(side=tk.RIGHT, padx=5, pady=5)
        Label(magni_box_frame, text='magnitude').pack(side=tk.RIGHT, padx=5, pady=5)
        magni_box_frame.pack(fill=tk.X, expand=True, padx=5, pady=5)

        depth_box_frame = ttk.Frame(eq_frame, relief=tk.FLAT)
        depth_box = Entry(depth_box_frame, width=8)
        depth_box.pack(side=tk.RIGHT, padx=5, pady=5)
        Label(depth_box_frame, text='depth').pack(side=tk.RIGHT, padx=5, pady=5)
        depth_box_frame.pack(fill=tk.X, expand=True, padx=5, pady=5)

        viseq_button = Button(eq_frame, text='visualize',
                              command=lambda: self._visualize_epanet('earthquake'))
        viseq_button.pack(side=tk.RIGHT, padx=5, pady=5)
        calculate_button = Button(eq_frame, text='calculate',
                                  command=lambda: self._calculate_epanet('earthquake',
                                                                         epix=float(epicx_box.get()),
                                                                         epiy=(epicy_box.get()),
                                                                         magnitude=float(magni_box.get()),
                                                                         depth=float(depth_box.get()),
                                                                         metrics=cb.get_checked_items()))
        calculate_button.pack(side=tk.RIGHT, padx=5, pady=5)

        eq_frame.pack()

        # pressure #
        pr_frame = ttk.Frame(frame, relief=tk.SUNKEN)
        Label(pr_frame, text='Pressure').pack(padx=5, pady=5)

        time_box_frame = ttk.Frame(pr_frame, relief=tk.FLAT)
        time_box = Entry(time_box_frame, width=8)
        time_box.pack(side=tk.RIGHT, padx=5, pady=5)
        Label(time_box_frame, text='time').pack(side=tk.RIGHT, padx=5, pady=5)
        time_box_frame.pack(fill=tk.X, expand=True, padx=5, pady=5)

        vispr_button = Button(pr_frame, text='visualize',
                              command=lambda: self._visualize_epanet('pressure'))
        vispr_button.pack(side=tk.RIGHT, padx=5, pady=5)
        calculate_button = Button(pr_frame, text='calculate',
                                  command=lambda: self._calculate_epanet('pressure',
                                                                         time=float(time_box.get()),
                                                                         metrics=cb.get_checked_items()))
        calculate_button.pack(side=tk.RIGHT, padx=5, pady=5)

        pr_frame.pack()

        # quality #
        ql_frame = ttk.Frame(frame, relief=tk.SUNKEN)
        Label(ql_frame, text='Quality').pack(padx=5, pady=5)

        tn_box_frame = ttk.Frame(ql_frame, relief=tk.FLAT)
        tn_box = Entry(tn_box_frame, width=8)
        tn_box.pack(side=tk.RIGHT, padx=5, pady=5)
        Label(tn_box_frame, text='trace node').pack(side=tk.RIGHT, padx=5, pady=5)
        tn_box_frame.pack(fill=tk.X, expand=True, padx=5, pady=5)

        visql_button = Button(ql_frame, text='visualize',
                              command=lambda: self._visualize_epanet('quality'))
        visql_button.pack(side=tk.RIGHT, padx=5, pady=5)
        calculate_button = Button(ql_frame, text='calculate',
                                  command=lambda: self._calculate_epanet('quality', trace_node=tn_box.get(),
                                                                         metrics=cb.get_checked_items()))
        calculate_button.pack(side=tk.RIGHT, padx=5, pady=5)

        ql_frame.pack()

    def _add_epidemic_nb(self):
        frame = ttk.Frame(self.nb)
        self.nb.add(frame, text='Epidemic')

        buttonframe = ttk.Frame(frame, relief=tk.SUNKEN)
        load_button = Button(buttonframe, text='load network',
                             command=lambda: self._load_file(self.root, filetypes=(("text files", "*.txt"),
                                                                                   ("all files", "*.*"))))
        load_button.pack(side=tk.LEFT, padx=5, pady=5)
        calculate_button = Button(buttonframe, text='calculate',
                                  command=lambda: self._calculate_epidemic(metrics=cb.get_checked_items(),
                                                                           transrate=float(transrate_box.get()),
                                                                           recrate=float(recrate_box.get()),
                                                                           tmax=float(tmax_box.get())))
        calculate_button.pack(side=tk.LEFT, padx=5, pady=5)
        export_button = Button(buttonframe, text='export', command=lambda: self._export_data())
        export_button.pack(side=tk.LEFT, padx=5, pady=5)
        animation_button = Button(buttonframe, text='animate', command=lambda: self._export_epidemic_animation())
        animation_button.pack(side=tk.LEFT, padx=5, pady=5)
        buttonframe.pack(side=tk.BOTTOM, fill=tk.X, expand=True)

        cb = self._generate_metrics_checklist(frame)
        cb.pack(side=tk.LEFT, padx=5, pady=5)

        input_frame = ttk.Frame(frame, relief=tk.FLAT)

        transrate_frame = ttk.Frame(input_frame, relief=tk.SUNKEN)
        transrate_box = Entry(transrate_frame, width=8)
        transrate_box.pack(side=tk.RIGHT, padx=5, pady=5)
        transrate_box.insert(0, '2.0')
        Label(transrate_frame, text='transmission rate').pack(side=tk.RIGHT, padx=5, pady=5)
        transrate_frame.pack(fill=tk.X, expand=True)

        recrate_frame = ttk.Frame(input_frame, relief=tk.SUNKEN)
        recrate_box = Entry(recrate_frame, width=8)
        recrate_box.pack(side=tk.RIGHT, padx=5, pady=5)
        recrate_box.insert(0, '1.0')
        Label(recrate_frame, text='recovery rate').pack(side=tk.RIGHT, padx=5, pady=5)
        recrate_frame.pack(fill=tk.X, expand=True)

        tmax_frame = ttk.Frame(input_frame, relief=tk.SUNKEN)
        tmax_box = Entry(tmax_frame, width=8)
        tmax_box.pack(side=tk.RIGHT, padx=5, pady=5)
        tmax_box.insert(0, '100')
        Label(tmax_frame, text='max simulation time').pack(side=tk.RIGHT, padx=5, pady=5)
        tmax_frame.pack(fill=tk.X, expand=True)

        input_frame.pack(side=tk.RIGHT, padx=5, pady=5)

    @staticmethod
    def _load_file(root, **kwargs):
        root.filename = filedialog.askopenfilename(title="Select network file", **kwargs)

    @staticmethod
    def _generate_metrics_checklist(frame):
        # metrics = ("Author", "John", "Mohan", "James", "Ankur", "Robert")
        metrics = dir(mtr)
        regex = re.compile('__*')
        metrics = [x for x in metrics if not regex.match(x)]
        metrics.remove('get_nx_network')
        metrics.remove('nx')

        return ChecklistBox(frame, metrics, bd=1, relief="sunken", background="white")

    def _export_data(self):
        if not hasattr(self.root, 'calculated_metrics'):
            messagebox.showerror('Error', 'No data to export')
            return
        path = filedialog.asksaveasfilename(title="Select file",
                                            defaultextension='.csv', filetypes=(("CSV", "*.csv"),
                                                                                ("all files", "*.*")))
        if path:
            export_csv(path, self.root.calculated_metrics)

    def _export_epidemic_animation(self):
        if not hasattr(self.root, 'epidemic_result'):
            messagebox.showerror('Error', 'No data to export')
            return

        path = filedialog.asksaveasfilename(title="Select file", defaultextension='.mp4',
                                            filetypes=(("mp4", "*.mp4"), ("all files", "*.*")))
        if path:
            animation = self.root.epidemic_result.animate()
            animation.save(path, fps=5, extra_args=['-vcodec', 'libx264'])

    def _calculate_simple(self, metrics: [str] = None):
        if not hasattr(self.root, 'filename'):
            messagebox.showerror('Error', 'No network file selected')
            return

        with open(self.root.filename) as file:
            json_network = file.read()
            network = from_json(json_network)

            self.root.solved_network = network.calculate_network_state()

            if metrics:
                self.root.calculated_metrics = calculate_metric_array('simple', self.root.solved_network, metrics)

                visualize_holoviews(self.root.solved_network, self.root.calculated_metrics)

    def _calculate_extended(self, metrics: [str] = None):
        if not hasattr(self.root, 'filename'):
            messagebox.showerror('Error', 'No network file selected')
            return

        with open(self.root.filename) as file:
            json_network = file.read()
            network = extended_from_json(json_network)
            solved_network = network.calculate_network_state()

            if metrics:
                self.root.calculated_metrics = calculate_metric_array('simple', solved_network, metrics)

                visualize_holoviews(solved_network, self.root.calculated_metrics)

    def _calculate_epanet(self, sim_type, epix=None, epiy=None, magnitude=None, depth=None,
                          time=None, trace_node=None, metrics: [str] = None):
        if not hasattr(self.root, 'filename'):
            messagebox.showerror('Error', 'No network file selected')
            return

        if sim_type == 'earthquake':
            if not (epix and epiy and magnitude and depth):
                raise ValueError('No all arguments have been passed')
            epanet_flow_network = EpanetFlowNetwork(self.root.filename, SimulationType.EARTHQUAKE,
                                                    epicenter=(epix, epiy),
                                                    magnitude=magnitude,
                                                    depth=depth)
        elif sim_type == 'pressure':
            if not time:
                raise ValueError('No time range has been passed')
            epanet_flow_network = EpanetFlowNetwork(self.root.filename, SimulationType.PRESSURE, time=time)
        elif sim_type == 'quality':
            if not trace_node:
                raise ValueError('No  trace node has been passed')
            epanet_flow_network = EpanetFlowNetwork(self.root.filename, SimulationType.QUALITY,
                                                    trace_node=trace_node)
        else:
            raise ValueError('Bad simulation type')

        epanet_flow_network.run_simulation()
        if metrics:
            self.root.calculated_metrics = calculate_metric_array('epanet', epanet_flow_network, metrics)

        self.root.epanet_network = epanet_flow_network

    def _visualize_epanet(self, sim_type):
        if not hasattr(self.root, 'epanet_network'):
            messagebox.showerror('Error', 'No data to show')
            return

        if hasattr(self.root, 'calculated_metrics'):
            visualize_holoviews(self.root.epanet_network, self.root.calculated_metrics)

        if sim_type == 'pressure' or sim_type == 'quality':
            save_animation(self.root.epanet_network, frames=100, fps=1)
        elif sim_type == 'earthquake':
            draw_epicenter_plot(self.root.epanet_network)
            draw_fragility_curve_plot(self.root.root.epanet_network)
            draw_distance_to_epicenter_plot(self.root.epanet_network)
            draw_peak_ground_acceleration_plot(self.root.epanet_network)
            draw_peak_ground_velocity_plot(self.root.epanet_network)
            draw_repair_rate_plot(self.root.epanet_network)
            draw_repair_rate_x_pipe_length(self.root.epanet_network)
            draw_probability_of_minor_leak(self.root.epanet_network)
            draw_probability_of_major_leak(self.root.epanet_network)
            draw_damage_states_plot(self.root.epanet_network)
            show_plots()

    def _calculate_epidemic(self, metrics: [str] = None, ntype: str = 'sis', transrate: float = 2.0,
                            recrate: float = 1.0, tmax: float = 100):

        if not hasattr(self.root, 'filename'):
            messagebox.showerror('Error', 'No network file selected')
            return

        epidemic_params = Parser()
        epidemic_params.parse_input(ntype, self.root.filename, transrate, recrate, tmax)
        simulation_config = epidemic_params.get_simulation_config()

        my_sim = Simulation(simulation_config)
        simulation_investigation = my_sim.run_simulation()

        if metrics:
            self.root.calculated_metrics = calculate_metric_array('simple', my_sim.get_network(), metrics)

            visualize_epidemic(my_sim.get_network(), simulation_investigation, metrics)

    def start(self):
        self.root.mainloop()
