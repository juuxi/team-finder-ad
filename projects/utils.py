from django.core.exceptions import ValidationError


def handle_clean_github_url(github_url):
    if not github_url:
        return None
    github_url = github_url.lower()
    website_part = github_url.split('://', 1)[-1]
    if not website_part.startswith('github.com'):
        raise ValidationError('Ссылка должна вести на github')

    return github_url
