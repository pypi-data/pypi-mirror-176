
Change History
==============


0.10.2 (2022-11-12)
-------------------

Bug fixes:

- Fix failing tests on Windows.
- Type hint on *root* parameter on `pathspec.pathspec.PathSpec.match_tree_entries()`.
- Type hint on *root* parameter on `pathspec.pathspec.PathSpec.match_tree_files()`.
- Type hint on *root* parameter on `pathspec.util.iter_tree_entries()`.
- Type hint on *root* parameter on `pathspec.util.iter_tree_files()`.
- `Issue #64`_: IndexError with my .gitignore file when trying to build a Python package.

Improvements:

- `Issue #58`_: CI: add GitHub Actions test workflow.


.. _`Issue #58`: https://github.com/cpburnz/python-pathspec/pull/58
.. _`Issue #64`: https://github.com/cpburnz/python-pathspec/issues/64


0.10.1 (2022-09-02)
-------------------

Bug fixes:

- Fix documentation on `pathspec.pattern.RegexPattern.match_file()`.
- `Issue #60`_: Remove redundant wheel dep from pyproject.toml.
- `Issue #61`_: Dist failure for Fedora, CentOS, EPEL.
- `Issue #62`_: Since version 0.10.0 pure wildcard does not work in some cases.

Improvements:

- Restore support for legacy installations using `setup.py`. See `Issue #61`_.


.. _`Issue #60`: https://github.com/cpburnz/python-pathspec/pull/60
.. _`Issue #61`: https://github.com/cpburnz/python-pathspec/issues/61
.. _`Issue #62`: https://github.com/cpburnz/python-pathspec/issues/62


0.10.0 (2022-08-30)
-------------------

Major changes:

- Dropped support of EOL Python 2.7, 3.5, 3.6. See `Issue #47`_.
- The *gitwildmatch* pattern `dir/*` is now handled the same as `dir/`. This means `dir/*` will now match all descendants rather than only direct children. See `Issue #19`_.
- Added `pathspec.GitIgnoreSpec` class (see new features).
- Changed build system to `pyproject.toml`_ and build backend to `setuptools.build_meta`_ which may have unforeseen consequences.
- Renamed GitHub project from `python-path-specification`_ to `python-pathspec`_. See `Issue #35`_.

API changes:

- Deprecated: `pathspec.util.match_files()` is an old function no longer used.
- Deprecated: `pathspec.match_files()` is an old function no longer used.
- Deprecated: `pathspec.util.normalize_files()` is no longer used.
- Deprecated: `pathspec.util.iter_tree()` is an alias for `pathspec.util.iter_tree_files()`.
- Deprecated: `pathspec.iter_tree()` is an alias for `pathspec.util.iter_tree_files()`.
-	Deprecated: `pathspec.pattern.Pattern.match()` is no longer used. Use or implement
	`pathspec.pattern.Pattern.match_file()`.

New features:

- Added class `pathspec.gitignore.GitIgnoreSpec` (with alias `pathspec.GitIgnoreSpec`) to implement *gitignore* behavior not possible with standard `PathSpec` class. The particular *gitignore* behavior implemented is prioritizing patterns matching the file directly over matching an ancestor directory.

Bug fixes:

- `Issue #19`_: Files inside an ignored sub-directory are not matched.
- `Issue #41`_: Incorrectly (?) matches files inside directories that do match.
- `Issue #51`_: Refactor deprecated unittest aliases for Python 3.11 compatibility.
- `Issue #53`_: Symlink pathspec_meta.py breaks Windows.
- `Issue #54`_: test_util.py uses os.symlink which can fail on Windows.
- `Issue #55`_: Backslashes at start of pattern not handled correctly.
- `Issue #56`_: pyproject.toml: include subpackages in setuptools config
- `Issue #57`_: `!` doesn't exclude files in directories if the pattern doesn't have a trailing slash.

Improvements:

- Support Python 3.10, 3.11.
- Modernize code to Python 3.7.
- `Issue #52`_: match_files() is not a pure generator function, and it impacts tree_*() gravely.


.. _`python-path-specification`: https://github.com/cpburnz/python-path-specification
.. _`python-pathspec`: https://github.com/cpburnz/python-pathspec
.. _`pyproject.toml`: https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/
.. _`setuptools.build_meta`: https://setuptools.pypa.io/en/latest/build_meta.html
.. _`Issue #19`: https://github.com/cpburnz/python-pathspec/issues/19
.. _`Issue #35`: https://github.com/cpburnz/python-pathspec/issues/35
.. _`Issue #41`: https://github.com/cpburnz/python-pathspec/issues/41
.. _`Issue #47`: https://github.com/cpburnz/python-pathspec/issues/47
.. _`Issue #51`: https://github.com/cpburnz/python-pathspec/pull/51
.. _`Issue #52`: https://github.com/cpburnz/python-pathspec/issues/52
.. _`Issue #53`: https://github.com/cpburnz/python-pathspec/issues/53
.. _`Issue #54`: https://github.com/cpburnz/python-pathspec/issues/54
.. _`Issue #55`: https://github.com/cpburnz/python-pathspec/issues/55
.. _`Issue #56`: https://github.com/cpburnz/python-pathspec/pull/56
.. _`Issue #57`: https://github.com/cpburnz/python-pathspec/issues/57


0.9.0 (2021-07-17)
------------------

- `Issue #44`_/`Issue #50`_: Raise `GitWildMatchPatternError` for invalid git patterns.
- `Issue #45`_: Fix for duplicate leading double-asterisk, and edge cases.
- `Issue #46`_: Fix matching absolute paths.
- API change: `util.normalize_files()` now returns a `Dict[str, List[pathlike]]` instead of a `Dict[str, pathlike]`.
- Added type hinting.

.. _`Issue #44`: https://github.com/cpburnz/python-pathspec/issues/44
.. _`Issue #45`: https://github.com/cpburnz/python-pathspec/pull/45
.. _`Issue #46`: https://github.com/cpburnz/python-pathspec/issues/46
.. _`Issue #50`: https://github.com/cpburnz/python-pathspec/pull/50


0.8.1 (2020-11-07)
------------------

- `Issue #43`_: Add support for addition operator.

.. _`Issue #43`: https://github.com/cpburnz/python-pathspec/pull/43


0.8.0 (2020-04-09)
------------------

- `Issue #30`_: Expose what patterns matched paths. Added `util.detailed_match_files()`.
- `Issue #31`_: `match_tree()` doesn't return symlinks.
- `Issue #34`_: Support `pathlib.Path`\ s.
- Add `PathSpec.match_tree_entries` and `util.iter_tree_entries()` to support directories and symlinks.
- API change: `match_tree()` has been renamed to `match_tree_files()`. The old name `match_tree()` is still available as an alias.
- API change: `match_tree_files()` now returns symlinks. This is a bug fix but it will change the returned results.

.. _`Issue #30`: https://github.com/cpburnz/python-pathspec/issues/30
.. _`Issue #31`: https://github.com/cpburnz/python-pathspec/issues/31
.. _`Issue #34`: https://github.com/cpburnz/python-pathspec/issues/34


0.7.0 (2019-12-27)
------------------

- `Issue #28`_: Add support for Python 3.8, and drop Python 3.4.
- `Issue #29`_: Publish bdist wheel.

.. _`Issue #28`: https://github.com/cpburnz/python-pathspec/pull/28
.. _`Issue #29`: https://github.com/cpburnz/python-pathspec/pull/29


0.6.0 (2019-10-03)
------------------

- `Issue #24`_: Drop support for Python 2.6, 3.2, and 3.3.
- `Issue #25`_: Update README.rst.
- `Issue #26`_: Method to escape gitwildmatch.

.. _`Issue #24`: https://github.com/cpburnz/python-pathspec/pull/24
.. _`Issue #25`: https://github.com/cpburnz/python-pathspec/pull/25
.. _`Issue #26`: https://github.com/cpburnz/python-pathspec/pull/26


0.5.9 (2018-09-15)
------------------

- Fixed file system error handling.


0.5.8 (2018-09-15)
------------------

- Improved type checking.
- Created scripts to test Python 2.6 because Tox removed support for it.
- Improved byte string handling in Python 3.
- `Issue #22`_: Handle dangling symlinks.

.. _`Issue #22`: https://github.com/cpburnz/python-pathspec/issues/22


0.5.7 (2018-08-14)
------------------

- `Issue #21`_: Fix collections deprecation warning.

.. _`Issue #21`: https://github.com/cpburnz/python-pathspec/issues/21


0.5.6 (2018-04-06)
------------------

- Improved unit tests.
- Improved type checking.
- `Issue #20`_: Support current directory prefix.

.. _`Issue #20`: https://github.com/cpburnz/python-pathspec/issues/20


0.5.5 (2017-09-09)
------------------

- Add documentation link to README.


0.5.4 (2017-09-09)
------------------

- `Issue #17`_: Add link to Ruby implementation of *pathspec*.
- Add sphinx documentation.

.. _`Issue #17`: https://github.com/cpburnz/python-pathspec/pull/17


0.5.3 (2017-07-01)
------------------

- `Issue #14`_: Fix byte strings for Python 3.
- `Issue #15`_: Include "LICENSE" in source package.
- `Issue #16`_: Support Python 2.6.

.. _`Issue #14`: https://github.com/cpburnz/python-pathspec/issues/14
.. _`Issue #15`: https://github.com/cpburnz/python-pathspec/pull/15
.. _`Issue #16`: https://github.com/cpburnz/python-pathspec/issues/16


0.5.2 (2017-04-04)
------------------

- Fixed change log.


0.5.1 (2017-04-04)
------------------

- `Issue #13`_: Add equality methods to `PathSpec` and `RegexPattern`.

.. _`Issue #13`: https://github.com/cpburnz/python-pathspec/pull/13


0.5.0 (2016-08-22)
------------------

- `Issue #12`_: Add `PathSpec.match_file()`.
- Renamed `gitignore.GitIgnorePattern` to `patterns.gitwildmatch.GitWildMatchPattern`.
- Deprecated `gitignore.GitIgnorePattern`.

.. _`Issue #12`: https://github.com/cpburnz/python-pathspec/issues/12


0.4.0 (2016-07-15)
------------------

- `Issue #11`_: Support converting patterns into regular expressions without compiling them.
- API change: Subclasses of `RegexPattern` should implement `pattern_to_regex()`.

.. _`Issue #11`: https://github.com/cpburnz/python-pathspec/issues/11


0.3.4 (2015-08-24)
------------------

- `Issue #7`_: Fixed non-recursive links.
- `Issue #8`_: Fixed edge cases in gitignore patterns.
- `Issue #9`_: Fixed minor usage documentation.
- Fixed recursion detection.
- Fixed trivial incompatibility with Python 3.2.

.. _`Issue #7`: https://github.com/cpburnz/python-pathspec/pull/7
.. _`Issue #8`: https://github.com/cpburnz/python-pathspec/pull/8
.. _`Issue #9`: https://github.com/cpburnz/python-pathspec/pull/9


0.3.3 (2014-11-21)
------------------

- Improved documentation.


0.3.2 (2014-11-08)
------------------

- `Issue #5`_: Use tox for testing.
- `Issue #6`_: Fixed matching Windows paths.
- Improved documentation.
- API change: `spec.match_tree()` and `spec.match_files()` now return iterators instead of sets.

.. _`Issue #5`: https://github.com/cpburnz/python-pathspec/pull/5
.. _`Issue #6`: https://github.com/cpburnz/python-pathspec/issues/6


0.3.1 (2014-09-17)
------------------

- Updated README.


0.3.0 (2014-09-17)
------------------

- `Issue #3`_: Fixed trailing slash in gitignore patterns.
- `Issue #4`_: Fixed test for trailing slash in gitignore patterns.
- Added registered patterns.

.. _`Issue #3`: https://github.com/cpburnz/python-pathspec/pull/3
.. _`Issue #4`: https://github.com/cpburnz/python-pathspec/pull/4


0.2.2 (2013-12-17)
------------------

- Fixed setup.py.


0.2.1 (2013-12-17)
------------------

- Added tests.
- Fixed comment gitignore patterns.
- Fixed relative path gitignore patterns.


0.2.0 (2013-12-07)
------------------

- Initial release.
