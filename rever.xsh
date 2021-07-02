$PROJECT = 'pytrackmate'

$ACTIVITIES = ['version_bump', 'tag', 'push_tag', 'pypi', 'ghrelease']

$VERSION_BUMP_PATTERNS = [('pytrackmate/_version.py', '__version__\s*=.*', "__version__ = '$VERSION'"),
                          ('setup.py', 'version\s*=.*,', "version='$VERSION',")
                          ]

$PUSH_TAG_REMOTE = 'git@github.com:hadim/pytrackmate.git'
$GITHUB_ORG = 'hadim'
$GITHUB_REPO = 'pytrackmate'
