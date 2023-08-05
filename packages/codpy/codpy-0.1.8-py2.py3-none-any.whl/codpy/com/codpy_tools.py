from random import random
import pandas as pd
import os,sys,time
import numpy as np
from functools import partial
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import axes3d,Axes3D
import abc 
import datetime
import copy
import codpydll
import codpypyd as cd
import QuantLib
import torch
import xarray

################general utilities from cebpl######################################

def get_closest_key(dic,mykey):
    return min(dic.keys(), key = lambda x: abs(x-mykey))
def get_last_key(dic):
    return list(dic.keys())[-1]
def get_closest_value(dic,mykey):
    return dic[get_closest_key(dic,mykey)]
def my_range(start, stop, step):
    start_type = type(start)
    out=[]
    while start < stop:
        out.append(start)
        start += step
    return out
def interpolate(x, fx, z, **kwargs):
    from scipy import interpolate
    x, fx, z = get_float(x), get_float(fx), get_float(z)
    if len(x) == 1: x.append(x[0]+1.), fx.append(fx[0])
    return interpolate.interp1d(x, fx, **kwargs)(z) 

def interpolate1D(x, fx, z, **kwargs):
    kind = str(kwargs.get("kind","linear"))
    bounds_error = bool(kwargs.get('bounds_error',False))
    copy = bool(kwargs.get('copy',False))
    var_col = kwargs.get('var_col',None)
    float_fun = kwargs.get('float_fun',None)
    fz = pd.DataFrame(columns = fx.columns)

    cols = fz.columns
    for col in cols:
        fz[col] = interpolate(x, fx[col], z,kind = kind, bounds_error = bounds_error, fill_value= (fx[col][0],fx[col][-1]), copy=copy)
        pass 
    return fz

def interpolate_nulls(data,**kwargs):
    kind = str(kwargs.get("kind","linear"))
    bounds_error = bool(kwargs.get('bounds_error',False))
    copy = bool(kwargs.get('copy',False))
    var_col = kwargs.get('var_col',None)
    float_fun = kwargs.get('float_fun',None)

    nulls = [col for col in data.columns if data[col].isnull().sum()]
    for col in nulls:
        fx = data.loc[data[col].notnull()][col].values
        if var_col is None:
            x = data.loc[data[col].notnull()].index.values
            z = data.index.values
        else: 
            x = data.loc[data[col].notnull()][var_col].values
            z = data[var_col].values
        if float_fun is not None: x,z=float_fun(x),float_fun(z)
        data[col] = interpolate(x, fx, z,kind = kind, bounds_error = bounds_error, fill_value= (fx[0],fx[-1]), copy=copy)
        pass 
    return data


def lazy_dic_evaluation(dic,key,fun):
    out = dic.get(key,None)
    if out is None: return fun()
    return out

################general utilities######################################

def format_32(x,**kwargs):
    if x.ndim==3:
        shapes = x.shape
        x = np.swapaxes(x,1,2)
        return x.reshape((x.shape[0]*x.shape[1],x.shape[2]))
def format_23(x,shapes,**kwargs):
    if x.ndim==2:
        out = x.reshape((shapes[0],shapes[2],shapes[1]))
        out = np.swapaxes(out,1,2)
        return out

def lexicographical_permutation(x,fx=[],**kwargs):
    # x = get_data(x)
    if x.ndim==1: index_array = np.argsort(x)
    else: 
        indexfx = kwargs.get("indexfx",0)
        index_array = np.argsort(a = x[:,indexfx])
    x_sorted = x[index_array]
    if (my_len(fx) != my_len(x_sorted)): return (x_sorted,index_array)
    if type(fx) == type([]): out = [s[index_array] for s in fx]
    # else: out = np.take_along_axis(arr = x,indices = index_array,axis = indexx)
    else: out = fx[index_array]
    return (x_sorted,out,index_array)


def null_rows(data_frame):
    import pandas as pd
    return data_frame[data_frame.isnull().any(axis = 1)]

def unity_partition(fx, unique_values = []):
    #print(fx)
    #print(unique_values)
    import numpy as np
    if len(unique_values) == 0: unique_values= np.unique(get_data(fx).flatten())
    P = len(unique_values)
    N = len(fx)
    out = np.zeros((N,P))
    d=0
    for v in unique_values :
        indices = np.where(fx == v)
        out[indices[0],d]=1.
        d=d+1
    #print(out)
    return out

def df_type(df:pd.DataFrame,**categ):
    import errno
    df_columns  = df.columns
    set_categ   = set(categ.keys())
    set_column  = set(list(df_columns))
    test = list(set_categ - set_column)
    if (test):
        raise NameError(errno.ENOSTR,os.strerror(errno.ENOSTR),test)
    out = df.astype(categ)
    return out

def get_dataframe_error(test_values:pd.DataFrame,extrapolated_values:pd.DataFrame):
    import errno
    num_cols = test_values._get_numeric_data().columns   
    print('get_dataframe_error.num_cols:',num_cols)
    cat_cols=list(set(test_values.columns) - set(num_cols))
    print('get_dataframe_error.cat_cols:',cat_cols)
    num_error = get_L2_error(test_values[num_cols].to_numpy(),extrapolated_values[num_cols].to_numpy())
    num_error += get_classification_error(test_values[cat_cols].to_numpy(),extrapolated_values[cat_cols].to_numpy())
    return num_error

def get_classification_error(test_values,extrapolated_values):
    if test_values.size == 0: return 0.
    out = [test_values[n] == extrapolated_values[n] for n in range(len(test_values))]
    out = np.sum(out)
    out /= test_values.size
    #print("\n ************  classification error ********** : %s" %   (out))
    return out
    
def get_relative_mean_squared_error(a,b):
    from sklearn.metrics import mean_squared_error
    a = get_data(a).flatten()
    b = get_data(b).flatten()
    out = np.linalg.norm(a-b)
    l = np.linalg.norm(a)
    r = np.linalg.norm(b)
    debug = l + r + 0.00001
    out /= debug
    return out 

def get_relative_error(x,z, ord = None):
    from numpy import linalg as la
    x,z = get_data(x),get_data(z)
    if (x.ndim == 1): x,z = x.reshape(len(x),1),z.reshape(len(x),1)
    debug = x-z
    debug = la.norm(debug.flatten(),ord)
    n = debug 
    debug = la.norm(x.flatten(),ord) + la.norm(z.flatten(),ord) + 1e-8
    n /= debug 
    # n *= n
    # print("\n ************  L2 error ********** : %s" %   (n))
    return n

def get_L2_error(x,z):
    return get_relative_error(x,z)

def softmaxindice(mat, axis=1):
    #print(mat[0:5])
    import numpy as np
    return np.argmax(get_matrix(mat), axis)
def softminindice(mat, axis=1):
    return softmaxindice(-mat, axis)

def execute(x_,fx_,y_,fy_,z_,fz_, Xs, Ys,fun):
    import numpy as np
    import pandas as pd
    import xarray as xr
    import time

    sizeXs = len(Xs)
    sizeYs = len(Ys)
    df_scores = xr.DataArray(np.zeros( (sizeXs, sizeYs) ), dims=('Nx', 'Ny'), coords={'Nx': Xs, 'Ny' : Ys})
    df_times = xr.DataArray(np.zeros( (sizeXs, sizeYs) ), dims=('Nx', 'Ny'), coords={'Nx': Xs, 'Ny' : Ys})
    for x in Xs:
        for y in Ys:
            start_time = time.time()
            # test = fun(x_[0:int(x)],fx_[0:int(x)],y_[0:int(y)],fy_[0:int(y)],z_,fz_)
            try:
                test = fun(x_[0:int(x)],fx_[0:int(x)],y_[0:int(y)],fy_[0:int(y)],z_,fz_)
            except :
                test = np.NaN
            # print("error:" + str(test) + " x:" + str(x) + " y:" + str(y) + "time:" + str(time.time() - start_time))
            df_scores.loc[x,y] = test
            df_times.loc[x,y] = time.time() - start_time
    return (df_scores,df_times)

def scenarios(x_, Xmax=0, X_steps=0):
    if (Xmax> 0) : Xs = np.arange(Xmax/X_steps,(Xmax/X_steps) *X_steps +1,int(Xmax/X_steps))
    else: Xs = np.arange(len(x_)/X_steps,(len(x_)/X_steps) *X_steps +1,int(len(x_)/X_steps)) 
    return Xs

def execute_function_list(**kwargs):
    import functools
    from inspect import signature
    fun_list_reverse = kwargs['fun_list'].copy()
    fun_list_reverse = fun_list_reverse[::-1]
    for fun_ in fun_list_reverse:
        kwargs = fun_(**kwargs)
    return kwargs

#########################codpy kernel wrappers###################

def get_codpy_param():
    return  {'rescale_kernel':{'max': 1000, 'seed':42},
    'sharp_discrepancy':{'max': 1000, 'seed':42},
    'discrepancy':{'max': 1000, 'seed':42},
    'validator_compute': ['accuracy_score','discrepancy_error','norm'],
    'set_codpy_kernel' : kernel_setters.kernel_helper(kernel_setters.set_tensornorm_kernel, 2,1e-8 ,map_setters.set_unitcube_map),
    'rescale': True,
    }

class codpy_param_getter:
    def get_params(**kwargs) : return kwargs.get('codpy',{})
    def get_kernel_fun(**kwargs): return codpy_param_getter.get_params(**kwargs)['set_kernel']

class factories:
    def get_kernel_factory_keys():
        return cd.factories.kernel_factory_keys()
    def get_map_factory_keys():
        return cd.factories.maps_factory_keys()

class kernel:
    def rescale(x=[],y=[],z=[],**kwargs):
        def get_param(**kwargs): return kwargs.get("rescale_kernel",None)
        param = get_param(**kwargs)
        if param is not None:
            max_ = param.get("max",None)
            if max_ is not None:
                seed_ = param.get("seed",None)
                x,y,z = random_select(x=x,xmax = max_,seed=seed_),random_select(x=y,xmax = max_,seed=seed_),random_select(x=z,xmax = max_,seed=seed_)
        cd.kernel.rescale(get_matrix(x),get_matrix(y),get_matrix(z))
    def get_kernel_ptr():
        return cd.get_kernel_ptr()
    def set_kernel_ptr(kernel_ptr):
        cd.set_kernel_ptr(kernel_ptr)
    def pipe_kernel_ptr(kernel_ptr):
        cd.kernel.pipe_kernel_ptr(kernel_ptr)
    def pipe_kernel_fun(kernel_fun, regularization = 1e-8):
        kern1 = kernel.get_kernel_ptr()
        kernel_fun()
        kern2 = kernel.get_kernel_ptr()
        kernel.set_kernel_ptr(kern1)
        kernel.pipe_kernel_ptr(kern2)
        cd.kernel.set_regularization(regularization)

class map_setters:
    class set:    
        def __init__(self,strings):
            self.strings = strings
        def __call__(self,**kwargs):    
            if isinstance(self.strings,list):
                ss = self.strings.copy()
                cd.kernel.set_map(ss.pop(0),kwargs)
                [pipe_map_setters.pipe(s) for s in ss]
            else: cd.kernel.set_map(self.strings,kwargs)
    def set_linear_map(**kwargs): cd.kernel.set_map("linear_map",kwargs)
    def set_affine_map(**kwargs): cd.kernel.set_map("affine_map",kwargs)
    def set_log_map(**kwargs): cd.kernel.set_map("log",kwargs)
    def set_exp_map(**kwargs): cd.kernel.set_map("exp",kwargs)
    def set_scale_std_map(**kwargs): cd.kernel.set_map("scale_std",kwargs)
    def set_erf_map(**kwargs): cd.kernel.set_map("scale_to_erf",kwargs)
    def set_erfinv_map(**kwargs): cd.kernel.set_map("scale_to_erfinv",kwargs)
    def set_unitcube_map(**kwargs): cd.kernel.set_map("scale_to_unitcube",kwargs)
    def set_grid_map(**kwargs): cd.kernel.set_map("map_to_grid",kwargs)
    def set_mean_distance_map(**kwargs): cd.kernel.set_map("scale_to_mean_distance",kwargs)
    def set_min_distance_map(**kwargs): cd.kernel.set_map("scale_to_min_distance",kwargs)
    def set_standard_mean_map(**kwargs):
        map_setters.set_mean_distance_map(**kwargs)
        pipe_map_setters.pipe_erfinv_map()
        pipe_map_setters.pipe_unitcube_map()
    def set_standard_min_map(**kwargs):
        map_setters.set_min_distance_map(**kwargs)
        pipe_map_setters.pipe_erfinv_map()
        pipe_map_setters.pipe_unitcube_map()
    def set_unitcube_min_map(**kwargs):
        map_setters.set_min_distance_map(**kwargs)
        pipe_map_setters.pipe_unitcube_map()
    def set_unitcube_erfinv_map(**kwargs):
        map_setters.set_erfinv_map()
        pipe_map_setters.pipe_unitcube_map()
    def set_unitcube_mean_map(**kwargs):
        map_setters.set_mean_distance_map(**kwargs)
        pipe_map_setters.pipe_unitcube_map()
    def map_helper(map_setter, **kwargs): return partial(map_setter, kwargs)


class kernel_setters:
    def kernel_helper(setter, polynomial_order:int = 0,regularization:float = 1e-8,set_map = None):
        return partial(setter, polynomial_order,regularization,set_map)
    def set_kernel(kernel_string,polynomial_order:int = 2,regularization:float = 1e-8,set_map = None):
        cd.kernel.set_polynomial_order(polynomial_order)
        cd.set_kernel(kernel_string)
        if (set_map) : set_map()
        if (polynomial_order > 0):
            linear_kernel = kernel_setters.kernel_helper(setter = kernel_setters.set_linear_regressor_kernel,polynomial_order = polynomial_order,regularization = regularization,set_map = map_setters.set_unitcube_map)
            kernel.pipe_kernel_fun(linear_kernel,regularization)
        cd.kernel.set_regularization(regularization)

    def set_linear_regressor_kernel(polynomial_order:int = 2,regularization:float = 1e-8,set_map = None):
        cd.kernel.set_polynomial_order(polynomial_order)
        cd.set_kernel("linear_regressor")
        cd.kernel.set_regularization(regularization)
        if (set_map) : set_map()

    def set_sumnorm_kernel(polynomial_order:int = 0,regularization:float = 1e-8,set_map = None): kernel_setters.set_kernel("sumnorm",polynomial_order,regularization,set_map)
    def set_tensornorm_kernel(polynomial_order:int = 0,regularization:float = 1e-8,set_map = None): kernel_setters.set_kernel("tensornorm",polynomial_order,regularization,set_map)
    def set_gaussian_kernel(polynomial_order:int = 0,regularization:float = 1e-8,set_map = None): kernel_setters.set_kernel("gaussian",polynomial_order,regularization,set_map)
    def set_matern_tensor_kernel(polynomial_order:int = 0,regularization:float = 1e-8,set_map = None): kernel_setters.set_kernel("materntensor",polynomial_order,regularization,set_map)
    default_multiquadricnorm_kernel_map = partial(map_setters.set_standard_mean_map, distance ='norm2')
    def set_multiquadricnorm_kernel(polynomial_order:int = 0,regularization:float = 1e-8,set_map = default_multiquadricnorm_kernel_map): kernel_setters.set_kernel("multiquadricnorm",polynomial_order,regularization,set_map)
    default_multiquadrictensor_kernel_map = partial(map_setters.set_standard_min_map, distance ='normifty')
    def set_multiquadrictensor_kernel(polynomial_order:int = 0,regularization:float = 1e-8,set_map = default_multiquadrictensor_kernel_map): kernel_setters.set_kernel("multiquadrictensor",polynomial_order,regularization,set_map)
    default_sincardtensor_kernel_map = partial(map_setters.set_min_distance_map, distance ='normifty')
    def set_sincardtensor_kernel(polynomial_order:int = 0,regularization:float = 1e-8,set_map = default_sincardtensor_kernel_map):
        kernel_setters.set_kernel("sincardtensor",polynomial_order,regularization,set_map)        
    default_sincardsquaretensor_kernel_map = partial(map_setters.set_min_distance_map, distance ='normifty')
    def set_sincardsquaretensor_kernel(polynomial_order:int = 0,regularization:float = 0,set_map = default_sincardsquaretensor_kernel_map): kernel_setters.set_kernel("sincardsquaretensor",polynomial_order,regularization,set_map)        
    def set_dotproduct_kernel(polynomial_order:int = 0,regularization:float = 1e-8,set_map = None):kernel_setters.set_kernel("DotProduct",polynomial_order,regularization,set_map)        
    def set_gaussianper_kernel(polynomial_order:int = 0,regularization:float = 1e-8,set_map = None):kernel_setters.set_kernel("gaussianper",polynomial_order,regularization,set_map)        
    def set_matern_norm_kernel(polynomial_order:int = 2,regularization:float = 1e-8,set_map = map_setters.set_mean_distance_map): kernel_setters.set_kernel("maternnorm",polynomial_order,regularization,set_map) 


class pipe_map_setters:
    def pipe(s,**kwargs):
        cd.kernel.pipe_map(s,kwargs)
    def pipe_log_map(**kwargs):pipe_map_setters.pipe("log",**kwargs)
    def pipe_exp_map(**kwargs):pipe_map_setters.pipe("exp",**kwargs)
    def pipe_linear_map(**kwargs):pipe_map_setters.pipe("linear_map",**kwargs)
    def pipe_affine_map(**kwargs):pipe_map_setters.pipe_affine_map("affine_map",**kwargs)
    def pipe_scale_std_map(**kwargs):pipe_map_setters.pipe("scale_std",**kwargs)
    def pipe_erf_map(**kwargs):pipe_map_setters.pipe("scale_to_erf",**kwargs)
    def pipe_erfinv_map(**kwargs):pipe_map_setters.pipe("scale_to_erfinv",**kwargs)
    def pipe_unitcube_map(**kwargs):pipe_map_setters.pipe("scale_to_unitcube",**kwargs)
    def pipe_mean_distance_map(**kwargs):pipe_map_setters.pipe("scale_to_mean_distance",**kwargs)
    def pipe_min_distance_map(**kwargs):pipe_map_setters.pipe("scale_to_min_distance",**kwargs)

class op:
    #set_codpy_kernel = kernel_setters.kernel_helper(kernel_setters.set_gaussian_kernel, 2,1e-8,map_setters.set_min_distance_map)
    set_codpy_kernel = kernel_setters.kernel_helper(kernel_setters.set_matern_tensor_kernel, 2,1e-8,map_setters.set_standard_mean_map)
    def sum_axis(x,axis=-1):
        if axis != -1: 
            out = np.sum(x,axis)
        else: out=x
        return out

    def discrepancy(x,z,y=[],set_codpy_kernel = None, rescale = False, disc_type="raw", **kwargs):
        if 'discrepancy:xmax' in kwargs: x= random_select_interface(x,xmaxlabel = 'discrepancy:xmax', seedlabel = 'discrepancy:seed',**kwargs)
        if 'discrepancy:ymax' in kwargs: y= random_select_interface(y,xmaxlabel = 'discrepancy:ymax', seedlabel = 'discrepancy:seed',**kwargs)
        if 'discrepancy:zmax' in kwargs: z= random_select_interface(z,xmaxlabel = 'discrepancy:zmax', seedlabel = 'discrepancy:seed',**kwargs)
        if 'discrepancy:nmax' in kwargs: 
            nmax = int(kwargs.get('discrepancy:nmax'))
            if len(x) + 2 * len(y) + len(z) > nmax: return np.NaN
        if (set_codpy_kernel): set_codpy_kernel()
        if (rescale): kernel.rescale(x,y,z,**kwargs)
        if (len(y)): 
            debug = cd.tools.discrepancy_error(x,y,disc_type)
            debug += cd.tools.discrepancy_error(y,z,disc_type)
            return np.sqrt(debug)
        else: return np.sqrt(cd.tools.discrepancy_error(x,z,disc_type))

    class discrepancy_functional:
        def __init__(self,set_codpy_kernel,x, y=[],rescale = True,**kwargs):
            self.Nx = len(x)
            self.x = x.copy()
            if (set_codpy_kernel): set_codpy_kernel()
            if (rescale): kernel.rescale(x,y)
            self.Kxx = np.sum(op.discrepancy_functional.Knm(x = x,y = x) ) 
        def Knm(x,y,set_codpy_kernel = None,rescale = False,**kwargs):
            Nx = len(x)
            Ny = len(y)
            return op.Knm(x = x,y = y, set_codpy_kernel = set_codpy_kernel, rescale = rescale) / (Nx*Ny)
        def eval(self,ys):
            if ys.ndim == 2: return kernel.discrepancy_error(self.x,ys)
            N = len(ys)
            out = np.zeros(N)
            for n in range(N):
                y = ys[n]
                Dxy = np.sum( op.discrepancy_functional.Knm(x = self.x,y = y) )
                Dyy = np.sum( op.discrepancy_functional.Knm(x = y,y = y) )
                out[n] = self.Kxx-2.*Dxy+Dyy
            return out

    def projection(x,y,z,fx=[], **kwargs):

        projection_format_switchDict = { pd.DataFrame: lambda x,y,z,fx,**kwargs :  projection_dataframe(x,y,z,fx,**kwargs) }
        def projection_dataframe(x,y,z,fx=[],**kwargs):
            f_z = cd.op.projection(get_matrix(x),get_matrix(y),get_matrix(z),get_matrix(fx))
            if isinstance(fx,pd.DataFrame): f_z = pd.DataFrame(f_z,columns = fx.columns, index = z.index)
            return f_z

        set_codpy_kernel = kwargs.get('set_codpy_kernel',None)
        if set_codpy_kernel is not None: set_codpy_kernel()
        rescale = kwargs.get('rescale',False)
        if (rescale): kernel.rescale(x,y,z,**kwargs)
        type_debug = type(x)

        def debug_fun(x,y,z,fx,**kwargs):
            x,y,z,fx = get_matrix(x),get_matrix(y),get_matrix(z),get_matrix(fx)
            fz = cd.op.projection(x,y,z,fx)
            return fz

        method = projection_format_switchDict.get(type_debug,debug_fun)
        f_z = method(x,y,z,fx,**kwargs)
        if kwargs.get('save_cd_data',None) is not None:
            class Object:pass
            temp = Object
            temp.x ,temp.y,temp.z,temp.fx,temp.f_z,temp.fz = x ,y,z,fx,f_z,kwargs.get("fz",[])
            data_generator.save_cd_data(temp,**kwargs)
        return f_z

    def extrapolation(x,fx,z, set_codpy_kernel = None, rescale = False):
        return op.projection(x=x,y=x,z=z,fx=fx,set_codpy_kernel = set_codpy_kernel, rescale = rescale)
    def interpolation(x,z,fx, set_codpy_kernel = None, rescale = False):
        return op.projection(x=x,y=z,z=z,fx=fx,set_codpy_kernel = set_codpy_kernel, rescale = rescale)

    def norm(x,y,z,fx, set_codpy_kernel = None, rescale = False,**kwargs):
        if (set_codpy_kernel): set_codpy_kernel()
        if (rescale): kernel.rescale(x,y,z,**kwargs)
        return cd.tools.norm_projection(get_matrix(x),get_matrix(y),get_matrix(z),get_matrix(fx))

    def coefficients(x,y,fx, set_codpy_kernel = None, rescale = False,**kwargs):
        if (set_codpy_kernel): set_codpy_kernel()
        if (rescale): kernel.rescale(x,y,**kwargs)
        return cd.op.coefficients(get_matrix(x),get_matrix(y),get_matrix(fx))
    def Knm(x,y,set_codpy_kernel = None, rescale = False, **kwargs):
        if (set_codpy_kernel): set_codpy_kernel()
        if (rescale): kernel.rescale(x,y,**kwargs)
        return cd.op.Knm(get_matrix(x),get_matrix(y))
    def Dnm(x,y,set_codpy_kernel = None, rescale = False, **kwargs):
        if (set_codpy_kernel): set_codpy_kernel()
        if (rescale): kernel.rescale(x,y,**kwargs)
        distance = kwargs.get('distance',None)
        if distance is not None:
            return cd.op.Dnm(get_matrix(x),get_matrix(y),{'distance':distance})
        return cd.op.Dnm(get_matrix(x),get_matrix(y))

    def nabla_Knm(x,y,set_codpy_kernel = None, rescale = False,**kwargs):
        if (set_codpy_kernel): set_codpy_kernel()
        if (rescale): kernel.rescale(x,y,**kwargs)
        return cd.op.nabla_Knm(get_matrix(x),get_matrix(y))
    def Knm_inv(x,y,set_codpy_kernel = None, rescale = False,**kwargs):
        if (set_codpy_kernel): set_codpy_kernel()
        if (rescale): kernel.rescale(x,y,**kwargs)
        return cd.op.Knm_inv(get_matrix(x),get_matrix(y))
    def nabla(x,y,z,fx = [],reg = [],set_codpy_kernel = None, rescale = False,**kwargs):
        if (set_codpy_kernel): set_codpy_kernel()
        if (rescale): kernel.rescale(x,y,z,**kwargs)
        return cd.op.nabla(get_matrix(x),get_matrix(y),get_matrix(z),get_matrix(fx),get_matrix(reg))
    def nabla_inv(x,y,z,fz = [],set_codpy_kernel = None, rescale = False,**kwargs):
        if (set_codpy_kernel): set_codpy_kernel()
        if (rescale): kernel.rescale(x,y,z,**kwargs)
        return cd.op.nabla_inv(get_matrix(x),get_matrix(y),get_matrix(z),fz)
    def nablaT(x,y,z,fz = [], set_codpy_kernel = None, rescale = False,**kwargs):
        if (set_codpy_kernel): set_codpy_kernel()
        if (rescale): kernel.rescale(x,y,z,**kwargs)
        return cd.op.nablaT(get_matrix(x),get_matrix(y),get_matrix(z),fz)
    def nablaT_inv(x,y,z,fx = [], set_codpy_kernel = None, rescale = False,**kwargs):
        if (set_codpy_kernel): set_codpy_kernel()
        if (rescale): kernel.rescale(x,y,z,**kwargs)
        return cd.op.nablaT_inv(get_matrix(x),get_matrix(y),get_matrix(z),get_matrix(fx))
    def nablaT_nabla(x,y,fx=[], set_codpy_kernel = None, rescale = False,**kwargs):
        if (set_codpy_kernel): set_codpy_kernel()
        if (rescale): kernel.rescale(x,y,**kwargs)
        return cd.op.nablaT_nabla(get_matrix(x),get_matrix(y),get_matrix(fx))
    def nablaT_nabla_inv(x,y, fx= [], set_codpy_kernel = None, rescale = False,**kwargs):
        if (set_codpy_kernel): set_codpy_kernel()
        if (rescale): kernel.rescale(x,y,**kwargs)
        return cd.op.nablaT_nabla_inv(get_matrix(x),get_matrix(y),get_matrix(fx))
    def Leray_T(x,y,fx=[], set_codpy_kernel = None, rescale = False,**kwargs):
        if (set_codpy_kernel): set_codpy_kernel()
        if (rescale): kernel.rescale(x,y,**kwargs)
        return cd.op.Leray_T(get_matrix(x),get_matrix(y),fx)
    def Leray(x,y,fx, set_codpy_kernel = None, rescale = False,**kwargs):
        if (set_codpy_kernel): set_codpy_kernel()
        if (rescale): kernel.rescale(x,y,**kwargs)
        return cd.op.Leray(get_matrix(x),get_matrix(y),fx)
    def hessian(x,y,z,fx = None,**kwargs):
        import itertools
        # z = x
        indices = alg.distance_labelling(z,x)
        grad = op.nabla(x=x, y=y, z=x, **kwargs)
        N_X = x.shape[0]
        N_Z = z.shape[0]
        D = x.shape[1]
        gradT = np.zeros([N_X,D,N_X])
        def helper(d) :gradT[:,d,:] = grad[:,d,:].T.copy()
        [helper(d) for d in range(D)]
        if fx is not None: 
            # gradf = np.squeeze(op.nabla(x=x, y=y, z=x, fx=np.squeeze(fx),**kwargs))
            # spot_baskets = z[:,1]
            # thetas = gradf[:,0]
            # deltas = gradf[:,1]
            # multi_plot([[z,thetas],[z,deltas]],plotD,projection='3d',loc = 'upper left',prop={'size': 3},mp_ncols=2,**kwargs)
            out = np.zeros( [N_X, D,D, fx.shape[1]])
            for d in itertools.product(range(D), range(D)):
                debug = grad[:,d[1],:] @ get_matrix(fx)
                # multi_plot([[z,debug]],plotD,projection='3d',loc = 'upper left',prop={'size': 3},mp_ncols=2,**kwargs)
                mat = gradT[:,d[0],:]
                out[:,d[0], d[1],:]  = -mat @ debug
                # multi_plot([[z,out[:,d[0], d[1],:]]],plotD,projection='3d',loc = 'upper left',prop={'size': 3},mp_ncols=2,**kwargs)
            out = out[indices,:,:,:]
            # codpy_hessians = np.squeeze(out)
            # thetas = codpy_hessians[:,0,0]
            # gammas = codpy_hessians[:,1,1]
            # crossed = codpy_hessians[:,1,0]
            # multi_plot([[z,fx],[z,thetas],[z,gammas],[z,crossed]],plotD,projection='3d',loc = 'upper left',prop={'size': 3},mp_ncols=2,**kwargs)

            return out
        else: 
            hess = np.zeros( [N_X, D,D, N_X])
            for d in itertools.product(range(D), range(D)):
                hess[:,d[0], d[1],:]  = -gradT[:,d[0],:] @ grad[:,d[1],:]
                # test = hess[:,d[0]*D + d[1],:]
            return hess[indices,:,:,:]





class alg:
    from functools import partial
    #set_codpy_kernel = kernel_setters.kernel_helper(kernel_setters.set_gaussian_kernel, 2,1e-8,map_setters.set_min_distance_map)
    #set_sampler_kernel = kernel_setters.kernel_helper(kernel_setters.set_matern_tensor_kernel, 3,1e-8 ,map_setters.set_standard_mean_map)

    # def set_sampler_kernel(polynomial_order:int = 2,regularization:float = 0,set_map = map_setters.set_unitcube_map):
    #     import codpypyd as cd
    #     cd.kernel.set_polynomial_order(polynomial_order)
    #     cd.kernel.set_regularization(regularization)
    #     cd.set_kernel("tensornorm")
    #     map_setters.set_unitcube_map()
    #     if (polynomial_order > 0):
    #         kern = kernel.get_kernel_ptr()
    #         cd.set_kernel("linear_regressor")
    #         map_setters.set_unitcube_map()
    #         cd.kernel.pipe_kernel_ptr(kern)


    set_sampler_kernel = kernel_setters.kernel_helper(kernel_setters.set_matern_tensor_kernel, 0,1e-8 ,map_setters.set_standard_mean_map)
    set_isoprobas_kernel = kernel_setters.kernel_helper(kernel_setters.set_matern_tensor_kernel, 0,1e-8 ,map_setters.set_standard_mean_map)
    set_reordering_kernel = kernel_setters.kernel_helper(kernel_setters.set_matern_tensor_kernel, 2,1e-8,map_setters.set_standard_min_map)

    def reordering(x,y,**kwargs):
        reordering_format_switchDict = { pd.DataFrame: lambda x,y,**kwargs :  reordering_dataframe(x,y,**kwargs) }
        def reordering_dataframe(x,y,**kwargs):
            a,b,permutation = alg.reordering(x.values,y.values,**kwargs)
            x,y = pd.DataFrame(a,columns = x.columns, index = x.index),pd.DataFrame(b,columns = y.columns, index = y.index)
            return x,y,permutation
        def reordering_np(x,y,**kwargs):
            D = op.Dnm(x,y,**kwargs)
            lsap_fun = kwargs.get("lsap_fun",alg.scipy_lsap)
            # test = D.trace().sum()
            permutation = lsap_fun(D)
            # D = D[permutation]
            # test = D.trace().sum()
            x = x[permutation]
            return x,y,permutation
        type_debug = type(x)
        method = reordering_format_switchDict.get(type_debug,reordering_np)
        return method(x,y,**kwargs)

    def grid_projection(x,**kwargs):
        import xarray
        grid_projection_switchDict = { pd.DataFrame: lambda x,**kwargs :  grid_projection_dataframe(x),
                                        xarray.core.dataarray.DataArray: lambda x,**kwargs :  grid_projection_xarray(x) }
        def grid_projection_dataframe(x,**kwargs):
            out = cd.alg.grid_projection(x.values)
            out = pd.DataFrame(out,columns = x.columns, index = x.index)
            return out
        def grid_projection_xarray(x,**kwargs):
            index_string = kwargs.get("index","N")
            indexes = x[index_string]
            out = x.copy()
            for index in indexes:
                mat = x[index_string==int(index)].values
                mat = cd.alg.grid_projection(mat.T)
                out[index_string==int(index)] = mat.T
            return out
        def grid_projection_np(x,**kwargs):
            if x.ndim==3:
                shapes = x.shape
                x = format_32(x)
                out = cd.alg.grid_projection(x,**kwargs)
                out = format_23(out,shapes)
                return out
            else: return cd.alg.grid_projection(get_matrix(x),**kwargs)
        type_debug = type(x)
        method = grid_projection_switchDict.get(type_debug,lambda x : grid_projection_np(x,**kwargs))
        return method(x)


    def scipy_lsap(C):
        from scipy.optimize import linear_sum_assignment
        N = C.shape[0]
        D = np.min((N,C.shape[1]))
        permutation = linear_sum_assignment(C, maximize=False)
        out = np.array(range(0,D))
        for n in range(0,D):
            out[permutation[1][n]] = permutation[0][n]
        return out
    def lsap(x):
        return cd.alg.LSAP(x)
    def get_xyz(fx,**kwargs):
        seed = kwargs.get("seed",42)
        rand = kwargs.get("random_sample",np.random.random_sample)
        grid_projection = kwargs.get("grid_projection",False)
        Nx = kwargs.get("Nx",fx.shape[0])
        Ny = kwargs.get("Ny",Nx)
        Nz = kwargs.get("Nz",Nx)
        if kwargs.get('sample_times',False) : Nz= Nz*len(kwargs.get('sample_times'))
        shape = [fx.shape[0],fx.shape[1]]
        np.random.seed(seed)
        x = rand(shape)
        shape[0] = Nz
        z = rand(shape)
        y = x
        if Ny >0: y = y[:Ny]
        if grid_projection: y = alg.grid_projection(y)
        if (kwargs.get("reordering",True)): 
            y,fy,permutation = alg.reordering(y,fx[:Ny],**kwargs)
            x[:Ny]=y

        if Nx==Ny: return y,y,z
        return x,y,z
        

    def sampler(fx, M:int,x= None, y = None, z= None,  seed = 42, **kwargs):
        if isinstance(fx,pd.DataFrame): 
            out,x,y,z = alg.sampler(get_matrix(fx),M=M,x=x,y=y,z=z,seed=seed,**kwargs)
            return pd.DataFrame(out,columns = fx.columns),x,y,z
        from reordering import reordering_plot 
        # test = np.random.randint(fx.shape[0],size = M)
        # return fx[test]
        if x is None or z is None or y is None:
            getxyz = kwargs.get('getxyz',alg.get_xyz)
            x,y,z = getxyz(fx,**kwargs)
            # x=y
            return alg.sampler(fx=fx,M=M,x=x,y=y,z=z,seed=seed,**kwargs)
        # xp,fx,permutation = alg.reordering(x,fx,**kwargs)
        # reordering_plot(x,fx,xp,fx,plot_fun = graph_plot)
        Nx = fx.shape[0]
        Ny = y.shape[0]

        if Nx >Ny: 
            # x[Ny:]= op.projection(x = fx[:Ny],y = fx[:Ny],z = fx[Ny:], fx = y,**kwargs)
            D = op.Dnm(x[Ny:],y,**kwargs)
            permutation = softminindice(D)
            fx[Ny:] = fx[permutation]
            # x,fx = x[:Ny],fx[:Ny]
        if kwargs.get('nablainv',False):
            fy = fx[:Ny]
            fz = op.nabla_inv(y,y,y,fy.reshape(fy.shape + (1,)),**kwargs)
            fz = op.nabla(x = y,y = y,z = z, fx = fz,**kwargs)
            fz = fz.squeeze()
        else:
            fz= op.projection(x = x,y = y,z = z, fx = fx,**kwargs)
            # nabla = op.nabla(x = x,y = x,z = x, fx = nabla_inv,**kwargs)
            # Leray = fxreshape - nabla
            # Leray = Leray.squeeze()
            # Leray= op.projection(x = x,y = x,z = z, fx = Leray,**kwargs) 
            # fz = Leray + nabla
            # multi_plot([(x,fx),(z,fz)],plot_trisurf,mp_ncols = 2, projection='3d',mp_max_items = -1, f_names=["x,fx","z,fz"])
        return fz,x,y,z



    def iso_probas_projection(x, fx, probas, fun_permutation = lexicographical_permutation, set_codpy_kernel = set_isoprobas_kernel, rescale = True,**kwargs):
        # print('######','iso_probas_projection','######')
        Nx,Dx = np.shape(x)
        Nx,Df = np.shape(fx)
        Ny = len(probas)
        fy,y,permutation = fun_permutation(fx,x)
        out = np.concatenate((y,fy), axis = 1)
        quantile = np.array(np.arange(start = .5/Nx,stop = 1.,step = 1./Nx)).reshape(Nx,1)
        out = op.projection(x = quantile,y = probas,z = probas, fx = out, set_codpy_kernel = set_codpy_kernel, rescale = rescale)
        return out[:,0:Dx],out[:,Dx:],permutation

    def Pi(x, z, fz=[], set_codpy_kernel = set_sampler_kernel, rescale = True,nmax=10,**kwargs):
        # print('######','Pi','######')
        if (set_codpy_kernel): set_codpy_kernel()
        if (rescale): kernel.rescale(x,z)
        out = cd.alg.Pi(x = x,y = x,z = z, fz = fz,nmax = nmax)
        return out
    def get_normals(N,D, **kwargs):
        set_codpy_kernel = kwargs.get('set_codpy_kernel',kernel_setters.kernel_helper(kernel_setters.set_sumnorm_kernel, 0,0,map_setters.set_unitcube_map))
        nmax = kwargs.get('nmax',10)
        # print('######','Pi','######')
        if (set_codpy_kernel): set_codpy_kernel()
        out = cd.alg.get_normals(N = N,D = D,nmax = nmax)
        return out
    def match(x, Ny, **kwargs):
        match_format_switchDict = { pd.DataFrame: lambda x,Ny,**kwargs :  match_dataframe(x,Ny,**kwargs) }
        def match_dataframe(x, Ny,**kwargs):
            out=alg.match(get_matrix(x),Ny,**kwargs)
            return pd.DataFrame(out,columns = x.columns)

        def debug_fun(x,Ny,**kwargs):
            if 'sharp_discrepancy:xmax' in kwargs: x= random_select_interface(x,xmaxlabel = 'sharp_discrepancy:xmax', seedlabel = 'sharp_discrepancy:seed',**kwargs)
            if 'set_codpy_kernel' in kwargs : kwargs['set_codpy_kernel']()
            if kwargs.get('rescale',False) : kernel.rescale(x,**kwargs) 
            out = cd.alg.match(x,Ny)
            return out
        type_debug = type(x)
        method = match_format_switchDict.get(type_debug,debug_fun)
        out = method(x,Ny,**kwargs)
        return out

    def sharp_discrepancy(x, Ny=None, **kwargs):
        itermax = int(kwargs.get('sharp_discrepancy:itermax',10))
        if Ny is None: return cd.alg.sharp_discrepancy(x,kwargs['y'],itermax)
        sharp_discrepancy_format_switchDict = { pd.DataFrame: lambda x,Ny,**kwargs :  sharp_discrepancy_dataframe(x,Ny,**kwargs) }
        def sharp_discrepancy_dataframe(x, Ny,**kwargs):
            out=alg.sharp_discrepancy(get_matrix(x),Ny,**kwargs)
            return pd.DataFrame(out,columns = x.columns)


        def debug_fun(x,Ny,**kwargs):
            out = alg.match(x,Ny,**kwargs)
            out = cd.alg.sharp_discrepancy(x,out,itermax)
            return out
        type_debug = type(x)
        method = sharp_discrepancy_format_switchDict.get(type_debug,debug_fun)
        out = method(x,Ny,**kwargs)
        return out

    def distance_labelling(x, y, axis=1,**kwargs):
        # print('######','distance_labelling','######')
        D = op.Dnm(x=x,y=y,**kwargs)
        return softminindice(D,axis=axis)

    def taylor_expansion(x, y, z, fx, nabla = op.nabla, hessian = op.hessian, **kwargs):
        # print('######','distance_labelling','######')
        x,y,z,fx = get_matrix(x),get_matrix(y),get_matrix(z),get_matrix(fx)
        xo,yo,zo,fxo = x,y,z,fx
        indices = kwargs.get("indices",[])
        if len(indices) != z.shape[0] :
            indices = alg.distance_labelling(x,z,axis=0,**kwargs)
        xo= x[indices]
        fxo= fx[indices]
        deltax = get_data(z - xo)
        taylor_order = int(kwargs.get("taylor_order",1))
        results = kwargs.get("taylor_explanation",None)
        if taylor_order >=1:
            grad = nabla(x=x, y=y, z=x, fx=fx, **kwargs)
            if grad.ndim >= 3:  grad= get_matrix(np.squeeze(grad))
            if grad.ndim == 1:  grad= get_matrix(grad).T
            if len(indices) : grad = grad[indices]
            # print("grad:",grad[0])
            product_ = np.reshape([np.dot(grad[n],deltax[n]) for n in range(grad.shape[0])],(len(grad),1))
            f_z = fxo  + product_
            if isinstance(fx,pd.DataFrame): f_z = pd.DataFrame(f_z, columns = fx.columns)
            if results is not None:
                results["indices"] = indices
                results["delta"] = deltax
                results["nabla"] = grad

        if taylor_order >=2:
            hess = hessian(x=x, y=x, z=x, fx=fx, **kwargs)
            if len(indices) : hess = hess[indices]
            deltax = np.reshape([np.outer(deltax[n,:],deltax[n,:]) for n in range(deltax.shape[0])], (hess.shape[0],hess.shape[1],hess.shape[2]))
            quadratic_form = np.reshape([np.trace( hess[n].T@deltax[n] ) for n in range(hess.shape[0])], (hess.shape[0],1))
            f_z += 0.5*quadratic_form
            if results is not None:
                results["quadratic"] = deltax
                results["hessian"] = hess
        return f_z

class FD:
    def nabla(x,fun,set_fun=None,**kwargs): 
        import numdifftools.nd_scipy as nd
        if isinstance(x,list): return [FD.nabla(x=x[n],fun=fun,**kwargs) for n in range(0,x.shape[0])]
        if set_fun is None: set_fun = lambda x,**k : k
        if x.ndim == 2 : 
            return np.concatenate([FD.nabla(x=x[n],fun=fun,set_fun=set_fun,**kwargs) for n in range(0,x.shape[0])], axis = 0)
        def lambda_helper(x,**kwargs):
            k = set_fun(x=x,**kwargs)
            out = fun(**k)
            return out
        out = nd.Gradient(lambda_helper)(x,**kwargs)
        # print("grad:",get_matrix(out).T)
        return get_matrix(out).T

    def hessian(x,fun,**kwargs): 
        import numdifftools.nd_scipy as nd
        # if fun == None: fun = option_param.price
        if isinstance(x,list): return [FD.hessian(x=x[n],fun=fun,**kwargs) for n in range(0,value.shape[0])]
        if x.ndim == 2 : 
            out = np.array([FD.hessian(x=x[n],fun=fun,**kwargs) for n in range(0,x.shape[0])])
            return out
        def hessian_helper(x,**kwargs):
            out = FD.nabla(x=x,fun=fun,**kwargs)
            out = np.squeeze(out)
            return out

        out = nd.Jacobian(hessian_helper)(x=x,**kwargs)
        # print("grad:",get_matrix(out).T)
        return out.T

    def nablas(fun, x,**kwargs): 
        copy_kwargs = copy.deepcopy(kwargs)
        # copy_kwargs = kwargs.copy()
        def helper(v): return FD.nabla(fun = fun, x = v,**copy_kwargs) 
        if isinstance(x,list): out = [helper(v) for v in get_matrix(x)]
        elif isinstance(x,np.ndarray): 
            if x.ndim == 1: return helper(x)
            out = [helper(x[n]) for n in range(0,x.shape[0]) ]
        elif isinstance(x,pd.DataFrame): return FD.nablas(fun=fun,x= x.values,**copy_kwargs)
        out = np.array(out).reshape(values.shape)
        return out

    def hessians(fun, x,**kwargs): 
        copy_kwargs = copy.deepcopy(kwargs)
        # copy_kwargs = kwargs.copy()
        def helper(v): return FD.hessian(fun = fun, x = v,**copy_kwargs) 
        if isinstance(x,list): out = [helper(v) for v in get_matrix(x)]
        elif isinstance(x,np.ndarray): 
            if x.ndim == 1: return helper(x)
            out = [helper(x[n]) for n in range(0,x.shape[0]) ]
        elif isinstance(x,pd.DataFrame): return FD.hessians(fun=fun,x= x.values,**copy_kwargs)
        out = np.array(out).reshape(x.shape[0],x.shape[1],x.shape[1])
        return out



class AAD:
    def gradient(fx, x, grad_outputs=None,**kwargs):
        import torch as torch
        if not isinstance(x,torch.Tensor) : 
            x = torch.tensor(x, requires_grad=True)
        if x.dim() == 1 : 
            out = torch.autograd.functional.jacobian(fx,x)
            return out
        N,D = x.shape[0],x.shape[1]
        out = [get_matrix(torch.autograd.functional.jacobian(fx,y)) for y in x]
        return np.asarray(out)

    def taylor_expansion(x, z, fx, order = False,**kwargs):
        # print('######','distance_labelling','######')
        xo,zo,fxo = get_matrix(x),get_matrix(z),get_matrix(fx(x))
        indices = kwargs.get("indices",[])
        if len(indices) != z.shape[0] :
            indices = alg.distance_labelling(x,z,axis=0,**kwargs)
        xo= xo[indices]
        fxo= fxo[indices]
        deltax = zo - xo
        order = int(kwargs.get("taylor_order",1))
        results = kwargs.get("taylor_explanation",None)
        if order >=1:
            grad = AAD.gradient(fx=fx, x=x, **kwargs)
            if grad.ndim==1:
                out = np.zeros(deltax.shape)
                def helper(n):out[n] = grad 
                [helper(n) for n in range(0,deltax.shape[0])]
                grad = out
            else:
                grad = np.squeeze(grad)
                if len(indices) : grad = grad[indices].reshape(deltax.shape)
            product_ = np.reshape([np.dot(grad[n],deltax[n]) for n in range(grad.shape[0])],(len(grad),1))
            f_z = get_matrix(fxo)  + product_
            if results is not None:
                results["delta"] = deltax
                results["nabla"] = grad

        if order >=2:
            Nx,D,Df = x.shape[0],x.shape[1],fxo.shape[1]
            hess = AAD.hessian(fx =fx, x=x, **kwargs)
            if len(indices): hess = hess[indices]
            deltax = np.reshape([np.outer(deltax[n,:],deltax[n,:]) for n in range(deltax.shape[0])], (hess.shape[0],hess.shape[1],hess.shape[2]))
            quadratic_form = np.reshape([np.trace( hess[n].T@deltax[n] ) for n in range(hess.shape[0])], (hess.shape[0],1))
            f_z += 0.5*quadratic_form
            if results is not None:
                results["quadratic"] = deltax
                results["hessian"] = hess
        return f_z

    def nabla(x,y,z,fx, grad_outputs=None,**kwargs):
        import torch as torch
        if grad_outputs is None:
            grad_outputs = torch.ones_like(y)
        grad = torch.autograd.grad(y, [x], grad_outputs = grad_outputs, create_graph=True)[0]
        if x.shape[0] == z.shape[0] : return grad
        indices = alg.distance_labelling(x,z,**kwargs)
        x= x[indices]
        fx= fx[indices]

        return grad[indices]

    def jacobian(y, x):
        import torch as torch
        jac = torch.zeros(y.shape[0], x.shape[0]) 
        for i in range(y.shape[0]):
            grad_outputs = torch.zeros_like(y)
            grad_outputs[i] = 1
            jac[i] = gradient(y, x, grad_outputs = grad_outputs)
        return jac

    def jacobianBatch(f, wrt):
        import torch as torch
        jacobian = []
        for i in range(wrt.shape[0]):
            jac = torch.autograd.functional.jacobian(f, wrt[i])
            jacobian.append(jac)
        return torch.stack(jacobian, 0)

    def hessian(fx,x,**kwargs):
        import torch as torch
        import torch as torch
        Nx,D = x.shape[0],x.shape[1]
        if not isinstance(x,torch.Tensor) : 
            x = torch.tensor(x, requires_grad=True)
        def hessian_helper(y):
            mat = torch.autograd.functional.hessian(func=fx,inputs= y)
            return get_matrix(mat)
        out = [hessian_helper(y= y.clone().detach().requires_grad_(True)) for y in x]
        return np.asarray(out)

    def divergence(y, x,**kwargs):
        import torch as torch
        div = 0.
        for i in range(y.shape[-1]):
            div += torch.autograd.grad(y[..., i], x, torch.ones_like(y[..., i]), create_graph=True)[0][..., i:i+1]
        return div

    def laplace(y, x,**kwargs):
        grad = gradient(y, x)
        return divergence(grad, x)

########################################### Auxiliary functions

get_date_switchDict = { str: lambda x,**kwargs :  datetime.datetime.strptime(x, kwargs.get('date_format','%d/%m/%Y')),
                        datetime.date:lambda x,**kwargs : x,
                        int : lambda x,**kwargs : get_date(datetime.date.fromordinal(x)),
                        float : lambda x,**kwargs : get_date(int(x)),
                        np.float64 : lambda x,**kwargs : get_date(int(x)),
                        pd._libs.tslibs.timestamps.Timestamp : lambda x,**kwargs : pd.to_datetime(x),
                        torch.Tensor : lambda x,**kwargs: get_date(get_float(x)),
                        datetime.datetime: lambda x,**kwargs: x,
                    }
def get_date(x,**kwargs):
    if isinstance(x,list): return [get_date(n) for n in x]
    type_debug = type(x)
    method = get_date_switchDict.get(type_debug,None)
    return method(x,**kwargs)



get_data_switchDict = { pd.DataFrame: lambda x :  x.values,
                        pd.Series: lambda x : np.array(x.array, dtype= 'float'),
                        torch.Tensor: lambda x : x.detach().numpy(),
                        tuple: lambda xs : [get_data(x) for x in xs],
                        xarray.core.dataarray.DataArray: lambda xs : get_data(xs.values) 
                    }
def get_data(x):
    type_debug = type(x)
    method = get_data_switchDict.get(type_debug,lambda x: np.asarray(x,dtype='float'))
    return method(x)

get_float_switchDict = {
                        QuantLib.QuantLib.Date: lambda x, **kwargs: get_float(datetime.datetime(x.year(), x.month(), x.dayOfMonth())),
                        pd.DataFrame: lambda x, **kwargs: get_data(x), 
                        pd._libs.tslibs.timedeltas.Timedelta: lambda x, **kwargs: float(x/datetime.timedelta(days=1)), 
                        pd._libs.tslibs.timestamps.Timestamp : lambda x, **kwargs: get_float(x.date(), **kwargs), 
                        pd._libs.tslibs.nattype.NaTType : lambda x, **kwargs: np.nan,
                        pd.core.indexes.base.Index : lambda x, **kwargs: get_float(x.tolist(), **kwargs),
                        pd.core.series.Series : lambda x, **kwargs: get_float(x.tolist(), **kwargs),
                        pd.core.indexes.datetimes.DatetimeIndex: lambda x, **kwargs: get_float(x.tolist(), **kwargs),
                        pd.Float64Index:lambda x, **kwargs: get_float(x.tolist(), **kwargs),
                        datetime.date :lambda x, **kwargs: float(x.toordinal()), 
                        datetime.datetime: lambda x, **kwargs: x.toordinal(),
                        datetime.timedelta: lambda x, **kwargs: x/datetime.timedelta(days=1), 
                        list: lambda x, **kwargs:  [get_float(z, **kwargs) for z in x], 
                        type({}.keys()) : lambda x, **kwargs: get_float(list(x), **kwargs),
                        type({}.values()) : lambda x, **kwargs: get_float(list(x), **kwargs),
                        str: lambda x, **kwargs: get_float(get_date(x.replace(',','.'),**kwargs),**kwargs),
                        np.array : lambda x, **kwargs: np.array([get_float(z, **kwargs) for z in x]),
                        np.ndarray : lambda x, **kwargs: np.array([get_float(z, **kwargs) for z in x]),
                        xarray.core.dataarray.DataArray: lambda xs, **kwargs : get_float(xs.values),                        
                        }
def get_float_nan(x, **k):
    if isinstance(x,list):return [get_float_nan(y,**k) for y in x]
    if isinstance(x,np.ndarray):return [get_float_nan(y,**k) for y in x]
    out = float(x)
    # out = np.array(x, dtype=float)
    nan_val = k.get("nan_val",np.nan)
    if pd.isnull(out) : 
        out = nan_val
    return out

def get_float(x, **kwargs):
    type_ = type(x)
    method = get_float_switchDict.get(type_,lambda x, **k : get_float_nan(x,**k))
    out = get_float_nan(method(x,**kwargs),**kwargs)
    return out

my_len_switchDict = {list: lambda x: len(x),
                    pd.core.indexes.base.Index  : lambda x: len(x),
                    np.array : lambda x: len(x),
                    np.ndarray : lambda x: x.size
                    }


def my_len(x):
    if is_primitive(x):return 0
    type_ = type(x)
    method = my_len_switchDict.get(type_,lambda x : 1)
    return method(x)

def tensor_vectorize(fun, x):
    N,D = x.shape[0],x.shape[1]
    E = len(fun(x[0]))
    out = np.zeros((N, E))
    for n in range(0, N):
        out[n] = fun(x[n])
    return out.reshape(N,E,1)

def matrix_vectorize(fun, x):
    N,D = x.shape[0],x.shape[1]
    out = np.zeros((N, 1))
    def helper(n) : out[n,0] = fun(x[n])
    [helper(n) for n in range(0, N)]
    return out


def data_gen(N, D = None, x=None, fun = None, nabla_fun = None, type = "sto", mins=[],maxs=[],**kwargs):
    import numpy as np
    import itertools as it

    if D==None: D = x.shape[1]
    sizez = (int(N**(1/D)) + 1) ** D

    if len(mins) != D: 
        if x is not None: mins = [np.min(get_matrix(x)[:,d]) for d in range(D)]
        else: mins = np.repeat(-1.,D)
    if len(maxs) != D: 
        if x is not None: maxs = [np.max(get_matrix(x)[:,d]) for d in range(D)]
        else: maxs = np.repeat(1.,D)

    #print('data_genMD.sizez:',sizez)
    #print('data_genMD.sizex:',sizex)

    if type == "sto":
        z = np.zeros([sizez,D])
        for d in range(0,D): z[:,d] = np.random.uniform(mins[d], maxs[d],sizez) 
    else:
        Dz = int(sizez**(1/D))
        z = np.linspace(mins[0],maxs[0], Dz)
        y = z
        for i in range(0, D-1):
            y = np.linspace(mins[i+1],maxs[i+1], Dz)
            z = tuple(it.product(z, y))
        z = np.reshape(z,(Dz*Dz,2))  

    fx, nabla_fx = None, None
    z,permutation = lexicographical_permutation(x=z)
    if isinstance(x, pd.DataFrame): z = pd.DataFrame(z,columns = x.columns)
    if fun is not None: fz = fun(z,**kwargs)
    else: return z
    if nabla_fun is not None: 
        nabla_fz = nabla_fun(z,**kwargs)
        return z,fz,nabla_fz
    else: return z,fz

primitive = (int, str, bool,np.float32,np.float64,float)
def is_primitive(thing):
    debug = type(thing)
    return isinstance(thing, primitive)

def get_matrix(x):
    if isinstance(x,list): return [get_matrix(y) for y in x]
    if isinstance(x,tuple): return [get_matrix(y) for y in x]
    x = get_data(x)
    if is_primitive(x) : return x
    dim = len(x.shape)
    if dim==2:return x
    if dim==1:return np.reshape(x,[len(x),1])
    if dim==0:return np.reshape(x,[1,1])

    raise AssertionError("projection accepts only matrix entries. len(x)="+str(dim))


def get_dictionnary(x, y):
    import numpy as np
    dic = {}
    switchDict = {np.ndarray: lambda x: x, pd.DataFrame: lambda x : x.data, pd.Series: lambda x : x.values}
    x_data = get_data(x)
    y_data = get_data(y)
    size_ = len(x_data)
    if size_ != len(y_data): raise AssertionError("map_array_inversion error, different length. len(x)="+len(x_data)," len(y)="+len(y_data))
    for i in np.unique(x_data):
        # find index of points in cluster
        index = np.where(x_data == i)
        value = list(y_data[index])
        dic[i] = max(value, key = value.count)

    return dic

def get_surjective_dictionnary(x, y):
    # return {X: Y for X, Y in zip(x, y)}
    dic = get_dictionnary(x, y)
    out = {}
    def helper(key,value): out[key] = value
    [helper(key,value) for key,value in dic.items()]
    return out

def remap(x, dic, missing_key_value = 0):
    switch_get_item = {np.ndarray: lambda item,dic: dic.get(item,missing_key_value)}
    get_item = switch_get_item[type(x)]
    return np.asarray([get_item(item,dic) for item in x])

def set_seed(seedlabel = 'seed',**kwargs):
    # print('######','sharp_discrepancy','######')
    if seedlabel in kwargs:
        seed = int(kwargs.get(seedlabel))
        np.random.seed(seed)


def random_select_ndarray(x,xmax,seed=0):
    if (len(x) > xmax):
        if seed: np.random.seed(seed)
        arr = np.arange(xmax)
        np.random.shuffle(arr)
        x = x[arr]
    return x

def random_select_dataframe(x,xmax,seed=0):
    if (len(x) > xmax):
        if seed: np.random.seed(seed)
        arr = np.arange(xmax)
        np.random.shuffle(arr)
        x = x.iloc[arr]
    return x


def random_select(x,xmax,seed=0):
    # print('######','sharp_discrepancy','######')
    if not len(x): return x
    test = type(x)
    switchDict = {np.ndarray: random_select_ndarray, pd.DataFrame: random_select_dataframe}
    if test in switchDict.keys(): return switchDict[type(x)](x,xmax,seed)
    else:
        raise TypeError("unknown type "+ str(test) + " in random_select")


def random_select_interface(x,xmaxlabel = 'xmax', seedlabel = 'xmaxseed',**kwargs):
    # print('######','sharp_discrepancy','######')
    seed = 0
    if xmaxlabel in kwargs: xmax = int(kwargs.get(xmaxlabel))
    else: return x
    if seedlabel in kwargs: seed = int(kwargs.get(seedlabel))
    return random_select(x=x,xmax = xmax,seed=seed)

def array_helper(x):
    if np.ndim(x) == 1:
        return np.reshape(len(x),1)
    return x

###################### wrappers for dataframes


def fun_extrapolation(x,fx,y,fy,z,fz, set_codpy_kernel = None, rescale = False):
    debug = op.projection(x = x,y = x,z = z, fx = fx,set_codpy_kernel=set_codpy_kernel,rescale = rescale)
    return get_classification_error(softmaxindice(fz),softmaxindice(debug))
def fun_discrepancy(x,fx,y,fy,z,fz, set_codpy_kernel = None, rescale = False):
    return 1.-op.discrepancy(x=x,z=z,set_codpy_kernel = set_codpy_kernel,rescale = rescale)
def fun_norm(x,fx,y,fy,z,fz, set_codpy_kernel = None, rescale = True):
    return op.norm(x=x,y=x,z=x,fx=fx,set_codpy_kernel = set_codpy_kernel,rescale = rescale)
def fun_projection(x,fx, y,fy,z,fz, set_codpy_kernel = None, rescale = True):
    debug = op.projection(x = x,y = y,z = z, fx = fx,set_codpy_kernel=set_codpy_kernel,rescale = rescale)
    return get_classification_error(softmaxindice(fz),softmaxindice(debug))

def fun_helper_base(**kwargs):
    set_codpy_kernel = kernel_setters.set_gaussian_kernel
    if 'set_codpy_kernel' in kwargs:
            set_codpy_kernel = kwargs['set_codpy_kernel']
    return set_codpy_kernel


def fun_helper_projection(**kwargs):
    set_codpy_kernel_ = fun_helper_base(**kwargs)
    x_,fx_, y_, fy_, z_, fz_ = kwargs['x'],kwargs['fx'],kwargs['y'],kwargs['fy'],kwargs['z'],kwargs['fz']
    out = fun_projection(x_,fx_,y_,fy_,z_,fz_, set_codpy_kernel = set_codpy_kernel)
    return out

def fun_helper_extrapolation(**kwargs):
    set_codpy_kernel = fun_helper_base(**kwargs)
    x_,fx_, z_,fz_ = kwargs['x'],kwargs['fx'],kwargs['z'],kwargs['fz']
    out = fun_extrapolation(x_,fx_,x_,fx_,z_,fz_,set_codpy_kernel = set_codpy_kernel)
    return out

def select_list_of_words(list,list_of_words):
    return [col for col in list if any(word in col for word in list_of_words) ]
def get_matching_cols(a,match):
    return [col for col in a.columns if match in col]
def get_starting_cols(a,match):
    return [col for col in a if any(col.startswith(m) for m in match)]

def flatten(list):
    import functools
    import operator
    return functools.reduce(operator.iconcat, list, [])

def variable_selector(x,y,z,fx,fz,error_fun,**kwargs):
    set_kernel = kwargs.get('set_kernel',None)
    rescale = kwargs.get('rescale',True)
    variable_selector_csv = kwargs.get('variables_selector_csv',[])

    def helper(xt,yt,zt,x,y,z,fx,fz,set_kernel,n):
        tempxt, tempyt, tempzt = get_matrix(x)[:,[n]],get_matrix(y)[:,[n]],get_matrix(z)[:,[n]]
        tempxt, tempyt, tempzt = np.concatenate([xt,tempxt], axis = 1),np.concatenate([yt,tempyt], axis = 1) ,np.concatenate( [zt,tempzt],axis = 1) 
        f_z = op.projection(x = tempxt,y = tempyt,z = tempzt, fx = fx,set_codpy_kernel = set_kernel, rescale = True)
        f_z = pd.DataFrame(data = f_z, columns = fx.columns)
        erreur = error_fun(fz, f_z)
        return erreur,f_z,tempxt, tempyt, tempzt
    
    xyzcolumns,variables_cols_keep,variables_cols_drop = list(x.columns),get_starting_cols(list(x.columns),kwargs.get('variables_cols_keep',[])),get_starting_cols(x.columns,kwargs.get('variables_cols_drop',[]))
    variables_indices_keep,variables_indices_drop = [xyzcolumns.index(col) for col in variables_cols_keep],[xyzcolumns.index(col) for col in variables_cols_drop]
    xt,yt,zt = x[variables_cols_keep],y[variables_cols_keep],z[variables_cols_keep]
    xt,yt,zt = get_matrix(xt),get_matrix(yt),get_matrix(zt)

    fxcolumns,values_cols_keep,values_cols_drop = list(fx.columns),get_starting_cols(fx.columns,kwargs.get('values_cols_keep',[])),get_starting_cols(fx.columns,kwargs.get('values_cols_drop',[]))
    if len(values_cols_keep): fxt,fzt = fx[values_cols_keep],fz[values_cols_keep]
    else: fxt,fzt = fx,fz
    values_indices_keep,values_indices_drop = [fxcolumns.index(col) for col in values_cols_keep],[fxcolumns.index(col) for col in values_cols_drop]

    test_indices = set(range(len(x.columns))) - set(variables_indices_keep) - set(variables_indices_drop)
    list_indices = list(test_indices)        
    erreurs = np.asarray([helper(xt,yt,zt,x,y,z,fxt,fzt,set_kernel,n)[0] for n in list_indices])
    erreurs, order = lexicographical_permutation(erreurs)
    best_erreur = erreurs[0]
    erreurs = list(np.repeat(best_erreur,len(values_indices_keep)))
    best_indice = list_indices[order[0]]
    erreur,f_z,xt, yt, zt = helper(xt,yt,zt,x,y,z,fx,fz,set_kernel,best_indice)
    erreurs.append(best_erreur)
    variables_indices_keep.append(best_indice)
    for n in order:
        index = list_indices[n]
        debug = xyzcolumns[n]
        if index not in variables_indices_keep:
            erreur,f_z,tempxt, tempyt, tempzt = helper(xt,yt,zt,x,y,z,fx,fz,set_kernel,index) 
            if erreur < best_erreur:
                out = f_z
                xt, yt, zt = tempxt, tempyt, tempzt
                best_erreur = erreur
                erreurs.append(best_erreur)
                variables_indices_keep.append(index)
    output = { 'keep_columns' : [xyzcolumns[n] for n in variables_indices_keep], 'errors' : erreurs}
    
    if len(variable_selector_csv): 
        csv_file = output.copy()
        csv_file['keep_columns'].insert(0,"NoNe") 
        csv_file['errors'].insert(0,error_fun(fz)) 
        pd.DataFrame(csv_file).to_csv(variable_selector_csv,sep = ';')
    return output['keep_columns']

ts_format_switchDict = { pd.DataFrame: lambda A,h,p,**kwargs :  ts_format_dataframe(A,h,p,**kwargs) }

def ts_format_np(A,h,p, **kwargs):
    dim = A.ndim
    if dim < 3:
        (first,second) = cd.tools.ts_format(get_matrix(A),h,p) 
        return (first,second)
    if dim == 3 :
        out = [A[n,:,:].T for n in range(A.shape[0])] #expected format is N = number of trajectory,D = Dim,T=number of time bucket, however ts_format suppose T,D
        out = parallel_task(out, lambda x:  ts_format_np(x,h,p,**kwargs),**kwargs)
        x,fx = [o[0] for o in out],[o[1] for o in out]
        N,Dx,Dfx = A.shape[0]*(A.shape[2] - h -p +1), A.shape[1]*h,A.shape[1]*p
        new_shapex,new_shapefx = (N,Dx),(N,Dfx)
        x,fx = np.reshape(x,new_shapex),np.reshape(fx,new_shapefx)
        pass
    return x,fx


def ts_format_dataframe(A,h,p, **kwargs):
    colsx, colsfx= [], []
    [ [colsx.append(col + str(n)) for col in A.columns] for n in range(0,h) ] 
    [ [colsfx.append(col + str(n)) for col in A.columns] for n in range(0,p) ] 

    ts_format_param = kwargs.get('ts_format',None)

    if ts_format_param is not None:
        x_csv = ts_format_param.get('x_csv',None)
        if x_csv is not None: x.to_csv(x_csv, sep = ';', index=False)
        fx_csv = ts_format_param.get('fx_csv',None)
        if fx_csv is not None: fx.to_csv(fx_csv, sep = ';', index=False)

    x,fx = ts_format_np(get_matrix(A),h,p,**kwargs)
    x,fx = pd.DataFrame(x,columns=colsx, index = A.index[:x.shape[0]]),pd.DataFrame(fx,columns=colsfx,index = A.index[h:fx.shape[0]+h])
    return x, fx

def ts_format_diff(A,h,p, **kwargs):
    A.values
    diff = A.diff(axis=0)
    diff.values
    diff = diff.dropna(axis = 'rows')
    x,fx = ts_format(A,h,p, **kwargs)
    diffx,difffx = ts_format(diff,h,p, **kwargs)
    return x.iloc[:-1,:], difffx

def ts_format(x,h,p, **kwargs):
    type_debug = type(x)
    method = ts_format_switchDict.get(type_debug,lambda x,h,p,**kwargs: ts_format_np(x,h,p,**kwargs))
    if method is not None: return method(x,h,p,**kwargs)


def hot_encoder(data_frame,cat_cols = []):
    # data_frame.to_csv (r'data_frame.csv', header=True)
    num_cols = set(data_frame.columns)
    if not len(cat_cols):
        num_dataframe = data_frame[num_cols].select_dtypes(include='number')
        cat_dataframe = data_frame.select_dtypes(exclude='number')
        num_cols = num_dataframe.columns
    else:
        num_cols.difference_update(cat_cols)
        num_dataframe = data_frame[num_cols].select_dtypes(include='number')
        cat_dataframe = data_frame[cat_cols]

    (cat_dataframe,cat_columns) = cd.tools.hot_encoder(cat_dataframe.to_numpy(),cat_dataframe.columns)
    cat_dataframe = pd.DataFrame(cat_dataframe, columns = cat_columns)
    if len(num_cols) :
        if not cat_dataframe.empty :
            cat_dataframe = pd.concat([num_dataframe,cat_dataframe], axis=1,join="inner")
        else :
            cat_dataframe = num_dataframe
    # cat_dataframe.to_csv (r'hot_encoder.csv', header=True)
    return cat_dataframe

def dataframe_discrepancy(df_x,df_z, set_codpy_kernel = None,rescale=True, max = 2000):
    if (set_codpy_kernel): set_codpy_kernel()
    x,z = format_df_xz_to_np(df_x,df_z)
    if (rescale): kernel.rescale(x,z)
    return cd.tools.discrepancy_error(x,z)

def dataframe_norm_projection(df_x:pd.DataFrame,df_z:pd.DataFrame,df_fx:pd.DataFrame, set_codpy_kernel = None, rescale=True, max = 2000):
    import numpy as np
    if (set_codpy_kernel): set_codpy_kernel()
    (x,z,fx,fx_columns) = format_df_to_np(df_x,df_z,df_fx)
    if (rescale): kernel.rescale(x,z)
    return cd.tools.norm_projection(x,x,z,fx)



def dataframe_extrapolation(df_x:pd.DataFrame,df_z:pd.DataFrame,df_fx:pd.DataFrame, set_codpy_kernel = kernel_setters.set_gaussian_kernel, rescale=True, max = 2000):
    import numpy as np
    set_codpy_kernel()
    (x,z,fx,fx_columns) = format_df_to_np(df_x,df_z,df_fx)
    if len(x) < max:
        fz = op.extrapolation(x=x,fx=fx,z=z,set_codpy_kernel=set_codpy_kernel,rescale=rescale)
    else:
        index  = np.random.choice(x.shape[0], size=max,replace = False)
        y = x[index]
        fz = op.projection(x=x,fx=fx,z=z,set_codpy_kernel=set_codpy_kernel,rescale=rescale)


    df_fz_format = pd.DataFrame(data = fz, columns=fx_columns)
    num_cols = df_fx._get_numeric_data().columns                          
    cat_cols=list(set(df_fx.columns) - set(num_cols))
    out = pd.DataFrame(columns=df_fx.columns)
    out[num_cols] = df_fz_format[num_cols]

    df_fz_format_cols = df_fz_format.columns

    for cat in cat_cols:
        list_col = [s for s in df_fz_format_cols if cat in s]
        list_cat = [str.split(s,':cat:')[-1] for s in list_col] 
        mat = df_fz_format[list_col].to_numpy()
        test = softmaxindice(mat)
        values = [list_cat[s] for s in test]
        out[cat] = values
    return out

def fun_helper_dataframe_extrapolation(**kwargs):
    set_codpy_kernel= fun_helper_base(**kwargs)
    df_x,df_fx, df_z, df_fz = kwargs['df_x'],kwargs['df_fx'],kwargs['df_z'],kwargs['df_fz']
    out = dataframe_extrapolation(df_x,df_z,df_fx, set_codpy_kernel=set_codpy_kernel)
    return get_dataframe_error(out,df_fz)
######################################################

#########################graphical utilities###################

########################################
def scatter_plot(param, **kwargs):
    scatter_params = kwargs.get("scatter_params",None)
    if scatter_params is None: scatter_params = ({'marker' : 'o','color' : 'blue'},{'marker' : 'o','color' : 'pink'})
    ax = kwargs.get("ax",None)
    x,y = get_matrix(param[0]),get_matrix(param[1])
    if ax is not None:
        ax.scatter(x[:,0], x[:,1], **scatter_params[0])
        ax.scatter(y[:,0], y[:,1], **scatter_params[1])
    else:
        plt.scatter(x[:,0], x[:,1], **scatter_params[0])
        plt.scatter(y[:,0], y[:,1], **scatter_params[1])

def graph_plot(param, **kwargs):
    scatter_plot(param, **kwargs)
    x,y = param[0],param[1]
    x,y = get_matrix(param[0]),get_matrix(param[1])
    N = min(len(x),len(y))
    plt.plot([y[0:N,0], x[0:N,0] ], [ y[0:N,1], x[0:N,1] ], linewidth=1,color = 'black')


def multiple_plot1D_fun(x,fx,title = 'Figure',labelx='fx-axis:',labely='fz-axis:',legend=[]):
    fig = plt.figure()
    if (len(x)):
        if (x.ndim == 1): x = x.reshape(len(x),1)
        if (fx.ndim == 1): fx = fx.reshape(len(fx),1)
        N,D = len(x), fx.shape[1]
        N = len(x)
        # print("N,D:",N,D)
        plotfx,plotx,permutation = lexicographical_permutation(fx,x)
        plotx = plotx.reshape(N)
        for i in range(D):
            curve = plotfx[:,i]
            plt.plot(plotx,curve,marker = 'o',ls='-',markersize=2)
    if (len(legend) != D):
        legend = []
        for i in range(D):
            legend.append('line plot '+str(i))
    plt.legend(legend)
    plt.title(title)
    plt.xlabel(labelx)
    plt.ylabel(labely)

def multiple_plot1D(x,fx,title = 'Figure',labelx='fx-axis:',labely='fz-axis:',legend=[]):
    multiple_plot1D_fun(flattenizer(x),flattenizer(fx),title,labelx,labely,legend)

def multiple_norm_error(x,fx,ord=None):
    N,D = fx.shape
    out = []
    if (len(x)):
        for i in range(D):
            out.append(np.linalg.norm(x-fx[:,i],ord))
    return out

def show_imgs(images, ax=None,**kwargs):
    j = 0
    if isinstance(images, list) :
        pixels = []
        for image in images:
            if not len(pixels): pixels = image
            else: pixels = np.concatenate( (pixels,image),axis=1)
        ax.imshow(pixels, cmap='gray')
    else: plt.imshow(images, cmap='gray')

def compare_plot_lists_ax(listxs, listfxs, ax, **kwargs):
    index = kwargs.get("index",0)
    labelx=kwargs.get("labelx",'x-units')
    fun_x=kwargs.get("fun_x",get_data)
    extra_plot_fun=kwargs.get("extra_plot_fun",None)
    labely=kwargs.get("labely",'f(x)-units')
    listlabels=kwargs.get("listlabels",[None for n in range(len(listxs))])
    listalphas=kwargs.get("alphas",np.repeat(1.,len(listxs)))
    xscale =kwargs.get("xscale",None)
    yscale =kwargs.get("yscale",None)
    figsize =kwargs.get("figsize",(2,2))
    loc =kwargs.get("loc",'upper left')
    prop =kwargs.get("prop",{'size': 6})


    for x,fx,label,alpha in zip(listxs, listfxs,listlabels,listalphas):
        plotx = fun_x(x)
        plotfx = get_data(fx)
        plotx,plotfx,permutation = lexicographical_permutation(plotx,plotfx,**kwargs)
        if extra_plot_fun is not None: extra_plot_fun(plotx,plotfx)
        ax.plot(plotx,plotfx,marker = 'o',ls='-',label= label, markersize=12 / len(plotx),alpha = alpha)
        ax.legend(prop={'size': 6})
    title = kwargs.get("title",'')
    ax.title.set_text(title)
    if yscale is not None: ax.set_yscale(yscale)
    if yscale is not None: ax.set_xscale(xscale)
    ax.title.set_text(title)
    ax.set_xlabel(labelx)
    ax.set_ylabel(labely)


    # if len(listlabels):
    #     for x,fx,label in zip(listxs, listfxs,listlabels):
    #         plotx,plotfx,permutation = lexicographical_permutation(x.flatten(),fx.flatten())
    #         ax.plot(plotx,plotfx,marker = 'o',ls='-',label= label)
    #         ax.legend()
    # else:
    #     for x,fx in zip(listxs, listfxs):
    #         plotx,plotfx,permutation = lexicographical_permutation(x.flatten(),fx.flatten())
    #         ax.plot(plotx,plotfx,marker = 'o',ls='-', markersize=12 / len(plotx))
    # ax.set_yscale(yscale)
    # ax.set_xscale(xscale)
    # ax.title.set_text(title)
    # ax.set_xlabel(labelx)
    # ax.set_ylabel(labely)

def compare_plot_lists(listxs, listfxs, ax = None,**kwargs):
    from matplotlib.dates import date2num
    if ax: return compare_plot_lists_ax(listxs, listfxs, ax, fun_axvspan = None, **kwargs)
    index = kwargs.get("index",0)
    labelx=kwargs.get("labelx",'x-units')
    fun_x=kwargs.get("fun_x",get_data)
    extra_plot_fun=kwargs.get("extra_plot_fun",None)
    labely=kwargs.get("labely",'f(x)-units')
    listlabels=kwargs.get("listlabels",[None for n in range(len(listxs))])
    listalphas=kwargs.get("alphas",np.repeat(1.,len(listxs)))
    xscale =kwargs.get("xscale",None)
    yscale =kwargs.get("yscale",None)
    figsize =kwargs.get("figsize",(2,2))
    Show = kwargs.get("Show",True)
    plt.figure(figsize=figsize)
    for x,fx,label,alpha in zip(listxs, listfxs,listlabels,listalphas):
        plotx = fun_x(x)
        plotfx = get_data(fx)
        plotx,plotfx,permutation = lexicographical_permutation(x=plotx,fx=plotfx,**kwargs)
        if extra_plot_fun is not None: extra_plot_fun(plotx,plotfx)
        plt.plot(plotx,plotfx,marker = 'o',ls='-',label= label, markersize=12 / len(plotx),alpha = alpha)
        plt.legend(prop={'size': 6})
    title = kwargs.get("title",'')
    plt.title(title)
    plt.xlabel(labelx)
    plt.ylabel(labely)
    if Show: plt.show()

def matrix_to_cartesian(x,fx):
    import numpy as np
    fx = fx.reshape((len(fx)))
    # print('matrix_to_cartesian:x:', x.shape)
    # print('matrix_to_cartesian:fx:', fx.shape)
    size = int(len(x)**(1/2))
    Xc = sorted(list(set(x[:,0])))
    Yc = sorted(list(set(x[:,1])))

    assert len(fx)==len(Xc)*len(Yc)
    X,Y = np.meshgrid(Xc,Yc)
    Z = np.zeros((len(Xc),len(Yc)))
    for i in range(len(fx)):
       indx = Xc.index(x[i,0])
       indy = Yc.index(x[i,1])
       Z[indx,indy] = fx[i]
       #Z[indx,indy] = x[i,0]+x[i,1]
       Y[indx,indy] = x[i,1]
       X[indx,indy] = x[i,0]
    #print('X:',X)
    #print('X.shape:',X.shape)
    #print('Y:',Y)
    #print('Y.shape:',Y.shape)
    #print('Z:',Z)
    #print('Z.shape:',Z.shape)
    return X,Y,Z
    
def multi_compare1D(x,fx, title = 'Figure',labelx='x-axis',labely='y-axis:',figsizex=6.4, figsizey=4.8, flip=True):
    if (len(x)):
        if (x.ndim == 1): x = x.reshape(len(x),1)
        D = x.shape[1]
        fig = plt.figure(figsize=(figsizex,figsizey))
        fig.suptitle(title)
        for d in np.arange(0,D): 
            if (flip):
                plotfx,plotx,permutation = lexicographical_permutation(fx.flatten(),x[:,d])
            else:
                plotfx,plotx,permutation = lexicographical_permutation(x[:,d],fx.flatten())
            plt.subplot(D, 1, d + 1)
            plt.plot(plotx,plotfx,marker = 'o',ls='-',label= labelx,markersize=2)
            plt.xlabel(labelx)
            plt.ylabel(labely + str(d))
    plt.show()

class fun_pca:
    pca = None
    def __call__(self, x):
        from sklearn.decomposition import PCA
        if not self.pca:
            self.pca = PCA()
            principal_components = self.pca.fit_transform(x)
        else: principal_components = self.pca.transform(x)
        return principal_components[:,0], principal_components[:,1]

def get_representation_function(**kwargs):
    fun = fun_pca()
    index1 = int(kwargs.get('index1',0))
    index2 = int(kwargs.get('index2',0))
    def fun_index(x):return x[:,index1], x[:,index2]
    if (index1 != index2): fun = fun_index
    return fun


def plotD(xfx,ax=None,**kwargs):
    x,fx=xfx[0],xfx[1]
    if isinstance(x,tuple):
        color = ['b','r','g','c','m','y','k','w']
        [plotD( (y,fy),ax,color = c,markersize = 2,**kwargs) for y,fy,c in zip(x,fx,color)]
    else: 
        if x.ndim == 1: return plot1D(xfx,ax,**kwargs)
        if x.shape[1] >= 2:return plot_trisurf(xfx,ax,**kwargs)
        if x.shape[1] == 1:return plot1D(xfx,ax,**kwargs)


def plot1D(xfx,ax=None,**kwargs):
    if isinstance(xfx,pd.DataFrame):return plot1D(xfx = xfx.values.T,ax=ax,**kwargs)
    x,fx=xfx[0],xfx[1]
    title = kwargs.get('title',"")
    suptitle = kwargs.get('suptitle',"")
    markersize = kwargs.get('markersize',3)
    markerfacecolor = kwargs.get('markerfacecolor','r')
    color  = kwargs.get('color','b')
    fmt = kwargs.get('fmt','-'+color+'o')
    if ax == None: fig, ax = plt.subplots()
    ax.title.set_text(suptitle)
    if (len(x)):
        plotx,plotfx,permutation = lexicographical_permutation(x=get_matrix(x),fx=get_matrix(fx),indexfx = 0)
        ax.plot(plotx.flatten(),plotfx.flatten(),fmt, markersize = markersize,markerfacecolor=markerfacecolor)
    title = kwargs.get("title",'')
    labelx=kwargs.get("labelx",'x-units')
    labely=kwargs.get("labely",'f(x)-units')
    plt.title(title)
    plt.xlabel(labelx)
    plt.ylabel(labely)

def get_ax_helper(ax,**kwargs):
    if ax is None:
        projection = kwargs.get('projection')
        fig = plt.figure()
        if len(projection): ax = fig.add_subplot(projection = projection)
        else: ax = fig.add_subplot()
    return ax



def plot_trisurf(xfx,ax,**kwargs):
    import numpy as np
    from math import pi
    from matplotlib import cm
    from matplotlib import pyplot as plt
    xp,fxp = xfx[0],xfx[1]
    x,fx=get_matrix(xp),get_matrix(fxp)
    if x.shape[1] > 2: fun = fun_pca()
    elif x.shape[1] == 2: fun = lambda x : [get_data(x)[:,0], get_data(x)[:,1]]

    suptitle = kwargs.get('suptitle',"")
    elev = kwargs.get('elev',90)
    azim = kwargs.get('azim',-100)
    linewidth  = kwargs.get('linewidth',None)
    antialiased  = kwargs.get('antialiased',False)
    cmap = kwargs.get('cmap',cm.jet)
    ax = get_ax_helper(ax,**kwargs)

    if len(fx)>0:
        X, Y = fun(x)
        Z = fx.flatten()

        ax.plot_trisurf(X, Y, Z, antialiased = antialiased, cmap = cmap, linewidth=linewidth)
        ax.view_init(azim = azim, elev = elev)
        ax.title.set_text(suptitle)
        if isinstance(xp,pd.DataFrame):
            ax.set_xlabel(xp.columns[0])
            ax.set_ylabel(xp.columns[1])
        if isinstance(fxp,pd.DataFrame):
            ax.set_zlabel(fxp.columns[0])

def plot2D_CartesianMesh(xfx,ax,**kwargs):
    import numpy as np
    from math import pi
    from matplotlib import cm
    from matplotlib import pyplot as plt
    x,fx=xfx[0],xfx[1]

    suptitle = kwargs.get('suptitle',"")
    elev = kwargs.get('elev',15)
    azim = kwargs.get('azim',-100)
    cmap = kwargs.get('cmap',cm.jet)

    if len(fx)>0:
        X, Y, Z = matrix_to_cartesian(x,fx)
        ax.plot_surface(X, Y, Z, cmap=cmap)
        ax.view_init(elev = elev, azim=azim)
        ax.title.set_text(suptitle)

def flattenizer(x):
    if is_primitive(x) : return x
    if (type(x) == type([])): 
        if len(x) == 1: return flattenizer(x[0])
        else:return [flattenizer(s) for s in x]
    if (type(x) == np.ndarray): 
        x = np.squeeze(x)
        return np.asarray([flattenizer(s) for s in x])
    s = []
    for n in range(0,x.ndim):
        if x.shape[n] > 1 : s.append(x.shape[n])
    if len(s): return x.reshape(s)
    return x
    

def plot_data_distribution(df_x,df_fx):
    from matplotlib import pyplot as plt
    import seaborn as sns
    nCol = df_x.columns.size
    # num_cols = df_x._get_numeric_data().columns                          
    # cat_cols=list(set(df_x.columns) - set(num_cols))
    # numerical_features = df_x[num_cols]
    fig = plt.figure(figsize=(12,18))
    for i in range(len(df_x.columns)):
        fig.add_subplot(nCol/4,4,i+1)
        sns.scatterplot(df_x.iloc[:, i],df_fx)
        plt.xlabel(df_x.columns[i])
    plt.tight_layout()
    plt.show()

def plot_data_correlation(df_x, thres = 0.8):
    from matplotlib import pyplot as plt
    import seaborn as sns
    num_correlation = df_x.select_dtypes(exclude='object').corr()
    plt.figure(figsize=(20,20))
    plt.title('High Correlation')
    sns.heatmap(num_correlation > thres, annot=True, square=True)
    plt.show()

def multi_plot(params ,fun_plot, **kwargs):
    max_items = kwargs.get('mp_max_items',min(len(params),4))
    if max_items == -1: max_items = len(params)
    title = kwargs.get('mp_title','')
    ncols = kwargs.get('mp_ncols',len(params))
    f_names = kwargs.get('f_names',["" for n in range(len(params)) ])
    fontsize = kwargs.get('fontsize',10)
    numbers = min(len(params),max_items)
    ncols = min(ncols,numbers)
    projection = kwargs.get('projection','')
    if numbers == 0:return
    j = 0
    nrows = max(round(numbers/ncols),1)
    figsize= kwargs.get('mp_figsize',(5, 2*nrows))
    fig = plt.figure(figsize = figsize)
    for param, f_name in zip(params, f_names):
        if len(projection): ax = fig.add_subplot(nrows,ncols,j+1, projection = projection)
        else: ax = fig.add_subplot(nrows,ncols,j+1)
        fun_plot(param,ax=ax,**kwargs )
        plt.title(f_name, fontsize=fontsize)
        
        j = j+1
        if j==ncols*nrows:break
    fig.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
    
    if title:    fig.suptitle(title, fontsize=12, fontweight='bold')
    
    plt.show()

#####################################################

################file utilities######################################
save_to_file_switchDict = { pd.DataFrame: lambda x,file_name,**kwargs :  x.to_csv(file_name,**kwargs),
                            list: lambda x,file_name,**kwargs :  [save_to_file(y,f) for y,f in zip(x,file_name)]
                    }

def save_to_file(x,file_name,**kwargs):
    type_debug = type(x)
    method = save_to_file_switchDict.get(type_debug,lambda x,file_name,**kwargs: save_to_file(pd.DataFrame(x),file_name,**kwargs))
    return method(x,file_name,**kwargs)


def find_helper(pathname, matchFunc = os.path.isfile):
    import sys,os
    import errno
    for dir in sys.path:
        candidate = os.path.join(dir,pathname)
        # print(candidate)
        if matchFunc(candidate):
            return candidate
    raise FileNotFoundError(errno.ENOENT,os.strerror(errno.ENOENT),pathname)

def find_dir(pathname):
    return find_helper(pathname, matchFunc = os.path.isdir)

def find_file(pathname):
    return find_helper(pathname)

def files_indir(dirname,extension=""):
    out=[]
    for root, directories, files in os.walk(dirname):
        for file in files:
            if not len(extension):out.append(os.path.join(root,file))
            else: 
                if(file.endswith(".png")):
                    out.append(os.path.join(root,file))
    return out

## multiprocessing utilities
# 
def parallel_task(param_list,fun,**kwargs):
    import multiprocessing as mp
    import shutil
    import concurrent.futures
    from tqdm import tqdm
    debug = kwargs.get('debug',True)
    if debug: return [fun(p) for p,i in zip(param_list,tqdm (range (len(param_list)), desc="parallel…", ascii=False, ncols=75))]
    if len(param_list) < 2: return [fun(p) for p in param_list]
    cores = min(mp.cpu_count(),len(param_list))

    out = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=cores) as executor:
        results = executor.map(fun, param_list, chunksize= max(int( len(param_list)/cores),1) )
        for result,i in zip(results,tqdm (range (len(param_list)), desc="parallel…", ascii=False, ncols=75)) :        
            out.append(result)

    # pool = mp.Pool(cores)
    # out = pool.map(fun, param_list)
    # pool.close()
    # pool.join()
    return out
          

def elapsed_time(fun,msg="elapsed_time in seconds:",**kwargs):
    start = time.time()
    out = fun(**kwargs)
    print(msg,time.time()-start)
    return out

def execution_time(**kwargs):
    import time
    start_time = time.time()
    out = execute_function_list(**kwargs)
    msg = 'time in seconds:'
    if 'msg' in kwargs:
        msg = kwargs['msg']
    print("*********execution time***********",msg,time.time() - start_time)
    return out

def df_intersect_concat(df_x:pd.DataFrame,df_z:pd.DataFrame):
    import pandas as pd
    cols = list( set(df_x.columns) & set(df_z.columns))
    out = pd.concat([df_x[cols],df_z[cols]], ignore_index=True)
    return out

def format_df_xz_to_np(df_x:pd.DataFrame,df_z:pd.DataFrame):
    
    import numpy as np
    df_xz = df_intersect_concat(df_x,df_z)
    df_xz_format = hot_encoder(df_xz)
    df_xz_format = df_xz_format.dropna()
    np_xz = df_xz_format.to_numpy()
    x = np_xz[:len(df_x)]
    z = np_xz[len(df_x):]
    return x,z


def format_df_to_np(df_x:pd.DataFrame,df_z:pd.DataFrame,df_fx:pd.DataFrame):
    import numpy as np
    x,z = format_df_xz_to_np(df_x,df_z)
    df_fx_format = hot_encoder(df_fx)
    fx = df_fx_format.to_numpy()
    columns = df_fx_format.columns
    return x,z,fx,columns


def get_train_test(datas,train_size=0.5, random_state=42, id_key = "ID_PERS"):
    from sklearn.model_selection import train_test_split
    from sklearn.datasets import make_blobs
    ids = list(get_ids(datas,id_key))
    ids_train, ids_test = train_test_split(ids, train_size = train_size, random_state = random_state)
    return datas.loc[datas[id_key].isin(ids_train)], datas.loc[datas[id_key].isin(ids_test)]

def column_selector(x,**kwargs):
    if isinstance(x,list):return [column_selector(y,**kwargs) for y in x]
    cols_drop = get_starting_cols(x.columns,kwargs.get('cols_drop',[]))
    cols_keep = get_starting_cols(x.columns,kwargs.get('cols_keep',[]))
    x0 = x
    if len(cols_drop):
        x0 = x0.drop(cols_drop,axis=1)
    if len(cols_keep):
        x0 = x0[cols_keep]
    return x0

def raw_data_column_selector(xs,**kwargs):
    if isinstance(xs,list): return [get_data_column_selector(x,**kwargs) for x in xs]
    params = data_generator.get_params(**kwargs)
    variables_cols_keep = params.get('variables_cols_keep',[])
    variables_cols_drop = params.get('variables_cols_drop',[])
    return column_selector(xs,cols_drop = variables_cols_drop, cols_keep = variables_cols_keep)



######################## Benchmark tools
# A generic multi-dimensional function

def my_fun(x):
    import numpy as np
    from math import pi
    coss = np.cos(2 * x * pi)
    if x.ndim == 1 : 
        coss = np.prod(coss, axis=0)
        ress = np.sum(x, axis=0)
    else : 
        coss = np.prod(coss, axis=1)
        ress = np.sum(x, axis=1)
    return ress+coss

def nabla_my_fun(x):
    import numpy as np
    from math import pi
    sinss = np.cos(2 * x * pi)
    if x.ndim == 1 : 
        sinss = np.prod(sinss, axis=0)
        D = len(x)
        out = np.ones((D))
        def helper(d) : out[d] += 2.* sinss * pi*np.sin(2* x[d] * pi) / np.cos(2 * x[d] * pi)
        [helper(d) for d in range(0,D)]
    else:
        sinss = np.prod(sinss, axis=1)
        N = x.shape[0]
        D = x.shape[1]
        out = np.ones((N,D))
        def helper(d) : out[:,d] += 2.* sinss * pi*np.sin(2* x[:,d] * pi) / np.cos(2 * x[:,d] * pi)
        [helper(d) for d in range(0,D)]
    return out




class data_generator(abc.ABC):
    index = []
    def get_index(self):
        return self.index
    index_z = []
    def get_index_z(self):
        if not len(self.index_z):
            self.index_z = [str(i) for i in range(0,len(self.fz))]
        return self.index_z

    @abc.abstractmethod
    def get_data(self,D=0,Nx=0,Ny=0,Nz=0,**kwargs):
        pass

    def id(self,name = "data_generator"):
        return name


    def set_data(self,D=0,Nx=0,Ny=0,Nz=0,**kwargs):
        self.D,self.Nx,self.Ny,self.Nz,self.Df = int(D),int(Nx),int(Ny),int(Nz),0
        self.x,self.y,self.z,self.fx,self.fy,self.fz,self.dfx,self.dfz = [],[],[],[],[],[],[],[]
        self.map_ids = []
        if self.Ny >0 & self.Nx >0 : self.Ny = min(self.Ny,self.Nx)
        def crop(x,Nx):
            if isinstance(x,list):return [crop(y,Nx) for y in x]
            if (Nx>0 and Nx < x.shape[0]):return x[:Nx]
            return x

        if abs(Nx)*abs(Ny)*abs(Nz) >0:
            self.x, self.fx, self.y, self.fy, self.z, self.fz = self.get_data(D,Nx,Ny,Nz, **kwargs)
            self.column_selector(**kwargs)
            if bool(kwargs.get('data_generator_crop',True)):
                self.x,self.fx,self.y,self.fy,self.z,self.fz = crop(self.x,Nx),crop(self.fx,Nx),crop(self.y,Ny),crop(self.fy,Ny),crop(self.z,Nz),crop(self.fz,Nz)
            self.Ny = get_matrix(self.y).shape[0]
            if  not isinstance(self.z,list): self.Nz = get_matrix(self.z).shape[0]
            self.Nx = get_matrix(self.x).shape[0]
            self.D = get_matrix(self.x).shape[1]
            if (len(get_matrix(self.fx))):
                if self.fx.ndim == 1: self.Df = 1
                else:self.Df = self.fx.shape[1]
    def get_nb_features(self):
        return self.fx.shape[1]
 
    def copy_data(self,out):
        out.x,out.y,out.z,out.fx,out.fy,out.fz, out.dfx,out.dfz = self.x.copy(),self.y.copy(),self.z.copy(),self.fx.copy(),self.fy.copy(),self.fz.copy(),self.dfx.copy(),self.dfz.copy()
        out.D,out.Nx,out.Ny,out.Nz = self.D,self.Nx,self.Ny,self.Nz
        return out

    def get_input_data(self):
        return self.D,self.Nx,self.Ny,self.Nz,self.Df
    def get_output_data(self):
        # print(self.x)
        # print(self.fx)
        return self.x,self.y,self.z,self.fx,self.fy,self.fz,self.dfx,self.dfz

    def get_params(**kwargs) :
        return kwargs.get('data_generator',None)

    def column_selector(self,**kwargs):
        params = data_generator.get_params(**kwargs)
        if params is None : return
        params = params.get('variables_selector',None)
        if params is None : return
        variables_cols_drop = params.get('variables_cols_drop',[])
        variables_cols_keep = params.get('variables_cols_keep',[])
        values_cols_drop = params.get('values_cols_drop',[])
        values_cols_keep = params.get('values_cols_keep',[])

        if len(variables_cols_drop) or len(variables_cols_keep):
            self.x = column_selector(self.x,cols_drop = variables_cols_drop, cols_keep = variables_cols_keep)
            self.y = column_selector(self.y,cols_drop = variables_cols_drop, cols_keep = variables_cols_keep)
            self.z = column_selector(self.z,cols_drop = variables_cols_drop, cols_keep = variables_cols_keep)
        if len(values_cols_drop) or len(values_cols_keep):
            self.fx = column_selector(self.fx,cols_drop = values_cols_drop, cols_keep = values_cols_keep)
            self.fy = column_selector(self.fy,cols_drop = values_cols_drop, cols_keep = values_cols_keep)
            self.fz = column_selector(self.fz,cols_drop = values_cols_drop, cols_keep = values_cols_keep)

    def save_cd_data(object,**params):
        if params is not None:
            save_cv_data = params.get('save_cv_data',None)
            if save_cv_data is not None:
                index = save_cv_data.get('index',False)
                header = save_cv_data.get('header',False)
                x_csv,y_csv,z_csv,fx_csv,fz_csv,f_z_csv = save_cv_data.get('x_csv',None),save_cv_data.get('y_csv',None),save_cv_data.get('z_csv',None),save_cv_data.get('fx_csv',None),save_cv_data.get('fz_csv',None),save_cv_data.get('f_z_csv',None)
                if x_csv is not None :  save_to_file(object.x, file_name=x_csv,sep = ';', index=index, header=header)
                if y_csv is not None :  save_to_file(object.y, file_name=y_csv,sep = ';', index=index, header=header)
                if z_csv is not None :  save_to_file(object.z, file_name=z_csv,sep = ';', index=index, header=header)
                if fx_csv is not None :  save_to_file(object.fx, file_name=fx_csv,sep = ';', index=index, header=header)
                if fz_csv is not None :  save_to_file(object.fz, file_name=fz_csv,sep = ';', index=index, header=header)
                if f_z_csv is not None :  save_to_file(object.f_z, file_name=f_z_csv,sep = ';', index=index, header=header)

    def __init__(self,D=0,Nx=0,Ny=0,Nz=0,**kwargs):
        self.set_data(D,Nx,Ny,Nz,**kwargs)

class data_predictor(abc.ABC):
    score,elapsed_predict_time,norm_function,discrepancy_error = np.NaN,np.NaN,np.NaN,np.NaN
    set_kernel,generator = None,None

    def get_params(**kwargs) :
        return kwargs.get('data_predictor',None)
    
    def __init__(self): pass
    def __init__(self,**kwargs):
        self.set_kernel = kwargs.get('set_kernel',kernel_setters.kernel_helper(kernel_setters.set_tensornorm_kernel, 2,1e-8 ,map_setters.set_unitcube_map))
        self.set_kernel()
        self.accuracy_score_function = kwargs.get('accuracy_score_function',get_relative_mean_squared_error)
        self.name = kwargs.get('name','data_predictor')
    def get_index(self):
        if (self.generator):return self.generator.get_index()
        else:return []
    def get_index_z(self):
        if (self.generator):return self.generator.get_index_z()
        else:return []
    def get_input_data(self):
        return self.x,self.y,self.z,self.fx,self.fy,self.fz, self.dfx, self.dfz
    def copy_data(self,out):
        out.generator, out.set_kernel = self.generator,self.set_kernel
        out.x,out.y,out.z,out.fx,out.fy, out.fz, out.dfx, out.dfz = self.x.copy(),self.y.copy(),self.z.copy(),self.fx.copy(),self.fy.copy(),self.fz.copy(),self.dfx.copy(),self.dfz.copy()
        out.f_z = self.f_z.copy()
        # out.df_z= self.df_z.copy()
        out.D,out.Nx,out.Ny,out.Nz,out.Df = self.D,self.Nx,self.Ny,self.Nz,self.Df
        out.elapsed_predict_time,out.norm_function,out.discrepancy_error,out.accuracy_score= self.elapsed_predict_time,self.norm_function,self.discrepancy_error,self.accuracy_score
        return out
    def set_data(self,generator,**kwargs):
        import time
        self.generator = generator
        self.D,self.Nx,self.Ny,self.Nz,self.Df = generator.get_input_data()
        self.x,self.y,self.z,self.fx, self.fy, self.fz, self.dfx, self.dfz = generator.get_output_data()
        self.column_selector(**kwargs)
        self.f_z,self.df_z = [],[]
        self.elapsed_predict_time,self.norm_function,self.discrepancy_error,self.accuracy_score = np.NaN,np.NaN,np.NaN,np.NaN
        if (self.D*self.Nx*self.Ny ):
            self.preamble(**kwargs)
            start = time.time()
            self.predictor(**kwargs)
            self.elapsed_predict_time = time.time()-start
            self.validator(**kwargs)

    def column_selector(self,**kwargs):
        params = data_predictor.get_params(**kwargs)
        if params is None : return
        params = params.get('variables_selector',None)
        if params is None : return
        def helper(values,**kwargs):
            if isinstance(values,list):return values
            sep = kwargs.get('sep',';')
            return pd.read_csv(values,sep=sep).keep_columns.values.tolist()
        variables_cols_drop = helper(params.get('variables_cols_drop',None),**params)
        variables_cols_keep = helper(params.get('variables_cols_keep',[]),**params)
        values_cols_drop = helper(params.get('values_cols_drop',[]),**params)
        values_cols_keep = helper(params.get('values_cols_keep',[]),**params)

        if len(variables_cols_drop) or len(variables_cols_keep):
            self.x = column_selector(self.x,cols_drop = variables_cols_drop, cols_keep = variables_cols_keep)
            self.y = column_selector(self.y,cols_drop = variables_cols_drop, cols_keep = variables_cols_keep)
            self.z = column_selector(self.z,cols_drop = variables_cols_drop, cols_keep = variables_cols_keep)
        if len(values_cols_drop) or len(values_cols_keep):
            self.fx = column_selector(self.fx,cols_drop = values_cols_drop, cols_keep = values_cols_keep)
            self.fy = column_selector(self.fy,cols_drop = values_cols_drop, cols_keep = values_cols_keep)
            # self.fz = column_selector(self.fz,cols_drop = values_cols_drop, cols_keep = values_cols_keep)


    def get_map_cluster_indices(self,cluster_indices=[],element_indices=[],**kwargs):
        if not len(element_indices): element_indices = self.f_z
        if not len(cluster_indices): 
            test = type(self.z)
            switchDict = {np.ndarray: self.get_index_z, pd.DataFrame: lambda : list(self.z.index)}
            if test in switchDict.keys(): cluster_indices = switchDict[test]()
            else:
                raise TypeError("unknown type "+ str(test) + " in standard_scikit_cluster_predictor.get_map_cluster_indices")

        if not len(cluster_indices): return {}
        if len(cluster_indices) == len(element_indices):
            return pd.DataFrame({'key': element_indices,'values':cluster_indices}).groupby("key")["values"].apply(list)
        else: return {}

    def preamble(self,**kwargs):
      return
    @abc.abstractmethod
    def predictor(self,**kwargs):
      pass
    
    def is_validator_compute(self,field,**kwargs):
        if 'validator_compute' in kwargs:
            debug = field in kwargs.get('validator_compute') 
            return debug
        return False

    def validator(self,**kwargs):
        kwargs['set_codpy_kernel'] = kwargs.get("set_codpy_kernel",self.set_kernel)
        kwargs['rescale'] = kwargs.get("rescale",True)
        if len(self.fx) and self.set_kernel: 
            if self.is_validator_compute(field ='norm_function',**kwargs): self.norm_function = op.norm(x= self.x,y= self.y,z= self.z,fx = self.fx,**kwargs)
        if len(self.fz)*len(self.f_z):
            if self.is_validator_compute(field = 'accuracy_score',**kwargs): self.accuracy_score = self.accuracy_score_function(self.fz, self.f_z)
        if len(self.x)*len(self.z) and self.set_kernel: 
            if ( self.is_validator_compute(field ='discrepancy_error',**kwargs)): self.discrepancy_error = op.discrepancy(x=self.x, y = self.y, z= self.z, **kwargs)


    def get_numbers(self):
        return self.D,self.Nx,self.Ny,self.Nz,self.Df

    def get_output_data(self):
        return self.f_z,self.df_z
    
    def get_params(**kwargs) :
        return kwargs.get('data_predictor',None)

    def get_new_params(self,**kwargs) :
        return kwargs

    def save_cd_data(self,**kwargs):
        params = data_predictor.get_params(**kwargs)
        if params is not None:
            x_csv,y_csv,z_csv,fx_csv,fz_csv,f_z_csv = params.get('x_csv',None),params.get('y_csv',None),params.get('z_csv',None),params.get('fx_csv',None),params.get('fz_csv',None),params.get('f_z_csv',None)
            if x_csv is not None :  self.x.to_csv(x_csv,sep = ';', index=False)
            if y_csv is not None :  self.y.to_csv(y_csv,sep = ';', index=False)
            if z_csv is not None :  self.z.to_csv(z_csv,sep = ';', index=False)
            if fx_csv is not None : self.fx.to_csv(fx_csv,sep = ';', index=False)
            if fz_csv is not None : self.fz.to_csv(fz_csv,sep = ';', index=False)
            if f_z_csv is not None: self.f_z.to_csv(f_z_csv,sep = ';', index=False)

    
    def id(self,name = ""):
        return self.name

class graphical_cluster_utilities:
    def plot_clusters(predictor ,ax, **kwargs):
        import seaborn as sns
        fun = get_representation_function(**kwargs)

        xlabel = kwargs.get('xlabel',"pca1")
        ylabel = kwargs.get('ylabel',"pca2")
        cluster_label = kwargs.get('cluster_label',"cluster:")


        x = np.asarray(predictor.z)
        fx = np.asarray(predictor.f_z)
        centers = np.asarray(predictor.y) 
        ny = len(centers)
        if (len(x)*len(fx)*len(centers)):
            colors = plt.cm.Spectral(fx / ny)
            x,y = fun(x)
            num = len(x)
            df = pd.DataFrame({'x': x, 'y':y, 'label':fx}) 
            groups = df.groupby(fx)
            for name, group in groups:
                ax.plot(group.x, group.y, marker='o', linestyle='', ms=50/np.sqrt(num), mec='none')
                ax.set_aspect('auto')
                ax.tick_params(axis='x',which='both',bottom='off',top='off',labelbottom='off')
                ax.tick_params(axis= 'y',which='both',left='off',top='off',labelleft='off')
            if len(centers):
                c1,c2 = fun(centers)
                ax.scatter(c1, c2,marker='o', c="black", alpha=1, s=200)
                for n in range(0,len(c1)):
                    a1,a2 = c1[n],c2[n]
                    ax.scatter(a1, a2, marker='$%d$' % n, alpha=1, s=50)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.title.set_text(cluster_label + str(ny))


class add_confusion_matrix:
    def confusion_matrix(self):
        import pandas as pd
        from sklearn.cluster import KMeans
        from sklearn.metrics import confusion_matrix
        out = []    
        if len(self.fz)*len(self.f_z):out = confusion_matrix(self.fz, self.f_z)
        return out
    def plot_confusion_matrix(predictor ,ax, **kwargs):
        import seaborn as sns
        sns.heatmap(predictor.confusion_matrix(), ax=ax, annot=True, fmt="d", cmap=plt.cm.copper)
        labels = kwargs.get('labels',[str(s) for s in np.unique(predictor.fz)])
        title = kwargs.get('title',"Conf. Mat.:")
        ax.set_title(title, fontsize=14)
        ax.set_xticklabels(labels, fontsize=14, rotation=90)
        ax.set_yticklabels(labels, fontsize=14, rotation=360)
    

class data_accumulator:
    def __init__(self,**kwargs):
        self.set_data(generators = [],predictors= [],**kwargs)

    def set_data(self,generators =[], predictors = [],**kwargs):
        self.generators,  self.predictors = generators,predictors

    def accumulate_reshape_helper(self,x):
        if len(x) == 0: return []
        newshape = np.insert(x.shape,0,1)
        return x.reshape(newshape)

    def accumulate(self,predictor,generator,**kwargs):
        self.generators.append(copy.copy(generator))
        self.predictors.append(copy.copy(predictor))

     
    def plot_learning_and_train_sets(self,xs=[],zs=[],title="training (red) vs test (green) variables and values",labelx='variables ',labely=' values'):
        D = len(self.generators)
        fig = plt.figure()
        d=0
        for d in range(0,D):
            g = self.generators[d]
            if (len(xs)): x = xs[d]
            else: x = self.generators[d].x[:,0]
            ax=fig.add_subplot(1,D,d+1)
            plotx,plotfx,permutation = lexicographical_permutation(x.flatten(),g.fx.flatten())
            ax.plot(plotx,plotfx,color = 'red')
            if (len(zs)): z = zs[d]
            else: z = self.generators[d].z[:,0]
            plotz,plotfz,permutation = lexicographical_permutation(z.flatten(),g.fz.flatten())
            ax.plot(plotz,plotfz,color = 'green')
            plt.xlabel(labelx)
            plt.ylabel(labely+self.predictors[d].id())
            d = d+1
        plt.title(title)
        plt.show()

    def plot_predicted_values(self,zs=[],title="predicted (red) vs test (green) variables and values",labelx='z',labely='predicted values'):
        d = 0
        D = len(self.predictors)
        fig = plt.figure()
        for d in range(0,D):
            p = self.predictors[d]
            if (len(zs)): z = zs[d]
            else: z = self.generators[d].z[:,0]
            ax=fig.add_subplot(1,D,d+1)
            plotx,plotfx,permutation = lexicographical_permutation(z.flatten(),p.f_z.flatten())
            ax.plot(plotx,plotfx,color = 'red')
            plotx,plotfx,permutation = lexicographical_permutation(z.flatten(),p.fz.flatten())
            ax.plot(plotx,plotfx,color = 'green')
            plt.xlabel(labelx)
            plt.ylabel(labely+p.id())
            d = d+1
        plt.title(title)
        plt.show()

    def plot_errors(self,fzs=[],title="error on predicted set ",labelx='f(z)',labely='error:'):
        d = 0
        D = len(self.predictors)
        fig = plt.figure()
        for p in self.predictors:
            ax=fig.add_subplot(1,D,d+1)
            if (len(fzs)): fz = fzs[d]
            else: fz = p.fz
            plotx,plotfx,permutation = lexicographical_permutation(get_matrix(fz).flatten(),get_matrix(p.f_z).flatten()-get_matrix(p.fz).flatten())
            ax.plot(plotx,plotfx, color= "red")
            ax.plot(plotx,get_matrix(p.fz).flatten()-get_matrix(p.fz).flatten(), color= "green")
            plt.xlabel(labelx)
            plt.ylabel(labely+p.id())
            d = d+1

        plt.title(title)
        plt.show()

    def format_helper(self,x):
        return x.reshape(len(x),1)
    def get_elapsed_predict_times(self):
        return  np.asarray([np.round(s.elapsed_predict_time,2) for s in self.predictors])
    def get_discrepancy_errors(self):
        return  np.asarray([np.round(s.discrepancy_error,4) for s in self.predictors])
    def get_norm_functions(self):
        return  np.asarray([np.round(s.norm_function,2) for s in self.predictors])
    def get_accuracy_score(self):
        return  np.asarray([np.round(s.accuracy_score,4) for s in self.predictors])
    def get_numbers(self):
        return  np.asarray([s.get_numbers() for s in self.predictors])
    def get_Nxs(self):
        return  np.asarray([s.Nx for s in self.predictors])
    def get_Nys(self):
        return  np.asarray([s.Ny for s in self.predictors])
    def get_Nzs(self):
        return  np.asarray([s.Nz for s in self.predictors])
    def get_predictor_ids(self):
        return  np.asarray([s.id() for s in self.predictors])
    def get_xs(self):
        return  [s.x for s in self.predictors]
    def get_ys(self):
        return  [s.y for s in self.predictors]
    def get_zs(self):
        return  [s.z for s in self.predictors]
    def get_fxs(self):
        return  [s.fx for s in self.predictors]
    def get_fys(self):
        return  [s.fy for s in self.predictors]
    def get_fzs(self):
        return  [s.fz for s in self.predictors]
    def get_f_zs(self):
        return  [s.f_z for s in self.predictors]

    def confusion_matrices(self):
        return  [s.confusion_matrix() for s in self.predictors]

    def plot_clusters(self, **kwargs):
        multi_plot(self.predictors ,graphical_cluster_utilities.plot_clusters, **kwargs)

    def plot_confusion_matrices(self, **kwargs):
        multi_plot(self.predictors ,add_confusion_matrix.plot_confusion_matrix, **kwargs)

    def get_maps_cluster_indices(self,cluster_indices=[],element_indices=[],**kwargs):
        out = []
        for predictor in self.predictors:
            out.append(predictor.get_map_cluster_indices(cluster_indices=cluster_indices,element_indices=element_indices,**kwargs))
        return out


    def get_output_datas(self):
        execution_time = self.format_helper(self.get_elapsed_predict_times())
        discrepancy_errors = self.format_helper(self.get_discrepancy_errors())
        norm_function = self.format_helper(self.get_norm_functions())
        scores = self.format_helper(self.get_accuracy_score())
        numbers = self.get_numbers()
        indices = self.format_helper(self.get_predictor_ids())
        indices = pd.DataFrame(data=indices,columns=["predictor_id"])
        numbers = np.concatenate((numbers,execution_time,scores,norm_function,discrepancy_errors), axis=1)
        numbers = pd.DataFrame(data=numbers,columns=["D", "Nx","Ny","Nz","Df","execution_time","scores","norm_function","discrepancy_errors"])
        numbers = pd.concat((indices,numbers),axis=1)
        return  numbers


class standard_cluster_predictor(data_predictor,graphical_cluster_utilities):
    import time
    score_silhouette, score_calinski_harabasz, homogeneity_test, inertia,  discrepancy = np.NaN,np.NaN,np.NaN,np.NaN,np.NaN
    estimator = None

    def copy_data(self,out):
        super().copy_data(out)
        out.score_silhouette,out.score_calinski_harabasz,out.homogeneity_test,out.inertia= self.score_silhouette,self.score_calinski_harabasz,self.homogeneity_test,self.inertia
        return out

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        if 'accuracy_score_function' not in kwargs: 
            from sklearn import metrics
            self.accuracy_score_function = metrics.accuracy_score

    def validator(self,**kwargs):
        super().validator(**kwargs)
        from sklearn import metrics
        from sklearn.metrics import silhouette_samples, silhouette_score
        if len(self.z)*len(self.f_z):
            try: 
                if self.is_validator_compute(field ='score_silhouette',**kwargs): self.score_silhouette = silhouette_score(self.z, self.f_z)
                if self.is_validator_compute(field ='score_calinski_harabasz',**kwargs): self.score_calinski_harabasz = metrics.calinski_harabasz_score(self.z, self.f_z)
            except:
                pass
        if len(self.fz)*len(self.f_z): 
            if self.is_validator_compute(field ='homogeneity_test',**kwargs): self.homogeneity_test = metrics.homogeneity_score(self.fz, self.f_z) 
        if (self.estimator):
            if self.is_validator_compute(field ='inertia',**kwargs): self.inertia = self.estimator.inertia_
        else:
            if self.is_validator_compute(field ='inertia',**kwargs):
                from sklearn.cluster import KMeans
                self.inertia = KMeans(n_clusters=self.Ny).fit(self.x).inertia_
        pass

class scenario_generator:
    gpa=[]
    results =[]
    data_generator,predictor,accumulator = [],[],[]
    def set_data(self,data_generator,predictor,accumulator,**kwargs):
        self.gpa.append((data_generator,predictor,accumulator))
    def __init__(self,data_generator = None,predictor= None,accumulator= None,**kwargs):
        if data_generator:self.set_data(data_generator,predictor,accumulator,**kwargs)
    def run_scenarios_cube(self,Ds, Nxs,Nys,Nzs,**kwargs):
        for d in Ds:
            for nx in Nxs:
                for ny in Nys:
                    for nz in Nzs:
                        self.data_generator.set_data(int(d),int(nx),int(ny),int(nz),**kwargs)
                        self.predictor.set_data(self.data_generator,**kwargs)
                        print("  predictor:",self.predictor.id()," d:", d," nx:",nx," ny:",ny," nz:",nz)
                        self.accumulator.accumulate(self.predictor,self.data_generator,**kwargs)
    def run_scenarios(self,list_scenarios,data_generator,predictor,accumulator,**kwargs):
        for scenario in list_scenarios:
            d,nx,ny,nz = scenario
            d,nx,ny,nz = int(d),int(nx),int(ny),int(nz)
            self.data_generator,self.predictor,self.accumulator = data_generator,predictor,accumulator
            data_generator.set_data(d,nx,ny,nz,**kwargs)
            predictor.set_data(data_generator,**kwargs)
            # print("predictor:",self.predictor.id()," d:", d," nx:",nx," ny:",ny," nz:",nz)
            accumulator.accumulate(predictor,data_generator,**kwargs)
        if not len(self.results): self.results = accumulator.get_output_datas()
        else: self.results = pd.concat((self.results,accumulator.get_output_datas()))
        # print(self.results)
    def run_all(self,list_scenarios,**kwargs):
        self.results = []
        for scenario in list_scenarios:
            d,nx,ny,nz = scenario
            d,nx,ny,nz = int(d),int(nx),int(ny),int(nz)
            # print(" d:", d," nx:",nx," ny:",ny," nz:",nz)
            for data_generator,predictor,accumulator in self.gpa:
                run_scenarios(self,list_scenarios,data_generator,predictor,accumulator,**kwargs)

    def compare_plot(self,axis_label, field_label, **kwargs):
        xs=[]
        fxs=[]
        # self.results.to_excel("results.xlsx")
        groups = self.results.groupby("predictor_id")
        predictor_ids = list(groups.groups.keys())
        groups = groups[(axis_label,field_label)]
        for name, group in groups:
            xs.append(group[axis_label].values.astype(float))
            fxs.append(group[field_label].values.astype(float))
            pass
        compare_plot_lists(listxs = xs, listfxs = fxs, listlabels=predictor_ids, xscale ="linear",yscale ="linear", Show = True,**kwargs)

    def compare_plot_ax(self,axis_field_label, ax,**kwargs):
        xs=[]
        fxs=[]
        axis_label,field_label = axis_field_label[0],axis_field_label[1]
        # self.results.to_excel("results.xlsx")
        groups = self.results.groupby("predictor_id")
        predictor_ids = list(groups.groups.keys())
        groups = groups[list((axis_label,field_label))]
        for name, group in groups:
            xs.append(group[axis_label].values.astype(float))
            fxs.append(group[field_label].values.astype(float))
        pass
        compare_plot_lists(listxs = xs, listfxs = fxs, ax=ax, 
        **{'listlabels':predictor_ids, 'labelx':axis_label,'labely':field_label,**kwargs}
        )


    def compare_plots(self,axis_field_labels, **kwargs):
        multi_plot(axis_field_labels,self.compare_plot_ax, **kwargs)
