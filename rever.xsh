$PROJECT = 'pytrackmate'

$ACTIVITIES = ['version_bump', 'tag', 'push_tag', 'pypi', 'ghrelease', 'conda_forge']

$VERSION_BUMP_PATTERNS = [('pytrackmate/_version.py', '__version__\s*=.*', "__version__ = '$VERSION'"),
                          ('setup.py', 'version\s*=.*,', "version='$VERSION',")
                          ]

$PUSH_TAG_REMOTE = 'git@github.com:hadim/pytrackmate.git'
$GITHUB_ORG = 'hadim'
$GITHUB_REPO = 'pytrackmate'

$CONDA_FORGE_FEEDSTOCK = 'pytrackmate-feedstock'
$CONDA_FORGE_SOURCE_URL = 'https://pypi.org/packages/source/p/pytrackmate/pytrackmate-$VERSION.tar.gz'
