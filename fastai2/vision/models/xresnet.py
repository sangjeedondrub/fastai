#AUTOGENERATED! DO NOT EDIT! File to edit: dev/11_vision.models.xresnet.ipynb (unless otherwise specified).

__all__ = ['init_cnn', 'XResNet', 'xresnet18', 'xresnet34', 'xresnet50', 'xresnet101', 'xresnet152', 'xresnet18_deep',
           'xresnet34_deep', 'xresnet50_deep', 'xresnet18_deeper', 'xresnet34_deeper', 'xresnet50_deeper']

#Cell
from ...torch_basics import *
from ...test import *
from torchvision.models.utils import load_state_dict_from_url

#Cell
def init_cnn(m):
    if getattr(m, 'bias', None) is not None: nn.init.constant_(m.bias, 0)
    if isinstance(m, (nn.Conv2d,nn.Linear)): nn.init.kaiming_normal_(m.weight)
    for l in m.children(): init_cnn(l)

#Cell
class XResNet(nn.Sequential):
    def __init__(self, expansion, layers, c_in=3, c_out=1000,
                 sa=False, sym=False, act_cls=defaults.activation,
                 ):
        sizes = [c_in, 16,32,64] if c_in < 3 else [c_in, 32, 64, 64]
        stem = [ConvLayer(sizes[i], sizes[i+1], stride=2 if i==0 else 1, act_cls=act_cls)
                for i in range(3)]

        block_szs = [64//expansion,64,128,256,512] +[256]*(len(layers)-4)
        blocks = [self._make_layer(expansion, ni=block_szs[i], nf=block_szs[i+1], blocks=l, stride=1 if i==0 else 2,
                                  sa=sa if i==len(layers)-4 else False, sym=sym, act_cls=act_cls)
                  for i,l in enumerate(layers)]
        super().__init__(
            *stem,
            nn.MaxPool2d(kernel_size=3, stride=2, padding=1),
            *blocks,
            nn.AdaptiveAvgPool2d(1), Flatten(),
            nn.Linear(block_szs[-1]*expansion, c_out),
        )
        init_cnn(self)

    def _make_layer(self, expansion, ni, nf, blocks, stride, sa, sym, act_cls):
        return nn.Sequential(
            *[ResBlock(expansion, ni if i==0 else nf, nf, stride if i==0 else 1,
                      sa if i==(blocks-1) else False, sym=sym, act_cls=act_cls)
              for i in range(blocks)])

#Cell
def _xresnet(pretrained, expansion, layers, **kwargs):
    # TODO pretrain all sizes. Currently will fail with non-xrn50
    url = 'https://s3.amazonaws.com/fast-ai-modelzoo/xrn50_940.pth'
    res = XResNet(expansion, layers, **kwargs)
    if pretrained: res.load_state_dict(load_state_dict_from_url(url, map_location='cpu')['model'], strict=False)
    return res

def xresnet18 (pretrained=False, **kwargs): return _xresnet(pretrained, 1, [2, 2,  2, 2], **kwargs)
def xresnet34 (pretrained=False, **kwargs): return _xresnet(pretrained, 1, [3, 4,  6, 3], **kwargs)
def xresnet50 (pretrained=False, **kwargs): return _xresnet(pretrained, 4, [3, 4,  6, 3], **kwargs)
def xresnet101(pretrained=False, **kwargs): return _xresnet(pretrained, 4, [3, 4, 23, 3], **kwargs)
def xresnet152(pretrained=False, **kwargs): return _xresnet(pretrained, 4, [3, 8, 36, 3], **kwargs)
def xresnet18_deep  (pretrained=False, **kwargs): return _xresnet(pretrained, 1, [2,2,2,2,1,1], **kwargs)
def xresnet34_deep  (pretrained=False, **kwargs): return _xresnet(pretrained, 1, [3,4,6,3,1,1], **kwargs)
def xresnet50_deep  (pretrained=False, **kwargs): return _xresnet(pretrained, 4, [3,4,6,3,1,1], **kwargs)
def xresnet18_deeper(pretrained=False, **kwargs): return _xresnet(pretrained, 1, [2,2,1,1,1,1,1,1], **kwargs)
def xresnet34_deeper(pretrained=False, **kwargs): return _xresnet(pretrained, 1, [3,4,6,3,1,1,1,1], **kwargs)
def xresnet50_deeper(pretrained=False, **kwargs): return _xresnet(pretrained, 4, [3,4,6,3,1,1,1,1], **kwargs)