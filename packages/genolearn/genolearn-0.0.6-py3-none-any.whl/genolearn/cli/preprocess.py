
def preprocess_cli(output_dir, sequence_data_path, batch_size, n_processes, sparse, dense, debug, verbose):
    from   genolearn.logger       import msg, Waiting
    from   genolearn              import utils, _data

    from   pathos.multiprocessing import cpu_count, Pool
    from   shutil                 import rmtree

    import numpy  as np

    import json
    import gzip
    import re
    import os

    if batch_size == -1:
        batch_size = np.inf

    n_processes = cpu_count() if n_processes == 'auto' else int(n_processes)

    gather_feature = lambda line : line[:line.index(' ')]
    gather_samples = lambda line : re.findall(r'[\w]+(?=:)', line)
    gather_counts  = lambda line : re.findall(r'(?<=:)[\w]+', line)
    
    if os.path.exists(output_dir):
        rmtree(output_dir)

    os.mkdir(output_dir)
    
    first_run  = True
    features   = []
    exceptions = set()
    C          = 0
    hi         = 0
    unique     = set()

    if sequence_data_path.endswith('.gz'):
        _open  = gzip.GzipFile
        decode = lambda line : line.decode()
    else:
        _open  = open
        decode = lambda line : line

    with _open(sequence_data_path) as gz:
       
        os.chdir(output_dir)

        os.mkdir('temp')
        os.mkdir('feature-selection')

        files = {}
        _data.set_files(files)

        while True:
           
            gz.seek(0)

            skip    = False
            skipped = False
            c       = 0
           
            for m, line in enumerate(gz, 1):

                line   = decode(line)

                srrs   = gather_samples(line)
                counts = gather_counts(line)

                if first_run:
                    features.append(gather_feature(line))
                    hi      = max(hi, *map(int, counts))
                    unique |= set(srrs)

                for SRR, count in zip(srrs, counts):
                    if SRR not in exceptions:
                        if SRR not in files:
                            if skip:
                                skipped = True
                                continue
                            files[SRR] = _data.init(SRR)
                            c         += 1
                            C         += 1
                            skip = c == batch_size
                        _data.add(files[SRR], m - 1, count)

                if m % verbose == 0:
                    msg(f'{C:10,d} {m:10,d}')
               
                if m == debug:
                    break
           
            if m % verbose:
                msg(f'{C:10,d} {m:10,d}')

            for f in files.values():
                f.close()

            if first_run:
                first_run = False

                n         = len(unique)
                d_dtype   = utils.get_dtype(hi)
                c_dtype   = utils.get_dtype(m)
                r_dtype   = utils.get_dtype(n)

                utils.set_m(m)

                with Waiting('compressing', 'compressed', 'features.txt.gz'):
                    with gzip.open('features.txt.gz', 'wb') as g:
                        g.write(' '.join(features).encode())
                
                features.clear()

                f = _data.init('meta', None, 'json')
                json.dump({'n' : len(unique), 'm' : m, 'max' : hi}, f)
                f.close()
               
                def to_sparse(npz, c, d):
                    np.savez_compressed(os.path.join('sparse', npz), col = c.astype(c_dtype), data = d.astype(d_dtype))

                def to_dense(npz, c, d):
                    arr = np.zeros(m, dtype = d.dtype)
                    arr[c] = d
                    np.savez_compressed(os.path.join('dense', npz), arr = arr)
               
                def convert(file):
                    txt  = os.path.join('temp', f'{file}.txt')
                    npz  = f'{file}.npz'
                    c, d = np.loadtxt(txt, dtype = c_dtype).T

                    for function in functions:
                        function(npz, c, d)

                    os.remove(txt)

                functions = []
                if sparse:
                    functions.append(to_sparse)
                    os.mkdir('sparse')

                if dense:
                    functions.append(to_dense)
                    os.mkdir('dense')

                _data.set_functions(functions)
           
            with Pool(n_processes) as pool:
                pool.map(convert, list(files))

            if not skipped:
                break

            exceptions |= set(files)

            if len(files) < batch_size:
                break

            files.clear()

        os.rmdir('temp')

        utils.create_log('.')
   
    msg('executed "genolearn.preprocess"')
