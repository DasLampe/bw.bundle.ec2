users = {}
files = {}
directories = {}

for username, user_attrs in node.metadata.get('ec2', {}).get('users', {}).items():
    if user_attrs.get('delete', False):
        users[username] = {
            'delete': True,
        }
    else:
        if user_attrs.get('passwordless_sudo', False):
            files[f'/etc/sudoers.d/{username}'] = {
                'content': f'{username} ALL=(ALL) NOPASSWD:ALL',
                'content_type': 'text',
                'mode': '0400',
                'owner': 'root',
                'group': 'root',
            }

        add_groups = user_attrs.get('add_groups', [])
        if user_attrs.get('sudo', False):
            add_groups += ['wheel']

        home = user_attrs.get('home', f'/home/{username}')

        directories[home] = {
            'owner': username,
            'group': username,
            'mode': "0700",
            'needs': [
                f'user:{username}',
            ]
        }

        users[username] = {
            'home': home,
            'password_hash': user_attrs.get('password_hash', '*'),
            'groups': add_groups,
            'full_name': user_attrs.get('full_name', ''),
            'shell': user_attrs.get('shell', '/bin/bash'),
        }

        # OpenSSH is already installed on EC2, so the openssh bundle isn't required. Have a Fallback. ;)
        if not node.has_bundle("openssh") and user_attrs.get('ssh_pubkey', []):
            files[f"{home}/.ssh/authorized_keys"] = {
                'content': "\n".join(user_attrs.get('ssh_pubkeys', [])) + "\n",
                'content_type': 'text',
                'owner': username,
                'group': username,
                'mode': "0600",
            }
