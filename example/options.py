options = {
    'base': 'models/gan/base.gin',
    'models': [
        {'models/gan/lsgan.gin': [
            'models/gan/conv_discriminator.gin',
            'models/gan/mfcc_discriminator.gin'
        ]},
        {'models/gan/wgan.gin': [
            'models/gan/conv_discriminator.gin',
            'models/gan/mfcc_discriminator.gin'
        ]},
        'models/gan/ae.gin'
    ],
    'decoder': [
        'models/gan/conv_decoder.gin',
        'models/gan/rnn_ddsp_decoder.gin'
    ]
}

commands_file = "generated/run_all.sh"
filename_prefix = "generated/"

base_command = """
ddsp_run \\
    --mode=train \\
    --alsologtostderr \\
    --gin_file=datasets/tfrecord.gin \\
    --gin_param="TFRecordProvider.file_pattern='$URMP_MONO'" \\
    --gin_param="batch_size=8" \\
    --gin_param="train_util.train.num_steps=36000" \\
    --gin_param="train_util.train.steps_per_save=300" \\
    --gin_param="train_util.train.steps_per_summary=100" \\
    --gin_param="trainers.Trainer.checkpoints_to_keep=2" \\
"""
