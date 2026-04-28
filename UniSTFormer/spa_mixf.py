import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
import math

def conv_branch_init(conv, branches):
    weight = conv.weight
    n = weight.size(0)
    k1 = weight.size(1)
    k2 = weight.size(2)
    nn.init.normal_(weight, 0, math.sqrt(2. / (n * k1 * k2 * branches)))
    nn.init.constant_(conv.bias, 0)

def conv_init(conv):
    nn.init.kaiming_normal_(conv.weight, mode='fan_out')
    nn.init.constant_(conv.bias, 0)

def bn_init(bn, scale):
    nn.init.constant_(bn.weight, scale)
    nn.init.constant_(bn.bias, 0)

class MultiScale_Pooling_Attention(nn.Module):
    """
    Simplified multi-scale pooling attention mechanism (only global + local, direct concat)
    """
    def __init__(self, out_channels):
        super(MultiScale_Pooling_Attention, self).__init__()
        self.out_channels = out_channels
        
        self.global_pool = nn.AdaptiveAvgPool2d(1)
        self.local_pool = nn.AdaptiveAvgPool2d(4)
        
        # Modification 1: MLP hidden dimension from 32 → 128, and add dropout(0.1)
        self.linear = nn.Sequential(
            nn.Linear(25 * 2, 128),
            nn.ReLU(),
            nn.Dropout(0.15),  
            nn.Linear(128, 25)
        )
        
        self.relu = nn.ReLU()
        self.soft = nn.Softmax(-1)

    def forward(self, x):
        N, C, T, V = x.size()
        x1 = x[:, :C//2, :, :]
        x2 = x[:, C//2:, :, :]
        
        def extract_features(x_input):
            f_global = self.global_pool(x_input.permute(0, 3, 1, 2)).squeeze(-1).squeeze(-1)
            f_local = self.local_pool(x_input.permute(0, 3, 1, 2)).mean(dim=[2, 3])
            return torch.cat([f_global, f_local], dim=-1)
        
        Q_concat = extract_features(x1)
        K_concat = extract_features(x2)
        
        Q_final = self.relu(self.linear(Q_concat))
        K_final = self.relu(self.linear(K_concat))
        
        attn = self.soft(torch.einsum('nv,nw->nvw', Q_final, K_final))
        attn = attn.unsqueeze(1).repeat(1, self.out_channels, 1, 1)
        
        return attn, Q_final, K_final

class Spatial_MixFormer(nn.Module):
    def __init__(self, in_channels, out_channels, A, groups=1, coff_embedding=16, num_subset=1, t_stride=1, t_padding=0, t_dilation=1, bias=True, first=False, residual=True, alpha=0.5):
        super(Spatial_MixFormer, self).__init__()
        
        inter_channels = out_channels // coff_embedding
        self.inter_c = inter_channels
        self.groups = groups
        self.out_channels = out_channels
        self.in_channels = in_channels
        self.num_subset = num_subset
        self.alpha = nn.Parameter(torch.tensor(alpha))
        
        self.A_GEME = nn.Parameter(torch.tensor(np.reshape(A.astype(np.float32), [3, 1, 25, 25]), dtype=torch.float32).repeat(1, groups, 1, 1), requires_grad=True)
        self.A_SE = Variable(torch.from_numpy(np.reshape(A.astype(np.float32), [3, 1, 25, 25]).repeat(groups, axis=1)), requires_grad=False)
        
        self.sigmoid = nn.Sigmoid()
        self.linear = nn.Linear(25, 25)
        
        self.Spa_Att = MultiScale_Pooling_Attention(out_channels)
        
        self.AvpChaRef = nn.AdaptiveAvgPool2d(1)
        self.ChaRef_conv = nn.Conv1d(1, 1, kernel_size=3, padding=1, bias=False)
        
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, in_channels, kernel_size=1, groups=in_channels),
            nn.BatchNorm2d(in_channels),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels, out_channels * num_subset, kernel_size=1, groups=2)
        )
        
        if residual:
            if in_channels != out_channels:
                self.down = nn.Sequential(
                    nn.Conv2d(in_channels, out_channels, 1),
                    nn.BatchNorm2d(out_channels)
                )
            else:
                self.down = lambda x: x
        else:
            self.down = lambda x: 0

        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU()
        self.soft = nn.Softmax(-1)

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                conv_init(m)
            elif isinstance(m, nn.BatchNorm2d):
                bn_init(m, 1)
        bn_init(self.bn, 1e-6)

    def forward(self, x0):
        N, C, T, V = x0.size()
        A = self.A_SE.cuda(x0.get_device()) + self.A_GEME
        norm_learn_A = A.repeat(1, self.out_channels // self.groups, 1, 1)
        A_final = torch.zeros([N, self.num_subset, self.out_channels, 25, 25], dtype=torch.float, device=x0.device).detach()

        m = self.conv(x0)
        n, kc, t, v = m.size()
        m = m.view(n, self.num_subset, kc // self.num_subset, t, v)

        # Temporal sampling
        if t > 2:
            t_sampled = max(t // 1, 1)
            m_sampled = F.interpolate(
                m.reshape(n * self.num_subset, -1, t, v),
                size=(t_sampled, v),
                mode='bilinear',
                align_corners=False
            ).reshape(n, self.num_subset, kc // self.num_subset, t_sampled, v)
        else:
            m_sampled = m

        # Spatial attention
        for i in range(self.num_subset):
            m1, Q1, K1 = self.Spa_Att(m[:, i, :, :, :])
            atten = m1 * 0.5 + norm_learn_A[i]
            A_final[:, i, :, :, :] = atten

        # Attention operation
        if t > 2:
            m = F.interpolate(
                torch.einsum('nkctv,nkcvw->nctw', (m_sampled, A_final)),
                size=(t, v),
                mode='bilinear',
                align_corners=False
            )
        else:
            m = torch.einsum('nkctv,nkcvw->nctw', (m, A_final))

        # Channel refinement
        CR_in = self.AvpChaRef(m)
        CR_in = self.ChaRef_conv(CR_in.squeeze(-1).transpose(-1, -2)).transpose(-1, -2).unsqueeze(-1)
        CR_out = m + m * self.sigmoid(CR_in).expand_as(m)

        out = self.bn(CR_out)
        out += self.down(x0)
        out = self.relu(out)
        return out
