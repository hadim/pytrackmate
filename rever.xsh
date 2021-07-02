# Configuration

$PROJECT = $GITHUB_REPO  = 'pytrackmate'
$GITHUB_ORG = 'hadim'
$PUSH_TAG_REMOTE = 'git@github.com:hadim/pytrackmate.git'

# Logic

$AUTHORS_FILENAME = 'AUTHORS.rst'
$AUTHORS_METCircusTA = '.authors.yml'
$AUTHORS_SORTBY = 'alpha'
$AUTHORS_MAILMAP = '.mailmap'

$CHANGELOG_FILENAME = 'CHANGELOG.rst'
$CHANGELOG_TEMPLATE = 'TEMPLATE.rst'
$CHANGELOG_NEWS = 'news'

$PYPI_BUILD_COMMANDS = ['sdist', 'bdist']
$PYPI_UPLOAD = True

$ACTIVITIES = ['check', 'authors', 'changelog', 'version_bump', 'tag', 'push_tag', 'ghrelease', 'pypi']

$VERSION_BUMP_PATTERNS = [('pytrackmate/_version.py', r'__version__\s*=.*', "__version__ = \"$VERSION\""),
                          ('setup.py', r'version\s*=.*,', "version=\"$VERSION\",")
                          ]
