import data


def is_contiguous(profile_layers):
    bottom = None
    return all(profile_layers['top'][1:].as_matrix() == profile_layers['bottom'][:-1].as_matrix())

def orgc_not_null(profile_layers):
    return all(profile_layers['orgc_value_avg'].notnull())

def density_not_null(profile_layers):
    return all(profile_layers['bdfi_value_avg'].notnull()) \
        or (
            all(profile_layers['bdws_value_avg'].notnull()) \
            and all(profile_layers['cfgr_value_avg'].notnull())
            and all(profile_layers['cfvo_value_avg'].notnull())
        )

def validate_profile(profile_layers):
    return is_contiguous(profile_layers) and orgc_not_null(profile_layers) and density_not_null(profile_layers)


if __name__ == '__main__':
    _, profiles, layers = data.load_data(exclude_profiles_cols=True, exclude_layers_cols=True)

    num_contiguous = 0
    num_orgc = 0
    num_density = 0
    num_all = 0
    for profile_id in profiles['profile_id']:
        profile_layers = layers[layers['profile_id'] == profile_id].sort_values('top')
        contiguous = is_contiguous(profile_layers)
        orgc = orgc_not_null(profile_layers)
        density = density_not_null(profile_layers)
        num_contiguous += contiguous
        num_orgc += orgc
        num_density += density
        num_all += contiguous and orgc and density

    print(f'# contiguous: {num_contiguous}')
    print(f'# complete orgc: {num_orgc}')
    print(f'# complete density: {num_density}')
    print(f'# all: {num_all}')
    print(f'# profiles: {len(profiles)}')
