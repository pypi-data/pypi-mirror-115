# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
"""Module for deprecation abstractions."""
from __future__ import absolute_import

import logging
import warnings

logger = logging.getLogger(__name__)

V2_URL = "https://sagemaker.readthedocs.io/en/stable/v2.html"


def _warn(msg):
    """Generic warning raiser referencing V2

    Args:
        phrase: The phrase to include in the warning.
    """
    full_msg = f"{msg} in sagemaker>=2.\nSee: {V2_URL} for details."
    warnings.warn(full_msg, DeprecationWarning, stacklevel=2)
    logger.warning(full_msg)


def removed_warning(phrase):
    """Raise a warning for a no-op in sagemaker>=2

    Args:
        phrase: the prefix phrase of the warning message.
    """
    _warn(f"{phrase} is a no-op")


def renamed_warning(phrase):
    """Raise a warning for a rename in sagemaker>=2

    Args:
        phrase: the prefix phrase of the warning message.
    """
    _warn(f"{phrase} has been renamed")


def renamed_kwargs(old_name, new_name, value, kwargs):
    """Checks if the deprecated argument is in kwargs

    Raises warning, if present.

    Args:
        old_name: name of deprecated argument
        new_name: name of the new argument
        value: value associated with new name, if supplied
        kwargs: keyword arguments dict

    Returns:
        value of the keyword argument, if present
    """
    if old_name in kwargs:
        value = kwargs.get(old_name, value)
        kwargs[new_name] = value
        renamed_warning(old_name)
    return value


def removed_arg(name, arg):
    """Checks if the deprecated argument is populated.

    Raises warning, if not None.

    Args:
        name: name of deprecated argument
        arg: the argument to check
    """
    if arg is not None:
        removed_warning(name)


def removed_kwargs(name, kwargs):
    """Checks if the deprecated argument is in kwargs

    Raises warning, if present.

    Args:
        name: name of deprecated argument
        kwargs: keyword arguments dict
    """
    if name in kwargs:
        removed_warning(name)


def removed_function(name):
    """A no-op deprecated function factory."""

    def func(*args, **kwargs):  # pylint: disable=W0613
        removed_warning(f"The function {name}")

    return func


def deprecated_function(func, name):
    """Wrap a function with a deprecation warning.

    Args:
        func: Function to wrap in a deprecation warning.
        name: The name that has been deprecated.

    Returns:
        The modified function
    """

    def deprecate(*args, **kwargs):
        renamed_warning(f"The {name}")
        return func(*args, **kwargs)

    return deprecate


def deprecated_serialize(instance, name):
    """Modifies a serializer instance serialize method.

    Args:
        instance: Instance to modify serialize method.
        name: The name that has been deprecated.

    Returns:
        The modified instance
    """
    instance.serialize = deprecated_function(instance.serialize, name)
    return instance


def deprecated_deserialize(instance, name):
    """Modifies a deserializer instance deserialize method.

    Args:
        instance: Instance to modify deserialize method.
        name: The name that has been deprecated.

    Returns:
        The modified instance
    """
    instance.deserialize = deprecated_function(instance.deserialize, name)
    return instance


def deprecated_class(cls, name):
    """Returns a class based on super class with a deprecation warning.

    Args:
        cls: The class to derive with a deprecation warning on __init__
        name: The name of the class.

    Returns:
        The modified class.
    """

    class DeprecatedClass(cls):
        """Provides a warning for the class name."""

        def __init__(self, *args, **kwargs):
            """Provides a warning for the class name."""
            renamed_warning(f"The class {name}")
            super(DeprecatedClass, self).__init__(*args, **kwargs)

    return DeprecatedClass
