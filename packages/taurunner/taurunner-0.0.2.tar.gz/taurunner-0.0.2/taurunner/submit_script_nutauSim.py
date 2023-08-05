#!/usr/bin/env python

import pycondor, argparse, sys, os.path
from glob import glob
import numpy as np

error = '/scratch/isafa/ANITA/error'
output = '/scratch/isafa/ANITA/output'
log = '/scratch/isafa/ANITA/log'
submit = '/scratch/isafa/ANITA/submit'

dagman = pycondor.Dagman('nutau_taurunner_set', submit=submit, verbose=2)

job_gen = pycondor.Job('generation','/data/user/isafa/ANITA/TauRunnerV2/master/TauRunner/taurunner/run_taurunner.sh',
            error=error,
            output=output,
            log=log,
            submit=submit,
            dag=dagman,
            universe='vanilla',
            verbose=2,
            request_memory=2000,
            extra_lines= ['should_transfer_files = YES', 'when_to_transfer_output = ON_EXIT']
            )

energies = [1e8, 1e9, 1e10]
angles   = [89.0, 88.0, 87.0, 86.0, 85.0, 83.0, 82.0, 80.0] 

nev = 1e6

for e in energies:
    for t in angles:
        for i in range(10):
            job_gen.add_arg('{} {} {} {} taus_{}_{}_{}'.format(int(nev), e, t, i, e, t, i))

#energies = [1e8, 1e9, 1e10]
angles   = [78.0, 75.0, 72., 70., 66., 63., 60., 55., 50.] 

#energies = [1e9]
#angles   = [40]
for e in energies:
    for t in angles:
        for i in range(100):
            job_gen.add_arg('{} {} {} {} taus_{}_{}_{}'.format(int(nev), e, t, i, e, t, i))
#            job_gen.add_arg('{} {} {} secondaries_{}_{}_{}'.format(e, t, i, e, t, i))


dagman.build_submit()
