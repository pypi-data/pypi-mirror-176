def feature_selection_cli(output, path, meta_path, identifier, target, values, group, method, aggregate, log, sparse):
    from   genolearn.feature_selection import base_feature_selection, fisher
    from   genolearn.logger  import print_dict, msg, Writing
    from   genolearn.dataloader import DataLoader
    from   genolearn         import utils

    from   argparse          import ArgumentParser, RawTextHelpFormatter
    import importlib
    import pkgutil

    import numpy  as np
    import os


    # parser = ArgumentParser(description = description, formatter_class = RawTextHelpFormatter)

    # parser.add_argument('output',     help = 'output file name')
    # parser.add_argument('path'  ,     help = 'path to preprocessed directory')
    # parser.add_argument('meta_path',  help = 'path to meta file')
    # parser.add_argument('identifier', help = 'column of meta data denoting the identifier')
    # parser.add_argument('target',     help = 'column of meta data denoting the target')
    # parser.add_argument('values', nargs = '*', help = 'incremental identifiers (or groups) to perform feature selection on')
    # parser.add_argument('-group', default = None, help = 'column of meta data denoting the grouping of labels')
    # parser.add_argument('-method', default = 'fisher', help = 'either "fisher" for built in Fisher Score or a module name (see example)')
    # parser.add_argument('-aggregate', default = False, action = 'store_true', help = 'removes incremental loop and performs a single outer loop')
    # parser.add_argument('-log', default = None, help = 'log file name')
    # parser.add_argument('--sparse', default = False, action = 'store_true', help = 'if sparse loading of data is preferred')

    dataloader = DataLoader(path, meta_path, identifier, target, group, sparse)
    
    os.makedirs(os.path.join(path, 'feature-selection'), exist_ok = True)

    if f'{method}' == 'fisher':

        module       = importlib.import_module(f'genolearn.feature_selection.fisher')

    elif f'{method}.py' in os.listdir():

        module       = importlib.import_module(method)

    else:
        raise Exception(f'"{method}.py" not in current directory!')

    variables    = dir(module)

    for name in ['init', 'inner_loop', 'outer_loop']:
        assert name in variables
        
    force_sparse = module.force_sparse if 'force_sparse' in variables else False
    force_dense  = module.force_dense  if 'force_dense'  in variables else False

    scores       = base_feature_selection(dataloader, module.init, module.inner_loop, module.outer_loop, values, force_dense, force_sparse, aggregate)

    save_path    = f'{path}/feature-selection/{output}'
    with Writing(save_path, inline = True):
        np.savez_compressed(save_path, **scores)

    utils.create_log(f'{path}/feature-selection', f'log-{method}.txt' if log is None else log)

    msg('executed "genolearn.feature_selection"')
