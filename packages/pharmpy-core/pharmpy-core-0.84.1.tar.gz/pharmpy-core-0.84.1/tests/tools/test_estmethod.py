import pytest

from pharmpy.tools.estmethod.algorithms import _clear_estimation_steps, _create_est_model
from pharmpy.tools.estmethod.tool import create_workflow


@pytest.mark.parametrize(
    'methods, solvers, no_of_models',
    [
        ('foce', None, 2),
        (['foce', 'laplace'], None, 4),
        (['laplace'], None, 3),
        ('foce', ['lsoda'], 4),
        ('foce', 'all', 14),
    ],
)
def test_algorithm(methods, solvers, no_of_models):
    wf = create_workflow('exhaustive', methods=methods, solvers=solvers)
    fit_tasks = [task.name for task in wf.tasks if task.name.startswith('run')]

    assert len(fit_tasks) == no_of_models


@pytest.mark.parametrize(
    'method, est_rec, eval_rec',
    [
        (
            'fo',
            '$ESTIMATION METHOD=ZERO INTER MAXEVAL=9999 AUTO=1 PRINT=10',
            '$ESTIMATION METHOD=IMP INTER EONLY=1 MAXEVAL=9999 ISAMPLE=10000 NITER=10 PRINT=10',
        ),
        (
            'laplace',
            '$ESTIMATION METHOD=COND LAPLACE INTER MAXEVAL=9999 AUTO=1 PRINT=10',
            '$ESTIMATION METHOD=IMP LAPLACE INTER EONLY=1 MAXEVAL=9999 ISAMPLE=10000 '
            'NITER=10 PRINT=10',
        ),
    ],
)
def test_create_est_model(load_model_for_test, pheno_path, method, est_rec, eval_rec):
    model = load_model_for_test(pheno_path)
    assert len(model.estimation_steps) == 1
    est_model = _create_est_model(method, None, model=model)
    assert len(est_model.estimation_steps) == 2
    assert est_model.model_code.split('\n')[-5] == est_rec
    assert est_model.model_code.split('\n')[-4] == eval_rec


def test_clear_estimation_steps(load_model_for_test, pheno_path):
    model = load_model_for_test(pheno_path)
    assert len(model.estimation_steps) == 1
    _clear_estimation_steps(model)
    assert len(model.estimation_steps) == 0
