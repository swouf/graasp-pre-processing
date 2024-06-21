def make_app_descriptor(name: str, short_name: str, git: str, graaspId: str):
    return {
        'name': name,
        'short-name': short_name,
        'git': git,
        'graasp-id': graaspId,
    }

app_ids = [
    make_app_descriptor('Short answer survey app', 'short-answer', '', '3497dc8d-79cd-4768-8b0b-ce34e9876df0')
]