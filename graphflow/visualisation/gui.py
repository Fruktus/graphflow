from tkinter import Tk, ttk, filedialog, Button, messagebox, Entry, Label
import tkinter as tk
import re

from graphflow.simple.simple_model_utils import from_json
from graphflow.extended.extended_model_utils import from_json as extended_from_json
from graphflow.epidemic.epidemic_simulation import Simulation
from graphflow.epidemic.epidemic_runner import Parser

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

        buttonframe = ttk.Frame(frame, relief=tk.SUNKEN)
        load_button = Button(buttonframe, text='load network',
                             command=lambda: self._load_file(self.root, filetypes=(("epanet files", "*.inp"),
                                                                                   ("all files", "*.*"))))
        load_button.pack(side=tk.LEFT, padx=5, pady=5)
        calculate_button = Button(buttonframe, text='calculate',
                                  command=lambda: self._calculate_epanet(metrics=cb.get_checked_items()))
        calculate_button.pack(side=tk.LEFT, padx=5, pady=5)
        export_button = Button(buttonframe, text='export', command=lambda: self._export_data())
        export_button.pack(side=tk.LEFT, padx=5, pady=5)
        buttonframe.pack(side=tk.BOTTOM, fill=tk.X, expand=True)

        cb = self._generate_metrics_checklist(frame)
        cb.pack(side=tk.LEFT, padx=5, pady=5)

    def _add_epidemic_nb(self):
        frame = ttk.Frame(self.nb)
        self.nb.add(frame, text='Epidemic')

        buttonframe = ttk.Frame(frame, relief=tk.SUNKEN)
        load_button = Button(buttonframe, text='load network',
                             command=lambda: self._load_file(self.root, filetypes=("all files", "*.*")))
        load_button.pack(side=tk.LEFT, padx=5, pady=5)
        calculate_button = Button(buttonframe, text='calculate',
                                  command=lambda: self._calculate_epidemic(metrics=cb.get_checked_items(),
                                                                           transrate=float(transrate_box.get()),
                                                                           recrate=float(recrate_box.get()),
                                                                           tmax=float(tmax_box.get())))
        calculate_button.pack(side=tk.LEFT, padx=5, pady=5)
        export_button = Button(buttonframe, text='export', command=lambda: self._export_data())
        export_button.pack(side=tk.LEFT, padx=5, pady=5)
        animation_button = Button(buttonframe, text='animate', command=lambda: self._export_animation())
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
        path = filedialog.asksaveasfilename(title="Select file", defaultextension='.csv', filetypes=(("CSV", "*.csv"),
                                            ("all files", "*.*")))
        if path:
            export_csv(path, self.root.calculated_metrics)

    def _export_animation(self):
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

    def _calculate_epanet(self, metrics: [str] = None):
        raise NotImplementedError

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

        visualize_epidemic(my_sim.get_network(), simulation_investigation, self.root.calculated_metrics)

    def start(self):
        self.root.mainloop()
