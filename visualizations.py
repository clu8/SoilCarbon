import os
import matplotlib.pyplot as plt
import seaborn as sns

import config
import data


def visualize_layers(layers):
    plt.figure()
    plt.scatter(layers.head(5000)['top'], layers.head(5000)['orgc_value_avg'])
    plt.show()

def visualize_profile_depth(layers):
    bottom_per_profile = layers.groupby(['profile_id'], sort=False)['bottom'].max().dropna()

    plt.figure()
    plt.suptitle('Distribution of bottom depth (cm) per profile')

    plt.subplot(211)
    sns.distplot(bottom_per_profile, kde=False)

    plt.subplot(212)
    sns.distplot(bottom_per_profile, bins=10, kde=False, hist_kws={'range': (0, 250)})

    plt.savefig(os.path.join(config.visualizations_dir, 'bottom_dist.png'))

if __name__ == '__main__':
    attributes, profiles, layers = data.load_data()
    print(f'Total layers: {len(layers)}')
    print(f'Total profiles: {len(profiles)}')
    visualize_profile_depth(layers)