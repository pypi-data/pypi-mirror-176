import os
import numpy as np

from kgcnn.data.datasets.GraphTUDataset2020 import GraphTUDataset2020


class MutagenicityDataset(GraphTUDataset2020):
    """Store and process Mutagenicity dataset."""

    def __init__(self, reload=False, verbose=1):
        """Initialize Mutagenicity dataset.

        Args:
            reload (bool): Whether to reload the data and make new dataset. Default is False.
            verbose (int): Print progress or info for processing where 0=silent. Default is 1.
        """
        # Use default base class init()
        super(MutagenicityDataset, self).__init__("Mutagenicity", reload=reload, verbose=verbose)

    def read_in_memory(self):
        r"""Load Mutagenicity Dataset into memory and already split into items with further cleaning and
        processing.
        """
        super(MutagenicityDataset, self).read_in_memory()

        node_translate = np.array([6, 8, 17, 1, 7, 9, 35, 16, 15, 53, 11, 19, 3, 20], dtype="int")
        atoms_translate = ['C', 'O', 'Cl', 'H', 'N', 'F', 'Br', 'S', 'P', 'I', 'Na', 'ksb', 'Li', 'Ca']
        z_translate = {node_translate[i]: atoms_translate[i] for i in range(len(node_translate))}

        edge_indices = self.obtain_property("edge_indices")
        node_labels = self.obtain_property("node_labels")
        edge_labels = self.obtain_property("edge_labels")
        graph_labels = self.obtain_property("graph_labels")

        nodes = [node_translate[np.array(x, dtype="int")][:, 0] for x in node_labels]
        atoms = [[atoms_translate[int(y[0])] for y in x] for x in node_labels]
        edges = [x[:, 0]+1 for x in edge_labels]
        labels = graph_labels

        # Require cleaning steps
        labels_clean = []
        nodes_clean = []
        edge_indices_clean = []
        edges_clean = []
        atoms_clean = []

        # Remove unconnected atoms. not Na Li etc.
        self.info("Checking database...")
        for i in range(len(nodes)):
            nats = nodes[i]
            cons = np.arange(len(nodes[i]))
            test_cons = np.sort(np.unique(edge_indices[i].flatten()))
            is_cons = np.zeros_like(cons, dtype="bool")
            is_cons[test_cons] = True
            is_cons[nats == 20] = True  # Allow to be unconnected
            is_cons[nats == 3] = True  # Allow to be unconnected
            is_cons[nats == 19] = True  # Allow to be unconnected
            is_cons[nats == 11] = True  # Allow to be unconnected
            if np.sum(is_cons) != len(cons):
                info_list = nodes[i][is_cons == False]
                info_list, info_cnt = np.unique(info_list, return_counts=True)
                info_list = {z_translate[info_list[j]]: info_cnt[j] for j in range(len(info_list))}
                self.info("Removing unconnected %s from molecule %s" % (info_list, i))
                nodes_clean.append(nats[is_cons])
                atoms_clean.append([atoms[i][j] for j in range(len(is_cons)) if is_cons[j] == True])
                # Need to correct edge_indices
                indices_used = cons[is_cons]
                indices_new = np.arange(len(indices_used))
                indices_old = np.zeros(len(nodes[i]), dtype="int")
                indices_old[indices_used] = indices_new
                edge_idx_new = indices_old[edge_indices[i]]
                edge_indices_clean.append(edge_idx_new)
            else:
                nodes_clean.append(nats)
                atoms_clean.append(atoms[i])
                edge_indices_clean.append(edge_indices[i])
            edges_clean.append(edges[i])
            labels_clean.append(labels[i])

        self.info("Database still has unconnected Na+, Li+, ksb+ etc.")

        # Since no attributes in graph dataset, we use labels as attributes
        self.assign_property("graph_labels", labels_clean)
        self.assign_property("edge_indices", edge_indices_clean)
        self.assign_property("node_attributes", nodes_clean)
        self.assign_property("edge_attributes", edges_clean)
        self.assign_property("node_labels", nodes_clean)
        self.assign_property("edge_labels", edges_clean)
        self.assign_property("node_symbol", atoms_clean)
        self.assign_property("node_number", nodes_clean)
        self.assign_property("graph_size", [len(x) for x in nodes_clean])

        # return labels,nodes,edge_indices,edges,atoms
        return self


# labels,nodes,edge_indices,edges,atoms = mutagenicity_graph()

# import rdkit
# import rdkit.Chem.AllChem
# import numpy as np

# def rdkit_mol_from_atoms_bonds(atoms,bonds,sani=False):
#     bond_names =  {'AROMATIC': rdkit.Chem.rdchem.BondType.AROMATIC, 'DATIVE': rdkit.Chem.rdchem.BondType.DATIVE,
#                   'DATIVEL': rdkit.Chem.rdchem.BondType.DATIVEL, 'DATIVEONE': rdkit.Chem.rdchem.BondType.DATIVEONE,
#                   'DATIVER': rdkit.Chem.rdchem.BondType.DATIVER, 'DOUBLE': rdkit.Chem.rdchem.BondType.DOUBLE,
#                   'FIVEANDAHALF': rdkit.Chem.rdchem.BondType.FIVEANDAHALF,
#                   'FOURANDAHALF': rdkit.Chem.rdchem.BondType.FOURANDAHALF,
#                   'HEXTUPLE': rdkit.Chem.rdchem.BondType.HEXTUPLE, 'HYDROGEN': rdkit.Chem.rdchem.BondType.HYDROGEN,
#                   'IONIC': rdkit.Chem.rdchem.BondType.IONIC, 'ONEANDAHALF': rdkit.Chem.rdchem.BondType.ONEANDAHALF,
#                   'OTHER': rdkit.Chem.rdchem.BondType.OTHER, 'QUADRUPLE': rdkit.Chem.rdchem.BondType.QUADRUPLE,
#                   'QUINTUPLE': rdkit.Chem.rdchem.BondType.QUINTUPLE, 'SINGLE': rdkit.Chem.rdchem.BondType.SINGLE,
#                   'THREEANDAHALF': rdkit.Chem.rdchem.BondType.THREEANDAHALF,
#                   'THREECENTER': rdkit.Chem.rdchem.BondType.THREECENTER, 'TRIPLE': rdkit.Chem.rdchem.BondType.TRIPLE,
#                   'TWOANDAHALF': rdkit.Chem.rdchem.BondType.TWOANDAHALF,
#                   'UNSPECIFIED': rdkit.Chem.rdchem.BondType.UNSPECIFIED,
#                   'ZERO': rdkit.Chem.rdchem.BondType.ZERO}
#     bond_vals = {0: rdkit.Chem.rdchem.BondType.UNSPECIFIED, 1: rdkit.Chem.rdchem.BondType.SINGLE,
#     2: rdkit.Chem.rdchem.BondType.DOUBLE, 3: rdkit.Chem.rdchem.BondType.TRIPLE,
#     4: rdkit.Chem.rdchem.BondType.QUADRUPLE, 5: rdkit.Chem.rdchem.BondType.QUINTUPLE,
#     6: rdkit.Chem.rdchem.BondType.HEXTUPLE, 7: rdkit.Chem.rdchem.BondType.ONEANDAHALF,
#     8: rdkit.Chem.rdchem.BondType.TWOANDAHALF, 9: rdkit.Chem.rdchem.BondType.THREEANDAHALF,
#     10: rdkit.Chem.rdchem.BondType.FOURANDAHALF, 11: rdkit.Chem.rdchem.BondType.FIVEANDAHALF,
#     12: rdkit.Chem.rdchem.BondType.AROMATIC, 13: rdkit.Chem.rdchem.BondType.IONIC,
#     14: rdkit.Chem.rdchem.BondType.HYDROGEN, 15: rdkit.Chem.rdchem.BondType.THREECENTER,
#     16: rdkit.Chem.rdchem.BondType.DATIVEONE, 17: rdkit.Chem.rdchem.BondType.DATIVE,
#     18: rdkit.Chem.rdchem.BondType.DATIVEL, 19: rdkit.Chem.rdchem.BondType.DATIVER,
#     20: rdkit.Chem.rdchem.BondType.OTHER, 21: rdkit.Chem.rdchem.BondType.ZERO}

#     mol = rdkit.Chem.RWMol()
#     for atm in atoms:
#         mol.AddAtom(rdkit.Chem.Atom(atm))

#     for i in range(len(bonds)):
#         if(not mol.GetBondBetweenAtoms(int(bonds[i][0]),int(bonds[i][1])) and int(bonds[i][0]) != int(bonds[i][1])):
#             if(len(bonds[i]) == 3):
#                 bi = bonds[i][2]
#                 if(isinstance(bi,str)):
#                     bond_type = bond_names[bi]
#                 elif(isinstance(bi,int)):
#                     bond_type = bond_vals[bi]
#                 else:
#                     bond_type = bi #or directly rdkit.Chem.rdchem.BondType
#                 mol.AddBond(int(bonds[i][0]), int(bonds[i][1]), bond_type)
#             else:
#                 mol.AddBond(int(bonds[i][0]), int(bonds[i][1]))

#     mol = mol.GetMol()

#     if(sani == True):
#         rdkit.Chem.SanitizeMol(mol)

#     return mol

# mol_list = []
# for rd_idx in range(len(nodes)):
#     bonds = np.concatenate([edge_indices[rd_idx],np.expand_dims(edges[rd_idx],axis=-1)],axis=-1).tolist()
#     mol = rdkit_mol_from_atoms_bonds(atoms[rd_idx],bonds)
#     mol_list.append(mol)

# test = MutagenicityDataset()