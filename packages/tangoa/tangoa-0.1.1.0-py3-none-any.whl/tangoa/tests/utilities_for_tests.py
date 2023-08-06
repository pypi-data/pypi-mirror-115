def get_model_parameters(high_level_solver):
    model_parameters = high_level_solver.solver.get_model_parameters()
    return model_parameters.Q, model_parameters.b, model_parameters.c, model_parameters.d, model_parameters.A, \
           model_parameters.w, model_parameters.G, model_parameters.u


def get_relaxation_solver(high_level_solver):
    return high_level_solver.solver.relaxation


def print_instance_name(name):
    print("")
    print("=" * 20)
    print("Running test on instance " + name)
    print("=" * 20)
