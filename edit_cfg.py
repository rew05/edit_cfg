from pathlib import Path
from collections import OrderedDict


class Cfg:
    """cfg paramater
    """
    def __init__(self, cfgfile: Path):
        """initialize

        Parameters
        ----------
        cfgfile : Path
            source cfg file
        """
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
            line = line.strip()
            # ignore blank or comment line
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
        lines = []
        # append [net]
        for k, v in self.param.items():
            if k == 'layer_name':
                lines.append('[net]')
            else:
                lines.append(f'{k} = {v}')

        lines.append('')  # blank
        # append network
        for layer in self.layers:
            for k, v in layer.items():
                if k == 'layer_name':
                    lines.append(f'[{v}]')
                else:
                    lines.append(f'{k} = {v}')
            lines.append('')  # blank

        return lines


    def write_cfg(self, dst_cfgfile: Path):
        with dst_cfgfile.open(mode='w') as f:
            f.writelines('\n'.join(self._dict2lines()))


if __name__ == '__main__':
    cfg = Cfg(Path('../_edit_cfg/yolov3.cfg'))
    print(cfg.param)
    print(cfg.param.keys())
    print(f'layers num : {len(cfg.layers)}')
    cfg.write_cfg(Path('out.cfg'))

