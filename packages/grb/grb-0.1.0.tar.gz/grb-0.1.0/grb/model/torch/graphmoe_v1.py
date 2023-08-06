"""Torch module for GCN."""
import torch
import torch.nn as nn
import torch.nn.functional as F

from .gcn import GCNConv
from .gin import GINConv
from .mlp import MLPLayer
from .tagcn import TAGConv


class GSMOE(nn.Module):
    def __init__(self, in_features, out_features, hidden_features, k_max, activation=F.leaky_relu, dropout=True):
        super(GSMOE, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        if type(hidden_features) is int:
            hidden_features = [hidden_features]

        self.expert_layers = nn.ModuleList()
        self.gate_layers = nn.ModuleList()
        self.expert_layers.append(
            GSMOEConv(in_features, hidden_features[0], k_max, activation=activation, dropout=dropout))
        self.n_expert = len(self.expert_layers[0].layers)
        self.gate_layers.append(nn.Linear(in_features, self.n_expert))
        for i in range(len(hidden_features) - 1):
            self.expert_layers.append(
                GSMOEConv(hidden_features[i], hidden_features[i + 1], k_max, activation=activation, dropout=dropout))
            self.gate_layers.append(nn.Linear(hidden_features[i], self.n_expert))
        self.expert_layers.append(GSMOEConv(hidden_features[-1], out_features, k_max))
        self.gate_layers.append(nn.Linear(hidden_features[-1], self.n_expert))

    @property
    def model_type(self):
        """Indicate type of implementation."""
        return "torch"

    def forward(self, x, adj, dropout=0.0):
        for i in range(len(self.expert_layers)):
            g = F.softmax(self.gate_layers[i](x), dim=1)
            x = self.expert_layers[i](x, adj, g, dropout)

        return x

    def predict_gate(self, x, adj, g, dropout=0.0):
        preds_gate = []
        for i in range(len(self.expert_layers)):
            g = F.softmax(self.gate_layers[i](x), dim=1)
            preds_gate.append(g)
            x = self.expert_layers[i](x, adj, g, dropout)

        return preds_gate


class GATE(nn.Module):
    def __init__(self, in_features, out_features):
        super(GATE, self).__init__()
        self.linear = nn.Linear(in_features, out_features)

    def forward(self, x, adj):
        x = torch.spmm(adj, x)
        g = self.linear(x)

        return g


class GSMOEConv(nn.Module):
    def __init__(self, in_features, out_features, k_max, activation=None, dropout=None):
        super(GSMOEConv, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.layers = nn.ModuleList()
        for k in range(k_max):
            self.layers.append(TAGConv(in_features=in_features,
                                       out_features=out_features,
                                       k=k,
                                       activation=activation,
                                       dropout=dropout))
        # self.layers.append(GAT(in_features=in_features,
        #                        out_features=out_features,
        #                        hidden_features=[64],
        #                        num_heads=4))
        self.layers.append(GINConv(in_features=in_features,
                                   out_features=out_features,
                                   activation=activation,
                                   dropout=dropout))
        self.layers.append(GCNConv(in_features=in_features,
                                   out_features=out_features,
                                   activation=activation,
                                   dropout=dropout))
        # self.layers.append(MLPLayer(in_features=in_features,
        #                             out_features=out_features,
        #                             activation=activation,
        #                             dropout=dropout))

    def forward(self, x, adj, g, dropout=0.0):
        s = None
        for i, layer in enumerate(self.layers):
            g_out = g[:, i].unsqueeze(dim=1)
            expert_out = layer(x, adj, dropout)
            if s is None:
                s = g_out * expert_out
            else:
                s += g_out * expert_out

        return s
