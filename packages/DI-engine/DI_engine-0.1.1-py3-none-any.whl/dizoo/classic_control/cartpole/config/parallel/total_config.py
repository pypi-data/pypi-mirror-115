exp_config = {
    'main': {
        'env': {
            'manager': {
                'episode_num': float("inf"),
                'max_retry': 1,
                'step_timeout': 60,
                'auto_reset': True,
                'reset_timeout': 60,
                'retry_waiting_time': 0.1,
                'cfg_type': 'BaseEnvManagerDict',
                'type': 'base'
            },
            'type': 'cartpole',
            'import_names': ['dizoo.classic_control.cartpole.envs.cartpole_env'],
            'collector_env_num': 8,
            'collector_episode_num': 2,
            'evaluator_env_num': 5,
            'evaluator_episode_num': 1,
            'stop_value': 195
        },
        'policy': {
            'model': {
                'obs_shape': 4,
                'action_shape': 2,
                'encoder_hidden_size_list': [128, 128, 64],
                'dueling': True
            },
            'learn': {
                'learner': {
                    'train_iterations': 1000000000,
                    'dataloader': {
                        'num_workers': 0
                    },
                    'hook': {
                        'load_ckpt_before_run': '',
                        'log_show_after_iter': 100,
                        'save_ckpt_after_iter': 10000,
                        'save_ckpt_after_run': True
                    },
                    'cfg_type': 'BaseLearnerDict',
                    'type': 'base',
                    'import_names': ['ding.worker.learner.base_learner'],
                    'learner_num': 1,
                    'send_policy_freq': 1
                },
                'multi_gpu': False,
                'update_per_collect': 3,
                'batch_size': 32,
                'learning_rate': 0.001,
                'target_update_freq': 100,
                'ignore_done': False
            },
            'collect': {
                'collector': {
                    'print_freq': 5,
                    'compressor': 'lz4',
                    'update_policy_second': 3,
                    'cfg_type': 'ZerglingCollectorDict',
                    'type': 'zergling',
                    'import_names': ['ding.worker.collector.zergling_collector'],
                    'collector_num': 2
                },
                'unroll_len': 1,
                'n_sample': 16
            },
            'eval': {
                'evaluator': {
                    'eval_freq': 50
                }
            },
            'other': {
                'replay_buffer': {
                    'type': 'priority',
                    'replay_buffer_size': 100000,
                    'max_use': float("inf"),
                    'max_staleness': float("inf"),
                    'alpha': 0.6,
                    'beta': 0.4,
                    'anneal_step': 100000,
                    'enable_track_used_data': False,
                    'deepcopy': False,
                    'thruput_controller': {
                        'push_sample_rate_limit': {
                            'max': float("inf"),
                            'min': 0
                        },
                        'window_seconds': 30,
                        'sample_min_limit_ratio': 1
                    },
                    'monitor': {
                        'sampled_data_attr': {
                            'average_range': 5,
                            'print_freq': 200
                        },
                        'periodic_thruput': {
                            'seconds': 60
                        }
                    },
                    'cfg_type': 'AdvancedReplayBufferDict'
                },
                'eps': {
                    'type': 'exp',
                    'start': 0.95,
                    'end': 0.1,
                    'decay': 100000
                },
                'commander': {
                    'collector_task_space': 2,
                    'learner_task_space': 1,
                    'eval_interval': 5,
                    'cfg_type': 'SoloCommanderDict',
                    'type': 'solo',
                    'import_names': ['ding.worker.coordinator.solo_parallel_commander'],
                    'path_policy': './cartpole_dqn/policy'
                }
            },
            'type': 'dqn_command',
            'cuda': False,
            'on_policy': False,
            'priority': False,
            'priority_IS_weight': False,
            'discount_factor': 0.97,
            'nstep': 3,
            'cfg_type': 'DQNCommandModePolicyDict'
        },
        'exp_name': 'cartpole_dqn'
    },
    'system': {
        'coordinator': {
            'collector_task_timeout': 30,
            'learner_task_timeout': 600,
            'operator_server': {},
            'cfg_type': 'CoordinatorDict',
            'host': '0.0.0.0',
            'port': 50219,
            'learner': {
                'learner0': ['learner0', '0.0.0.0', 50220]
            },
            'collector': {
                'collector0': ['collector0', '0.0.0.0', 50221],
                'collector1': ['collector1', '0.0.0.0', 50222]
            }
        },
        'learner0': {
            'type': 'flask_fs',
            'import_names': ['ding.worker.learner.comm.flask_fs_learner'],
            'host': '0.0.0.0',
            'port': 50220,
            'path_data': './cartpole_dqn/data',
            'path_policy': './cartpole_dqn/policy',
            'multi_gpu': False,
            'gpu_num': 1,
            'aggregator': False
        },
        'collector0': {
            'type': 'flask_fs',
            'import_names': ['ding.worker.collector.comm.flask_fs_collector'],
            'host': '0.0.0.0',
            'port': 50221,
            'path_data': './cartpole_dqn/data',
            'path_policy': './cartpole_dqn/policy'
        },
        'collector1': {
            'type': 'flask_fs',
            'import_names': ['ding.worker.collector.comm.flask_fs_collector'],
            'host': '0.0.0.0',
            'port': 50222,
            'path_data': './cartpole_dqn/data',
            'path_policy': './cartpole_dqn/policy'
        }
    },
    'seed': 0
}
