import click
from   genolearn.logger import print_dict

@click.group()
def cli():
    pass

@cli.command()
@click.argument('output_dir')
@click.argument('sequence_data_path')
@click.option('-b', '--batch-size', default = 512, show_default = True, help = 'number of temporary txt files to generate over a single parse of the genome data')
@click.option('-n', '--n-processes', default = 'auto', show_default = True, help = 'number of processes to run in parallel when compressing txt to npy files')
@click.option('--sparse', is_flag = True, default = True, show_default = True, help = 'output sparse npz files')
@click.option('--dense', is_flag = True, default = True, show_default = True, help = 'output dense npz files')
@click.option('--debug', default = -1, show_default = True, help = 'integer denoting first number of features to consider (-1 results in all features)')
@click.option('--verbose', default = 250000, show_default = True, help = 'number of iterations before giving verbose update')
def preprocess(output_dir, sequence_data_path, batch_size, n_processes, sparse, dense, debug, verbose):
    """
    \b
    Processes a gunzip (gz) compressed text file containing genome sequence data of the following sparse format

        \b
        sequence_1 | identifier_{1,1}:count_{1,1} identifier_{1,1}:count_{2,1} ...
        sequence_2 | identifier_{2,1}:count_{2,1} identifier_{2,1}:count_{2,2} ...
        ...

    \b
    into a directory of .npz files, a list of all the features, and some meta information containing number of
    identifiers, sequences, and non-zero counts.

    \b
    Example Usage
    >>> genolearn preprocess data raw-data/STEC_14-19_fsm_kmers.txt.gz --batch-size 256
    """
    print_dict('executing "preprocess" with parameters:', locals())
    from genolearn.cli import preprocess_cli
    preprocess_cli(output_dir, sequence_data_path, batch_size, n_processes, sparse, dense, debug, verbose)

@cli.command()
@click.argument('output_dir')
@click.argument('sequence_data_path')
@click.option('-b', '--batch-size', default = 512, show_default = True, help = 'number of temporary txt files to generate over a single parse of the genome data')
@click.option('-n', '--n-processes', default = 'auto', show_default = True, help = 'number of processes to run in parallel when compressing txt to npy files')
@click.option('--sparse', is_flag = True, default = True, show_default = True, help = 'output sparse npz files')
@click.option('--dense', is_flag = True, default = True, show_default = True, help = 'output dense npz files')
@click.option('--debug', default = -1, show_default = True, help = 'integer denoting first number of features to consider (-1 results in all features)')
@click.option('--verbose', default = 250000, show_default = True, help = 'number of iterations before giving verbose update')
def combine(output_dir, sequence_data_path, batch_size, n_processes, sparse, dense, debug, verbose):
    print_dict('executing "combine" with parameters:', locals())
    from genolearn.cli import combine_cli
    combine_cli(output_dir, sequence_data_path, batch_size, n_processes, sparse, dense, debug, verbose)

@cli.command()
@click.argument('model')
@click.argument('data_config')
@click.argument('feature_selection')
@click.argument('key')
@click.argument('values')
@click.argument('output')
@click.option('-a', '--ascending', is_flag = True, default = False)
def evaluate(model, data_config, feature_selection, ascending, key, values, output):
    print_dict('executing "evaluate" with parameters:', locals())
    from genolearn.cli import evaluate_cli
    evaluate_cli(model, data_config, feature_selection, ascending, key, values, output)

@cli.command()
@click.argument('path')
@click.argument('feature_selection')
@click.argument('key')
@click.argument('model')
@click.argument('output')
def feature_importance(path, feature_selection, key, model, output):
    print_dict('executing "feature-importance" with parameters:', locals())
    from genolearn.cli import feature_importance_cli
    feature_importance_cli(path, feature_selection, key, model, output)

@cli.command()
@click.argument('output')
@click.argument('path')
@click.argument('meta_path')
@click.argument('identifier')
@click.argument('target')
@click.argument('values')
@click.argument('group')
@click.argument('method')
@click.argument('aggregate')
@click.argument('log')
@click.option('-s', '--sparse', is_flag = True, default = False)
def feature_selection(output, path, meta_path, identifier, target, values, group, method, aggregate, log, sparse):
    r"""
    Generates an ordered list of features and meta information.

    Example
    =======

    >>> # fisher score default
    >>> python -m genolearn.feature_selection fisher-scores.npz data raw-data/meta-data.csv Accession Regions 2014 2015 2016 2017 2018 2019 -group Year

    >>> # custom (expected custom.py)
    >>> python -m genolearn.feature_selection custom-scores.npz data raw-data/meta-data.csv Accession Regions 2014 2015 2016 2017 2018 2019 -group Year -method custom

    """
    print_dict('executing "feature-selection" with parameters:', locals())
    from genolearn.cli import feature_selection_cli
    feature_selection_cli(output, path, meta_path, identifier, target, values, group, method, aggregate, log, sparse)

@cli.command()
@click.argument('path')
@click.argument('model')
@click.argument('data_config')
@click.argument('model_config')
@click.argument('train')
@click.argument('test')
@click.argument('K')
@click.argument('order')
@click.argument('order_key')
@click.argument('ascending')
@click.argument('min_count')
@click.argument('target_subset')
@click.argument('metric')
@click.argument('mean_func')
@click.argument('overwrite')
@click.option('-s', '--sparse', is_flag = True, default = False)
def train(path, model, data_config, model_config, train, test, K, order, order_key, ascending, min_count, target_subset, metric, mean_func, overwrite):
    print_dict('executing "train" with parameters:', locals())
    from genolearn.cli import train_cli
    train_cli(path, model, data_config, model_config, train, test, K, order, order_key, ascending, min_count, target_subset, metric, mean_func, overwrite)

if __name__ == '__main__':
    cli()