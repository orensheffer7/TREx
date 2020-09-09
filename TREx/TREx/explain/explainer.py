import os
import time
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

colors = 'cgmybrk'


class ExplainEngine:

    def __init__(self, env, dataset):
        self.env = env
        self.ds = dataset
        self.g = nx.Graph()

    def build_constraints_graphs(self):
        tic = time.clock()
        for attr in self.ds.attr_to_idx:
            self.g.add_node(attr, color="skyblue", n_type="attr")

        for constraint_index in range(len(self.ds.constraints)):
            dc_name = "_".join(["dc", str(constraint_index)])
            self.g.add_node(dc_name, color="skyblue", n_type="dc")
            constraint = self.ds.constraints[constraint_index]
            for attr in constraint.components:
                self.g.add_edge(attr, dc_name)

        toc = time.clock()
        return toc - tic

    def plot_constraints_graphs(self):
        plt.figure(figsize=(20, 10))
        pos = nx.spring_layout(self.g, k=2. / len(self.g.nodes) ** 0.5)
        # nodes
        nx.draw_networkx_nodes(self.g, pos,
                               nodelist=[attr for attr in self.ds.attr_to_idx],
                               node_color='skyblue',
                               node_size=2000,
                               alpha=0.8)
        nx.draw_networkx_nodes(self.g, pos,
                               nodelist=["_".join(["dc", str(constraint_index)]) for constraint_index in
                                         range(len(self.ds.constraints))],
                               node_color='gray',
                               node_size=2000,
                               alpha=0.8)
        # edges
        nx.draw_networkx_edges(self.g, pos, width=3.0, alpha=0.8)
        nx.draw_networkx_labels(self.g, pos, font_size=12)
        plt.axis('off')
        plt.plot()

    def plot_explanation(self, row):
        g = row['graph']
        tid = row['_tid_']
        col = row['col']

        plt.figure(figsize=(20, 10))
        pos = nx.spring_layout(g, k=2. / len(g.nodes) ** 0.5)
        # nodes
        nx.draw_networkx_nodes(g, pos,
                               nodelist=[tid],
                               node_color='red',
                               node_size=2000,
                               alpha=0.8)
        nx.draw_networkx_nodes(g, pos,
                               nodelist=[x for x in g.nodes if x != tid],
                               node_color='blue',
                               node_size=2000,
                               alpha=0.8)
        # edges
        nx.draw_networkx_edges(g, pos, width=3.0, alpha=0.8)
        dcs = {e[2]['dc'] for e in g.edges.data()}
        for i, dc in enumerate(dcs):
            nx.draw_networkx_edges(g, pos,
                                   edgelist=[(e[0], e[1]) for e in g.edges.data() if e[2]['dc'] == dc],
                                   width=6, alpha=0.5, edge_color=colors[i % len(colors)])

        nx.draw_networkx_labels(g, pos, font_size=16)
        labels = dict((n, d['values']) for n, d in g.nodes(data=True))
        nx.draw_networkx_labels(g, pos, labels, font_size=12)

        plt.title(col + ': ' + row['raw_value'] + '-->' + row['repaired_value'], fontsize=18)
        plt.axis('off')
        plt.savefig(os.sep.join(['explanations', str(tid) + '_' + col + '.png']))
        plt.close('all')

    def explain_repairs(self, detectors):
        tic = time.clock()
        raw_data = self.ds.raw_data.df
        repaired_data = self.ds.repaired_data.df

        # TODO Generalise
        conflicts = detectors[1].get_conflicts()

        explainations = []
        for raw_row, repaired_row in zip(raw_data.iterrows(), repaired_data.iterrows()):
            raw_row = raw_row[1]
            repaired_row = repaired_row[1]
            tid = raw_row['_tid_']
            changes = raw_row != repaired_row
            for item, value in changes.iteritems():
                if value:
                    relevant_conflicts = conflicts[conflicts['_tid_'] == tid]
                    g = nx.Graph()
                    g.add_node(tid)
                    tid_values = {}
                    for dc_index in range(len(self.ds.constraints)):
                        dc = self.ds.constraints[dc_index]
                        if item in dc.components:
                            conflicting_tuples = relevant_conflicts[relevant_conflicts['dc'] == dc_index]['_tid2_']
                            if conflicting_tuples.shape[0] > 0:
                                for tuple in conflicting_tuples.values[0]:
                                    g.add_node(tuple, values={attr: raw_data[raw_data['_tid_'] == tuple][attr].values[0]
                                                              for attr in dc.components})
                                    g.add_edge(tid, tuple, dc=dc_index)
                                for attr in dc.components:
                                    tid_values[attr] = raw_data[raw_data['_tid_'] == tid][attr].values[0]

                    nx.set_node_attributes(g, {tid: tid_values}, 'values')
                    explainations.append({'_tid_': tid,
                                          'col': item,
                                          'raw_value': raw_row[item],
                                          'repaired_value': repaired_row[item],
                                          'graph': g
                                          })
        toc = time.clock()
        explain_time = toc - tic
        return explainations, explain_time
