"""Module of infoset database functions.

Classes for agent data

"""
# Python standard libraries
from collections import defaultdict

# Infoset libraries
from infoset.utils import log
from infoset.utils import jm_general
from infoset.db import db
from infoset.db.db_orm import Agent, Datapoint


class GetIDX(object):
    """Class to return agent data.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, idx_agent):
        """Function for intializing the class.

        Args:
            idx_agent: Agent idx

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)

        # Get the result
        database = db.Database()
        session = database.session()
        result = session.query(Agent).filter(
            Agent.idx == idx_agent)

        # Massage data
        if result.count() == 1:
            for instance in result:
                self.data_dict['uid'] = jm_general.decode(instance.id)
                self.data_dict['name'] = jm_general.decode(instance.name)
                self.data_dict['enabled'] = instance.enabled
                self.data_dict['last_timestamp'] = instance.last_timestamp
                break
        else:
            log_message = ('Agent IDX %s not found.') % (idx_agent)
            log.log2die(1035, log_message)

        # Return the session to the database pool after processing
        session.close()

    def uid(self):
        """Get uid value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['uid']
        return value

    def name(self):
        """Get agent name.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['name']
        return value

    def enabled(self):
        """Get agent enabled.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = bool(self.data_dict['enabled'])

        # Return
        return value

    def last_timestamp(self):
        """Get agent last_timestamp.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['last_timestamp']
        return value

    def everything(self):
        """Get all agent data.

        Args:
            None

        Returns:
            value: Data as a dict

        """
        # Initialize key variables
        value = self.data_dict
        return value


class GetUID(object):
    """Class to return agent data.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, uid):
        """Function for intializing the class.

        Args:
            uid: UID of agent

        Returns:
            None

        """
        # Initialize important variables
        self.data_dict = defaultdict(dict)
        value = uid.encode()
        self.uid = value

        # Establish a database session
        database = db.Database()
        session = database.session()
        result = session.query(Agent).filter(Agent.id == value)

        # Massage data
        if result.count() == 1:
            for instance in result:
                self.data_dict['idx'] = instance.idx
                self.data_dict['name'] = jm_general.decode(instance.name)
                self.data_dict['enabled'] = instance.enabled
                self.data_dict['last_timestamp'] = instance.last_timestamp
                break
        else:
            log_message = ('uid %s not found.') % (value)
            log.log2die(1042, log_message)

        # Return the session to the database pool after processing
        session.close()

    def idx(self):
        """Get idx value.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['idx']
        return value

    def name(self):
        """Get agent name.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['name']
        return value

    def enabled(self):
        """Get agent enabled.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = bool(self.data_dict['enabled'])

        # Return
        return value

    def last_timestamp(self):
        """Get agent last_timestamp.

        Args:
            None

        Returns:
            value: Value to return

        """
        # Initialize key variables
        value = self.data_dict['last_timestamp']
        return value

    def everything(self):
        """Get all agent data.

        Args:
            None

        Returns:
            value: Data as a dict

        """
        # Initialize key variables
        value = self.data_dict
        return value


class GetDataPoint(object):
    """Class to return agent data.

    Args:
        None

    Returns:
        None

    Methods:

    """

    def __init__(self, idx_agent):
        """Function for intializing the class.

        Args:
            idx: idx of agent

        Returns:
            None

        """
        # Initialize important variables
        self.data_point_dict = defaultdict(dict)

        # Get the result
        database = db.Database()
        session = database.session()
        result = session.query(Datapoint).filter(
            Datapoint.idx_agent == idx_agent)

        # Massage data
        if result.count() > 0:
            for instance in result:
                agent_label = jm_general.decode(instance.agent_label)
                idx = instance.idx
                uncharted_value = jm_general.decode(instance.uncharted_value)
                self.data_point_dict[agent_label] = (idx, uncharted_value)
        else:
            log_message = ('Agent idx %s not found.') % (idx_agent)
            log.log2die(1050, log_message)

        # Return the session to the database pool after processing
        session.close()

    def everything(self):
        """Get all datapoints.

        Args:
            None

        Returns:
            value: Dictionary of data_points

        """
        # Return
        value = self.data_point_dict
        return value


def uid_exists(uid):
    """Determine whether the UID exists.

    Args:
        uid: UID value for agent

    Returns:
        found: True if found

    """
    # Initialize key variables
    found = False
    value = uid.encode()

    # Establish a database session
    database = db.Database()
    session = database.session()
    result = session.query(Agent.id).filter(Agent.id == value)

    # Massage data
    if result.count() == 1:
        for instance in result:
            _ = instance.id
            break
        found = True

    # Return the session to the database pool after processing
    session.close()

    # Return
    return found


def idx_exists(idx):
    """Determine whether the idx exists.

    Args:
        idx: idx value for datapoint

    Returns:
        found: True if found

    """
    # Initialize key variables
    found = False

    # Establish a database session
    database = db.Database()
    session = database.session()
    result = session.query(Agent.idx).filter(Agent.idx == idx)

    # Massage data
    if result.count() == 1:
        for instance in result:
            _ = instance.idx
            break
        found = True

    # Return the session to the database pool after processing
    session.close()

    # Return
    return found
