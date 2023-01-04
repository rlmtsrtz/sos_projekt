import matplotlib.pyplot as plt
import pandas as pd
import torch.nn.functional as f
import torch.optim as optim


def get_parameter_sets(classifier='digit_identifier'):
    if classifier == 'digit_identifier':
        step1_out = [40]
        step1_kernel_size = [4]
        step2_kernel_size = [2]
        step4_out = [40]
        step4_kernel_size = [5]
        step6_kernel_size = [2]
        step9_out = [60]

        forward_sets = []
        for s1o in step1_out:
            for s1ks in step1_kernel_size:
                for s2ks in step2_kernel_size:
                    for s4o in step4_out:
                        for s4ks in step4_kernel_size:
                            for s6ks in step6_kernel_size:
                                for s9o in step9_out:
                                    dic = {'step1': {'action': 'layer', 'layer': 'conv2d', 'in': 1, 'out': s1o,
                                                     'kernel_size': s1ks},
                                           'step2': {'action': 'f.max_pool2d', 'kernel_size': s2ks},
                                           'step3': {'action': 'f.relu'},
                                           'step4': {'action': 'layer', 'layer': 'conv2d', 'in': s1o,
                                                     'out': s4o, 'kernel_size': s4ks},
                                           'step5': {'action': 'layer', 'layer': 'conv_dropout2d'},
                                           'step6': {'action': 'f.max_pool2d', 'kernel_size': s6ks},
                                           'step7': {'action': 'f.relu'},
                                           'step8': {'action': 'view', 'dim1': -1},
                                           'step9': {'action': 'layer', 'layer': 'linear', 'in': 0, 'out': s9o},
                                           'step10': {'action': 'f.relu'},
                                           'step11': {'action': 'layer', 'layer': 'linear', 'in': s9o, 'out': 10},
                                           'step12': {'action': 'f.log_softmax', 'dim': 1}}
                                    forward_sets.append(dic)

        batch_size = [64]
        optimizer = ['optim.SGD']
        sgd_lr = [0.1]
        sgd_momentum = [0.5]
        loss_fn = [f.nll_loss]

        para_sets = []

        for opt in optimizer:
            for lfn in loss_fn:
                for bs in batch_size:
                    if opt == 'optim.SGD':
                        for lr in sgd_lr:
                            for momentum in sgd_momentum:
                                dic = {'batch_size': bs, 'loss_fn': lfn, 'optimizer': opt, 'lr': lr,
                                       'momentum': momentum,
                                       'weight_decay': 0}
                                para_sets.append(dic)
                    elif opt == 'optim.Adadelta':
                        dic = {'batch_size': bs, 'loss_fn': lfn, 'optimizer': opt, 'lr': 0, 'weight_decay': 0,
                               'momentum': 0}
                        para_sets.append(dic)
                    elif opt == 'optim.Adagrad':
                        dic = {'batch_size': bs, 'loss_fn': lfn, 'optimizer': opt, 'lr': 0, 'weight_decay': 0,
                               'momentum': 0}
                        para_sets.append(dic)
                    elif opt == 'optim.AdamW':
                        dic = {'batch_size': bs, 'loss_fn': lfn, 'optimizer': opt, 'lr': 0, 'weight_decay': 0,
                               'momentum': 0}
                        para_sets.append(dic)
                    elif opt == 'optim.SparseAdam':
                        dic = {'batch_size': bs, 'loss_fn': lfn, 'optimizer': opt, 'lr': 0, 'weight_decay': 0,
                               'momentum': 0}
                        para_sets.append(dic)
                    elif opt == 'optim.Adamax':
                        dic = {'batch_size': bs, 'loss_fn': lfn, 'optimizer': opt, 'lr': 0, 'weight_decay': 0,
                               'momentum': 0}
                        para_sets.append(dic)
                    elif opt == 'optim.ASGD':
                        dic = {'batch_size': bs, 'loss_fn': lfn, 'optimizer': opt, 'lr': 0, 'weight_decay': 0,
                               'momentum': 0}
                        para_sets.append(dic)
                    elif opt == 'optim.LBFGS':
                        dic = {'batch_size': bs, 'loss_fn': lfn, 'optimizer': opt, 'lr': 0, 'weight_decay': 0,
                               'momentum': 0}
                        para_sets.append(dic)
                    elif opt == 'optim.NAdam':
                        dic = {'batch_size': bs, 'loss_fn': lfn, 'optimizer': opt, 'lr': 0, 'weight_decay': 0,
                               'momentum': 0}
                        para_sets.append(dic)
                    elif opt == 'optim.RAdam':
                        dic = {'batch_size': bs, 'loss_fn': lfn, 'optimizer': opt, 'lr': 0, 'weight_decay': 0,
                               'momentum': 0}
                        para_sets.append(dic)
                    elif opt == 'optim.RMSprop':
                        dic = {'batch_size': bs, 'loss_fn': lfn, 'optimizer': opt, 'lr': 0, 'weight_decay': 0,
                               'momentum': 0}
                        para_sets.append(dic)
                    elif opt == 'optim.Rprop':
                        dic = {'batch_size': bs, 'loss_fn': lfn, 'optimizer': opt, 'lr': 0, 'weight_decay': 0,
                               'momentum': 0}
                        para_sets.append(dic)
                    elif opt == 'optim.Adam':
                        dic = {'batch_size': bs, 'loss_fn': lfn, 'optimizer': opt, 'lr': 0.1, 'momentum': 0.8,
                               'weight_decay': 0}
                        para_sets.append(dic)
                    else:
                        print('optimizer not treated')
                        dic = {'batch_size': bs, 'loss_fn': lfn, 'optimizer': opt, 'lr': 0.1, 'momentum': 0.8,
                               'weight_decay': 0}
                        para_sets.append(dic)
        return forward_sets, para_sets

    elif classifier == 'catdog_classifier':
        step1_out = [10]
        step4_out = [15]
        step7_out = [20]
        step14_out = [1000]
        step16_out = [500]

        forward_sets = []
        for s1o in step1_out:
            for s4o in step4_out:
                for s7o in step7_out:
                    for s14o in step14_out:
                        for s16o in step16_out:
                            dic = {'step1': {'action': 'layer', 'layer': 'conv2d', 'in': 3, 'out': s1o, 'kernel_size': 3},
                                   'step2': {'action': 'f.max_pool2d', 'kernel_size': 2},
                                   'step3': {'action': 'f.relu'},
                                   'step4': {'action': 'layer', 'layer': 'conv2d', 'in': s1o, 'out': s4o, 'kernel_size': 3},
                                   'step5': {'action': 'f.max_pool2d', 'kernel_size': 2},
                                   'step6': {'action': 'f.relu'},
                                   'step7': {'action': 'layer', 'layer': 'conv2d', 'in': s4o, 'out': s7o, 'kernel_size': 3},
                                   'step8': {'action': 'f.max_pool2d', 'kernel_size': 2},
                                   'step9': {'action': 'f.relu'},
                                   'step13': {'action': 'view', 'dim1': -1},
                                   'step14': {'action': 'layer', 'layer': 'linear', 'in': 0, 'out': s14o},
                                   'step15': {'action': 'f.relu'},
                                   'step16': {'action': 'layer', 'layer': 'linear', 'in': s14o, 'out': s16o},
                                   'step17': {'action': 'f.relu'},
                                   'step18': {'action': 'layer', 'layer': 'linear', 'in': s16o, 'out': 2},
                                   'step19': {'action': 'f.log_softmax', 'dim': 1}}
                            forward_sets.append(dic)

        batch_size = [64]
        optimizer = ['optim.SGD']
        sgd_lr = [0.1]
        sgd_momentum = [0.5]
        loss_fn = [f.nll_loss]

        para_sets = []

        for opt in optimizer:
            for lfn in loss_fn:
                for bs in batch_size:
                    if opt == 'optim.SGD':
                        for lr in sgd_lr:
                            for momentum in sgd_momentum:
                                dic = {'batch_size': bs, 'loss_fn': lfn, 'optimizer': opt, 'lr': lr, 'momentum': momentum,
                                       'weight_decay': 0}
                                para_sets.append(dic)
                    elif opt == 'optim.Adam':
                        dic = {'batch_size': bs, 'loss_fn': lfn, 'optimizer': opt, 'lr': 0.01, 'momentum': 0.8,
                               'weight_decay': 0}
                        para_sets.append(dic)
                    else:
                        print('optimizer not treated')
                        dic = {'batch_size': bs, 'loss_fn': lfn, 'optimizer': opt, 'lr': 0.1, 'momentum': 0.8,
                               'weight_decay': 0}
                        para_sets.append(dic)

        return forward_sets, para_sets


def plot_pandas(classifier='digit_identifier', start_index=0, end_index=None):
    if classifier == 'digit_identifier':
        path = 'panda_tables/runs_digit_identifier.csv'
    elif classifier == 'catdog_classifier':
        path = 'panda_tables/runs_catdog_classifier.csv'
    else:
        path = ''
    df = pd.read_csv(path)
    if end_index is None:
        end_index = len(pd.read_csv(path))

    list_of_indices = list(range(start_index, end_index, 1))
    df = df.iloc[list_of_indices, :]
    fig, ax = plt.subplots(figsize=(15, 7))
    fig.subplots_adjust(right=0.75)
    ax.plot(df['average_accuracy_test'], color='steelblue')
    ax.set_xlabel('Run')
    ax.set_ylabel('average accuracy test', color='steelblue')
    if classifier == 'digit_identifier':
        ax.axis(ymin=98, ymax=100)
    ax2 = ax.twinx()
    ax2.plot(df['memory_used'], color='red')
    ax2.set_ylabel('memory used', color='red')
    ax3 = ax.twinx()
    ax3.spines.right.set_position(("axes", 1.2))
    ax3.plot(df['needed_time'], color='green')
    ax3.set_ylabel('needed time', color='green')
    plt.show()
