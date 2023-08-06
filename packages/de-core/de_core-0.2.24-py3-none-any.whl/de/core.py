"""
develop and setup helper functions
==================================

this core portion of the 'de' namespace is providing helper functions for the development and the setup of namespace
root packages and their namespace portions.


helper functions
----------------

use :func:`file_content` to read e.g. the content of README file of your portion project, to provide it to the
`long_description` kwarg of `setuptools.setup`.

while :func:`code_file_version` determines the current version of any code file, :func:`bump_file_version` let you
increment this version number easily.

use the function :func:`sh_exec` to execute any console commands, optionally getting back the console output (from
stdout/stderr) as a list of output lines.


namespace environment variables
-------------------------------

the function :func:`namespace_env_vars` returns a complete mapping of the properties (names, urls, file paths, version,
...) of your namespace portion::

    nev = namespace_env_vars()

after adding this function call at the top of the `setup.py` file of your namespace portion project you can easily
access the properties from the `nev` variable, either via :func:`nev_str`, :func:`nev_val` or directly via getitem. the
following example is retrieving a string property reflecting the package name of a portion::

    package_name = nev_str(nev, 'package_name')

other useful properties in the `nev` mapping dictionary are e.g. `package_version` (taken from the __version__ variable
of your portion) or `repo_root` (the url to the remote/origin repository of your portion at gitlab.com). for a complete
list check the returned `nev` variable or the code in the function :func:`namespace_env_vars`.


using setup hooks to adapt/extend individual namespace portions
---------------------------------------------------------------

the variables and constants of the namespace environment mapping can be adopted individually for each portion of
your namespace by adding a hook method to your portions project. the default hook name is specified by the namespace
environment constant :data:`NAMESPACE_EXTEND_ENTRY_POINT`.


using templates for common files of the namespace portions
----------------------------------------------------------

this portion can also be used in the root package/portion of your namespace to create, maintain, update and deploy
common files for all the other portions.


installation and setup
----------------------

use pip to install this package for your namespace root and each of their portions::

    pip install de_core

within the file `setup.py` (respectively `setup.cfg`) of your namespace portion project add this package to
`install_requires` and `setup_requires` kwargs of the `setuptools.setup` method (respectively the related config
variables).

setup files can alternatively be created and maintained as templates within the root package project of your
namespace and then batch deployed from there to the individual portions.

.. hint:: an example of such a root project is `the ae namespace root project <https://gitlab.com/ae-group/ae>`_.


optional dependencies
---------------------

.. note::
    this portion has two optional dependencies that are only needed for special cases, like setup hooks or template
    processing.

the :mod:`ae.literal` portion of the 'ae' namespace is optionally needed for
:func:`de.core.replace_with_file_content_or_default` (which is currently used only used by the 'ae' namespace root
package to patch the .gitlab-ci.yml file for the portions ae.db_pg, ae.gui_app and ae.kivy_app).

the :mod:`ae.inspector` portion of the 'ae' namespace is optionally needed as fallback for
:func:`de.core.replace_with_file_content_or_default` and for :func:`de.core.nev_update_hook` (which is currently not
used by any ae portion).

therefore if your namespace portion or app is using one of these two helper functions than the containing repository
project has to include :mod:`ae.inspector` respective :mod:`ae.literal` explicitly in their requirements.txt respective
test_requirements.txt files.
"""
import glob
import os
import re
import subprocess
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union


__version__ = '0.2.24'       # also change in setup.py


NevVarType = Union[str, List[str], Tuple[str, ...]]
NevType = Dict[str, NevVarType]


NAMESPACE_EXTEND_ENTRY_POINT = "setup_hooks:extend_namespace_env_vars"  #: default extend nev hook

PORTIONS_COMMON_DIR = 'portions_common_root'            #: default folder in root package for portions common files

APP_PRJ: str = 'app'                                    #: application project type
MODULE_PRJ: str = 'module'                              #: module portion/project type
PACKAGE_PRJ: str = 'sub-package'                        #: sub-package portion/project type
ROOT_PRJ: str = 'namespace-root'                        #: namespace root project type

PY_EXT = '.py'                                          #: default file extension for portions and hooks

REQ_FILE_NAME = 'requirements.txt'                      #: default file name for all/dev requirements
REQ_TEST_FILE_NAME = 'test_requirements.txt'            #: default file name for test requirements

TEMPLATE_FILE_NAME_PREFIX = 'de_tpl_'                   #: template file name prefix
TEMPLATE_PLACEHOLDER_ID_PREFIX = "# "                   #: template id prefix marker
TEMPLATE_PLACEHOLDER_ID_SUFFIX = "#("                   #: template id suffix marker
TEMPLATE_PLACEHOLDER_ARGS_SUFFIX = ")#"                 #: template args suffix marker
TEMPLATE_INCLUDE_FILE_PLACEHOLDER_ID = "IncludeFile"    #: placeholder id (func:`replace_with_file_content_or_default`)

TESTS_FOLDER = 'tests'                                  #: folder name to store unit/integration tests

VERSION_QUOTE = "'"
VERSION_PREFIX = "__version__ = " + VERSION_QUOTE
VERSION_MATCHER = re.compile("^" + VERSION_PREFIX + r"(\d+)[.](\d+)[.](\d+)[a-z]*" + VERSION_QUOTE, re.MULTILINE)
""" pre-compiled regular expression for to detect and bump the app/portion file version numbers of a version string """


def bump_file_version(file_name: str, version_part: int = 3) -> str:
    """ increment part of version number of module/script file, also removing any pre/alpha version number suffixes.

    :param file_name:           module/script file name to be patched/version-bumped.
    :param version_part:        version number part to increment: 1=mayor, 2=minor, 3=build/revision (default=3).
    :return:                    empty string on success, else error string.
    """
    msg = f"bump_file_version({file_name}) expects "
    if not os.path.exists(file_name):
        return msg + f"existing code file in folder {os.getcwd()}"
    content = file_content(file_name)
    if not content:
        return msg + f"non-empty code file in {os.getcwd()}"

    content, replaced = VERSION_MATCHER.subn(
        lambda m: VERSION_PREFIX + ".".join(str(int(m.group(p)) + 1) if p == version_part else m.group(p)
                                            for p in range(1, 4)) + VERSION_QUOTE,
        content)

    if replaced != 1:
        return msg + f"single occurrence of module variable __version__, but found {replaced} times"
    with open(file_name, 'w') as file_handle:
        file_handle.write(content)
    return ""


def code_file_version(file_name: str) -> str:
    """ read version of Python code file - from __version__ module variable initialization.

    :param file_name:           name (and optional path) of module/script file to read the version number from.
    :return:                    version number string or empty string if file or version-in-file not found.
    """
    try:
        content = file_content(file_name)
        version_match = re.search("^" + VERSION_PREFIX + "([^" + VERSION_QUOTE + "]*)" + VERSION_QUOTE, content, re.M)
    except (FileNotFoundError, OSError):
        version_match = None
    return version_match.group(1) if version_match else ""


def file_content(file_name: str) -> str:
    """ returning content of the file specified by file_name arg as string.

    :param file_name:           file name to load into a string.
    :return:                    file content string.
    """
    with open(file_name) as file_handle:
        return file_handle.read()


def find_package_data(namespace_name: str, portion_name: str) -> List[str]:
    """ find kv lang files, i18n translation texts, images and sound resource files of package portion.

    :param namespace_name:      name space name/id.
    :param portion_name:        portion name.
    :return:                    list of resource files to be used in the setup package_data kwarg value.
    """
    pgk_path = os.path.join(namespace_name, portion_name)
    files = list()

    for file in glob.glob(os.path.join(pgk_path, "**", "*.kv"), recursive=True):
        if os.path.isfile(file):
            files.append(os.path.relpath(file, pgk_path))

    for resource_folder in ('img', 'loc', 'snd'):
        for file in glob.glob(os.path.join(pgk_path, resource_folder, "**", "*"), recursive=True):
            if os.path.isfile(file):
                files.append(os.path.relpath(file, pgk_path))

    return files


def load_requirements(namespace_name: str, nev: NevType, path: str) -> List[str]:
    """ load requirements from *requirements.txt and return list of portions package names.

    :param namespace_name:      name space name/id.
    :param nev:                 dict of namespace environment variables.
    :param path:                folder from where to load the *requirements.txt files.
    :return:                    portion package names.
    """
    dev_require: List[str] = list()
    requirements_file = os.path.join(path, nev_str(nev, 'REQ_FILE_NAME'))
    if os.path.exists(requirements_file):
        dev_require.extend(
            _ for _ in file_content(requirements_file).strip().split('\n') if _ and not _.startswith('#'))
    if 'de_core' not in dev_require:
        dev_require.append('de_core')
    nev['docs_require'] = [_ for _ in dev_require if _.startswith('sphinx_')]
    nev['install_require'] = [_ for _ in dev_require if _ and not _.startswith('sphinx_')]
    # if a namespace portion is needed for the setup process then use hyphen/dash instead of underscore
    # e.g. ae-literal instead of ae_literal (then ae.literal will be included in setup_require)
    nev['setup_require'] = [_ for _ in nev['install_require'] if not _.startswith(f'{namespace_name}_')]
    nev['portions_package_names'] = portions_package_names = [_ for _ in dev_require
                                                              if _.startswith(f'{namespace_name}_')]

    tests_require: List[str] = list()
    requirements_file = os.path.join(path, nev_str(nev, 'REQ_TEST_FILE_NAME'))
    if os.path.exists(requirements_file):
        tests_require.extend(_ for _ in file_content(requirements_file).strip().split('\n') if not _.startswith('#'))
    nev['tests_require'] = tests_require

    return portions_package_names


def namespace_guess(root_path: str) -> str:
    """ guess name of namespace name from the package/app/project directory content.

    :param root_path:           optional rel/abs path to package/app/project root (def=current working directory).
    :return:                    name-prefix of the current folder.
    """
    return os.path.basename(root_path).split("_", maxsplit=1)[0]


def namespace_env_vars(namespace_name: str = "", root_path: str = "", old_nev: Optional[NevType] = None) -> NevType:
    """ analyse and map the development environment of a package/app/project into a dict of variables.

    :param namespace_name:      name of this namespace (def=value returned by :func:`namespace_guess`).
    :param root_path:           optional rel/abs path of package/app/project root (def=current working directory).
    :param old_nev              optional current namespace environment variables to be updated (and returned).
    :return:                    namespace environment variables/info dict (:paramref:`~namespace_env_vars.old_nev`).
    """
    if isinstance(old_nev, dict):
        nev: NevType = old_nev
    else:
        nev = dict()
        for var_name, var_val in globals().items():
            if not var_name.startswith('_') and var_name not in nev and isinstance(var_val, str):
                nev[var_name] = var_val     # add string globals like PORTIONS_COMMON_DIR if not already added

    if not root_path:
        root_path = os.getcwd()
    elif not os.path.isabs(root_path):
        root_path = os.path.join(os.getcwd(), root_path)
    nev['root_path'] = root_path

    if os.path.exists(os.path.join(root_path, 'conf.py')):  # called by RTDocs build
        setup_path = os.path.join(root_path, '..')
    else:
        setup_path = root_path
    nev['setup_path'] = setup_path
    setup_file = os.path.join(setup_path, 'setup.py')
    if os.path.exists(setup_file):
        nev['setup_file'] = setup_file

    if not namespace_name:
        namespace_name = namespace_guess(setup_path)
    nev['namespace_name'] = namespace_name

    # extend nev with all requirement-types, read from all *requirements.txt files
    load_requirements(namespace_name, nev, setup_path)
    nev['project_license'] = "OSI Approved :: GNU General Public License v3 or later (GPLv3+)"
    nev['pypi_root'] = "https://pypi.org/project"
    nev['repo_root'] = f"https://gitlab.com/{namespace_name}-group"
    nev['repo_pages'] = f"https://{namespace_name}-group.gitlab.io"
    if os.path.exists(os.path.join(setup_path, 'buildozer.spec')):  # ae.base.BUILD_CONFIG_FILE
        nev['project_type'] = APP_PRJ
        update_app_env_vars(nev)
    else:
        portion_root_path = os.path.join(setup_path, namespace_name)
        portion_type, portion_name, portion_modules = portion_type_name_modules(portion_root_path)
        if portion_type:
            nev['project_type'] = portion_type
            nev['portion_name'] = portion_name
            nev['portion_modules'] = portion_modules
            update_portion_env_vars(nev)
        elif 'setup_file' in nev:
            nev['project_type'] = ROOT_PRJ
            update_root_env_vars(nev)
        else:
            nev['project_type'] = ''

    # finally check if optional hook exists and if yes then run it for to change the nev values accordingly
    if nev_update_hook(nev, root_path) and old_nev is None:
        # run this function one time recursively for to update nev with extended env var values
        nev = namespace_env_vars(namespace_name=namespace_name, root_path=root_path, old_nev=nev)

    return nev


def nev_update_hook(nev: NevType, path: str = "") -> bool:
    """ check if optional NAMESPACE_EXTEND_ENTRY_POINT hook file exists and if yes then run it to change nev values.

    :param nev:                 namespace environment variables.
    :param path:                optional path where the hook file is situated (only needed if path is not is sys.path).
    :return:                    True if nev got updated, else False.
    """
    try:
        from ae.inspector import module_callable, try_call      # type: ignore   # mypy
    except ImportError:                                         # pragma: no cover
        return False

    entry_point = nev_str(nev, 'NAMESPACE_EXTEND_ENTRY_POINT')
    module, callee = module_callable(entry_point, module_path=path)
    if module and callee:
        try_call(callee, nev)
        if nev_str(nev, 'NAMESPACE_EXTEND_ENTRY_POINT') != entry_point:
            # run the redirected hook recursively, now with a new hook file or function name
            nev_update_hook(nev, path=path)
        return True
    return False


def nev_str(nev: NevType, var_name: str) -> str:
    """ determine string value of namespace environment variable from passed nev or use default.

    AssertionError will be raised if the specified variable value is not of type str. use :func:`nev_val` instead.

    :param nev:                 namespace environment variables.
    :param var_name:            name of variable.
    :return:                    variable value or if not exists in nev then the constant/default value of this module or
                                an empty string. AssertionError will be raised if the specified variable value is not of
                                type str. Use :func:`nev_val` instead.
    """
    val = nev_val(nev, var_name)
    assert isinstance(val, str), f"nev_str() returns environment variable values of type string, got {type(val)}"
    return val


def nev_val(nev: NevType, var_name: str) -> NevVarType:
    """ determine value of namespace environment variable from passed nev or use default.

    :param nev:                 namespace environment variables.
    :param var_name:            name of variable.
    :return:                    variable value or if not exists in nev then the constant/default value of this module or
                                empty-string/"".
    """
    return nev.get(var_name, globals().get(var_name, ""))


def patch_string(string: str, placeholder: str, replacer: Callable[[str], str], nev: Optional[NevType] = None) -> str:
    """ load file content, then replace patch_name placeholders and return patched/extended file content.

    :param string:              file name to patch (mostly a template).
    :param placeholder:         name/id of the placeholder.
    :param replacer:            callable to convert placeholder args into replacement string.
    :param nev:                 optional namespace environment vars used (needed if TEMPLATE_* constants got patched).
    :return:                    file content extended with include snippets found in the same directory.
    """
    if nev is None:
        nev = dict()

    beg = 0
    pre = nev_str(nev, 'TEMPLATE_PLACEHOLDER_ID_PREFIX') + placeholder + nev_str(nev, 'TEMPLATE_PLACEHOLDER_ID_SUFFIX')
    len_pre = len(pre)
    suf = nev_str(nev, 'TEMPLATE_PLACEHOLDER_ARGS_SUFFIX')
    len_suf = len(suf)

    while True:
        beg = string.find(pre, beg)
        if beg == -1:
            break
        end = string.find(suf, beg)
        assert end != -1, f"patch_string() is missing args suffix marker ({suf})"
        string = string[:beg] + replacer(string[beg + len_pre: end]) + string[end + len_suf:]

    return string


def patch_templates(nev: NevType, *exclude_folders: str, **replacer: Callable[[str], str]) -> List[str]:
    """ convert ae namespace package templates found in the cwd or underneath (except excluded) to the final files.

    :param nev:                 dict namespace environment variables (determined by :func:`namespace_env_vars`).
    :param exclude_folders:     directory name prefixes that will be excluded from templates search.
    :param replacer:            optional dict of replacer with key=placeholder-id and value=callable.
                                if not passed then only the replacer with id TEMPLATE_INCLUDE_FILE_PLACEHOLDER_ID and
                                its callable/func :func:`replace_with_file_content_or_default` will be executed.
    :return:                    list of patched template file names.
    """
    patched = list()
    fn_prefix = nev_str(nev, 'TEMPLATE_FILE_NAME_PREFIX')
    if len(replacer) == 0:
        replacer[nev_str(nev, 'TEMPLATE_INCLUDE_FILE_PLACEHOLDER_ID')] = replace_with_file_content_or_default
    for file_path in glob.glob(f"**/{fn_prefix}*.*", recursive=True):
        for folder_prefix in exclude_folders:
            if file_path.startswith(folder_prefix):
                break
        else:
            content = file_content(file_path)
            content = content.format(**nev)
            for key, func in replacer.items():
                content = patch_string(content, key, func)
            path, file = os.path.split(file_path)
            with open(os.path.join(path, file[len(fn_prefix):]), 'w') as file_handle:
                file_handle.write(content)
            patched.append(file_path)
    return patched


def portion_type_name_modules(portion_root_path: str) -> Tuple[str, str, Tuple[str, ...]]:
    """ determine portion type, name and optional portion modules (if portion is a sub-package).

    :param portion_root_path:   file path of the root of the namespace portions.
    :return:                    the portion type, the portion name/placeholder and a tuple of package module names.
    """
    if not os.path.exists(portion_root_path):
        # return placeholders if not run/imported by portion repository (e.g. imported by namespace root repo)
        return "", "{portion-name}", ()

    # first search for single module portion
    files = glob.glob(os.path.join(portion_root_path, '*' + PY_EXT))
    if len(files) == 1:
        return MODULE_PRJ, os.path.basename(files[0])[:-len(PY_EXT)], ()
    if len(files) > 1:
        raise RuntimeError(f"More than one portion module found: {files}")

    # must be a sub-package (with optional extra modules)
    files = glob.glob(os.path.join(portion_root_path, '*', '*' + PY_EXT))
    if len(files) == 0:
        raise RuntimeError(f"Neither {MODULE_PRJ} nor {PACKAGE_PRJ} found in package path {portion_root_path}")
    extra_modules = list()
    name = ""
    for file_path in files:
        path, mod = os.path.split(file_path)
        if mod == '__init__' + PY_EXT:
            name = os.path.basename(path)
        else:
            extra_modules.append(mod)
    return PACKAGE_PRJ, name, tuple(extra_mod[:-len(PY_EXT)] for extra_mod in extra_modules)


def replace_with_file_content_or_default(args_str: str) -> str:
    """ return file content if file name specified in first string arg exists, else return empty string or 2nd arg str.

    :param args_str:            pass either file name or file name and default string separated by a comma character.
    :return:                    file content or default string or empty string (if file not exists and no default string
                                defined as 2nd argument string).
    """
    file_name, *default = args_str.split(",", maxsplit=1)
    file_name = file_name.strip()
    if os.path.exists(file_name):
        ret = file_content(file_name)
    elif default:
        try:
            # noinspection PyUnresolvedReferences
            from ae.literal import Literal              # type: ignore  # mypy
            ret = Literal(default[0]).value
        except ImportError:                             # pragma: no cover
            try:
                # noinspection PyUnresolvedReferences
                from ae.inspector import try_eval       # type: ignore  # mypy
                # noinspection PyUnresolvedReferences
                from ae.base import UNSET               # type: ignore  # mypy

                ret = try_eval(default[0], ignored_exceptions=(Exception, ))
                if ret is UNSET:
                    ret = default[0]

            except ImportError:
                ret = default[0]
    else:
        ret = ""
    return ret


def sh_exec(command_line: str, extra_args: Sequence = (), console_input: str = "",
            lines_output: Optional[List[str]] = None, app: Optional[Any] = None) -> int:
    """ execute command in the current working directory of the OS console/shell.

    :param command_line:        command line string - optionally including arguments - to execute on the console/shell.
    :param extra_args:          optional sequence of extra command line arguments.
    :param console_input:       optional string to be sent to the stdin stream of the console/shell.
    :param lines_output:        optional list to return the lines printed to stdout/stderr on execution.
    :param app:                 optional :class:`~ae.console.ConsoleApp` instance, only used for logging.
    :return:                    return code of the executed command or 999 if execution raised any other exception.
    """
    args = command_line.split(' ') + list(extra_args)
    print_out = app.po if app else print
    print_out(f".     executing at {os.getcwd()}: {args}")
    pipe = None if lines_output is None else subprocess.PIPE
    run_result: Union[subprocess.CompletedProcess, subprocess.CalledProcessError]   # having: stdout/stderr/returncode
    try:
        run_result = subprocess.run(args, stdout=pipe, stderr=pipe, input=console_input.encode(), check=True)
    except subprocess.CalledProcessError as ex:                                             # pragma: no cover
        print_out(f"****  subprocess.run({args}) returned non-zero exit code {ex.returncode}; exception={ex}")
        run_result = ex
    except Exception as ex:
        print_out(f"****  subprocess.run({args}) raised exception {ex}")
        return 999

    if lines_output is not None:
        if run_result.stdout:
            lines_output.extend([line for line in run_result.stdout.decode().split('\n') if line])
        if run_result.stderr:
            lines_output.append(f"STDERR={run_result.stderr.decode()}")
    return run_result.returncode


def update_app_env_vars(nev: NevType):
    """ update dev env for an app project. """
    nev['root_version'] = code_file_version('main.py')


def update_portion_env_vars(nev: NevType):
    """ update dev env with portion project info. """
    namespace_name = nev_str(nev, 'namespace_name')      # ==cast(str, nev['namespace_name']) for mypy
    portion_name = nev_str(nev, 'portion_name')
    portion_type = nev['project_type']
    setup_path = nev_str(nev, 'setup_path')
    portion_root_path = os.path.join(setup_path, namespace_name)

    nev['portion_file_name'] = portion_file_name = \
        portion_name + (os.path.sep + '__init__.py' if portion_type == PACKAGE_PRJ else nev_str(nev, 'PY_EXT'))
    nev['portion_file_path'] = portion_file_path = \
        os.path.abspath(os.path.join(portion_root_path, portion_file_name))
    nev['package_name'] = f"{namespace_name}_{portion_name}"
    nev['pip_name'] = f"{namespace_name}-{portion_name.replace('_', '-')}"
    nev['import_name'] = f"{namespace_name}.{portion_name}"
    nev['package_version'] = code_file_version(portion_file_path)
    nev['portion_pypi_root'] = f"{nev['pypi_root']}/{nev['pip_name']}"

    nev['find_packages_include'] = [namespace_name + (".*" if portion_type == PACKAGE_PRJ else "")]
    nev['package_resources'] = find_package_data(namespace_name, portion_name)


def update_root_env_vars(nev: NevType):
    """ update dev env with info of the namespace root project. """
    namespace_name = nev_str(nev, 'namespace_name')     # ==cast(str, nev['namespace_name']) for mypy
    namespace_len = len(namespace_name)
    setup_path = nev_str(nev, 'setup_path')

    nev['root_version'] = code_file_version(nev_str(nev, 'setup_file'))

    pypi_refs = list()
    idx_names = list()
    for p_name in nev['portions_package_names']:
        pypi_refs.append(f'* [{p_name}]({nev["pypi_root"]}/{p_name} "{namespace_name} namespace portion {p_name}")')
        dot_name = p_name[:namespace_len] + '.' + p_name[namespace_len + 1:]
        idx_names.append(dot_name)
        _pt, _pn, extra_modules = portion_type_name_modules(os.path.join(setup_path, '..', p_name, namespace_name))
        for e_mod in extra_modules:
            idx_names.append(dot_name + '.' + e_mod)
    nev['portions_pypi_refs_md'] = "\n".join(pypi_refs)                 # used in root README.md.tpl
    nev['portions_import_names'] = ("\n" + " " * 4).join(idx_names)     # used in docs/index.rst.tpl
