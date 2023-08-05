# -*- coding: utf-8 -*-
# Auto-generated by Stone, do not modify.
# @generated
# flake8: noqa
# pylint: skip-file
from __future__ import unicode_literals
from stone.backends.python_rsrc import stone_base as bb
from stone.backends.python_rsrc import stone_validators as bv

class PhotoSourceArg(bb.Union):
    """
    This class acts as a tagged union. Only one of the ``is_*`` methods will
    return true. To get the associated value of a tag (if one exists), use the
    corresponding ``get_*`` method.

    :ivar str account.PhotoSourceArg.base64_data: Image data in base64-encoded
        bytes.
    """

    _catch_all = 'other'
    # Attribute is overwritten below the class definition
    other = None

    @classmethod
    def base64_data(cls, val):
        """
        Create an instance of this class set to the ``base64_data`` tag with
        value ``val``.

        :param str val:
        :rtype: PhotoSourceArg
        """
        return cls('base64_data', val)

    def is_base64_data(self):
        """
        Check if the union tag is ``base64_data``.

        :rtype: bool
        """
        return self._tag == 'base64_data'

    def is_other(self):
        """
        Check if the union tag is ``other``.

        :rtype: bool
        """
        return self._tag == 'other'

    def get_base64_data(self):
        """
        Image data in base64-encoded bytes.

        Only call this if :meth:`is_base64_data` is true.

        :rtype: str
        """
        if not self.is_base64_data():
            raise AttributeError("tag 'base64_data' not set")
        return self._value

    def _process_custom_annotations(self, annotation_type, field_path, processor):
        super(PhotoSourceArg, self)._process_custom_annotations(annotation_type, field_path, processor)

PhotoSourceArg_validator = bv.Union(PhotoSourceArg)

class SetProfilePhotoArg(bb.Struct):
    """
    :ivar account.SetProfilePhotoArg.photo: Image to set as the user's new
        profile photo.
    """

    __slots__ = [
        '_photo_value',
    ]

    _has_required_fields = True

    def __init__(self,
                 photo=None):
        self._photo_value = bb.NOT_SET
        if photo is not None:
            self.photo = photo

    # Instance attribute type: PhotoSourceArg (validator is set below)
    photo = bb.Attribute("photo", user_defined=True)

    def _process_custom_annotations(self, annotation_type, field_path, processor):
        super(SetProfilePhotoArg, self)._process_custom_annotations(annotation_type, field_path, processor)

SetProfilePhotoArg_validator = bv.Struct(SetProfilePhotoArg)

class SetProfilePhotoError(bb.Union):
    """
    This class acts as a tagged union. Only one of the ``is_*`` methods will
    return true. To get the associated value of a tag (if one exists), use the
    corresponding ``get_*`` method.

    :ivar account.SetProfilePhotoError.file_type_error: File cannot be set as
        profile photo.
    :ivar account.SetProfilePhotoError.file_size_error: File cannot exceed 10
        MB.
    :ivar account.SetProfilePhotoError.dimension_error: Image must be larger
        than 128 x 128.
    :ivar account.SetProfilePhotoError.thumbnail_error: Image could not be
        thumbnailed.
    :ivar account.SetProfilePhotoError.transient_error: Temporary infrastructure
        failure, please retry.
    """

    _catch_all = 'other'
    # Attribute is overwritten below the class definition
    file_type_error = None
    # Attribute is overwritten below the class definition
    file_size_error = None
    # Attribute is overwritten below the class definition
    dimension_error = None
    # Attribute is overwritten below the class definition
    thumbnail_error = None
    # Attribute is overwritten below the class definition
    transient_error = None
    # Attribute is overwritten below the class definition
    other = None

    def is_file_type_error(self):
        """
        Check if the union tag is ``file_type_error``.

        :rtype: bool
        """
        return self._tag == 'file_type_error'

    def is_file_size_error(self):
        """
        Check if the union tag is ``file_size_error``.

        :rtype: bool
        """
        return self._tag == 'file_size_error'

    def is_dimension_error(self):
        """
        Check if the union tag is ``dimension_error``.

        :rtype: bool
        """
        return self._tag == 'dimension_error'

    def is_thumbnail_error(self):
        """
        Check if the union tag is ``thumbnail_error``.

        :rtype: bool
        """
        return self._tag == 'thumbnail_error'

    def is_transient_error(self):
        """
        Check if the union tag is ``transient_error``.

        :rtype: bool
        """
        return self._tag == 'transient_error'

    def is_other(self):
        """
        Check if the union tag is ``other``.

        :rtype: bool
        """
        return self._tag == 'other'

    def _process_custom_annotations(self, annotation_type, field_path, processor):
        super(SetProfilePhotoError, self)._process_custom_annotations(annotation_type, field_path, processor)

SetProfilePhotoError_validator = bv.Union(SetProfilePhotoError)

class SetProfilePhotoResult(bb.Struct):
    """
    :ivar account.SetProfilePhotoResult.profile_photo_url: URL for the photo
        representing the user, if one is set.
    """

    __slots__ = [
        '_profile_photo_url_value',
    ]

    _has_required_fields = True

    def __init__(self,
                 profile_photo_url=None):
        self._profile_photo_url_value = bb.NOT_SET
        if profile_photo_url is not None:
            self.profile_photo_url = profile_photo_url

    # Instance attribute type: str (validator is set below)
    profile_photo_url = bb.Attribute("profile_photo_url")

    def _process_custom_annotations(self, annotation_type, field_path, processor):
        super(SetProfilePhotoResult, self)._process_custom_annotations(annotation_type, field_path, processor)

SetProfilePhotoResult_validator = bv.Struct(SetProfilePhotoResult)

PhotoSourceArg._base64_data_validator = bv.String()
PhotoSourceArg._other_validator = bv.Void()
PhotoSourceArg._tagmap = {
    'base64_data': PhotoSourceArg._base64_data_validator,
    'other': PhotoSourceArg._other_validator,
}

PhotoSourceArg.other = PhotoSourceArg('other')

SetProfilePhotoArg.photo.validator = PhotoSourceArg_validator
SetProfilePhotoArg._all_field_names_ = set(['photo'])
SetProfilePhotoArg._all_fields_ = [('photo', SetProfilePhotoArg.photo.validator)]

SetProfilePhotoError._file_type_error_validator = bv.Void()
SetProfilePhotoError._file_size_error_validator = bv.Void()
SetProfilePhotoError._dimension_error_validator = bv.Void()
SetProfilePhotoError._thumbnail_error_validator = bv.Void()
SetProfilePhotoError._transient_error_validator = bv.Void()
SetProfilePhotoError._other_validator = bv.Void()
SetProfilePhotoError._tagmap = {
    'file_type_error': SetProfilePhotoError._file_type_error_validator,
    'file_size_error': SetProfilePhotoError._file_size_error_validator,
    'dimension_error': SetProfilePhotoError._dimension_error_validator,
    'thumbnail_error': SetProfilePhotoError._thumbnail_error_validator,
    'transient_error': SetProfilePhotoError._transient_error_validator,
    'other': SetProfilePhotoError._other_validator,
}

SetProfilePhotoError.file_type_error = SetProfilePhotoError('file_type_error')
SetProfilePhotoError.file_size_error = SetProfilePhotoError('file_size_error')
SetProfilePhotoError.dimension_error = SetProfilePhotoError('dimension_error')
SetProfilePhotoError.thumbnail_error = SetProfilePhotoError('thumbnail_error')
SetProfilePhotoError.transient_error = SetProfilePhotoError('transient_error')
SetProfilePhotoError.other = SetProfilePhotoError('other')

SetProfilePhotoResult.profile_photo_url.validator = bv.String()
SetProfilePhotoResult._all_field_names_ = set(['profile_photo_url'])
SetProfilePhotoResult._all_fields_ = [('profile_photo_url', SetProfilePhotoResult.profile_photo_url.validator)]

set_profile_photo = bb.Route(
    'set_profile_photo',
    1,
    False,
    SetProfilePhotoArg_validator,
    SetProfilePhotoResult_validator,
    SetProfilePhotoError_validator,
    {'auth': 'user',
     'host': 'api',
     'style': 'rpc'},
)

ROUTES = {
    'set_profile_photo': set_profile_photo,
}

