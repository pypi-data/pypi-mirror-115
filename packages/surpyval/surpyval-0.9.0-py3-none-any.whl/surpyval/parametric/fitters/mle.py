import autograd.numpy as np
from autograd import jacobian, hessian, value_and_grad
from autograd.numpy.linalg import inv
from scipy.optimize import minimize, approx_fprime

import sys
import copy

def _create_censor_flags(x_mle, gamma, c, dist):
    if 2 in c:
        l_flag = x_mle[:, 0] <= np.min([gamma, dist.support[0]])
        r_flag = x_mle[:, 1] >= dist.support[1]
        mask = np.vstack([l_flag, r_flag]).T
        inf_c_flags = (mask).astype(int)
        x_mle[(c == 2).reshape(-1, 1) & mask] = 1
    else:
        inf_c_flags = np.zeros_like(x_mle)

    return inf_c_flags, x_mle


def mle(model):
    """
    Maximum Likelihood Estimation (MLE)

    """
    dist = model.dist
    x, c, n, t = model.data['x'], model.data['c'], model.data['n'], model.data['t']
    const = model.fitting_info['const']
    trans = model.fitting_info['transform']
    inv_trans = model.fitting_info['inv_trans']
    inv_f = model.fitting_info['inv_f']
    init = model.fitting_info['init']
    fixed_idx = model.fitting_info['fixed_idx']
    offset = model.offset
    lfp = model.lfp
    zi = model.zi

    if hasattr(dist, 'mle'):
        return dist.mle(x, c, n, t, const, trans, inv_trans, init, fixed_idx, offset)

    old_err_state = np.seterr(invalid='raise',
                              divide='raise',
                              over='ignore',
                              under='ignore')

    results = {}

    # Need to flag entries where truncation is inf or -inf so that the autograd doesn't fail. Because
    # autograd fails if it encounters any inf, nan, -inf etc even if they don't affect the gradient
    # Very important to the autograd! And it worked, yay!
    t_flags = np.ones_like(t)
    t_mle = copy.copy(t)
    # Create flags to indicate where the truncation values are infinite
    t_flags[:, 0] = np.where(np.isfinite(t[:, 0]), 1, 0)
    t_flags[:, 1] = np.where(np.isfinite(t[:, 1]), 1, 0)
    # Convert the infinite values to a finite value to ensure the autodiff functions don't fail
    t_mle[:, 0] = np.where(t_flags[:, 0] == 1, t[:, 0], 1)
    t_mle[:, 1] = np.where(t_flags[:, 1] == 1, t[:, 1], 1)

    results['t_flags'] = t_flags
    results['t_mle'] = t_mle

    # Create the objective function
    def fun(params, offset=False, lfp=False, zi=False, transform=True, gamma=0.):
        x_mle = np.copy(x)
        if transform:
            params = inv_trans(const(params))

        if offset:
            gamma = params[0]
            params = params[1::]
        else:
            # Use the assumed value. Useful for hessian calcs holding gamma constant
            pass

        if zi:
            f0 = params[-1]
            params = params[0:-1]
        else:
            f0 = 0.

        if lfp:
            p = params[-1]
            params = params[0:-1]
        else:
            p = 1.

        inf_c_flags, x_mle = _create_censor_flags(x_mle, gamma, c, dist)

        return dist.neg_ll(x_mle, c, n, inf_c_flags, t_mle, t_flags, gamma, p, f0, *params)

    jac  = jacobian(fun)
    hess = hessian(fun)

    try:
        # First attempt to be with with jacobian and hessian from autograd
        res = minimize(fun, init, args=(offset, lfp, zi, True), method='Newton-CG', jac=jac, hess=hess)
        if not res.success:
            raise Exception
    except:
        # If first attempt fails, try a second time with only jacobian from autograd
        # print("MLE with autodiff hessian and jacobian failed, trying without hessian", file=sys.stderr)
        try:
            res = minimize(fun, init, args=(offset, lfp, zi, True), method='BFGS', jac=jac)
            if not res.success:
                raise Exception
        except:
            # If second attempt fails, try a third time with only the objective function
            # print("MLE with autodiff jacobian failed, trying without jacobian or hessian", file=sys.stderr)
            # try:
            np.seterr(all='ignore')
            res = minimize(fun, init, args=(offset, lfp, zi, True))
            # except:
                # Something really went wrong
            if res['message'] == 'Desired error not necessarily achieved due to precision loss.':
                print("""Precision was lost, try:
    - Using alternate fitting method
    - visually checking model fit
    - change data to be closer to 1.""", file=sys.stderr)
            elif (not res.success) | (np.isnan(res.x).any()):
                np.seterr(**old_err_state)
                print("""MLE Failed: Try making the values of the data closer to 1 by dividing or multiplying by
some constant.

Or try setting the `init` keyword in the `fit()` method to a value you believe is closer.
A good way to do this is to set any shape parameter to 1. and any scale parameter to be 
the mean of the data (or it's inverse)
                    """, file=sys.stderr)
                return {'res' : res}

    try:
        p_hat = inv_trans(const(res.x))
    except:
        p_hat = [None] * len(init)

    if offset:
        results['gamma'] = p_hat[0]
        params = p_hat[1:]
    else:
        results['gamma'] = 0
        params = p_hat

    if zi:
        results['f0'] = params[-1]
        params = params[0:-1]
    else:
        results['f0'] = 0.
        params = params

    if lfp:
        results['p'] = params[-1]
        results['params'] = params[0:-1]
    else:
        results['p'] = 1.
        results['params'] = params

    try:
        results['hess_inv'] = inv(hess(results['params'], *(False, lfp, zi, False, results['gamma'])))
    except:
        results['hess_inv'] = None

    results['_neg_ll'] = res['fun']
    results['res'] = res

    np.seterr(**old_err_state)

    return results
