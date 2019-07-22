# pylint: skip-file
"""Provides graphical interface for module"""
from tkinter import Tk, ttk, filedialog, Button, messagebox, Entry, Label
import tkinter as tk
import re

from graphflow.analysis.metric_utils import metric_list
from graphflow.models.epanet.epanet_model import SimulationType
from graphflow.models.epanet.epanet_network import EpanetNetwork
from graphflow.models.epidemic.epidemic_network import EpidemicNetwork
from graphflow.models.extended.extended_network import ExtendedNetwork

from graphflow.models.simple.simple_network import SimpleNetwork

import graphflow.analysis.metrics as mtr


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
        visualize_button = Button(button_frame, text='visualize', command=lambda: self._visualize_data())
        visualize_button.pack(side=tk.LEFT, padx=5, pady=5)
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
        visualize_button = Button(buttonframe, text='visualize', command=lambda: self._visualize_data())
        visualize_button.pack(side=tk.LEFT, padx=5, pady=5)

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
        visualize_button = Button(buttonframe, text='visualize', command=lambda: self._visualize_data())
        visualize_button.pack(side=tk.LEFT, padx=5, pady=5)

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
                              command=lambda: self._visualize_data())
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
                              command=lambda: self._visualize_data())
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
                              command=lambda: self._visualize_data())
        visql_button.pack(side=tk.RIGHT, padx=5, pady=5)
        calculate_button = Button(ql_frame, text='calculate',
                                  command=lambda: self._calculate_epanet('quality', trace_node=tn_box.get(),
                                                                         metrics=cb.get_checked_items()))
        calculate_button.pack(side=tk.RIGHT, padx=5, pady=5)

        ql_frame.pack()

    def _add_epidemic_nb(self):
        frame = ttk.Frame(self.nb)
        self.nb.add(frame, text='Epidemic')

        types = {0: 'sir', 1: 'sis'}

        buttonframe = ttk.Frame(frame, relief=tk.SUNKEN)
        load_button = Button(buttonframe, text='load network',
                             command=lambda: self._load_file(self.root, filetypes=(("gml files", "*.gml"),
                                                                                   ("all files", "*.*"))))
        load_button.pack(side=tk.LEFT, padx=5, pady=5)
        calculate_button = Button(buttonframe, text='calculate',
                                  command=lambda: self._calculate_epidemic(ntype=types[type_box.curselection()[0]],
                                                                           metrics=cb.get_checked_items(),
                                                                           transrate=float(transrate_box.get()),
                                                                           recrate=float(recrate_box.get()),
                                                                           tmax=float(tmax_box.get())))
        calculate_button.pack(side=tk.LEFT, padx=5, pady=5)
        export_button = Button(buttonframe, text='export', command=lambda: self._export_data())
        export_button.pack(side=tk.LEFT, padx=5, pady=5)
        animation_button = Button(buttonframe, text='animate', command=lambda: self._export_epidemic_animation())
        animation_button.pack(side=tk.LEFT, padx=5, pady=5)
        visualize_button = Button(buttonframe, text='visualize', command=lambda: self._visualize_data())
        visualize_button.pack(side=tk.LEFT, padx=5, pady=5)
        buttonframe.pack(side=tk.BOTTOM, fill=tk.X, expand=True)

        cb = self._generate_metrics_checklist(frame, epidemic=True)
        cb.pack(side=tk.LEFT, padx=5, pady=5)

        input_frame = ttk.Frame(frame, relief=tk.FLAT)

        type_frame = ttk.Frame(input_frame, relief=tk.SUNKEN)
        type_box = tk.Listbox(type_frame, width=6, height=2)
        type_box.pack(fill=tk.X, expand=True, side=tk.RIGHT, padx=5, pady=5)
        Label(type_frame, text='network type').pack(side=tk.RIGHT, padx=5, pady=5)
        type_frame.pack(fill=tk.X, expand=True)

        type_box.insert(tk.END, 'sir')
        type_box.insert(tk.END, 'sis')
        type_box.select_set(0)

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
        tmax_box.insert(0, '2')
        Label(tmax_frame, text='max simulation time').pack(side=tk.RIGHT, padx=5, pady=5)
        tmax_frame.pack(fill=tk.X, expand=True)

        input_frame.pack(side=tk.RIGHT, padx=5, pady=5)

    @staticmethod
    def _load_file(root, **kwargs):
        root.filename = filedialog.askopenfilename(title="Select network file", **kwargs)

    @staticmethod
    def _generate_metrics_checklist(frame, epidemic=False):
        metrics = metric_list()

        if epidemic:
            metrics += metric_list(model='general')

        return ChecklistBox(frame, metrics, bd=1, relief="sunken", background="white")

    def _export_data(self):
        if not hasattr(self.root, 'calculated_network'):
            messagebox.showerror('Error', 'No data to export')
            return
        path = filedialog.asksaveasfilename(title="Select file",
                                            defaultextension='.csv', filetypes=(("CSV", "*.csv"),
                                                                                ("all files", "*.*")))
        if path:
            self.root.calculated_network.export(path)

    def _visualize_data(self):
        if not hasattr(self.root, 'calculated_network'):
            messagebox.showerror('Error', 'No data to export')
            return

        self.root.calculated_network.visualize()

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

        self.root.calculated_network = SimpleNetwork(self.root.filename, metrics)

        self.root.calculated_network.calculate()

    def _calculate_extended(self, metrics: [str] = None):
        if not hasattr(self.root, 'filename'):
            messagebox.showerror('Error', 'No network file selected')
            return

        self.root.calculated_network = ExtendedNetwork(self.root.filename, metrics)

        self.root.calculated_network.calculate()

    def _calculate_epanet(self, sim_type, epix=None, epiy=None, magnitude=None, depth=None,
                          time=None, trace_node=None, metrics: [str] = None):
        if not hasattr(self.root, 'filename'):
            messagebox.showerror('Error', 'No network file selected')
            return

        self.root.calculated_network = None

        if sim_type == 'earthquake':
            if sim_type == 'earthquake':
                if not (epix and epiy and magnitude and depth):
                    raise ValueError('No all arguments have been passed')
                self.root.calculated_network = EpanetNetwork(self.root.filename, metrics, SimulationType.EARTHQUAKE,
                                                             epicenter=(epix, epiy),
                                                             magnitude=magnitude,
                                                             depth=depth)

        elif sim_type == 'pressure':
            if not time:
                raise ValueError('No time range has been passed')
            self.root.calculated_network = EpanetNetwork(self.root.filename, metrics, SimulationType.PRESSURE,
                                                         time=time)

        elif sim_type == 'quality':
            if not trace_node:
                raise ValueError('No  trace node has been passed')
            self.root.calculated_network = EpanetNetwork(self.root.filename, metrics, SimulationType.QUALITY,
                                                         trace_node=trace_node)

        else:
            raise ValueError('Bad simulation type')

        self.root.calculated_network.calculate()

    def _calculate_epidemic(self, metrics: [str] = None, ntype: str = 'sis', transrate: float = 2.0,
                            recrate: float = 1.0, tmax: float = 100):
        if not hasattr(self.root, 'filename'):
            messagebox.showerror('Error', 'No network file selected')
            return

        self.root.calculated_network = EpidemicNetwork(self.root.filename, metrics,
                                                       ntype, transrate, recrate, tmax)

        self.root.calculated_network.calculate()

    def start(self):
        self.root.mainloop()
