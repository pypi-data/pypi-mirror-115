from pathlib import Path, PurePosixPath
import datetime
import logging
from uuid import UUID
import itertools

import requests.exceptions

from iblutil.io import hashfile

import one.alf.io as alfio
from one.alf.files import rel_path_parts, session_path_parts, get_session_path
import one.alf.exceptions as alferr
from one.api import ONE
from one.util import ensure_list

_logger = logging.getLogger(__name__)


def register_dataset(file_list, one=None, created_by=None, repository=None, server_only=False,
                     versions=None, default=True, dry=False, max_md5_size=None):
    """
    Registers a set of files belonging to a session only on the server

    Parameters
    ----------
    file_list : list, str, pathlib.Path
        A filepath (or list thereof) of ALF datasets to register to Alyx
    one : one.api.OneAlyx
        Optional one object, will create a default instance if none provided
    created_by : str
        Name of Alyx user (defaults to whoever is logged in to ONE instance)
    repository : str
        Name of the repository in Alyx to register to
    server_only : bool
        Will only create file records in the 'online' repositories and skips local repositories
    versions : list of str
        Optional version tags
    default : bool
        Whether to set as default revision (defaults to True)
    dry : bool
        When true returns POST data for registration endpoint without submitting the data
    max_md5_size : int
        Maximum file in bytes to compute md5 sum (always compute if None)

    Returns
    -------
        A list of newly created Alyx dataset records or the registration data if dry == true
    """
    if created_by is None:
        created_by = getattr(one.alyx, 'user', None)
    if file_list is None or file_list == '' or file_list == []:
        return
    elif not isinstance(file_list, list):
        file_list = [Path(file_list)]

    assert len(set(get_session_path(f) for f in file_list)) == 1, 'Multiple sessions in list'

    assert all([Path(f).exists() for f in file_list])
    if isinstance(versions, str):
        versions = [versions for _ in file_list]
    assert isinstance(versions, list) and len(versions) == len(file_list)

    # Determine revisions from file paths
    revisions = [rel_path_parts(x, assert_valid=False)[1] for x in file_list]

    # computing the md5 can be very long, so this is an option to skip if the file is bigger
    # than a certain threshold
    if max_md5_size:
        hashes = [hashfile.md5(p) if
                  p.stat().st_size < max_md5_size else None for p in file_list]
    else:
        hashes = [hashfile.md5(p) for p in file_list]

    session_path = get_session_path(file_list[0])

    # first register the file
    r = {'created_by': created_by,
         'path': session_path.relative_to((session_path.parents[2])).as_posix(),
         'filenames': [p.relative_to(session_path).as_posix() for p in file_list],
         'name': repository,
         'server_only': server_only,
         'hashes': hashes,
         'filesizes': [p.stat().st_size for p in file_list],
         'versions': versions,
         'revisions': revisions,
         'default': default}
    if not dry:
        one = one or ONE()
        response = one.alyx.rest('register-file', 'create', data=r, no_cache=True)
        for p in file_list:
            _logger.info(f"ALYX REGISTERED DATA: {p}")
        return response
    else:
        return r


class RegistrationClient:
    """
    Object that keeps the ONE instance and provides method to create sessions and register data.
    """
    def __init__(self, one=None):
        self.one = one
        if not one:
            self.one = ONE(cache_rest=None)
        self.dtypes = self.one.alyx.rest('dataset-types', 'list')
        self.registration_patterns = [
            dt['filename_pattern'] for dt in self.dtypes if dt['filename_pattern']]
        self.file_extensions = [df['file_extension'] for df in
                                self.one.alyx.rest('data-formats', 'list', no_cache=True)]

    def create_sessions(self, root_data_folder, glob_pattern='**/create_me.flag', dry=False):
        """
        Create sessions looking recursively for flag files

        Parameters
        ----------
        root_data_folder : str, pathlib.Path
            Folder to look for sessions
        glob_pattern : str
            Register valid sessions that contain this pattern
        dry : bool
            If true returns list of sessions without creating them on Alyx

        Returns
        -------
            TODO document return values
        """
        flag_files = Path(root_data_folder).glob(glob_pattern)
        for flag_file in flag_files:
            if dry:
                print(flag_file)
                continue
            _logger.info('creating session for ' + str(flag_file.parent))
            # providing a false flag stops the registration after session creation
            self.create_session(flag_file.parent)
            flag_file.unlink()
        return [ff.parent for ff in flag_files]

    def create_session(self, session_path):
        """
        create_session(session_path)
        """
        return self.register_session(session_path, file_list=False)

    def create_new_session(self, subject, session_root=None, date=None, register=True):
        """Create a new local session folder and optionally create session record on Alyx

        Parameters
        ----------
        subject : str
            The subject name.  Must exist on Alyx.
        session_root : str, pathlib.Path
            The root folder in which to create the subject/date/number folder.  Defaults to ONE
            cache directory.
        date : datetime.datetime, datetime.date, str
            An optional date for the session.  If None the current time is used.
        register : bool
            If true, create session record on Alyx database

        Returns
        -------
        New local session path; the experiment UUID if register is true

        Examples
        --------
        # Create a local session only
        session_path, _ = RegistrationClient.create_new_session('Ian', register=False)
        # Register a session on Alyx in a specific location
        session_path, eid = RegistrationClient.create_new_session('Ian', '/data/mylab/Subjects')
        # Create a session for a given date
        session_path, eid = RegistrationClient.create_new_session('Ian', date='2020-01-01')
        """
        assert not self.one.offline, 'ONE must be in online mode'
        date = self.ensure_ISO8601(date)  # Format, validate
        # Ensure subject exists on Alyx
        self.assert_subject_exists(subject)
        session_root = Path(session_root or self.one.alyx.cache_dir) / subject / f'{date:%Y-%m-%d}'
        session_path = alfio.next_num_folder(session_root)
        eid = UUID(self.create_session(session_path)['url'][-36:]) if register else None
        return session_path, eid

    def find_files(self, session_path):
        """
        Returns an generator of file names that match one of the dataset type patterns in Alyx

        Parameters
        ----------
        session_path : str, pathlib.Path
            The session path to search

        Returns
        -------
        Iterable of file paths that match the dataset type patterns in Alyx
        """
        session_path = Path(session_path)
        types = (x['filename_pattern'] for x in self.dtypes if x['filename_pattern'])
        dsets = itertools.chain.from_iterable(session_path.rglob(x) for x in types)
        return (x for x in dsets if x.is_file() and
                any(x.name.endswith(y) for y in self.file_extensions))

    def assert_subject_exists(self, subject: str) -> None:
        """Raise an error if a given subject doesn't exist on Alyx database

        Parameters
        ----------
        subject : str
            The subject nickname to verify

        Raises
        -------
        one.alf.exceptions.AlyxSubjectNotFound
            Subject does not exist on Alyx
        requests.exceptions.HTTPError
            Failed to connect to Alyx database
        """
        try:
            subject = self.one.alyx.rest('subjects', 'read', id=subject, no_cache=True)
        except requests.exceptions.HTTPError as ex:
            if '404' not in str(ex):
                raise ex
            else:
                raise alferr.AlyxSubjectNotFound(subject)

    def assert_user_exists(self, user):
        """Raise an error if a given user doesn't exist on Alyx database

        Parameters
        ----------
        user : str, list
            The username to verify

        Raises
        -------
        one.alf.exceptions.ALFError
            User does not exist on Alyx
        requests.exceptions.HTTPError
            Failed to connect to Alyx database
        """
        if isinstance(user, str):
            try:
                self.one.alyx.rest('users', 'read', id=user, no_cache=True)
            except requests.exceptions.HTTPError as ex:
                if '404' not in str(ex):
                    raise ex
                else:
                    raise alferr.ALFError(f'User "{user}" doesn\'t exist in Alyx')
        else:
            for x in user:
                self.assert_user_exists(x)

    def assert_repository_exists(self, name):
        """

        Parameters
        ----------
        name

        Returns
        -------

        """
        try:
            self.one.alyx.rest('repository', 'read', id=name, no_cache=True)
        except requests.exceptions.HTTPError as ex:
            if '404' not in str(ex):
                raise ex
            else:
                raise alferr.ALFError(f'Repository "{name}" doesn\'t exist in Alyx')

    @staticmethod
    def ensure_ISO8601(date) -> str:
        """Ensure provided date is ISO 8601 compliant

        Parameters
        ----------
        date : str, None, datetime.date, datetime.datetime
            An optional date to convert to ISO string.  If None, the current datetime is used.

        Returns
        -------
        The datetime as an ISO 8601 str
        """
        date = date or datetime.datetime.now()  # If None get current time
        if isinstance(date, str):
            date = datetime.datetime.fromisoformat(date)  # Validate by parsing
        elif type(date) is datetime.date:
            date = datetime.datetime.fromordinal(date.toordinal())
        return datetime.datetime.isoformat(date)

    def register_session(self, ses_path, users=None, file_list=True, **kwargs):
        """
        Register session in Alyx

        Parameters
        ----------
        ses_path : str, pathlib.Path
            The local session path
        users : str, list
            The user(s) to attribute to the session
        file_list : bool, list
            An optional list of file paths to register.  If True, all valid files within the
            session folder are registered.  If False, no files are registered
        location : str
            The optional location within the lab where the experiment takes place
        procedures : str, list
            An optional list of procedures, e.g. 'Behavior training/tasks'
        n_correct_trials : int
            The number of correct trials (optional)
        n_trials : int
            The total number of completed trials (optional)
        json : dict, str
            Optional JSON data
        project: str, list
            The project(s) to which the experiment belongs (optional)
        type : str
            The experiment type, e.g. 'Experiment', 'Base'
        task_protocol : str
            The task protocol (optional)

        Returns
        -------
        TODO Document
        """
        if isinstance(ses_path, str):
            ses_path = Path(ses_path)
        details = session_path_parts(ses_path.as_posix(), as_dict=True, assert_valid=True)
        # query alyx endpoints for subject, error if not found
        self.assert_subject_exists(details['subject'])

        # look for a session from the same subject, same number on the same day
        session_id, session = self.one.search(subject=details['subject'],
                                              date_range=details['date'],
                                              number=details['number'],
                                              details=True, query_type='remote')
        users = ensure_list(users or self.one.alyx.user)
        self.assert_user_exists(users)
        # this is the generic relative path: subject/yyyy-mm-dd/NNN
        rel_path = PurePosixPath(details['subject'], details['date'], details['number'])

        # if nothing found create a new session in Alyx
        ses_ = {'subject': details['subject'],
                'users': users,
                'lab': details['lab'] or None,
                'type': 'Experiment',
                'number': details['number']}
        if kwargs.get('end_time', False):
            ses_['end_time'] = self.ensure_ISO8601(kwargs.pop('end_time'))
        start_time = kwargs.pop('start_time', None)
        if kwargs.get('procedures', False):
            ses_['procedures'] = ensure_list(kwargs.pop('procedures'))
        assert ('subject', 'number') not in kwargs
        ses_.update(kwargs)

        if not session:  # Create from scratch
            ses_['start_time'] = self.ensure_ISO8601(start_time)
            session = self.one.alyx.rest('sessions', 'create', data=ses_)
        else:  # Update existing
            if start_time:
                ses_['start_time'] = self.ensure_ISO8601(start_time)
            session = self.one.alyx.rest('sessions', 'update', id=session_id[0], data=ses_)

        _logger.info(session['url'] + ' ')
        # at this point the session has been created. If create only, exit
        if file_list: #
            self.register_datasets()

        return session

    def register_files(self, filelist):
        F = []  # empty list whose keys will be relative paths and content filenames
        md5s = []
        file_sizes = []

        for fn in self.find_files(ses_path) if file_list is True else file_list:
            if fn.suffix in EXCLUDED_EXTENSIONS:
                _logger.debug('Excluded: ', str(fn))
                continue
            if not _check_filename_for_registration(fn, self.registration_patterns):
                _logger.warning('No matching dataset type for: ' + str(fn))
                continue
            if fn.suffix not in self.file_extensions:
                _logger.warning('No matching dataformat (ie. file extension) for: ' + str(fn))
                continue
            if not _register_bool(fn.name, file_list):
                _logger.debug('Not in filelist: ' + str(fn))
                continue
            try:
                assert (str(gen_rel_path) in str(fn))
            except AssertionError as e:
                strerr = 'ALF folder mismatch: data is in wrong subject/date/number folder. \n'
                strerr += ' Expected ' + str(gen_rel_path) + ' actual was ' + str(fn)
                _logger.error(strerr)
                raise e
            # extract the relative path of the file
            rel_path = Path(str(fn)[str(fn).find(str(gen_rel_path)):])
            F.append(str(rel_path.relative_to(gen_rel_path).as_posix()))
            file_sizes.append(fn.stat().st_size)
            md5s.append(hashfile.md5(fn) if fn.stat().st_size < 1024 ** 3 else None)
            _logger.info('Registering ' + str(fn))

        r_ = {'created_by': user,
              'path': rel_path.as_posix(),
              'filenames': F,
              'hashes': md5s,
              'filesizes': file_sizes,
              'versions': [version.ibllib() for _ in F]
              }
        self.one.alyx.post('/register-file', data=r_)

    def register_water_administration(self, subject, volume, **kwargs):
        """
        Register a water administration to Alyx for a given subject

        Parameters
        ----------
        subject : str
            A subject nickname that exists on Alyx
        volume : float
            The total volume administrated in ml
        date_time : str, datetime.datetime, datetime.date
            The time of administration.  If None, the current time is used.
        water_type : str
            A water type that exists in Alyx; default is 'Water'
        user : str
            The user who administrated the water.  Currently logged-in user is the default.
        session : str, UUID, pathlib.Path, dict
            An optional experiment ID to associate
        adlib : bool
            If true, indicates that the subject was given water ad libitum

        Returns
        -------
        A water administration record

        Raises
        ------
        one.alf.exceptions.AlyxSubjectNotFound
            Subject does not exist on Alyx
        one.alf.exceptions.ALFError
            User does not exist on Alyx
        ValueError
            date_time is not a valid ISO date time or session ID is not valid
        requests.exceptions.HTTPError
            Failed to connect to database, or submitted data not valid (500)
        """
        # Ensure subject exists
        self.assert_subject_exists(subject)
        # Ensure user(s) exist
        user = ensure_list(kwargs.pop('user', [])) or self.one.alyx.user
        self.assert_user_exists(user)
        # Ensure volume not zero
        if volume == 0:
            raise ValueError('Water volume must be greater than zero')
        # Post water admin
        wa_ = {
            'subject': subject,
            'date_time': self.ensure_ISO8601(kwargs.pop('date_time', None)),
            'water_administered': float(f'{volume:.4g}'),  # Round to 4 s.f.
            'water_type': kwargs.pop('water_type', 'Water'),
            'user': user,
            'adlib': kwargs.pop('adlib', False)
        }
        # Ensure session is valid; convert to eid
        if kwargs.get('session', False):
            wa_['session'] = self.one.to_eid(kwargs.pop('session'))
            if not wa_['session']:
                raise ValueError('Failed to parse session ID')

        return self.one.alyx.rest('water-administrations', 'create', data=wa_)

    def register_weight(self, subject, weight, date_time=None, user=None):
        """
        Register a subject weight to Alyx

        Parameters
        ----------
        subject : str
            A subject nickname that exists on Alyx
        weight : float
            The subject weight in grams
        date_time : str, datetime.datetime, datetime.date
            The time of weighing.  If None, the current time is used.
        user : str
            The user who performed the weighing.  Currently logged-in user is the default.

        Returns
        -------
        An Alyx weight record

        Raises
        ------
        one.alf.exceptions.AlyxSubjectNotFound
            Subject does not exist on Alyx
        one.alf.exceptions.ALFError
            User does not exist on Alyx
        ValueError
            date_time is not a valid ISO date time or weight < 1e-4
        requests.exceptions.HTTPError
            Failed to connect to database, or submitted data not valid (500)
        """
        # Ensure subject exists
        self.assert_subject_exists(subject)
        # Ensure user(s) exist
        user = user or self.one.alyx.user
        self.assert_user_exists(user)
        # Ensure weight not zero
        if weight == 0:
            raise ValueError('Water volume must be greater than 0')

        # Post water admin
        wei_ = {'subject': subject,
                'date_time': self.ensure_ISO8601(date_time),
                'weight': float(f'{weight:.4g}'),  # Round to 4 s.f.
                'user': user}
        return self.one.alyx.rest('weighings', 'create', data=wei_)


def _register_bool(fn, file_list):
    if isinstance(file_list, bool):
        return file_list
    if isinstance(file_list, str):
        file_list = [file_list]
    return any([str(fil) in fn for fil in file_list])


def _glob_session(ses_path):
    """
    Glob for files to be registered on an IBL session

    Parameters
    ----------
    ses_path : str, pathlib.Path
        A session path

    Returns
    -------
    A list of files to potentially be registered
    """
    fl = []
    for gp in REGISTRATION_GLOB_PATTERNS:
        fl.extend(list(Path(ses_path).glob(gp)))
    return fl
