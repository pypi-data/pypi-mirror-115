exp_config = {
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
        'collector_env_num': 8,
        'evaluator_env_num': 5,
        'n_evaluator_episode': 5,
        'stop_value': 195
    },
    'policy': {
        'model': {
            'obs_shape': 4,
            'action_shape': 2,
            'encoder_hidden_size_list': [64, 64, 128],
            'critic_head_hidden_size': 128,
            'actor_head_hidden_size': 128
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
            'update_per_collect': 6,
            'batch_size': 64,
            'learning_rate': 0.001,
            'value_weight': 0.5,
            'entropy_weight': 0.01,
            'clip_ratio': 0.2,
            'adv_norm': False,
            'ignore_done': False
        },
        'collect': {
            'collector': {
                'deepcopy_obs': False,
                'transform_obs': False,
                'collect_print_freq': 100,
                'cfg_type': 'SampleCollectorDict'
            },
            'unroll_len': 1,
            'discount_factor': 0.9,
            'gae_lambda': 0.95,
            'n_sample': 128
        },
        'eval': {
            'evaluator': {
                'eval_freq': 50,
                'cfg_type': 'BaseSerialEvaluatorDict',
                'stop_value': 195,
                'n_episode': 5
            }
        },
        'other': {
            'replay_buffer': {
                'type': 'naive',
                'replay_buffer_size': 1000,
                'deepcopy': False,
                'enable_track_used_data': False,
                'cfg_type': 'NaiveReplayBufferDict'
            }
        },
        'type': 'dqn',
        'cuda': False,
        'on_policy': True,
        'priority': False,
        'priority_IS_weight': False,
        'nstep_return': False,
        'nstep': 3,
        'cfg_type': 'PPOPolicyDict'
    },
    'reward_model': {
        'type': 'rnd',
        'intrinsic_reward_type': 'add',
        'learning_rate': 0.001,
        'batch_size': 32,
        'hidden_size_list': [64, 64, 128],
        'update_per_collect': 10,
        'cfg_type': 'RndRewardModelDict',
        'obs_shape': 4
    },
    'exp_name': 'cartpole_ppo_rnd',
    'seed': 0
}
