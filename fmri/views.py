from django.http import JsonResponse
import scipy.io as spio
import os
import json
import codecs
from django.core.files import File
import pandas as pd
from django_pandas.io import read_frame


def index(request):
    comments = [
        {
            'name': 'eunji cho',
            'email': 'eyet010@gmail.com'
        },
        {
            'name': 'yunjin jung',
            'email': 'yunjin@gmail.com'
        }
    ]

    return JsonResponse({'comments': comments})


def readMatFile(request):
    mat_file = spio.loadmat('/Users/clms/vscode_workspace/python_django/venvs/hyd_sample/fmri/behavior-data.mat',
                            struct_as_record=False,
                            squeeze_me=True)

    print(mat_file)
    return check_keys(mat_file)


def check_keys(dict):
    print(dict)
    for key in dict:
        print(dict[key])
        if isinstance(dict[key], spio.matlab.mio5_params.mat_struct):
            dict[key] = _todict(dict[key])

    return dict


def _todict(matobj):
    dict = {}
    for strg in matobj._filednames:

        elem = matobj.__dict__[strg]
        if isinstance(elem, spio.matlab.mio5_params.mat_struct):
            dict[strg] = _todict(elem)
        else:
            dict[strg] = elem
    return dict


def mat2json(mat_path=None, filepath=None):
    """
    Converts .mat file to .json and writes new file
    Parameters
    ----------
    mat_path: Str
        path / filename .mat storage path
    filepath: Str
                 If you need to save to json, add this path. Otherwise, do not save
    Returns
                 Returns the transformed dictionary
    -------
    None
    Examples
    --------
    >>> mat2json(blah blah)
    """

    matlabFile = spio.loadmat(
        '/Users/clms/vscode_workspace/python_django/venvs/hyd_sample/fmri/behavior-data.mat')
    # print('??? ' + matlabFile)
    # pop all those dumb fields that don't let you jsonize file
    matlabFile.pop('__header__')
    matlabFile.pop('__version__')
    matlabFile.pop('__globals__')
    # jsonize the file - orientation is 'index'
    matlabFile = pd.Series(matlabFile).to_json()

    return JsonResponse({'ok': 'ok'})

    # if filepath:
    #     json_path = os.path.splitext(os.path.split(mat_path)[1])[0] + '.json'
    #     with open(json_path, 'w') as f:
    #         f.write(matlabFile)
    # return matlabFile


def matToJson(request):
    matlabFile = spio.loadmat(
        '/Users/clms/vscode_workspace/python_django/venvs/hyd_sample/fmri/behavior-data.mat')

    matlabFile.pop('__header__')
    matlabFile.pop('__version__')
    matlabFile.pop('__globals__')

    alldata = []
    alldata.append(matlabFile)

    # your path variables
    file_path = "/Users/clms/vscode_workspace/python_django/venvs/hyd_sample/fmri/path.json"

    json.dump(alldata, codecs.open(file_path, 'w', encoding='utf-8'),
              separators=(',', ':'), sort_keys=True, indent=4)
    return JsonResponse({'okk': 'oii'})
