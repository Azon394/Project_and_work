from dsmltf import classify
from math import log
from collections import Counter, defaultdict
from functools import partial

def entropy(class_probabilities):
    return sum(-p*log(p, 2) for p in class_probabilities if p)


def class_probabilities(labels):
    total_count = len(labels)
    return [count / total_count for count in Counter(labels).values()]


def data_entropy(labeled_data):
    labels = [label for _, label in labeled_data]
    probabilities = class_probabilities(labels)
    return entropy(probabilities)


def partition_entropy(subsets):
    total_count = sum(len(subset) for subset in subsets)
    return sum(data_entropy(subset) *
               len(subset) / total_count for subset in subsets)


def partition_by(inputs, attribute):
    # разбиение входящих данных по атрибуту
    groups = defaultdict(list)
    for inp in inputs:
        key = inp[0][attribute]
        groups[key].append(inp)
    return groups


def partition_entropy_by(inputs, attribute):
    # энтропия разбиения входящих данных по атрибуту
    partitions = partition_by(inputs, attribute)
    return partition_entropy(partitions.values())


def build_tree_id3(inputs, split_candidates=None):
    # построим дерево на ID3
    if split_candidates is None:
        split_candidates = inputs[0][0].keys()
    num_inputs = len(inputs)
    num_trues = len([label for item, label in inputs if label])
    num_falses = num_inputs - num_trues
    if num_trues == 0:
        return False
    if num_falses == 0:
        return True
    if not split_candidates:
        return num_trues >= num_falses
    best_attribute = min(split_candidates, key=partial(partition_entropy_by, inputs))
    partitions = partition_by(inputs, best_attribute)
    print(best_attribute,partitions)
    new_candidates = [a for a in split_candidates if a != best_attribute]
    subtrees = {attribute_value: build_tree_id3(subset, new_candidates)
                for attribute_value, subset in iter(partitions.items())}
    subtrees[None] = num_trues > num_falses
    return (best_attribute, subtrees)

inputs = [
    ({'level': 'Middle', 'lang': 'C++', 'exp': '5', 'high_edu': 'yes', 'gender': 'male'}, True),
    ({'level': 'Middle', 'lang': 'PHP', 'exp': '3', 'high_edu': 'no', 'gender': 'male'}, False),
    ({'level': 'Junior', 'lang': 'Python', 'exp': '2', 'high_edu': 'no', 'gender': 'male'}, False),
    ({'level': 'Middle', 'lang': 'Python', 'exp': '4', 'high_edu': 'yes', 'gender': 'female'}, False),
    ({'level': 'Middle', 'lang': 'JS', 'exp': '3', 'high_edu': 'no', 'gender': 'male'}, True),
    ({'level': 'Junior', 'lang': 'Java', 'exp': '2', 'high_edu': 'yes', 'gender': 'male'}, True),
    ({'level': 'Senior', 'lang': 'PHP', 'exp': '6', 'high_edu': 'yes', 'gender': 'male'}, False),
    ({'level': 'Junior', 'lang': 'C++', 'exp': '2', 'high_edu': 'no', 'gender': 'female'}, False),
    ({'level': 'Junior', 'lang': 'PHP', 'exp': '3', 'high_edu': 'yes', 'gender': 'female'}, False),
    ({'level': 'Middle', 'lang': 'JS', 'exp': '4', 'high_edu': 'yes', 'gender': 'male'}, True),
    ({'level': 'Senior', 'lang': 'Python', 'exp': '6', 'high_edu': 'yes', 'gender': 'male'}, True),
    ({'level': 'Senior', 'lang': 'Java', 'exp': '5', 'high_edu': 'yes', 'gender': 'female'}, False),
    ({'level': 'Senior', 'lang': 'C++', 'exp': '6', 'high_edu': 'yes', 'gender': 'male'}, True),
    ({'level': 'Middle', 'lang': 'PHP', 'exp': '4', 'high_edu': 'no', 'gender': 'male'}, False),
    ({'level': 'Junior', 'lang': 'JS', 'exp': '2', 'high_edu': 'no', 'gender': 'male'}, False),
    ({'level': 'Senior', 'lang': 'JS', 'exp': '5', 'high_edu': 'yes', 'gender': 'female'}, False),
    ({'level': 'Middle', 'lang': 'Java', 'exp': '4', 'high_edu': 'no', 'gender': 'male'}, False),
    ({'level': 'Middle', 'lang': 'Java', 'exp': '5', 'high_edu': 'yes', 'gender': 'male'}, True),
    ({'level': 'Middle', 'lang': 'Python', 'exp': '4', 'high_edu': 'yes', 'gender': 'male'}, True),
    ({'level': 'Junior', 'lang': 'C++', 'exp': '3', 'high_edu': 'yes', 'gender': 'male'}, True),
    ({'level': 'Junior', 'lang': 'PHP', 'exp': '3', 'high_edu': 'no', 'gender': 'female'}, False),
    ({'level': 'Middle', 'lang': 'Python', 'exp': '5', 'high_edu': 'yes', 'gender': 'male'}, True),
    ({'level': 'Senior', 'lang': 'JS', 'exp': '6', 'high_edu': 'no', 'gender': 'male'}, True),
    ({'level': 'Junior', 'lang': 'Java', 'exp': '2', 'high_edu': 'yes', 'gender': 'female'}, False),
    ({'level': 'Middle', 'lang': 'C++', 'exp': '4', 'high_edu': 'yes', 'gender': 'male'}, True),
    ({'level': 'Senior', 'lang': 'Python', 'exp': '6', 'high_edu': 'yes', 'gender': 'male'}, True),
    ({'level': 'Junior', 'lang': 'JS', 'exp': '3', 'high_edu': 'no', 'gender': 'female'}, False),
    ({'level': 'Middle', 'lang': 'Java', 'exp': '5', 'high_edu': 'yes', 'gender': 'male'}, True),
    ({'level': 'Senior', 'lang': 'PHP', 'exp': '6', 'high_edu': 'yes', 'gender': 'male'}, False),
    ({'level': 'Junior', 'lang': 'Python', 'exp': '4', 'high_edu': 'no', 'gender': 'male'}, False),
    ({'level': 'Middle', 'lang': 'C++', 'exp': '6', 'high_edu': 'yes', 'gender': 'female'}, False),
    ({'level': 'Senior', 'lang': 'JS', 'exp': '5', 'high_edu': 'no', 'gender': 'male'}, False),
    ({'level': 'Junior', 'lang': 'Java', 'exp': '3', 'high_edu': 'no', 'gender': 'male'}, False),
    ({'level': 'Middle', 'lang': 'Python', 'exp': '6', 'high_edu': 'yes', 'gender': 'male'}, True),
    ({'level': 'Senior', 'lang': 'C++', 'exp': '6', 'high_edu': 'no', 'gender': 'male'}, True),
    ({'level': 'Junior', 'lang': 'PHP', 'exp': '4', 'high_edu': 'yes', 'gender': 'male'}, False),
    ({'level': 'Middle', 'lang': 'JS', 'exp': '5', 'high_edu': 'no', 'gender': 'female'}, False),
    ({'level': 'Senior', 'lang': 'Java', 'exp': '4', 'high_edu': 'yes', 'gender': 'male'}, True),
    ({'level': 'Junior', 'lang': 'Python', 'exp': '3', 'high_edu': 'no', 'gender': 'male'}, False),
    ({'level': 'Middle', 'lang': 'C++', 'exp': '7', 'high_edu': 'yes', 'gender': 'female'}, False)
]

inputs_tren = [
    ({'specialization': '090301', 'has_recent_debt': 'yes',
      'attendance_class': '30%-50%', 'registered_vk': 'yes', 'registered_classroom': 'no',
      'athlete': 'no', 'student_events': 'yes', 'teacher_feedback': 'плохо'}, False),

    ({'specialization': '090304', 'has_recent_debt': 'no',
      'attendance_class': '<30%', 'registered_vk': 'no', 'registered_classroom': 'yes',
      'athlete': 'yes', 'student_events': 'no', 'teacher_feedback': 'хорошо'}, False),

    ({'specialization': '100503', 'has_recent_debt': 'no',
      'attendance_class': '50%-80%', 'registered_vk': 'yes', 'registered_classroom': 'yes',
      'athlete': 'no', 'student_events': 'no', 'teacher_feedback': 'отлично'}, True),

    ({'specialization': '090301', 'has_recent_debt': 'yes',
      'attendance_class': '<30%', 'registered_vk': 'no', 'registered_classroom': 'no',
      'athlete': 'no', 'student_events': 'no', 'teacher_feedback': 'плохо'}, False),

    ({'specialization': '090304', 'has_recent_debt': 'no',
      'attendance_class': '50%-80%', 'registered_vk': 'yes', 'registered_classroom': 'yes',
      'athlete': 'yes', 'student_events': 'yes', 'teacher_feedback': 'отлично'}, True),

    ({'specialization': '100503', 'has_recent_debt': 'yes',
      'attendance_class': '30%-50%', 'registered_vk': 'no', 'registered_classroom': 'no',
      'athlete': 'no', 'student_events': 'yes', 'teacher_feedback': 'плохо'}, False),

    ({'specialization': '090301', 'has_recent_debt': 'no',
      'attendance_class': '50%-80%', 'registered_vk': 'yes', 'registered_classroom': 'yes',
      'athlete': 'no', 'student_events': 'yes', 'teacher_feedback': 'хорошо'}, True),

    ({'specialization': '090304', 'has_recent_debt': 'no',
      'attendance_class': '>80%', 'registered_vk': 'yes', 'registered_classroom': 'yes',
      'athlete': 'yes', 'student_events': 'yes', 'teacher_feedback': 'отлично'}, True),

    ({'specialization': '100503', 'has_recent_debt': 'yes',
      'attendance_class': '<30%', 'registered_vk': 'no', 'registered_classroom': 'no',
      'athlete': 'no', 'student_events': 'no', 'teacher_feedback': 'плохо'}, False),

    ({'specialization': '090301', 'has_recent_debt': 'no',
      'attendance_class': '50%-80%', 'registered_vk': 'yes', 'registered_classroom': 'yes',
      'athlete': 'no', 'student_events': 'no', 'teacher_feedback': 'хорошо'}, True),

    ({'specialization': '090304', 'has_recent_debt': 'yes',
      'attendance_class': '30%-50%', 'registered_vk': 'no', 'registered_classroom': 'no',
      'athlete': 'yes', 'student_events': 'no', 'teacher_feedback': 'плохо'}, False),

    ({'specialization': '100503', 'has_recent_debt': 'no',
      'attendance_class': '>80%', 'registered_vk': 'yes', 'registered_classroom': 'yes',
      'athlete': 'yes', 'student_events': 'yes', 'teacher_feedback': 'отлично'}, True),

    ({'specialization': '090301', 'has_recent_debt': 'no',
      'attendance_class': '50%-80%', 'registered_vk': 'yes', 'registered_classroom': 'yes',
      'athlete': 'no', 'student_events': 'yes', 'teacher_feedback': 'хорошо'}, True),

    ({'specialization': '090304', 'has_recent_debt': 'yes',
      'attendance_class': '<30%', 'registered_vk': 'no', 'registered_classroom': 'no',
      'athlete': 'no', 'student_events': 'no', 'teacher_feedback': 'плохо'}, False),

    ({'specialization': '100503', 'has_recent_debt': 'no',
      'attendance_class': '30%-50%', 'registered_vk': 'yes', 'registered_classroom': 'yes',
      'athlete': 'yes', 'student_events': 'no', 'teacher_feedback': 'хорошо'}, True),

    ({'specialization': '090301', 'has_recent_debt': 'no',
      'attendance_class': '>80%', 'registered_vk': 'yes', 'registered_classroom': 'yes',
      'athlete': 'no', 'student_events': 'yes', 'teacher_feedback': 'отлично'}, True),

    ({'specialization': '090304', 'has_recent_debt': 'yes',
      'attendance_class': '50%-80%', 'registered_vk': 'no', 'registered_classroom': 'no',
      'athlete': 'no', 'student_events': 'yes', 'teacher_feedback': 'плохо'}, False),

    ({'specialization': '100503', 'has_recent_debt': 'no',
      'attendance_class': '50%-80%', 'registered_vk': 'yes', 'registered_classroom': 'yes',
      'athlete': 'yes', 'student_events': 'yes', 'teacher_feedback': 'отлично'}, True),

    ({'specialization': '090301', 'has_recent_debt': 'no',
      'attendance_class': '<30%', 'registered_vk': 'no', 'registered_classroom': 'no',
      'athlete': 'no', 'student_events': 'no', 'teacher_feedback': 'плохо'}, False),

    ({'specialization': '090304', 'has_recent_debt': 'yes',
      'attendance_class': '30%-50%', 'registered_vk': 'no', 'registered_classroom': 'no',
      'athlete': 'no', 'student_events': 'no', 'teacher_feedback': 'плохо'}, False),

    ({'specialization': '100503', 'has_recent_debt': 'no',
      'attendance_class': '>80%', 'registered_vk': 'yes', 'registered_classroom': 'yes',
      'athlete': 'yes', 'student_events': 'yes', 'teacher_feedback': 'хорошо'}, True),

    ({'specialization': '090301', 'has_recent_debt': 'no',
      'attendance_class': '50%-80%', 'registered_vk': 'yes', 'registered_classroom': 'yes',
      'athlete': 'no', 'student_events': 'yes', 'teacher_feedback': 'хорошо'}, True),

    ({'specialization': '090304', 'has_recent_debt': 'yes',
      'attendance_class': '<30%', 'registered_vk': 'no', 'registered_classroom': 'no',
      'athlete': 'no', 'student_events': 'no', 'teacher_feedback': 'плохо'}, False)
]

tree1 = build_tree_id3(inputs_tren)
print(tree1)
count = 0
for student in inputs_tren:
    if classify(tree1, student[0]) == student[1]:
        count += 1
print(f"Правильно предсказано {count} из {len(inputs_tren)} \n")

tree = build_tree_id3(inputs)
print(tree)
count = 0
for proger in inputs:
    if classify(tree, proger[0]) == proger[1]:
        count += 1
print(f"Правильно предсказано {count} из {len(inputs)}")

