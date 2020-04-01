from pathlib import Path
from collections import OrderedDict


class Cfg:
    def __init__(self, cfgfile: Path):
        lines = cfgfile.read_text().splitlines()
        self.param, self.layers = self._get_layers(lines)


    def _get_section_name(self, line:str) -> str:
        return line[1:-1]


    def _split_key_and_value(self, line:str) -> (str, str):
        k, v = line.split('=')
        return k.strip(), v.strip()


    def _get_layers(self, lines:list):
        param = OrderedDict()
        layer = OrderedDict()
        layers = []
        for line in lines:
            # 空行、コメントは無視
            if line == '':
                continue
            elif line[0] == '#':
                continue

            # layers
            elif line[0] == '[':
                if layer == {}:
                    pass
                elif layer['layer_name'] == 'param':
                    param = layer
                else:
                    layers.append(layer)

                layer = OrderedDict()
                if self._get_section_name(line) == 'net':
                    layer['layer_name'] = 'param'
                else:
                    layer['layer_name'] = self._get_section_name(line)
                continue

            # param
            key, value = self._split_key_and_value(line)
            layer[key] = value

        return param, layers


    def _dict2lines(self):
        pass

    def write_cfg(self, dst_cfgfile: Path):
        with dst_cfgfile.open(mode='w') as f:
            pass



if __name__ == '__main__':
    cfg = Cfg(Path('yolov3.cfg'))
    print(cfg.param)
    print(cfg.param.keys())
    print(f'layers num : {len(cfg.layers)}')

