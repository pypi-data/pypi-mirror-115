exp_config={
    'env': {
        'manager': {
            'episode_num': float("inf"),
            'max_retry': 1,
            'step_timeout': 60,
            'auto_reset': True,
            'reset_timeout': 60,
            'retry_waiting_time': 0.1,
            'cfg_type': 'BaseEnvManagerDict'
        },
        'collector_env_num': 16,
        'evaluator_env_num': 5,
        'act_scale': True,
        'n_evaluator_episode': 5,
        'stop_value': -250
    },
    'policy': {
        'model': {
            'obs_shape': 3,
            'action_shape': 1,
            'encoder_hidden_size_list': [64, 64],
            'continuous': True,
            'actor_head_layer_num': 0,
            'critic_head_layer_num': 0,
            'sigma_type': 'fixed',
            'bound_type': 'tanh'
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
                'cfg_type': 'BaseLearnerDict'
            },
            'multi_gpu': False,
            'epoch_per_collect': 10,
            'batch_size': 128,
            'learning_rate': 0.001,
            'value_weight': 0.5,
            'entropy_weight': 0.0,
            'clip_ratio': 0.2,
            'adv_norm': True,
            'value_norm': True,
            'ppo_param_init': True,
            'grad_clip_type': 'clip_norm',
            'grad_clip_value': 0.5,
            'ignore_done': True
        },
        'collect': {
            'collector': {
                'deepcopy_obs': False,
                'transform_obs': False,
                'collect_print_freq': 100,
                'cfg_type': 'SampleCollectorDict'
            },
            'unroll_len': 1,
            'discount_factor': 0.95,
            'gae_lambda': 0.95,
            'n_sample': 3200
        },
        'eval': {
            'evaluator': {
                'eval_freq': 200,
                'cfg_type': 'BaseSerialEvaluatorDict',
                'stop_value': -250,
                'n_episode': 5
            }
        },
        'other': {
            'replay_buffer': {
                'type': 'naive',
                'name': 'default',
                'replay_buffer_size': 10000,
                'deepcopy': False,
                'enable_track_used_data': False,
                'cfg_type': 'NaiveReplayBufferDict'
            }
        },
        'type': 'ppo',
        'cuda': False,
        'on_policy': True,
        'priority': False,
        'priority_IS_weight': False,
        'recompute_adv': True,
        'continuous': True,
        'cfg_type': 'PPOPolicyDict'
    },
    'seed': 0
}
