#!/usr/bin/python3

from faker import Faker

# path name
PATH_LIST = [
    'Admitted', 'Call Closed', 'Discharged', 'Emergency dentist',
    'Minor injuries unit', 'Not picked up in an ambulance', 'Out-of-hours',
    'Out-patient clinic', 'Seen by A&E doctor', 'Spoke to a primary care service',
    'Walk-in centre'
]

# different colors for path
DIFFERENT_COLORS = [
    '#88CCEE', '#CC6677', '#DDCC77',
    '#117733', '#332288', '#AA4499',
    '#44AA99', '#999933', '#661100',
    '#6699CC', '#888888'
]

#  same colors for path
SAME_COLORS = [
    '#FFFFFF', '#FFFFFF', '#FFFFFF',
    '#FFFFFF', '#FFFFFF', '#FFFFFF',
    '#FFFFFF', '#FFFFFF', '#FFFFFF',
    '#FFFFFF', '#FFFFFF'
]

# value range and target path value
__min__ = 50
__max__ = 650

# target min
__target_min__ = 650
# target value
__target_max__ = 1200

# sets of numbers
__data_len__ = 9


def random_normal_cost():
    """
    Gets the value of the cost of the ordinary path
    :return:
    """
    f = Faker(locale='zh_CN')
    random_int = f.random_int(min=__min__, max=__max__)
    return random_int


def random_target_cost():
    """
    Gets the value of the maximum path cost
    :return:
    """
    f = Faker(locale='zh_CN')
    random_int = f.random_int(min=__target_min__, max=__target_max__)
    return random_int


def get_path_data():
    """
    take a random set of data
    :return: path_data_list
    """
    # Path name and cost data
    path_data_list = []
    # Iterate through the path names, setting a basic random value for each path
    for path in PATH_LIST:
        path_data = {
            "path_name": path,
            "path_cost": random_normal_cost(),
            "max_target": False
        }
        path_data_list.append(path_data)

    # Pick one at random from the data as the maximum
    faker = Faker(locale='zh_CN')
    random = faker.random_int(1, len(path_data_list))
    # Set the randomly selected cost to the maximum
    target = path_data_list[random - 1]
    target['path_cost'] = random_target_cost()
    target['max_target'] = True
    # Assemble a list of
    path_data_list[random - 1] = target
    return path_data_list


class Data:

    @staticmethod
    def init_data():

        total_path = []
        for i in range(__data_len__):
            total_path.append(get_path_data())
        return total_path
