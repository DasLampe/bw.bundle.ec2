@metadata_reactor
def add_users(metadata):
    if node.has_bundle("users"):
        raise Exception("Incompatible bundle 'users'.")

    return {
        'users': metadata.get('ec2', {}).get('users', {}),
    }
