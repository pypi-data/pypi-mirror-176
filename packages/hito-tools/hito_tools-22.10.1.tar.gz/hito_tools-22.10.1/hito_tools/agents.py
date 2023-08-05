import csv
import re
import unicodedata
from string import capwords
from typing import Dict, Set, Tuple

from .utils import str_to_list

HITO_ARCHIVED_FIELD = "Archivé ?"
HITO_EMAIL_FIELD = "email"
HITO_FIRSTNAME_FIELD = "Prénom"
HITO_LASTNAME_FIELD = "Nom"
HITO_OFFICE_FIELD = "Bureau"
HITO_PHONE_FIELD = "Téléphone"
HITO_RESEDA_EMAIL_FIELD = "ID Connexion"
HITO_TEAM_FIELD = "Équipe"

MAPPINGS_HITO_NAME = "Hito"
MAPPINGS_RESEDA_NAME = "RESEDA"

NSIP_AGENT_PROJECT_FIELD = "Id Projet"
NSIP_CONTACT_EMAIL_FIELD = "contact_email"
NSIP_DEPARTURE_DATE = "Date de fin de contrat"
NSIP_FIRSTNAME_FIELD = "firstname"
NSIP_LASTNAME_FIELD = "lastname"
NSIP_OFFICES_FIELD = "offices"
NSIP_RESEDA_EMAIL_FIELD = "username"
NSIP_PHONE_NUMBERS = "phone_numbers"
NSIP_TEAM_ID_FIELD = "team ID"

NSIP_INVALID_EMAIL_PATTERN = r"[0-9a-f]+(@in2p3\.fr)?$"


class Agent:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        team: str = None,
        email: str = None,
        reseda_email: str = None,
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        # email_alias is the lab official email for the agent
        self.email_alias = None
        self.reseda_email = reseda_email
        if len(self.first_name) == 0:
            self.name = self.last_name
        elif len(self.last_name) == 0:
            self.name = self.first_name
        else:
            self.name = f"{self.first_name} {self.last_name}"
        self.projects = set()
        self.team = team
        self.offices = set()
        self.phone_numbers = set()
        self.matched = False
        self.disabled = False

    def add_office(self, office: str) -> None:
        self.offices.add(office)

    def add_phone(self, phone: str) -> None:
        self.phone_numbers.add(phone)

    def add_project(self, project: str) -> None:
        self.projects.add(project)

    def get_ascii_firstname(self) -> str:
        return ascii_lower_nohyphen(self.first_name)

    def get_ascii_lastname(self) -> str:
        return ascii_lower_nohyphen(self.last_name)

    def get_ascii_name(self) -> str:
        return ascii_lower_nohyphen(self.name)

    def get_email(self) -> str:
        return self.email

    def get_email_alias(self) -> str:
        return self.email_alias

    def get_emails(self) -> Tuple[str, str]:
        return self.email, self.reseda_email

    def get_firstname(self) -> str:
        return self.first_name

    def get_fullname(self) -> str:
        return self.name

    def get_lastname(self) -> str:
        return self.last_name

    def get_offices(self) -> Set[str]:
        return self.offices

    def get_phones(self) -> Set[str]:
        return self.phone_numbers

    def get_projects(self) -> Set[str]:
        return self.projects

    def get_reseda_email(self) -> str:
        return self.reseda_email

    def get_team(self) -> str:
        return self.team

    def is_matched(self) -> bool:
        return self.matched

    def is_disabled(self) -> bool:
        return self.disabled

    def remove_office(self, office: str) -> None:
        if office in self.offices:
            self.offices.remove(office)
            pass

    def set_matched(self) -> None:
        self.matched = True

    def set_disabled(self) -> None:
        self.disabled = True

    def set_email_alias(self, alias: str) -> None:
        self.email_alias = alias


def nsip_agent_active(agent_email: str):
    """
    Returns true if the email is a valid email, meaning that the agent is active, False otherwise.

    :param agent_email: email of the agent
    :return: True or False
    """

    if re.match(NSIP_INVALID_EMAIL_PATTERN, agent_email):
        return False
    else:
        return True


def capitalize_name(name):
    """
    Captitalize a name composed of several words separated by withespaces or hyphens

    :param name: name to capitalize
    :return: the capitalized name
    """

    m = re.match(r".*(?P<sep>\s*-\s*)\S", name)
    if m:
        return capwords(name, m.group("sep"))
    else:
        return capwords(name)


def ascii_name(string: str) -> str:
    """
    Helper function to replace accented characters by ASCII characters and replace
    multiple withespaces by only one space

    :param string: string to convert
    :return: string with only ASCII characters
    """
    ascii_string = unicodedata.normalize("NFD", string).encode("ascii", "ignore").decode("ascii")
    ascii_string = re.sub(r"\s+", " ", ascii_string)
    return ascii_string


def translate_to_ascii(string: str) -> str:
    """
    Helper function to translate a string with accented characters to ASCII and replace all
    consecutive white spaces by a single '-' and suppress existing withespaces around '-'

    :param string: string to convert
    :return: string with only ASCII characters
    """
    ascii_string = unicodedata.normalize("NFD", string).encode("ascii", "ignore").decode("ascii")
    ascii_string = re.sub(r"\s+", "-", ascii_string)
    return re.sub("-+", "-", ascii_string)


def ascii_lower(string: str) -> str:
    """
    Helper function to translate a string with accented characters to ASCII lowercase
    characters and replace all consecutive white spaces by a single '-'.

    :param string: string to convert
    :return: string with only ASCII characters
    """
    return translate_to_ascii(string).lower()


def ascii_lower_nohyphen(string: str) -> str:
    """
    Helper function that removes hyphens and whitespaces after all the transformation done by
    ascii-lower()

    :param string: string to convert
    :return: string with only ASCII characters
    """
    string = re.sub(r"\s", "", string)
    return re.sub("-", "", ascii_lower(string))


def read_hito_agents(
    file: str,
    ignore_if_no_team: bool = False,
    use_archived: bool = False,
    ascii_name_only: bool = False,
) -> Dict[str, Agent]:
    """
    Read a Hito export CSV and return a list of Agent as a dict where for each agent 2 keys are
    added: one corresponding ot the full name (givenname + lastname) and the other to the
    lowercase ASCII version of the fullname.

    :param file: Hito export CSV
    :param ignore_if_no_team: if True ignore agents not assigned to a team
    :param use_archived: if true, also use archived users in the CSV file (if any)
    :param ascii_name_only: use only the ASCII lowercase full name as a key in the agent list
    :return: dict representing the agent list
    """

    agent_list: Dict[str, Agent] = {}

    try:
        with open(file, "r", encoding="utf-8") as f:
            csv_reader = csv.DictReader(f, delimiter=";")
            for e in csv_reader:
                if (
                    HITO_ARCHIVED_FIELD in e
                    and e[HITO_ARCHIVED_FIELD].lower() == "o"
                    and not use_archived
                ):
                    continue
                agent = Agent(
                    e[HITO_FIRSTNAME_FIELD],
                    e[HITO_LASTNAME_FIELD],
                    e[HITO_TEAM_FIELD],
                    e[HITO_EMAIL_FIELD].lower(),
                    e[HITO_RESEDA_EMAIL_FIELD].lower(),
                )
                if HITO_OFFICE_FIELD in e:
                    for office in str_to_list(e[HITO_OFFICE_FIELD]):
                        agent.add_office(office)
                if HITO_PHONE_FIELD in e:
                    for phone_number in str_to_list(e[HITO_PHONE_FIELD]):
                        agent.add_phone(phone_number)
                # Ignore agents in Hito not assigned to a team
                if ignore_if_no_team and len(e[HITO_TEAM_FIELD]) == 0:
                    print(f"INFO: '{agent.get_fullname()}' doesn't belong to a team: ignoring it.")
                    continue
                if not ascii_name_only:
                    agent_list[agent.get_fullname()] = agent
                # Also add a lowercase with no hyphen and no accented chars entry to help
                # with matching
                agent_list[agent.get_ascii_name()] = agent
    except:  # noqa: E722
        print(f"Error reading Hito CSV ({file})")
        raise

    return agent_list


def get_nsip_agents(nsip_session, context: str = "NSIP") -> Dict[str, Agent]:
    """
    Function to retrieve agents from NSIP through the NSIP API and return a list of Agent as a
    dict where for each agent 2 keys are added: one corresponding ot the full name (givenname
    + lastname) and the other to the lowercase ASCII version of the  fullname.

    :param nsip_session: a NSIPConnection object
    :param context: either 'NSIP' (all agents presents at least one day during the semester)
                    or 'DIRECTORY' (only agents with an active contract)
    :return: dict representing the list of agents
    """

    agent_list: Dict[str, Agent] = {}

    agents = nsip_session.get_agent_list(context)

    for e in agents:
        agent = Agent(e["firstname"], e["lastname"], e["team"], e["email"], e["email_reseda"])
        if e["offices"]:
            for office in e["offices"]:
                if len(office) > 0:
                    agent.add_office(office)
        if e["phoneNumbers"]:
            for number in e["phoneNumbers"]:
                if len(number) > 0:
                    agent.add_phone(number)
        if not nsip_agent_active(agent.get_reseda_email()):
            agent.set_disabled()
        agent_list[agent.get_fullname()] = agent

    return agent_list


def name_mapping_exceptions(file: str) -> Dict[str, str]:
    """
    Read a CSV defining the RESEDA/Hito name mapping for special cases and return them as a dict
    where the key is the NSIP name and the value is the Hito name.

    :param file: CSV file defining the exceptions
    :return: dict
    """
    hito_nsip_explicit_mappings: Dict[str, str] = {}

    try:
        with open(file, "r", encoding="utf-8") as f:
            mappings_reader = csv.DictReader(f, delimiter=";")
            for e in mappings_reader:
                hito_nsip_explicit_mappings[e[MAPPINGS_RESEDA_NAME]] = e[MAPPINGS_HITO_NAME]
    except:  # noqa: E722
        print(f"Error reading Hito/RESEDA mappings CSV ({file})")
        raise

    return hito_nsip_explicit_mappings


def match_hito_agent_name(
    project_agent: Agent,
    hito_agent_list: Dict[str, Agent],
    hito_nsip_explicit_mappings: Dict[str, str] = {},
    global_users: Dict[str, str] = {},
    verbose: bool = False,
) -> Tuple[str, bool]:
    """
    Function returning the Hito agent name matching a NSIP agent name, taking into account a list
    of explicit mappins.

    :param project_agent: project agent object
    :param hito_agent_list: Hito agent list (a dict where the key is the agent full name)
    :param hito_nsip_explicit_mappings: a list of explicit mappings
    :return: Hito agent name or None if no match found, approximate_match flag (boolean),
             approximate match criteria
    """

    approximate_matching = False
    match_criteria = ""
    project_agent_name = project_agent.get_fullname()

    if project_agent_name in hito_nsip_explicit_mappings:
        hito_name = hito_nsip_explicit_mappings[project_agent_name]
        print(
            f"INFO: explicit Hito match defined for NSIP agent '{project_agent_name}': {hito_name}"
        )
    else:
        hito_name = project_agent_name
    hito_ascii_name = ascii_lower_nohyphen(hito_name)
    # global_users are pseudo-users used in the local project CSV that match a team
    if (
        hito_name in hito_agent_list
        or hito_ascii_name in hito_agent_list
        or hito_name in global_users
    ):
        if hito_name not in hito_agent_list and hito_name not in global_users:
            approximate_matching = True
            match_criteria = "fullname spelling"
            hito_name = hito_agent_list[hito_ascii_name].get_fullname()
    else:
        _, project_agent_email = project_agent.get_emails()
        # Remove duplicated entries
        # First attempt to match by emails: as every entry is duplicated (full name + ascii name),
        # 2 matches are expected
        matching_agents = [
            x.get_fullname()
            for x in hito_agent_list.values()
            if re.match(f".*{project_agent_email}$", x.get_emails()[1])
        ]
        expected_matches = 2
        match_criteria = "email"
        if len(matching_agents) == 0:
            # If it failed, attempt a partial match (Hito name at the end of the project name)
            matching_agents = [x for x in hito_agent_list.keys() if re.match(f".*{hito_name}$", x)]
            expected_matches = 1
            match_criteria = "partial fullname"
        if len(matching_agents) == expected_matches:
            approximate_matching = True
            hito_name = matching_agents[0]
        else:
            if len(matching_agents) > 1:
                print(
                    (
                        f"ERROR: approximate match for project agent '{hito_name}'"
                        f" failed, too many matches"
                    )
                )
            elif verbose:
                print(f"ERROR: agent {hito_name} not found in Hito.")
            hito_name = None

    return hito_name, approximate_matching, match_criteria
