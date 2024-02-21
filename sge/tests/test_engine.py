def test_symreg():
    import sge
    from examples.symreg import SymbolicRegression
    eval_func = SymbolicRegression()
    sge.evolutionary_algorithm(evaluation_function=eval_func, parameters_file="parameters/standard.yml")