from .utils import sequence_padding
import paddle
import re


def dict_collate(batch):
    return {k: paddle.to_tensor(sequence_padding(v)) for k, v in batch.items()}


def list_collate(batch):
    return [sequence_padding(x) for x in batch]


def param_groups_lrd(model, num_layers, lr, weight_decay=0.1, layer_decay=1.):
    param_group_names = {}
    param_groups = {}
    layer_scales = list(layer_decay ** (num_layers - i) for i in range(num_layers + 1))
    for n, p in model.named_parameters():
        if not p.trainable:
            continue
        if p.ndim == 1 or 'bias' in n.lower() or 'norm' in n.lower():
            g_decay = "no_decay"
            this_decay = 0.
        else:
            g_decay = "decay"
            this_decay = weight_decay

        layer_id = get_layer_id(n, num_layers)
        group_name = "layer_%d_%s" % (layer_id, g_decay)

        if group_name not in param_group_names:
            this_scale = layer_scales[layer_id]

            param_group_names[group_name] = {
                "lr": this_scale,
                "weight_decay": this_decay,
                "params": [],
            }
            param_groups[group_name] = {
                "lr_scale": this_scale,
                "weight_decay": this_decay,
                "params": [],
            }

        param_group_names[group_name]["params"].append(n)
        param_groups[group_name]["params"].append(p)

    # print("parameter groups: \n%s" % json.dumps(param_group_names, indent=2))
    param_groups = param_groups.values()
    for param_group in param_groups:
        if "lr_scale" in param_group:
            param_group["lr"] = lr * param_group["lr_scale"]
        else:
            param_group["lr"] = lr
    return param_groups


def get_layer_id(name, num_layers):
    pattern = 'encoder\\.layers?\\.'
    if 'embedding' in name:
        return 0
    elif re.search(pattern, name):
        idx = re.search(pattern, name).span()[1]
        layer_id = int(name[idx:].split('.')[0]) + 1
        return layer_id
    else:
        return num_layers


def create_optimizer(model, args, num_layers):
    param_groups = param_groups_lrd(model, num_layers, args.lr, weight_decay=args.weight_decay,
                                    layer_decay=args.layer_decay)
    optimizer = paddle.optimizer.AdamW(args.lr, parameters=param_groups)
    return optimizer

